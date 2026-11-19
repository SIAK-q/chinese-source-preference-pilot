"""建筑原值检查，区分材料和结构体系。"""
import argparse
import hashlib
import re
from datetime import datetime

from prepare_person import BASE, read, save_new

parser = argparse.ArgumentParser()
parser.add_argument("entity_id")
args = parser.parse_args()
folder = BASE / "entities" / args.entity_id
raw = read(folder / "original.raw.json")
inputs = read(folder / "original.input.json")
saved = read(folder / "01_input.execution_record.json")
fields = read(BASE / "fields.json")["building"]
checks = {
    "six_expected_fields": set(raw) == {"id", "name", "entity_class", *fields},
    "identity_matches": all(raw[k] == inputs[k] for k in ("id", "name", "entity_class")),
    "architect_matches_prepared_name": raw["设计师"] == inputs["fixed_architect"],
    "year_valid": bool(re.fullmatch(r"\d{4}年", raw["建成年份"])) and 1 <= int(raw["建成年份"][:-1]) <= 2026,
    "positive_height_floors_capacity": all(re.fullmatch(r"[1-9]\d*" + unit, raw[field]) for field, unit in (("高度", "米"), ("层数", "层"), ("容纳人数", "人"))),
    "material_not_structure_label": bool(raw["主要材料"]) and not re.search(r"框架|剪力墙|结构体系", raw["主要材料"]),
    "prompt_unchanged": hashlib.sha256((folder / "original.prompt.txt").read_bytes()).hexdigest() == saved["prompt_sha256"],
}
assert all(checks.values()), checks
save_new(folder / "02_output.execution_record.json", {
    "date": datetime.now().astimezone().isoformat(), "actor": "Codex",
    "step": "building_original_generated_then_checked", "model": saved["model"], "sampling_parameters": "不可见",
    "input_record": "01_input.execution_record.json", "raw_output": "original.raw.json",
    "raw_output_sha256": hashlib.sha256((folder / "original.raw.json").read_bytes()).hexdigest(),
    "checks": checks, "check_script": "../../check_building_output.py",
    "assistant_review": "生成时同时考虑用途、高度、层数、材料及人数；这是候选搭配判断，不是工程设计验证。",
    "user_review": "未审核", "edits": [],
})
print(args.entity_id, "原值检查通过")
