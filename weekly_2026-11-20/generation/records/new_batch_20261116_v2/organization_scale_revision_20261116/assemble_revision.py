"""另存机构规模修订版；其余七家及所有无关字段保持原样。"""
import copy
import hashlib
import json
import math
import random
import re
import sys
from datetime import datetime
from decimal import Decimal, ROUND_FLOOR
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
sys.path.insert(0, str(BASE))
from prepare_person import read, save_new
sys.path.insert(0, str(BASE.parents[1]))
from data_review.validate_entity_batch import check
from prompt_zh import create_entity_table
from run_baseline import build_records


def numeric_alternatives(value, percent):
    m = re.fullmatch(r"(\d+(?:\.\d+)?)(.+)", value)
    assert m
    original, unit = Decimal(m[1]), m[2]
    precision = max(0, -original.as_tuple().exponent)
    step = Decimal(1).scaleb(-precision)
    n = int((original * Decimal(percent) / 100 / step).to_integral_value(rounding=ROUND_FLOOR))
    assert n >= 2, "同精度不够四值，不允许悄悄放宽"
    offsets = [-n, -math.ceil(n / 2), math.ceil(n / 2), n]
    values = [original + step * delta for delta in offsets]
    assert all(v > 0 and abs(v - original) / original <= Decimal(percent) / 100 for v in values)
    return [value, *[f"{v:.{precision}f}{unit}" for v in values]], {
        "maximum_percent": percent, "unit": unit, "step": str(step), "offsets_in_steps": offsets,
        "actual_maximum_percent": str(max(abs(v - original) / original * 100 for v in values)),
        "rule": "同单位同精度，两低两高，最大幅度内取整数步长，半幅向上取整",
    }


inputs = read(HERE / "revision.input.json")
old_path = BASE / "organization.entities.pending_review.jsonl"
assert hashlib.sha256(old_path.read_bytes()).hexdigest() == inputs["source_sha256"]
old = [json.loads(line) for line in old_path.read_text().splitlines()]
rows = copy.deepcopy(old)
new_originals = {r["id"]: r for r in read(HERE / "revised_originals.raw.json")}
script_hash = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
changes = []
for entity in rows:
    eid = entity["id"]
    if eid not in new_originals:
        continue
    original = new_originals[eid]
    folder = HERE / "entities" / eid
    industry_record = read(folder / "04_industry_output.execution_record.json")
    assert hashlib.sha256((folder / "industry.raw.json").read_bytes()).hexdigest() == industry_record["raw_output_sha256"]
    save_new(folder / "05_rule_inputs.execution_record.json", {
        "date": datetime.now().astimezone().isoformat(), "actor": "Codex",
        "step": "revision_rule_inputs_saved_before_execution", "script": "../../assemble_revision.py",
        "script_sha256": script_hash, "original": original,
        "employees_percent": 5, "revenue_percent": 10,
        "keep_unchanged": ["成立时间", "总部所在地", "row_order"],
    })
    entity["所属行业"] = [original["所属行业"], *read(folder / "industry.raw.json")]
    steps = []
    for field, percent in (("员工人数", 5), ("年营业额", 10)):
        before = entity[field]
        entity[field], detail = numeric_alternatives(original[field], percent)
        steps.append({"field": field, **detail})
        changes.append({"id": eid, "field": field, "before": before, "after": entity[field],
            "reason": "扩大规模覆盖；人数营业额原值联合修订，再按相同百分比规则生成四备选。"})
    save_new(folder / "entity.pending_review.json", entity)
    save_new(folder / "06_assembly.execution_record.json", {
        "date": datetime.now().astimezone().isoformat(), "actor": "Codex",
        "step": "revised_numeric_alternatives_assembled", "steps": steps,
        "industry_values": "根据修订整表重新考虑后保留原四候选，见03/04记录。",
        "user_review": "修订候选未审核", "output": "entity.pending_review.json",
    })

for before, after in zip(old, rows):
    if before["id"] not in new_originals:
        assert before == after
    else:
        assert {k for k in before if before[k] != after[k]} == {"员工人数", "年营业额"}

validation = check(rows, require_row_order=True, per_type={"organization": 10})
assert not validation["errors"], validation["errors"]
records = build_records(rows, (1, 2, 3, 4))
assert len(records) == 400
fields = read(BASE / "fields.json")["organization"]
for entity in rows:
    for field in fields:
        first = create_entity_table(entity, field, entity[field][0])
        for alt in entity[field][1:]:
            second = create_entity_table(entity, field, alt)
            assert [key for key in first if first[key] != second[key]] == [field]
for n in range(0, len(records), 2):
    a, b = records[n:n+2]
    assert (a["value_a"], a["value_b"]) == (b["value_b"], b["value_a"])
assert hashlib.sha256(old_path.read_bytes()).hexdigest() == inputs["source_sha256"]
out = HERE / "organization.entities.pending_review.jsonl"
with out.open("x") as f:
    f.write("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows))
with (HERE / "baseline_prompt_preview.jsonl").open("x") as f:
    f.write("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in records))
save_new(HERE / "07_revision_checks.execution_record.json", {
    "date": datetime.now().astimezone().isoformat(), "actor": "Codex",
    "step": "机构规模修订完整候选另存并检查", "script": "assemble_revision.py", "script_sha256": script_hash,
    "validation": validation, "changes": changes,
    "checks": {"only_three_entities_and_two_fields_changed": True, "seven_others_identical": True,
        "old_source_hash_unchanged": True, "400_prompts_without_inference": True,
        "each_pair_only_one_field_differs": True, "table_orders_reverse_values": True},
    "source_sha256": inputs["source_sha256"], "output_sha256": hashlib.sha256(out.read_bytes()).hexdigest(),
    "assistant_selection_reason": inputs["assistant_selection_reason"],
    "user_review": "本次修订未审核", "model_inference_run": False,
})
print(json.dumps({"min_employees": min(int(e["员工人数"][0][:-1]) for e in rows),
    "max_employees": max(int(e["员工人数"][0][:-1]) for e in rows),
    "above_1000": sum(int(e["员工人数"][0][:-1]) > 1000 for e in rows),
    "errors": validation["errors"], "review": validation["review"]}, ensure_ascii=False))
