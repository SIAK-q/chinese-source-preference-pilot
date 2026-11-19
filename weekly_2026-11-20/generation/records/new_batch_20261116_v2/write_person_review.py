"""生成用户查看表并同步Obsidian；数据与历史记录不覆盖。"""
import hashlib
import json
from datetime import datetime

from prepare_person import BASE, read, save_new

entities = [json.loads(line) for line in (BASE / "person.entities.pending_review.jsonl").read_text().splitlines()]
review = ["# 新批次人物备选", "",
    "- **已生成**：10人物、90属性项，每项原值＋四备选；新备选尚未由用户审核。",
    "- **已检查**：五值互异、身高体重范围、原值未变；720题只做组题预览，未运行模型。",
    "- **怎么看**：下表展示两组成对生成结果；实际实验每题只替换一个字段，其余保持原值。",
    "- **本轮重点**：职业与学历的说法及搭配；身高体重由助手同时考虑，范围检查通过。", ""]
for e in entities:
    review += [f"## {e['name']}", "", f"- **背景**：{e['性别']}，出生日期原值{e['出生日期'][0]}；婚姻状况原值{e['婚姻状况'][0]}。", "",
        "| 类型 | 职业 | 学历 | 身高 | 体重 |", "|---|---|---|---|---|"]
    for i in range(5):
        label = "原值" if i == 0 else f"备选{i}"
        review.append("| " + " | ".join([label, *[e[k][i] for k in ("职业", "学历", "身高", "体重")]]) + " |")
    review += ["", "<details>", "<summary>日期、婚姻及城市备选</summary>", "", "| 属性 | 原值 | 备选1 | 备选2 | 备选3 | 备选4 |", "|---|---|---|---|---|---|"]
    for field in ("出生日期", "婚姻状况", "现居城市", "出生地", "籍贯"):
        review.append("| " + " | ".join([field, *e[field]]) + " |")
    review += ["", "</details>", ""]
text = "\n".join(review)
with (BASE / "REVIEW_person.md").open("x") as f:
    f.write(text)
mirror = BASE.parents[1] / "notes/02 数据/合成数据/新批次人物备选.md"
with mirror.open("x") as f:
    f.write(text)
readme = BASE / "README.md"
with (BASE / "README.before_person_alternatives.md").open("x") as f:
    f.write(readme.read_text())
readme.write_text("""# 新批次生成记录

- **当前**：人物10个已生成原值和四备选，90属性项；其余六类尚未生成。
- **查看**：[人物备选表](REVIEW_person.md)，已同步Obsidian《新批次人物备选》。用户已认可展示的职业学历原值，新备选未审。
- **实际输入**：七类模板先保存于templates，冻结哈希见00记录；每个人先保存原值prompt再生成，备选两组prompt也先存后生成。
- **数据**：person.entities.pending_review.jsonl；20份成对raw及每人01至06记录保留。日期、婚姻和城市由assemble_person.py按已定规则生成。
- **检查**：五值互异、数值范围及组题检查通过；720题预览未推理，检查无ERROR或REVIEW标记。结构通过不代表等可信。
- **留痕**：02_original_review_decisions.json存用户认可范围；03_person_complete.execution_record.json存脚本版本、种子输入、数据哈希及检查；原始输出未修改。
- **边界**：当前会话历史含旧批次，非隔离API调用；具体模型版本和采样参数不可见；旧批次完整保留。
- **下一步**：用户看人物备选，按具体反馈修订；再推进机构类。
""")
save_new(BASE / "04_person_review_export.execution_record.json", {
    "date": datetime.now().astimezone().isoformat(), "actor": "Codex",
    "step": "导出人物备选表及更新进度说明", "script": "write_person_review.py",
    "input": "person.entities.pending_review.jsonl",
    "input_sha256": hashlib.sha256((BASE / "person.entities.pending_review.jsonl").read_bytes()).hexdigest(),
    "outputs": ["REVIEW_person.md", str(mirror), "README.md"],
    "checks": {"mirror_identical": mirror.read_text() == text},
    "changes": "新增备选表及镜像；更新README，改前副本README.before_person_alternatives.md保留。无数据修改。",
    "user_decision": "备选未审核", "model_version_and_parameters": "本步仅脚本导出；未调用模型。",
})
assert mirror.read_text() == text
print("人物备选查看表与Obsidian镜像一致；历史原值表与原始输出保留。")
