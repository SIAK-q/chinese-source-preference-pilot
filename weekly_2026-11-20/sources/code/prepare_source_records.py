"""Prepare opt-in source-condition prompts, with paired table orders and a log.

This writes a separate preview bundle; it does not run inference or rewrite
the historical pilot files. Conditions keep the historical comparison set.

2026-11-18: source names come from data_generation/source_names.py (11-09 rules:
five newspaper suffixes, equal probability, no 商报; 1-3 agencies per entity type;
two social-handle forms 1:1; individual names fresh per pair). Places come from the
filtered pool (pool50_filtered_20261112.txt) minus every place used in the entity
data. The old source_sampling.py (11-04) is kept unchanged for earlier previews.
"""
import argparse
import hashlib
import json
import random
import sys
from pathlib import Path

from prompt_zh import SYSTEM_MESSAGE, build_two_table_prompt, get_question
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "data_generation"))
from source_names import SourceNamer, read_names, sha  # noqa: E402

PLACE_POOL = HERE / "name_generation/reports/recovered/pool50_filtered_20261112.txt"
CONDITIONS = {"baseline": (None, None),
              "gov_vs_social": ("government", "social_media"),
              "gov_vs_person": ("government", "person"),
              "news_vs_social": ("newspaper", "social_media"),
              "none_vs_gov": ("no_source", "government")}
EXCLUDED = {"id", "name", "entity_class", "description", "timeline_id", "row_order"}


def build_records(entities, sampler, conditions, alts=(1, 2, 3, 4)):
    # Keep binding randomisation independent of nickname-generation retries.
    binding_rng = random.Random(f"source-binding:{sampler.seed}")
    records = []
    for cond in conditions:
        cat_a, cat_b = CONDITIONS[cond]
        for entity in entities:
            for field, values in entity.items():
                if field in EXCLUDED or not isinstance(values, list):
                    continue
                for alt in alts:
                    if not 0 < alt < len(values):
                        raise ValueError(f"Invalid alternative {alt}: {entity['id']} / {field}")
                    pair_id = f"{field}:0-{alt}"
                    key = [cond, entity["id"], field, alt]
                    src0 = sampler.draw(cat_a, entity, key)
                    src1 = sampler.draw(cat_b, entity, key)
                    # Like WFW, randomly choose which category carries the original.
                    flip = bool(binding_rng.getrandbits(1)) if cond != "baseline" else False
                    if flip:
                        src0, src1 = src1, src0
                    for order in (0, 1):
                        va, vb = (values[0], values[alt]) if order == 0 else (values[alt], values[0])
                        sa, sb = (src0, src1) if order == 0 else (src1, src0)
                        name_a = sa["name"] if sa else None
                        name_b = sb["name"] if sb else None
                        q = get_question(entity["entity_class"], field, entity["name"])
                        records.append({"condition": cond, "entity_id": entity["id"],
                                        "entity_name": entity["name"], "entity_class": entity["entity_class"],
                                        "field": field, "pair_id": pair_id, "alt_index": alt,
                                        "order": order, "value_a": va, "value_b": vb,
                                        "source_a": name_a, "source_b": name_b,
                                        "group_a": sa["category"] if sa else "no_source",
                                        "group_b": sb["category"] if sb else "no_source",
                                        "source_metadata_a": sa, "source_metadata_b": sb,
                                        "source_binding_reversed": flip,
                                        "system": SYSTEM_MESSAGE,
                                        "prompt": build_two_table_prompt(entity, field, va, vb, name_a, name_b, q)})
    return records


def validate_records(records):
    grouped = {}
    for row in records:
        key = (row["condition"], row["entity_id"], row["pair_id"])
        orders = grouped.setdefault(key, {})
        if row["order"] in orders:
            raise ValueError(f"Duplicate table order: {key}")
        orders[row["order"]] = row
    for key, orders in grouped.items():
        if set(orders) != {0, 1}:
            raise ValueError(f"Missing table order: {key}")
        a, b = orders[0], orders[1]
        for f0, f1 in [("value_a", "value_b"), ("source_a", "source_b"),
                       ("group_a", "group_b"), ("source_metadata_a", "source_metadata_b")]:
            if a[f0] != b[f1] or a[f1] != b[f0]:
                raise ValueError(f"Binding or table reversal failed: {key} / {f0}")
    return {"pairs": len(grouped), "prompts": len(records), "source_value_swap_verified": True}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--data", type=Path, default=HERE / "data/entities_zh.jsonl")
    ap.add_argument("--out-dir", type=Path, required=True)
    ap.add_argument("--conditions", nargs="+", choices=list(CONDITIONS), default=["baseline"])
    ap.add_argument("--alts", nargs="+", type=int, default=[1, 2, 3, 4])
    ap.add_argument("--seed", type=int, default=20261111)
    ap.add_argument("--places", type=Path, default=PLACE_POOL, help="信源地名池（筛后1327个）")
    ap.add_argument("--people", type=Path, default=None,
                    help="不填 = 个人信源每对现抽（用户11-16定，同WFW）；填名单文件 = 从名单抽")
    ap.add_argument("--fetch-wiki", action="store_true", help="现抽个人信源名未查过维基时联网查询（结果追加到 name_generation/person/wiki_requests.json）")
    args = ap.parse_args()
    entities = [json.loads(s) for s in args.data.read_text().splitlines() if s.strip()]
    pool = read_names(args.places)
    data_text = args.data.read_text()
    used = sorted(p for p in pool if p in data_text)   # 实体数据里出现过的地名一律不作信源地名
    places = [p for p in pool if p not in set(used)]
    people = read_names(args.people) if args.people else None
    for _round in range(11):   # 11-19：现抽个人信源名查中文维基；查到页面的名字下一轮跳过、按同一种子重抽
        sampler = SourceNamer(places, people, args.seed, exclude_places=used)
        records = build_records(entities, sampler, args.conditions, args.alts)
        pending = sampler.wiki_pending() if people is None else []
        if not pending:
            break
        if not args.fetch_wiki:
            raise SystemExit(f"{len(pending)} 个个人信源名尚未查中文维基；加 --fetch-wiki")
        sampler.wiki_fetch(pending)
    else:
        raise RuntimeError("维基查重轮数用尽")
    checks = validate_records(records)
    args.out_dir.mkdir(parents=True, exist_ok=True)
    target = args.out_dir / "prompts.jsonl"
    if target.exists():
        raise FileExistsError(f"Use a new output directory: {target}")
    target.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in records))
    manifest = {"status": "Prepared prompts; no inference run", "command": sys.argv,
                "data": str(args.data), "data_sha256": sha(args.data),
                "preparation_script_sha256": sha(__file__), "conditions": args.conditions,
                "alts": args.alts, "validation": checks,
                "prompts_sha256": sha(target), "sampling": {**sampler.provenance(args.places, args.people),
                             "places_excluded_as_entity_places": used},
                "scope": "Sources are fresh per comparison-condition and conflict pair; both table orders share them. Government/newspaper place matching within a comparison has not been imposed."}
    (args.out_dir / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(checks, ensure_ascii=False))


if __name__ == "__main__":
    main()
