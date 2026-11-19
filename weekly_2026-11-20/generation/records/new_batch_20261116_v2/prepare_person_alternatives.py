"""先保存人物两组成对任务的实际prompt，再由当前会话生成输出。"""
import hashlib
from datetime import datetime

from prepare_person import BASE, read, save_new

template_path = BASE / "templates/person.paired_alternatives.txt"
template = template_path.read_text()
config = read(BASE / "batch.input.json")
frozen = read(BASE / "00_templates_frozen.execution_record.json")
assert hashlib.sha256(template_path.read_bytes()).hexdigest() == frozen["template_hashes"]["templates/person.paired_alternatives.txt"]
groups = {"occupation_education": "职业＋学历", "height_weight": "身高＋体重"}

import json
for i in range(1, 11):
    folder = BASE / "entities" / f"PERSON-{i:02}"
    original = read(folder / "original.raw.json")
    prompt_paths = {}
    for key, fields in groups.items():
        text = template.replace("{{original_table_json}}", json.dumps(original, ensure_ascii=False, indent=2)).replace("{{paired_fields}}", fields)
        path = folder / f"alternatives.{key}.prompt.txt"
        with path.open("x") as f:
            f.write(text)
        prompt_paths[key] = {"path": path.name, "sha256": hashlib.sha256(text.encode()).hexdigest()}
    save_new(folder / "03_alternatives_input.execution_record.json", {
        "date": datetime.now().astimezone().isoformat(), "actor": "Codex",
        "step": "both_paired_prompts_saved_before_output", "input": "original.raw.json",
        "input_sha256": hashlib.sha256((folder / "original.raw.json").read_bytes()).hexdigest(),
        "prompts": prompt_paths, "model": config["model"], "sampling_parameters": "不可见",
        "context_boundary": config["context_boundary"],
        "execution_unit": "本会话读取同一人物两份实际任务prompt，分别保存两组成对输出；不是两次隔离API请求。",
        "raw_outputs": None, "user_review": "备选尚未生成及审核",
    })

save_new(BASE / "02_original_review_decisions.json", {
    "date": datetime.now().astimezone().isoformat(), "actor": "用户；Codex记录",
    "input_shown": "十个人物的姓名、职业、学历表；完整原值表链接同时提供。",
    "verbatim_feedback": ["没问题。但是工程预算员是什么职业", "OK没问题。然后呢？"],
    "confirmed_scope": "用户认可展示的职业与学历搭配，并接受工程预算员的解释；保留对应原值。",
    "not_inferred": "不把此反馈记为所有未展示属性或尚未生成备选已经逐项人工审核。",
    "changes": [], "next_step": "两组成对生成，其他字段按已定规则生成。",
})
print("十个人物的两组成对任务prompt已先保存；原值认可范围已单独记录。")
