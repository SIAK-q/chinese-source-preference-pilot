"""检查已保存原值并记录结果，不修改生成输出。"""
import argparse
import hashlib
import json
import re
from datetime import date, datetime
from pathlib import Path

from prepare_person import BASE, read, save_new


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("entity_id")
    args = parser.parse_args()
    folder = BASE / "entities" / args.entity_id
    raw = read(folder / "original.raw.json")
    inputs = read(folder / "original.input.json")
    fields = read(BASE / "fields.json")["person"]
    saved = read(folder / "01_input.execution_record.json")
    match = re.fullmatch(r"(\d{4})年(\d{1,2})月(\d{1,2})日", raw["出生日期"])
    birthday = date(*map(int, match.groups())) if match else None
    checks = {
        "exact_fields": set(raw) == {"id", "name", "entity_class", "性别", *fields},
        "identity_matches_input": all(raw[k] == inputs[k] for k in ("id", "name", "entity_class")),
        "gender_matches_input": raw["性别"] == inputs["fixed_gender"],
        "all_values_strings": all(isinstance(v, str) and v for v in raw.values()),
        "birth_date_valid": birthday is not None and birthday <= date.fromisoformat(inputs["date"]),
        "height_integer_cm": bool(re.fullmatch(r"[1-9]\d*厘米", raw["身高"])),
        "weight_integer_kg": bool(re.fullmatch(r"[1-9]\d*公斤", raw["体重"])),
        "marital_category": raw["婚姻状况"] in ("已婚", "未婚", "离异", "再婚", "丧偶"),
        "cities_from_pool": all(raw[k] in inputs["entity_places"] for k in ("现居城市", "出生地", "籍贯")),
        "prompt_unchanged": hashlib.sha256((folder / "original.prompt.txt").read_bytes()).hexdigest() == saved["prompt_sha256"],
    }
    assert all(checks.values()), checks
    age = int(inputs["date"][:4]) - birthday.year - (
        (int(inputs["date"][5:7]), int(inputs["date"][8:])) < (birthday.month, birthday.day)
    )
    record = {
        "date": datetime.now().astimezone().isoformat(), "actor": "Codex",
        "step": "original_generated_then_checked", "entity_id": args.entity_id,
        "method": "当前会话读已先保存的任务prompt后撰写JSON；非独立API调用。",
        "model": saved["model"], "sampling_parameters": "不可见",
        "raw_output": "original.raw.json",
        "raw_output_sha256": hashlib.sha256((folder / "original.raw.json").read_bytes()).hexdigest(),
        "check_script": "../../check_person_output.py", "checks": checks,
        "age_at_generation": age,
        "assistant_review": "格式检查通过；整表搭配仍需助手审阅与用户反馈，未证明等可信。",
        "user_review": "未审核", "edits": [], "alternatives_generated": False,
    }
    save_new(folder / "02_output.execution_record.json", record)
    print(json.dumps({"id": args.entity_id, "age": age, "checks_passed": all(checks.values())}, ensure_ascii=False))


if __name__ == "__main__":
    main()
