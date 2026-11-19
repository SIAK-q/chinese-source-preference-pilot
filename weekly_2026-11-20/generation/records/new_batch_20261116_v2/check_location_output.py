"""地点原值格式检查；不把格式通过当作地理真实性核验。"""
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
fields = read(BASE / "fields.json")["location"]
patterns = {"人口": r"[1-9]\d*(?:\.\d+)?(?:万)?人", "面积": r"[1-9]\d*(?:\.\d+)?平方公里",
    "海拔": r"[1-9]\d*米", "下辖乡镇数": r"[1-9]\d*个"}
checks = {"exact_fields": set(raw) == {"id", "name", "entity_class", *fields},
    "identity_matches_input": all(raw[k] == inputs[k] for k in ("id", "name", "entity_class")),
    "all_units_and_positive_numbers": all(isinstance(raw[f], str) and re.fullmatch(patterns[f], raw[f]) is not None for f in fields),
    "prompt_unchanged": hashlib.sha256((folder / "original.prompt.txt").read_bytes()).hexdigest() == saved["prompt_sha256"]}
assert all(checks.values()), checks
save_new(folder / "02_output.execution_record.json", {
    "date": datetime.now().astimezone().isoformat(), "actor": "Codex",
    "step": "location_original_generated_then_checked", "input_record": "01_input.execution_record.json",
    "model": saved["model"], "sampling_parameters": "不可见",
    "raw_output": "original.raw.json", "raw_output_sha256": hashlib.sha256((folder / "original.raw.json").read_bytes()).hexdigest(),
    "checks": checks, "check_script": "../../check_location_output.py",
    "assistant_review": "同时考虑四项属性，未标出人口、面积和乡镇数的明显搭配冲突；城区海拔与全域面积分开理解。",
    "user_review": "新地点候选未审核", "edits": [],
})
print(args.entity_id, "原值格式检查通过")
