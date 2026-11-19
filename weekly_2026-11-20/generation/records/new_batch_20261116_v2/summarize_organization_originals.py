"""汇总机构原值及阶段进度，保留所有旧数据和改前文档。"""
import hashlib
import json
from datetime import datetime

from prepare_person import BASE, read, save_new

fields = read(BASE / "fields.json")["organization"]
rows = []
hashes = {}
for i in range(1, 11):
    folder = BASE / "entities" / f"ORG-{i:02}"
    raw = read(folder / "original.raw.json")
    inputs = read(folder / "original.input.json")
    output_record = read(folder / "02_output.execution_record.json")
    assert inputs["previous_same_type_originals"] == rows
    assert all(output_record["checks"].values())
    assert set(raw) == {"id", "name", "entity_class", *fields}
    rows.append(raw)
    hashes[raw["id"]] = hashlib.sha256((folder / "original.raw.json").read_bytes()).hexdigest()

path = BASE / "organization.originals.pending_review.jsonl"
with path.open("x") as f:
    f.write("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows))
lines = ["# 新批次机构原值", "",
    "- **已生成**：10家机构的完整原值；五项属性重新填写，名称和ID沿用旧批次。四备选尚未生成，用户尚未审核。",
    "- **生成要求**：行业、员工人数、年营业额一起考虑；不另设80组合检查任务。",
    "- **检查**：字段、年月、人数、币种、总部地名池及前序输入一致性通过；生成记录与raw分别保留。",
    "- **边界**：本步未外查公司名称或逐行业现实数据；不把模型判断当作等可信证明。",
    "", "| 公司 | 成立时间 | 行业 | 总部 | 员工人数 | 年营业额 |", "|---|---|---|---|---|---|"]
for row in rows:
    lines.append("| " + " | ".join([row["name"], *[row[k] for k in fields]]) + " |")
text = "\n".join(lines) + "\n"
with (BASE / "REVIEW_organization_originals.md").open("x") as f:
    f.write(text)
mirror = BASE.parents[1] / "notes/02 数据/合成数据/新批次机构原值.md"
with mirror.open("x") as f:
    f.write(text)

changes = []
person_doc = BASE / "REVIEW_person.md"
person_mirror = BASE.parents[1] / "notes/02 数据/合成数据/新批次人物备选.md"
for n, doc in enumerate((person_doc, person_mirror)):
    before = doc.read_bytes()
    with (BASE / f"person_review_before_user_acceptance_{n}.md").open("xb") as f:
        f.write(before)
    content = before.decode().replace(
        "- **已生成**：10人物、90属性项，每项原值＋四备选；新备选尚未由用户审核。",
        "- **已生成**：10人物、90属性项，每项原值＋四备选。\n- **用户反馈（2026-11-16）**：本轮职业学历备选“没问题”，保留；不据此声称其余字段已逐项人工审核，决定见05_person_review_decisions.json。"
    )
    doc.write_text(content)
    changes.append({"path": str(doc), "before_sha256": hashlib.sha256(before).hexdigest(), "after_sha256": hashlib.sha256(doc.read_bytes()).hexdigest()})

readme = BASE / "README.md"
before = readme.read_bytes()
with (BASE / "README.before_organization_originals.md").open("xb") as f:
    f.write(before)
content = before.decode().replace(
    "- **当前**：人物10个已生成原值和四备选，90属性项；其余六类尚未生成。",
    "- **当前**：人物10个已生成原值和四备选；机构10家原值已生成、四备选尚未生成；其余五类尚未生成。"
).replace(
    "用户已认可展示的职业学历原值，新备选未审。",
    "用户已认可本轮职业学历原值及备选；其他字段不记作已逐项人工审核。\n- **机构原值**：[查看表](REVIEW_organization_originals.md)，已同步Obsidian；数据organization.originals.pending_review.jsonl。"
).replace(
    "- **下一步**：用户看人物备选，按具体反馈修订；再推进机构类。",
    "- **下一步**：用户查看机构原值；随后带完整原值表生成行业备选，其余四项按已定规则处理。"
)
readme.write_text(content)
changes.append({"path": str(readme), "before_sha256": hashlib.sha256(before).hexdigest(), "after_sha256": hashlib.sha256(readme.read_bytes()).hexdigest()})
assert person_doc.read_bytes() == person_mirror.read_bytes()
assert mirror.read_text() == text
save_new(BASE / "06_organization_originals.execution_record.json", {
    "date": datetime.now().astimezone().isoformat(), "actor": "Codex",
    "step": "机构十原值汇总及人审状态同步", "script": "summarize_organization_originals.py",
    "input": "ORG-01至10的original.input、original.prompt、original.raw及01/02执行记录",
    "method": "原值由当前会话逐实体读先存prompt后撰写；本脚本只汇总，不重新生成。",
    "model": read(BASE / "batch.input.json")["model"], "sampling_parameters": "不可见",
    "raw_output_hashes": hashes, "dataset_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
    "checks": {"10_originals_complete": True, "prior_inputs_match_real_outputs": True,
        "all_format_checks_passed": True, "two_document_mirror_pairs_identical": True},
    "document_changes": changes, "raw_data_changes": [],
    "review_state": {"person_career_education_alternatives": "用户说没问题，保留", "organization_originals": "未审核"},
    "alternatives_generated_for_organizations": False, "baseline_run": False,
    "next_step": "用户查看机构原值，再按规程带完整表生成行业备选，数值日期城市按规则生成。",
})
print("10机构原值汇总完成；两对查看表/Obsidian镜像一致，未生成机构备选。")
