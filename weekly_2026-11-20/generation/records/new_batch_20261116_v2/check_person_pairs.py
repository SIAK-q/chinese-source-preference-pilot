"""检查成对输出的字段、互异性及数值范围；不替代语义审核。"""
import argparse
import hashlib
import re
from datetime import datetime
from decimal import Decimal

from prepare_person import BASE, read, save_new

parser = argparse.ArgumentParser()
parser.add_argument("entity_id")
args = parser.parse_args()
folder = BASE / "entities" / args.entity_id
original = read(folder / "original.raw.json")
saved = read(folder / "03_alternatives_input.execution_record.json")
checks = {}
for key, fields in {"occupation_education": ("职业", "学历"), "height_weight": ("身高", "体重")}.items():
    prompt = saved["prompts"][key]
    assert hashlib.sha256((folder / prompt["path"]).read_bytes()).hexdigest() == prompt["sha256"]
    path = folder / f"alternatives.{key}.raw.json"
    pairs = read(path)
    assert isinstance(pairs, list) and len(pairs) == 4
    assert all(set(p) == set(fields) for p in pairs)
    for field in fields:
        values = [original[field], *[p[field] for p in pairs]]
        assert all(isinstance(v, str) and v for v in values)
        assert len(set(values)) == 5, (args.entity_id, field)
        if key == "height_weight":
            unit = "厘米" if field == "身高" else "公斤"
            assert all(re.fullmatch(r"[1-9]\d*" + unit, v) for v in values)
            numbers = [Decimal(v.removesuffix(unit)) for v in values]
            diffs = [n - numbers[0] for n in numbers[1:]]
            assert all(abs(d) / numbers[0] <= Decimal("0.05") for d in diffs)
            assert sum(d < 0 for d in diffs) == sum(d > 0 for d in diffs) == 2
    checks[key] = {"four_pairs_and_five_distinct_values": True,
        "raw_output": path.name, "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "prompt_hash_unchanged": True}
save_new(folder / "04_paired_outputs.execution_record.json", {
    "date": datetime.now().astimezone().isoformat(), "actor": "Codex",
    "step": "read_saved_prompts_then_generate_two_paired_outputs",
    "model": saved["model"], "sampling_parameters": "不可见",
    "input_record": "03_alternatives_input.execution_record.json", "check_script": "../../check_person_pairs.py",
    "checks": checks,
    "assistant_review": "当前会话生成时一起考虑职业学历、身高体重，并考虑单字段替换配原值；未标出明显搭配冲突。这是助手判断，不是用户审核或资格核验。",
    "user_review": "新备选未审核", "edits": [],
})
print(args.entity_id, "两组成对输出检查通过")
