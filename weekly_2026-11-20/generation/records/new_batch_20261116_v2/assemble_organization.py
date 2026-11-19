"""按已定规则生成机构数值/日期/地名备选；不新增配对审核。"""
import hashlib
import json
import math
import random
import re
import sys
from datetime import datetime
from decimal import Decimal, ROUND_FLOOR
from pathlib import Path

from prepare_person import BASE, read, save_new

sys.path.insert(0, str(BASE.parents[1]))
from data_review.validate_entity_batch import check
from prompt_zh import create_entity_table, make_row_order
from run_baseline import build_records


def numeric_alternatives(value, percent):
    m = re.fullmatch(r"(\d+(?:\.\d+)?)(.+)", value)
    assert m, value
    original, unit = Decimal(m[1]), m[2]
    precision = max(0, -original.as_tuple().exponent)
    step = Decimal(1).scaleb(-precision)
    maximum_steps = int((original * Decimal(percent) / 100 / step).to_integral_value(rounding=ROUND_FLOOR))
    assert maximum_steps >= 2, (value, "精度内不能生成四个备选；须报告，不能放宽")
    offsets = [-maximum_steps, -math.ceil(maximum_steps / 2), math.ceil(maximum_steps / 2), maximum_steps]
    numbers = [original + step * n for n in offsets]
    assert all(n > 0 and abs(n - original) / original <= Decimal(percent) / 100 for n in numbers)
    return [value, *[f"{n:.{precision}f}{unit}" for n in numbers]], {
        "method": "同单位同精度、两低两高", "maximum_percent": percent,
        "step": str(step), "offsets_in_steps": offsets,
        "actual_maximum_percent": str(max(abs(n - original) / original * 100 for n in numbers)),
        "precision_exception": None,
    }


config = read(BASE / "batch.input.json")
fields = read(BASE / "fields.json")["organization"]
script_hash = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
entities = []
raw_hashes = {}
for i in range(1, 11):
    folder = BASE / "entities" / f"ORG-{i:02}"
    original = read(folder / "original.raw.json")
    eid = original["id"]
    industry_record = read(folder / "04_industry_output.execution_record.json")
    raw_hashes[eid] = hashlib.sha256((folder / "original.raw.json").read_bytes()).hexdigest()
    seeds = {field: f"42:{eid}:{field}" for field in ("成立时间", "总部所在地")}
    save_new(folder / "05_rule_inputs.execution_record.json", {
        "date": datetime.now().astimezone().isoformat(), "actor": "Codex",
        "step": "rule_script_and_inputs_saved_before_generation",
        "script": "../../assemble_organization.py", "script_sha256": script_hash,
        "python_version": sys.version, "original": original,
        "industry_input": "alternatives.industry.raw.json",
        "seeds": seeds, "employees_percent": 5, "revenue_percent": 10,
        "month_offset_intervals": [[-12, -7], [-6, -1], [1, 6], [7, 12]],
        "city_pool": config["entity_places"], "row_order_seed": f"42:{eid}",
        "user_review": "原值暂保留，非商业数量级人工确认；新备选未审核。",
    })
    entity = {k: v for k, v in original.items() if k not in fields}
    industry = read(folder / "alternatives.industry.raw.json")
    assert hashlib.sha256((folder / "alternatives.industry.raw.json").read_bytes()).hexdigest() == industry_record["raw_output_sha256"]
    entity["所属行业"] = [original["所属行业"], *industry]
    steps = [{"field": "所属行业", "method": "带完整原值表按已存prompt生成", "raw": "alternatives.industry.raw.json"}]
    for field, percent in (("员工人数", 5), ("年营业额", 10)):
        entity[field], detail = numeric_alternatives(original[field], percent)
        steps.append({"field": field, **detail})
    year, month = map(int, re.findall(r"\d+", original["成立时间"]))
    rng = random.Random(seeds["成立时间"])
    offsets = [rng.randint(lo, hi) for lo, hi in ((-12, -7), (-6, -1), (1, 6), (7, 12))]
    alternative_months = [year * 12 + month - 1 + n for n in offsets]
    assert all((n // 12, n % 12 + 1) <= (2026, 11) for n in alternative_months)
    entity["成立时间"] = [original["成立时间"], *[f"{n // 12}年{n % 12 + 1}月" for n in alternative_months]]
    steps.append({"field": "成立时间", "method": "前后12月内分四段抽取", "seed": seeds["成立时间"], "offset_months": offsets})
    pool = [city for city in config["entity_places"] if city != original["总部所在地"]]
    entity["总部所在地"] = [original["总部所在地"], *random.Random(seeds["总部所在地"]).sample(pool, 4)]
    steps.append({"field": "总部所在地", "method": "实体地名池无放回抽四个", "seed": seeds["总部所在地"]})
    entity["row_order"] = make_row_order(entity)
    assert all(entity[field][0] == original[field] and len(entity[field]) == len(set(entity[field])) == 5 for field in fields)
    save_new(folder / "entity.pending_review.json", entity)
    save_new(folder / "06_assembly.execution_record.json", {
        "date": datetime.now().astimezone().isoformat(), "actor": "Codex",
        "step": "organization_alternatives_assembled", "steps": steps,
        "output": "entity.pending_review.json",
        "output_sha256": hashlib.sha256((folder / "entity.pending_review.json").read_bytes()).hexdigest(),
        "checks": {"original_values_unchanged": True, "five_attributes_with_five_distinct_values": True},
        "edits_to_raw_outputs": [], "user_review": "备选未审核",
    })
    entities.append(entity)

validation = check(entities, require_row_order=True, per_type={"organization": 10})
assert not validation["errors"], validation["errors"]
records = build_records(entities, (1, 2, 3, 4))
assert len(records) == 400
for n in range(0, len(records), 2):
    a, b = records[n:n+2]
    assert (a["value_a"], a["value_b"]) == (b["value_b"], b["value_a"])
for entity in entities:
    for field in fields:
        first = create_entity_table(entity, field, entity[field][0])
        for alt in entity[field][1:]:
            other = create_entity_table(entity, field, alt)
            assert [k for k in first if first[k] != other[k]] == [field]
    assert hashlib.sha256((BASE / "entities" / entity["id"] / "original.raw.json").read_bytes()).hexdigest() == raw_hashes[entity["id"]]
data = BASE / "organization.entities.pending_review.jsonl"
with data.open("x") as f:
    f.write("".join(json.dumps(e, ensure_ascii=False) + "\n" for e in entities))
with (BASE / "organization.baseline_prompt_preview.jsonl").open("x") as f:
    f.write("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in records))
save_new(BASE / "08_organization_complete.execution_record.json", {
    "date": datetime.now().astimezone().isoformat(), "actor": "Codex",
    "step": "机构备选组装及组题检查完成", "script": "assemble_organization.py", "script_sha256": script_hash,
    "input": "ORG-01至10完整原值和行业备选，逐人规则输入已先存05记录。",
    "raw_original_hashes": raw_hashes, "dataset_sha256": hashlib.sha256(data.read_bytes()).hexdigest(),
    "validation": validation,
    "measurement_checks": {"400_prompts_without_inference": True, "reverse_values_correctly": True,
        "only_one_field_differs": True, "originals_unchanged": True},
    "user_feedback": "原值暂时保留；不记录为商业规模确认或备选已人审。",
    "model_inference_run": False, "next_step": "展示行业备选；其余五类尚未生成。",
})
print(json.dumps({"entities": len(entities), "attributes": validation["instances"], "prompts_previewed": len(records), "errors": validation["errors"], "review": validation["review"]}, ensure_ascii=False))
