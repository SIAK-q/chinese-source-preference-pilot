---
updated: 2026-11-05
status: 提交版草稿，待审核
---
# 数据修订 prompt 与结果 / Data revision prompts and results

本页按实施顺序整理从原始 pilot 数据到修订版 v1 的过程。以下列出各步骤的完整 prompt；脚本规则和结果可通过对应文件核对。旧数据保留不变。

This page presents the revision from the original pilot data to revised v1 in implementation order. The complete prompts for each step are presented below. Script rules and results can be checked against the corresponding files. The original data remains unchanged.

## 版本 / Versions

| 版本 / Version | 冲突属性 / Attributes | 题量 / Items | 数据文件 / Data file |
|---|---:|---:|---|
| 原始 pilot 数据 / Original pilot data | 151 | 1208 | `pilot/data/entities_zh.jsonl` |
| 修订版 v1 / Revised v1 | 151 | 1208 | `full_v1/entities_full_v1.jsonl` |

每个属性有四个备选值，每对值使用两种表序。本文直接展示原始 pilot 数据和修订版 v1。

Each attribute has four alternatives, and each pair is presented in both table orders. This page presents the original pilot data and revised v1 directly.

## 1. 制定规则并试做 / Define rules and prepare examples

**目标 / Aim**：缩小数值备选与原值的差距，并检查备选值与同一实体其他信息的相容性。
Reduce the distance between numerical alternatives and the original value, and check compatibility with the entity's other attributes.

**Prompt**：为需要修改的属性制定取值和检查规则，先从七类实体中各选一个做示例。每次只改变一个属性，其他属性保持原值；另存示例，不覆盖旧数据。
Set value and checking rules for attributes requiring revision, then demonstrate them on one entity from each of the seven types. Change one attribute at a time, keeping the others at their original values. Save examples separately without overwriting the original data.

**结果 / Result**：`demo_entities.jsonl`、`demo_changes.json` 和 `acceptance_2ab.json`、`acceptance_2c.json`、`acceptance_2d.json`。

## 2. 生成修订数据 / Generate revised data

**Prompt**：将取值规则用于全部 30 个实体，记录修改前后的值、方法和理由；未确定的参数标为暂定。
Apply the value rules to all 30 entities. Record the old and new values, methods and reasons, and mark unsettled parameters as provisional.

**脚本规则 / Script rules**（`draftA_20261104_149/build_full_v1.py`，固定随机种子 / fixed random seed）：

| 属性类型 / Type | 规则 / Rule |
|---|---|
| 连续数值 / Continuous | 原值 ±5%，两低两高 / ±5%, two lower and two higher |
| 年营业额 / Revenue | ±10% |
| 完整日期 / Full dates | ±365 天，四个区间各取一天；举办日期保持星期几 / ±365 days, one per interval; event dates retain the weekday |
| 年月 / Year–month | ±12 个月 / ±12 months |
| 年份 / Years | −2、−1、+1、+2 |
| 计数 / Counts | n−2、n−1、n+1、n+2 |
| 类别 / Categories | 沿用旧备选 / Keep original alternatives |

**说明 / Note**：上表记录批量生成阶段使用的规则；具体字段在后续审核中有调整，以当前修订版的实际取值为准。
The table records the rules used in batch generation; subsequent review adjusted individual fields. The current revised data contains the resulting values.


## 3. 逐字段检查取值 / Review attribute values

**Prompt**：列出规则尚未确定或可能与背景不相容的字段。先定义字段含义，再查相关中文资料，提出取值及备选方案；区分资料支持的事实与本项目选择的规则。每次检查一个备选值与其他原值是否相容。
List attributes with unsettled rules or potential conflicts with background information. Define each attribute, consult relevant Chinese sources, and propose values and alternatives. Distinguish source-supported facts from project choices. Check each alternative against the other original values.

**主要结果 / Main outcomes**：

