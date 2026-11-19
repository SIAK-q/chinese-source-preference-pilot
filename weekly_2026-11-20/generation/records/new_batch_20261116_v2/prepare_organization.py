"""逐机构先保存实际prompt，前一家输出必须已经检查留档。"""
import hashlib
import json
from datetime import datetime

from prepare_person import BASE, read, save_new

batch = read(BASE / "batch.input.json")
config = read(BASE / "organization.input.json")
template_path = BASE / "templates/organization.original.txt"
template = template_path.read_text()
assert hashlib.sha256(template_path.read_bytes()).hexdigest() == read(BASE / "00_templates_frozen.execution_record.json")["template_hashes"]["templates/organization.original.txt"]
previous = []
for identity in config["identities"]:
    folder = BASE / "entities" / identity["id"]
    raw = folder / "original.raw.json"
    if raw.exists():
        assert (folder / "02_output.execution_record.json").exists(), "前一家输出尚未检查留档"
        previous.append(read(raw))
        continue
    if (folder / "original.prompt.txt").exists():
        print((folder / "original.prompt.txt").read_text())
        break
    inputs = {"date": config["date"], **identity, "entity_class": "organization",
        "entity_places": batch["entity_places"], "previous_same_type_originals": previous,
        "references": [], "identity_note": config["selection"]}
    prompt = template.replace("{{entity_type_zh}}", "机构").replace("{{input_json}}", json.dumps(inputs, ensure_ascii=False, indent=2))
    assert "{{" not in prompt
    save_new(folder / "original.input.json", inputs)
    with (folder / "original.prompt.txt").open("x") as f:
        f.write(prompt)
    save_new(folder / "01_input.execution_record.json", {
        "date": datetime.now().astimezone().isoformat(), "actor": "Codex",
        "step": "organization_prompt_saved_before_generation", "input": "original.input.json",
        "prompt": "original.prompt.txt", "prompt_sha256": hashlib.sha256(prompt.encode()).hexdigest(),
        "template_sha256": hashlib.sha256(template_path.read_bytes()).hexdigest(),
        "model": batch["model"], "sampling_parameters": "不可见",
        "context_boundary": batch["context_boundary"], "raw_output": None,
    })
    print(prompt)
    break
else:
    print("十家机构原值均已生成并记录。")
