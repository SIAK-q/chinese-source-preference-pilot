"""导出机构查看表，明确区分暂保留和用户确认。"""
import hashlib
import json
from datetime import datetime

from prepare_person import BASE, read, save_new

rows = [json.loads(line) for line in (BASE / "organization.entities.pending_review.jsonl").read_text().splitlines()]
lines = ["# 新批次机构备选", "",
    "- **当前**：10机构、50属性项，原值＋四备选已生成；原值暂保留，备选待看。",
    "- **生成**：行业带完整原表生成；人数±5%、营业额±10%，年月和总部按既定规则处理。",
    "- **检查**：五值互异、数值范围及400题组题预览通过；本轮可重点看行业名称。",
    "- **实验**：每题只替换一个属性，其他字段保持原值。", ""]
for e in rows:
    lines += [f"## {e['name']}", "", "| 属性 | 原值 | 备选1 | 备选2 | 备选3 | 备选4 |", "|---|---|---|---|---|---|"]
    for field in read(BASE / "fields.json")["organization"]:
        lines.append("| " + " | ".join([field, *e[field]]) + " |")
    lines.append("")
text = "\n".join(lines)
path = BASE / "REVIEW_organization.md"
with path.open("x") as f:
    f.write(text)
mirror = BASE.parents[1] / "notes/02 数据/合成数据/新批次机构备选.md"
with mirror.open("x") as f:
    f.write(text)

changes = []
original_docs = [BASE / "REVIEW_organization_originals.md", BASE.parents[1] / "notes/02 数据/合成数据/新批次机构原值.md"]
for n, doc in enumerate(original_docs):
    before = doc.read_bytes()
    with (BASE / f"organization_original_review.before_alternatives_{n}.md").open("xb") as f:
        f.write(before)
    content = before.decode().replace(
        "四备选尚未生成，用户尚未审核。",
        "四备选已另存《新批次机构备选》；用户对本表反馈“好像没问题。。。吧。。。”，记为暂保留。"
    )
    doc.write_text(content)
    changes.append({"path": str(doc), "before_sha256": hashlib.sha256(before).hexdigest(), "after_sha256": hashlib.sha256(doc.read_bytes()).hexdigest()})

readme = BASE / "README.md"
before = readme.read_bytes()
with (BASE / "README.before_organization_alternatives.md").open("xb") as f:
    f.write(before)
content = before.decode().replace(
    "机构10家原值已生成、四备选尚未生成",
    "机构10家原值与四备选已生成，原值暂保留、新备选待看"
).replace(
    "- **机构原值**：[查看表](REVIEW_organization_originals.md)，已同步Obsidian；数据organization.originals.pending_review.jsonl。",
    "- **机构**：[完整备选表](REVIEW_organization.md)已同步Obsidian；数据organization.entities.pending_review.jsonl，08记录保存检查结果及哈希。"
).replace(
    "- **下一步**：用户查看机构原值；随后带完整原值表生成行业备选，其余四项按已定规则处理。",
    "- **下一步**：用户看机构行业备选名称；再推进地点类。"
)
readme.write_text(content)
changes.append({"path": str(readme), "before_sha256": hashlib.sha256(before).hexdigest(), "after_sha256": hashlib.sha256(readme.read_bytes()).hexdigest()})
assert mirror.read_text() == text
assert original_docs[0].read_bytes() == original_docs[1].read_bytes()
save_new(BASE / "09_organization_review_export.execution_record.json", {
    "date": datetime.now().astimezone().isoformat(), "actor": "Codex",
    "step": "导出机构备选及同步暂保留状态", "script": "write_organization_review.py",
    "input": "organization.entities.pending_review.jsonl", "output": [path.name, str(mirror)],
    "checks": {"review_mirror_identical": True, "original_review_mirror_identical": True},
    "changes": changes, "raw_data_edits": [],
    "user_decision": "原值暂保留，不冒称已通过商业数量级复核；新备选未人审。",
    "model_version_and_parameters": "本步脚本导出未调用模型。",
})
print("机构完整备选表已导出并同步Obsidian；原值暂保留状态单独记录。")
