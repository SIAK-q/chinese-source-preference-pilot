"""机构原值格式检查，不设营业额/人数配对阈值。"""
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
fields = read(BASE / "fields.json")["organization"]
month = re.fullmatch(r"(\d{4})年(\d{1,2})月", raw["成立时间"])
year_month = tuple(map(int, month.groups())) if month else None
checks = {
    "exact_fields": set(raw) == {"id", "name", "entity_class", *fields},
    "identity_matches": all(raw[k] == inputs[k] for k in ("id", "name", "entity_class")),
    "nonempty_strings": all(isinstance(v, str) and v for v in raw.values()),
    "year_month_valid": year_month is not None and year_month[0] > 0 and 1 <= year_month[1] <= 12 and year_month <= (2026, 11),
    "city_from_pool": raw["总部所在地"] in inputs["entity_places"],
    "employees_positive_integer": bool(re.fullmatch(r"[1-9]\d*人", raw["员工人数"])),
    "revenue_explicit_RMB": bool(re.fullmatch(r"[1-9]\d*(?:\.\d+)?(?:万|亿)元人民币", raw["年营业额"])),
    "prompt_unchanged": hashlib.sha256((folder / "original.prompt.txt").read_bytes()).hexdigest() == saved["prompt_sha256"],
}
assert all(checks.values()), checks
save_new(folder / "02_output.execution_record.json", {
    "date": datetime.now().astimezone().isoformat(), "actor": "Codex",
    "step": "organization_original_generated_then_checked",
    "method": "当前会话读预存prompt后撰写；行业、人数和营业额一起考虑。",
    "model": saved["model"], "sampling_parameters": "不可见",
    "raw_output": "original.raw.json", "raw_output_sha256": hashlib.sha256((folder / "original.raw.json").read_bytes()).hexdigest(),
    "check_script": "../../check_organization_output.py", "checks": checks,
    "assistant_review": "生成时未标出行业/人数/营业额的明显数量级冲突；没有以真实企业资料验证本表，不证明等可信。",
    "user_review": "未审核", "changes": [], "alternatives_generated": False,
})
print(args.entity_id, "原值格式检查通过")
