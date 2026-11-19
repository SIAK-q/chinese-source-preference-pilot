"""汇总原始输出、顺序记录和待审表；不改变数据。"""
import hashlib
import json
from collections import Counter
from datetime import datetime
from pathlib import Path

from prepare_person import BASE, read, save_new

rows = []
checks = []
frozen = read(BASE / "00_templates_frozen.execution_record.json")
old_rows = {
    row["id"]: row
    for row in (
        json.loads(line)
        for line in (BASE.parent / "night_batch_20261116/entities.pending_review.jsonl").read_text().splitlines()
    )
}
for relative, digest in frozen["template_hashes"].items():
    assert hashlib.sha256((BASE / relative).read_bytes()).hexdigest() == digest
for i in range(1, 11):
    folder = BASE / "entities" / f"PERSON-{i:02}"
    raw = read(folder / "original.raw.json")
    inputs = read(folder / "original.input.json")
    record = read(folder / "02_output.execution_record.json")
    assert inputs["previous_same_type_originals"] == rows
    assert all(record["checks"].values())
    old = old_rows[raw["id"]]
    assert any(raw[k] != old[k][0] for k in read(BASE / "fields.json")["person"])
    height = int(raw["身高"].removesuffix("厘米"))
    weight = int(raw["体重"].removesuffix("公斤"))
    checks.append({
        "id": raw["id"], "age": record["age_at_generation"],
        "bmi_description_only": round(weight / ((height / 100) ** 2), 2),
        "prior_originals_match": True,
        "assistant_review": "未标出职业学历、年龄职业或身高体重的明显搭配冲突；未作职业资格核验。",
        "user_review": "未审核",
    })
    rows.append(raw)

data_path = BASE / "person.originals.pending_review.jsonl"
with data_path.open("x") as f:
    f.write("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows))

md = ["# 新批次人物原值", "", "- **已完成**：七类模板先保存，10个人物逐个保存输入后生成原值；四备选尚未生成。", "- **姓名**：沿用已认可姓名池，属性重新填写；旧批次审核意见不转移到新值。", "- **检查**：字段、单位、日期、地名池与前序输入一致性通过；助手未标出明显搭配冲突，用户尚未审核。", "- **生成方式**：当前Codex会话依次执行保存的任务prompt；已见旧候选的历史上下文仍可见，具体模型版本和采样参数不可见。", "", "| 姓名 | 年龄／性别 | 职业 | 学历 | 身高／体重 | 婚姻状况 |", "|---|---|---|---|---|---|"]
for row, check in zip(rows, checks):
    md.append(f"| {row['name']} | {check['age']}／{row['性别']} | {row['职业']} | {row['学历']} | {row['身高']}／{row['体重']} | {row['婚姻状况']} |")
md += ["", "<details>", "<summary>出生日期及地名字段</summary>", "", "| 姓名 | 出生日期 | 现居城市 | 出生地 | 籍贯 |", "|---|---|---|---|---|"]
for row in rows:
    md.append("| " + " | ".join(row[k] for k in ("name", "出生日期", "现居城市", "出生地", "籍贯")) + " |")
md += ["", "</details>", ""]
text = "\n".join(md)
with (BASE / "REVIEW_person_originals.md").open("x") as f:
    f.write(text)
mirror = BASE.parents[1] / "notes/02 数据/合成数据/新批次人物原值.md"
with mirror.open("x") as f:
    f.write(text)
save_new(BASE / "01_person_originals.execution_record.json", {
    "date": datetime.now().astimezone().isoformat(), "actor": "Codex",
    "step": "汇总十个人物原值并检查生成记录顺序",
    "inputs": "entities/PERSON-01至10的输入、prompt、原始输出和检查记录",
    "script": "summarize_person_originals.py",
    "script_fix": "首次汇总在读取旧PERSON-01独立文件时失败；旧批次该人沿用外部样例。失败发生在写汇总输出前；改为读取旧整批JSONL，脚本改前副本保留。",
    "model_version_and_parameters": "不可见；本步仅脚本汇总",
    "checks": checks, "raw_output_edits": [], "user_decision": "未审核新批次",
    "check_summaries": {"all_prior_inputs_match_actual_outputs": True,
        "all_template_hashes_unchanged": True, "review_mirror_identical": mirror.read_text() == text,
        "education_levels_descriptive": dict(Counter(r["学历"].split("（")[0] for r in rows)),
        "marital_status_descriptive": dict(Counter(r["婚姻状况"] for r in rows))},
    "output": data_path.name, "output_sha256": hashlib.sha256(data_path.read_bytes()).hexdigest(),
    "alternatives_generated": False, "other_entity_types_generated": False,
    "baseline_run": False,
    "next_step": "展示人物原值供用户看职业学历及表达；随后按先存prompt再生成的流程联合生成两组备选。",
})
with (BASE / "README.md").open("x") as f:
    f.write("# 新批次生成记录\n\n- **范围**：计划七类各10实体；当前仅生成10个人物原值，未生成四备选或其他六类。\n- **输入**：batch.input.json、fields.json；templates先保存，哈希见00_templates_frozen.execution_record.json，规则快照保留。\n- **过程**：逐实体先保存original.input和original.prompt，再由当前会话生成original.raw；每人01/02记录分开存，脚本不替代模型生成。\n- **查看**：[人物原值表](REVIEW_person_originals.md)；输出person.originals.pending_review.jsonl，汇总检查见01_person_originals.execution_record.json。\n- **边界**：当前会话历史含旧候选；不是隔离API调用；具体模型版本及参数不可见。旧数据保留，用户尚未审核新批次。\n- **下一步**：处理人物原值反馈，再生成职业学历、身高体重联合备选及其余字段备选；未跑baseline。\n")
print(json.dumps({"person_originals": len(rows), "alternatives_generated": False, "review_mirror_identical": mirror.read_text() == text}, ensure_ascii=False))
