"""逐建筑保存实际任务prompt；使用已定主要材料字段。"""
import hashlib
import json
from datetime import datetime

from prepare_person import BASE, read, save_new

config = read(BASE / "building.input.json")
batch = read(BASE / "batch.input.json")
template_path = BASE / "templates/building.original.txt"
assert hashlib.sha256(template_path.read_bytes()).hexdigest() == read(BASE / "00_templates_frozen.execution_record.json")["template_hashes"]["templates/building.original.txt"]
previous = []
for identity in config["identities"]:
    folder = BASE / "entities" / identity["id"]
    raw = folder / "original.raw.json"
    if raw.exists():
        assert (folder / "02_output.execution_record.json").exists()
        previous.append(read(raw))
        continue
    if (folder / "original.prompt.txt").exists():
        print((folder / "original.prompt.txt").read_text())
        break
    inputs = {"date": config["date"], **identity, "entity_class": "building",
        "fixed_architect": identity["architect_candidates"][0],
        "architect_rule": "设计师原值固定为上述fixed_architect，另外四名保留给设计师备选。",
        "material_definition": config["material_definition"], "other_definitions": config["other_definitions"],
        "coverage_requirement": config["coverage_requirement"],
        "previous_same_type_originals": previous, "references": []}
    prompt = template_path.read_text().replace("{{entity_type_zh}}", "建筑").replace("{{input_json}}", json.dumps(inputs, ensure_ascii=False, indent=2))
    assert "{{" not in prompt
    save_new(folder / "original.input.json", inputs)
    with (folder / "original.prompt.txt").open("x") as f:
        f.write(prompt)
    save_new(folder / "01_input.execution_record.json", {
        "date": datetime.now().astimezone().isoformat(), "actor": "Codex",
        "step": "building_prompt_saved_before_output", "input": "original.input.json",
        "prompt": "original.prompt.txt", "prompt_sha256": hashlib.sha256(prompt.encode()).hexdigest(),
        "model": batch["model"], "sampling_parameters": "不可见",
        "context_boundary": batch["context_boundary"], "raw_output": None,
    })
    print(prompt)
    break
else:
    print("十建筑原值均已生成并留档。")
