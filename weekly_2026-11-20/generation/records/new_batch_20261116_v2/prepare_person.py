"""保存下一个人物的实际任务prompt；必须先完成并记录上一个输出。"""
import hashlib
import json
from datetime import datetime
from pathlib import Path

BASE = Path(__file__).resolve().parent


def read(path):
    return json.loads(path.read_text())


def save_new(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x") as f:
        f.write(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def main():
    config = read(BASE / "batch.input.json")
    fields = read(BASE / "fields.json")["person"]
    previous = []
    for i, person in enumerate(config["people"], 1):
        eid = f"PERSON-{i:02}"
        folder = BASE / "entities" / eid
        raw = folder / "original.raw.json"
        if raw.exists():
            if not (folder / "02_output.execution_record.json").exists():
                raise SystemExit(f"{eid}输出尚未检查留档。")
            previous.append(read(raw))
            continue
        if (folder / "original.prompt.txt").exists():
            print((folder / "original.prompt.txt").read_text())
            return
        inputs = {
            "date": config["date"], "id": eid, "name": person["name"],
            "entity_class": "person",
            "fixed_gender": "男" if person["usage_stratum"] == "male_usage" else "女",
            "entity_places": config["entity_places"],
            "previous_same_type_originals": previous,
            "references": [],
        }
        template_path = BASE / "templates/person.original.txt"
        prompt = template_path.read_text().replace("{{entity_type_zh}}", "人物").replace(
            "{{input_json}}", json.dumps(inputs, ensure_ascii=False, indent=2)
        )
        assert "{{" not in prompt
        save_new(folder / "original.input.json", inputs)
        (folder / "original.prompt.txt").write_text(prompt)
        save_new(folder / "01_input.execution_record.json", {
            "date": datetime.now().astimezone().isoformat(), "actor": "Codex",
            "step": "prompt_saved_before_output", "entity_id": eid,
            "input": "original.input.json", "prompt": "original.prompt.txt",
            "prompt_sha256": hashlib.sha256(prompt.encode()).hexdigest(),
            "template_sha256": hashlib.sha256(template_path.read_bytes()).hexdigest(),
            "model": config["model"], "sampling_parameters": "不可见",
            "context_boundary": config["context_boundary"],
            "raw_output": None, "user_review": "未审核",
        })
        print(prompt)
        return
    print("十个人物原值均已生成并留档。")


if __name__ == "__main__":
    main()
