"""按规则生成地点四备选，保存整数精度例外与检查记录。"""
import hashlib
import json
import math
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


def alternatives(value):
    m = re.fullmatch(r"(\d+(?:\.\d+)?)(.+)", value)
    original, unit = Decimal(m[1]), m[2]
    precision = max(0, -original.as_tuple().exponent)
    step = Decimal(1).scaleb(-precision)
    n = int((original * Decimal("0.05") / step).to_integral_value(rounding=ROUND_FLOOR))
    exception = None
    if n < 2:
        n = 2
        exception = "同精度下±5%不足四个不同值；按已定一般数值例外保留精度，改取相邻两档并记录最大幅度。"
    offsets = [-n, -math.ceil(n / 2), math.ceil(n / 2), n]
    numbers = [original + step * k for k in offsets]
    assert all(k > 0 for k in numbers)
    return [value, *[f"{n:.{precision}f}{unit}" for n in numbers]], {
        "rule": "两低两高，约±5%；半幅与最大幅按原值精度取整",
        "step": str(step), "offsets_in_steps": offsets,
        "actual_maximum_percent": str(max(abs(n - original) / original * 100 for n in numbers)),
        "precision_exception": exception,
    }


fields = read(BASE / "fields.json")["location"]
script_hash = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
rows = []
originals = []
exceptions = []
for i in range(1, 11):
    folder = BASE / "entities" / f"LOCATION-{i:02}"
    original = read(folder / "original.raw.json")
    inputs = read(folder / "original.input.json")
    assert inputs["previous_same_type_originals"] == originals
    assert all(read(folder / "02_output.execution_record.json")["checks"].values())
    original_hash = hashlib.sha256((folder / "original.raw.json").read_bytes()).hexdigest()
    save_new(folder / "03_rule_inputs.execution_record.json", {
        "date": datetime.now().astimezone().isoformat(), "actor": "Codex",
        "step": "rule_inputs_saved_before_generation", "script": "../../assemble_location.py",
        "script_sha256": script_hash, "original": original,
        "general_numeric_percent": 5, "precision_exception_rule": "±5%内精度不足四值时扩大到相邻两档，保留整数并记录最大幅度。",
        "town_count_rule": "n-2、n-1、n+1、n+2；本批均为正整数。",
        "row_order_seed": f"42:{original['id']}", "output": None,
    })
    entity = {k: v for k, v in original.items() if k not in fields}
    steps = []
    for field in ("人口", "面积", "海拔"):
        entity[field], detail = alternatives(original[field])
        steps.append({"field": field, **detail})
        if detail["precision_exception"]:
            exceptions.append({"id": original["id"], "field": field, "values": entity[field], **detail})
    count = int(original["下辖乡镇数"].removesuffix("个"))
    counts = [count - 2, count - 1, count + 1, count + 2]
    assert min(counts) >= 1
    entity["下辖乡镇数"] = [original["下辖乡镇数"], *[f"{n}个" for n in counts]]
    steps.append({"field": "下辖乡镇数", "rule": "相邻整数", "offsets": [-2, -1, 1, 2]})
    entity["row_order"] = make_row_order(entity)
    assert all(len(entity[field]) == len(set(entity[field])) == 5 and entity[field][0] == original[field] for field in fields)
    assert hashlib.sha256((folder / "original.raw.json").read_bytes()).hexdigest() == original_hash
    save_new(folder / "entity.pending_review.json", entity)
    save_new(folder / "04_assembly.execution_record.json", {
        "date": datetime.now().astimezone().isoformat(), "actor": "Codex",
        "step": "location_rules_executed_and_assembled", "steps": steps,
        "output": "entity.pending_review.json", "user_review": "原值及备选尚未审核",
        "checks": {"four_attributes_five_distinct_values": True, "originals_unchanged": True},
        "edits_to_raw_outputs": [],
    })
    rows.append(entity)
    originals.append(original)

assert {(x["id"], x["field"]) for x in exceptions} == {("LOCATION-02", "海拔"), ("LOCATION-10", "海拔")}
validation = check(rows, require_row_order=True, per_type={"location": 10})
assert not validation["errors"], validation["errors"]
records = build_records(rows, (1, 2, 3, 4))
assert len(records) == 320
for n in range(0, len(records), 2):
    a, b = records[n:n+2]
    assert (a["value_a"], a["value_b"]) == (b["value_b"], b["value_a"])
for entity in rows:
    for field in fields:
        a = create_entity_table(entity, field, entity[field][0])
        for alt in entity[field][1:]:
            b = create_entity_table(entity, field, alt)
            assert [key for key in a if a[key] != b[key]] == [field]
out = BASE / "location.entities.pending_review.jsonl"
with out.open("x") as f:
    f.write("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows))
with (BASE / "location.originals.pending_review.jsonl").open("x") as f:
    f.write("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in originals))
with (BASE / "location.baseline_prompt_preview.jsonl").open("x") as f:
    f.write("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in records))
save_new(BASE / "10_location_complete.execution_record.json", {
    "date": datetime.now().astimezone().isoformat(), "actor": "Codex",
    "step": "地点10实体原值及备选完成", "script": "assemble_location.py", "script_sha256": script_hash,
    "validation": validation, "precision_exceptions": exceptions,
    "checks": {"prior_inputs_match_actual_outputs": True, "originals_unchanged": True,
        "320_prompts_without_inference": True, "table_orders_reverse_values": True,
        "only_one_attribute_differs": True},
    "data_sha256": hashlib.sha256(out.read_bytes()).hexdigest(), "user_review": "原值及备选尚未审核",
    "actual_model_version_and_parameters": "原值在当前会话生成，具体型号版本参数不可见；备选由脚本规则生成，不调用模型。",
    "model_inference_run": False, "next_step": "同步Obsidian供用户查看，然后建筑类。",
})
print(json.dumps({"entities": 10, "attributes": 40, "prompts_previewed": len(records),
    "precision_exceptions": [(x["id"], x["field"], x["actual_maximum_percent"]) for x in exceptions],
    "errors": validation["errors"], "review": validation["review"]}, ensure_ascii=False))