| 字段 / Attribute | 修订后取值或规则 / Revised values or rule |
|---|---|
| 马拉松持续时间 / Marathon duration | 定义为大众组首枪至终点关门的时限；原值 6小时15分钟，备选 6小时、6小时5分钟、6小时25分钟、6小时30分钟。/ Time from the first mass start to the finish cutoff; original 6 h 15 min, alternatives 6 h, 6 h 5 min, 6 h 25 min, 6 h 30 min. |
| 图书馆高度 / Library height | 原值 24 米；备选 22、23、25、26 米。/ Original 24 m; alternatives 22, 23, 25, 26 m. |
| 图书馆层数 / Library floors | 原值 3 层；备选 4、5、6、7 层。/ Original 3 floors; alternatives 4, 5, 6, 7 floors. |
| 年营业额 / Revenue | ±10%；屹嘉股份采用一位小数。/ ±10%; one decimal place for Yijia. |
| 下辖乡镇数 / Towns | 原值保留；备选按 ±1、±2。/ Keep the original; alternatives ±1 and ±2. |
| 公司成立时间 / Founding date | 年月格式，±12 个月。/ Year–month format, ±12 months. |

## 4. 全表审核 / Review the full table

**Prompt**：逐行审核拟修改项；仅在备选明显反直觉时修改类别值，不为格式统一而改变原值。数值备选兼顾该实体的合理性与自然写法。
Review the proposed changes item by item. Change categorical alternatives only when clearly counter-intuitive, and do not change original values merely for formatting consistency. Choose numerical alternatives that are plausible for the entity and naturally written.

**结果 / Result**：采用一项职业备选替换；其余拟替换的类别备选保留。四个原值保留原有写法，数值备选相应调整。具体改动记录在 `full_v1/build_full_v1.py` 的 `REVIEW_EDITS` 和 `full_v1/` 的变更文件中。修订版 v1 共 151 个属性、1208 题。Qwen2.5-7B、Llama-3.1-8B 和 Gemma-4-E4B 的无信源 baseline 已运行，结果见实验记录。
One occupation alternative was replaced; the other proposed categorical replacements were not adopted. Four original values retained their original written form and their numerical alternatives were adjusted. Details are recorded in `REVIEW_EDITS` in `full_v1/build_full_v1.py` and the change files in `full_v1/`. Revised v1 has 151 attributes and 1,208 items. Source-free baselines have been run with Qwen2.5-7B, Llama-3.1-8B and Gemma-4-E4B; results are in the experiment records.

## 5. 属性相容性筛查 / Attribute compatibility screen

**Prompt**：在实际出题方式下，逐一检查原值和每个备选与该实体其他原值的搭配；对明确的相容性疑点提出修改，记录修改原因。
Check each original and alternative against the other original attributes under the actual item construction. Propose changes where compatibility issues are identified, and record the reasons.

**结果 / Result**：筛查后修改三个备选：蒋雨柔职业的「县医院药剂师」改为「县医院ICU护士」，学历的「大专（医学检验技术）」改为「大专（助产）」；新定会展中心主体结构的「膜结构」改为「框架-剪力墙结构」。前两项改善职业和学历的搭配，第三项改善结构类型与多层建筑背景的搭配。原始取值及逐项对照见完整数据表。
Three alternatives were revised after the screen: Jiang Yurou's occupation from county-hospital pharmacist to county-hospital ICU nurse, and education from medical laboratory technology to midwifery; Xinding Convention and Exhibition Centre's structure from membrane structure to frame–shear-wall structure. The first two improve occupation–education compatibility; the third better fits the multi-storey building context. The original values and item-level comparison are in the full data table.

## 文件 / Files

原始 pilot 数据 / Original pilot data: `pilot/data/entities_zh.jsonl`；当前修订版 / current revised data: `full_v1/entities_full_v1.jsonl`；修订脚本和变更记录 / revision script and change records: `full_v1/`。
