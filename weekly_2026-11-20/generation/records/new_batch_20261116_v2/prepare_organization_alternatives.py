"""先保存带完整原表的行业任务prompt，之后由当前会话生成四备选。"""
import hashlib
import json
from datetime import datetime

from prepare_person import BASE, read, save_new

batch = read(BASE / "batch.input.json")
template_path = BASE / "templates/organization.alternatives.txt"
template = template_path.read_text()
assert hashlib.sha256(template_path.read_bytes()).hexdigest() == read(BASE / "00_templates_frozen.execution_record.json")["template_hashes"]["templates/organization.alternatives.txt"]
save_new(BASE / "07_organization_original_feedback.json", {
    "date": datetime.now().astimezone().isoformat(), "actor": "用户；Codex记录",
    "user_verbatim": "好像没问题。。。吧。。。",
    "input_shown": "十家公司名称、所属行业、员工人数、年营业额；完整原值表链接同时提供。",
    "decision": "暂时保留，继续生成候选备选；不是用户已确认商业数量级或最终定稿。",
    "assistant_action": "带完整原值表生成行业备选；人数±5%、营业额±10%按规则生成，不新增80组合审核任务。",
    "changes_to_originals": [],
})
for i in range(1, 11):
    folder = BASE / "entities" / f"ORG-{i:02}"
    original = read(folder / "original.raw.json")
    prompt = template.replace("{{original_table_json}}", json.dumps(original, ensure_ascii=False, indent=2)).replace(
        "{{target_field}}", "所属行业"
    ).replace("{{field_requirements}}", "四个行业均须与原员工人数、原年营业额及成立时间相配；不用同义改写或仅增加修饰词充当不同取值。公司名称不是行业依据；不声称做过外部核验。")
    assert "{{" not in prompt
    path = folder / "alternatives.industry.prompt.txt"
    with path.open("x") as f:
        f.write(prompt)
    save_new(folder / "03_alternatives_input.execution_record.json", {
        "date": datetime.now().astimezone().isoformat(), "actor": "Codex",
        "step": "industry_prompt_saved_before_output", "input": "original.raw.json",
        "input_sha256": hashlib.sha256((folder / "original.raw.json").read_bytes()).hexdigest(),
        "prompt": path.name, "prompt_sha256": hashlib.sha256(prompt.encode()).hexdigest(),
        "model": batch["model"], "sampling_parameters": "不可见", "raw_output": None,
        "context_boundary": batch["context_boundary"], "user_review": "新备选未生成或审核",
    })
    print(f"--- {original['id']} 实际任务prompt ---")
    print(prompt)
