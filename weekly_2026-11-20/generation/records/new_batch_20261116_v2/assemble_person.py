"""按已定脚本规则补人物备选，保存组装记录及只读组题预览。"""
import hashlib
import json
import random
import re
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

from prepare_person import BASE, read, save_new

PILOT = BASE.parents[1]
sys.path.insert(0, str(PILOT))
from prompt_zh import create_entity_table, make_row_order
from run_baseline import build_records
from data_review.validate_entity_batch import check

config = read(BASE / "batch.input.json")
fields = read(BASE / "fields.json")["person"]
frozen = read(BASE / "00_templates_frozen.execution_record.json")
for path, digest in frozen["template_hashes"].items():
    assert hashlib.sha256((BASE / path).read_bytes()).hexdigest() == digest
entities = []
original_hashes = {}
script_hash = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()

for i in range(1, 11):
    folder = BASE / "entities" / f"PERSON-{i:02}"
    original = read(folder / "original.raw.json")
    eid = original["id"]
    original_hashes[eid] = hashlib.sha256((folder / "original.raw.json").read_bytes()).hexdigest()
    assert (folder / "04_paired_outputs.execution_record.json").exists()
    seeds = {field: f"42:{eid}:{field}" for field in ("出生日期", "现居城市", "出生地", "籍贯")}
    save_new(folder / "05_rule_inputs.execution_record.json", {
        "date": datetime.now().astimezone().isoformat(), "actor": "Codex",
        "step": "script_and_rule_inputs_saved_before_generation",
        "script": "../../assemble_person.py", "script_sha256": script_hash,
        "python_version": sys.version, "original_input": original,
        "paired_inputs": ["alternatives.occupation_education.raw.json", "alternatives.height_weight.raw.json"],
        "seeds": seeds, "city_pool": config["entity_places"],
        "date_offset_ranges_in_days": [[-365, -183], [-182, -30], [30, 182], [183, 365]],
        "marital_values": ["已婚", "未婚", "离异", "再婚", "丧偶"],
        "row_order_seed": f"42:{eid}", "output": None,
    })
    entity = {k: v for k, v in original.items() if k not in fields}
    steps = []
    for key, pair_fields in {"occupation_education": ("职业", "学历"), "height_weight": ("身高", "体重")}.items():
        paired = read(folder / f"alternatives.{key}.raw.json")
        for field in pair_fields:
            entity[field] = [original[field], *[row[field] for row in paired]]
            steps.append({"field": field, "method": "当前会话按预存prompt成对生成", "raw": f"alternatives.{key}.raw.json"})
    birthday = date(*map(int, re.findall(r"\d+", original["出生日期"])))
    rng = random.Random(seeds["出生日期"])
    offsets = [rng.randint(lo, hi) for lo, hi in ((-365, -183), (-182, -30), (30, 182), (183, 365))]
    dates = [birthday + timedelta(days=n) for n in offsets]
    assert all(d <= date.fromisoformat(config["date"]) for d in dates)
    entity["出生日期"] = [original["出生日期"], *[f"{d.year}年{d.month}月{d.day}日" for d in dates]]
    steps.append({"field": "出生日期", "method": "分区间确定种子抽样", "seed": seeds["出生日期"], "offset_days": offsets})
    entity["婚姻状况"] = [original["婚姻状况"], *[v for v in ("已婚", "未婚", "离异", "再婚", "丧偶") if v != original["婚姻状况"]]]
    steps.append({"field": "婚姻状况", "method": "固定五类中排除原值，取剩余四值"})
    for field in ("现居城市", "出生地", "籍贯"):
        pool = [p for p in config["entity_places"] if p != original[field]]
        entity[field] = [original[field], *random.Random(seeds[field]).sample(pool, 4)]
        steps.append({"field": field, "method": "实体地名池无放回抽四个", "seed": seeds[field]})
    entity["row_order"] = make_row_order(entity)
    assert all(entity[field][0] == original[field] and len(set(entity[field])) == 5 for field in fields)
    save_new(folder / "entity.pending_review.json", entity)
    save_new(folder / "06_assembly.execution_record.json", {
        "date": datetime.now().astimezone().isoformat(), "actor": "Codex",
        "step": "deterministic_rules_executed_and_paired_outputs_assembled",
        "script_sha256": script_hash, "steps": steps,
        "output": "entity.pending_review.json",
        "output_sha256": hashlib.sha256((folder / "entity.pending_review.json").read_bytes()).hexdigest(),
        "checks": {"original_values_unchanged": True, "nine_attributes_with_five_distinct_values": True},
        "user_review": "职业学历原值已认可；新备选未审核",
        "edits_to_raw_outputs": [], "model_inference_run": False,
    })
    entities.append(entity)

validation = check(entities, require_row_order=True, per_type={"person": 10})
assert not validation["errors"], validation["errors"]
records = build_records(entities, (1, 2, 3, 4))
assert len(records) == 720
for i in range(0, len(records), 2):
    a, b = records[i:i+2]
    assert (a["value_a"], a["value_b"]) == (b["value_b"], b["value_a"])
for entity in entities:
    for field in fields:
        original_table = create_entity_table(entity, field, entity[field][0])
        for alt in entity[field][1:]:
            other_table = create_entity_table(entity, field, alt)
            assert [k for k in original_table if original_table[k] != other_table[k]] == [field]
    assert hashlib.sha256((BASE / "entities" / entity["id"] / "original.raw.json").read_bytes()).hexdigest() == original_hashes[entity["id"]]

path = BASE / "person.entities.pending_review.jsonl"
with path.open("x") as f:
    f.write("".join(json.dumps(e, ensure_ascii=False) + "\n" for e in entities))
with (BASE / "person.baseline_prompt_preview.jsonl").open("x") as f:
    f.write("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in records))
save_new(BASE / "03_person_complete.execution_record.json", {
    "date": datetime.now().astimezone().isoformat(), "actor": "Codex",
    "step": "人物备选组装完成与只读组题检查", "script": "assemble_person.py", "script_sha256": script_hash,
    "model_version_and_parameters": "脚本组装未调用模型；成对生成具体型号/版本和采样参数不可见。",
    "validation": validation,
    "measurement_checks": {"720_prompts_previewed_without_inference": True, "reverse_values_correctly": True,
        "only_one_field_differs_between_tables": True, "original_raw_hashes_unchanged": True},
    "dataset_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
    "assistant_review": "生成时考虑成对与单字段替换搭配；脚本验证结构、范围和组题，不证明等可信。",
    "user_review": "新备选尚未审核", "baseline_run": False,
    "next_step": "给用户看人物备选表，按具体反馈修订并留档。",
})
print(json.dumps({"entities": len(entities), "attributes": validation["instances"], "prompts_previewed": len(records), "errors": validation["errors"], "review_flags": validation["review"]}, ensure_ascii=False))
