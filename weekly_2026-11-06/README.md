# 本周工作：数据修订与无信源 baseline / Weekly work: data revision and source-free baseline

本目录为 11 月 6 日会议的完整数据与实验材料。当前为 30 个虚构实体、151 个冲突属性；修订版 v1 数据用于下述无信源诊断。

This directory contains the data and experiment materials for the 6 November meeting. It covers 30 fictional entities and 151 conflict attributes; revised v1 was used for the source-free diagnostics below.

## 从哪里看 / Where to start

- [原始生成过程、指令、输入与输出 / Original generation process, instructions, inputs and outputs](../generation/)：此前已整理的 original pilot data 生成记录。/ The previously shared generation records for Original.
- [Original → v1 完整对照表 / Full Original → v1 comparison](pilot/data_review/value_revision/full_v1/DATA_V1_FULL_SUBMISSION_ZH_EN.md)：全部 30 个实体、151 个属性、每项原值与四个备选，中英对照及修订说明。/ All 30 entities and 151 attributes, with original values, four alternatives and revision rationales in Chinese and English.
- [修订阶段指令与结果 / Revision instructions and results](pilot/data_review/value_revision/PROMPTS_REVISION_SUBMISSION.md)：修订规则、相容性检查及修改。/ Revision rules, compatibility screening and changes.
- [WFW 与中文测试 prompt 对照 / WFW–Chinese prompt comparison](PROMPT_COMPARISON.md)：系统指令与测试形式。/ System instructions and test format.
- [无信源输入与输出示例 / Example input and output](BASELINE_EXAMPLE.md)：一道真实题的两个表序、英文释义及三个模型输出。/ One actual pair in both table orders, an English reading translation and the three models' outputs.
- [baseline 结果与全部文件 / Baseline results and complete files](#无信源-baseline--source-free-baseline)：逐模型输入、原始输出、分析和汇总。/ Complete model inputs, raw outputs, analysis and summaries.

## 数据与方法 / Data and method

- [Original 数据 / Original data](pilot/data/entities_zh.jsonl)；[v1 数据 / Revised v1 data](pilot/data_review/value_revision/full_v1/entities_full_v1.jsonl)。每组五值中，第一个是原值，其余四个是备选。/ Each five-value list contains an original value and four alternatives.
- 修订后每道题仅改变一个属性，其他属性保持原值；每个原值与四个备选配对，每对交换表序，共 604 对、1208 题。/ Each test item changes one attribute while retaining the others' original values; each original–alternative pair is shown in both orders, for 604 pairs and 1,208 items.
- **原始 pilot 数据生成：**模型生成了大部分原值和备选，部分值由代码按规则填入。详见[原始生成记录](../generation/MODEL_INPUT.md)。
  **Original pilot data generation:** The model generated most original values and alternatives; code filled some values using fixed rules. See the [original generation record](../generation/MODEL_INPUT.md).
- **v1 数据修订：**保留大部分原值；数值和日期备选主要由脚本重新生成。为改善相容性，人工确定并替换了四个类别备选，具体见[完整对照表](pilot/data_review/value_revision/full_v1/DATA_V1_FULL_SUBMISSION_ZH_EN.md)。
  **v1 data revision:** Most original values were retained, while scripts regenerated numerical and date alternatives. Four categorical alternatives were manually selected for replacement to improve compatibility; see the [full comparison](pilot/data_review/value_revision/full_v1/DATA_V1_FULL_SUBMISSION_ZH_EN.md).
- **怎么检查：**把每个备选与同一实体的其他原值搭配，检查是否合理。例如，身高备选配原体重，职业备选配原学历。
  **How compatibility was checked:** Each alternative was considered with the same entity’s other original values. For example, height alternatives were checked against original weight, and occupation alternatives against original education.
- 详细材料：[修订生成脚本 / Revision script](pilot/data_review/value_revision/full_v1/build_full_v1.py) · [变更记录 / Change record](pilot/data_review/value_revision/full_v1/changes_from_draft.json) · [相容性筛查 / Compatibility screen](pilot/data_review/value_revision/full_v1/compat_check_v1.json)
- 基础生成规则见[脚本](pilot/data_review/value_revision/draftA_20261104_149/build_full_v1.py)；最终修订脚本读取的[中间输入](pilot/data_review/value_revision/draftB_20261105_150/entities_full_v2.jsonl)也保留，供复核生成过程。/ The [base-generation script](pilot/data_review/value_revision/draftA_20261104_149/build_full_v1.py) and the [intermediate input](pilot/data_review/value_revision/draftB_20261105_150/entities_full_v2.jsonl) consumed by the final revision script are retained for verification.

## 无信源 baseline / Source-free baseline

- 三次运行使用同一版 v1 数据。每对值测试两次：先将原值放在表一、备选放在表二，再交换位置。
  All three runs use v1. Each pair is tested twice: first with the original in Table 1 and the alternative in Table 2, then with their positions swapped.

- **P(备选)**：模型选择备选值的平均概率，看模型偏向原值还是备选。
  **P(alternative):** the mean probability of choosing the alternative, indicating preference for the alternative versus the original.
- **P(表二)**：模型选择第二张表所含值的平均概率，看模型是否偏向这个位置。
  **P(Table 2):** the mean probability of choosing the value in the second table, indicating preference for that position.
- **两种表序均偏向同一值（>80%）**：统计交换位置前后，模型对同一个值的概率都超过 80% 的值对。80% 是本项目暂用的筛查门槛。
  **Same value preferred in both orders (>80%):** the number of pairs where the model assigns more than 80% probability to the same value in each table order. The 80% threshold is a provisional screening choice for this project.

| 模型 / Model | P(备选) / P(alternative) | P(表二) / P(Table 2) | 两种表序均偏向同一值（>80%） / Same value preferred in both orders (>80%) |
|---|---:|---:|---:|
| Qwen2.5-7B-Instruct | 49.9% | 63.2% | 126 / 604 |
| Llama-3.1-8B-Instruct | 50.6% | 71.9% | 96 / 604 |
| Gemma-4-E4B-it | 51.7% | 58.8% | 284 / 604 |

[三模型中英结果说明 / Bilingual results for all three models](BASELINE_RESULTS_ZH_EN.md)

| 模型 / Model | 全部输入 / All prompts | 原始输出 / Raw output | 逐题分析 / Analysis | 汇总 / Summary |
|---|---|---|---|---|
| Qwen2.5-7B | [prompts](pilot/results_baseline/Qwen2.5-7B-Instruct_full_v1/prompts.jsonl) | [raw](pilot/results_baseline/Qwen2.5-7B-Instruct_full_v1/raw.json) | [analysis](pilot/results_baseline/Qwen2.5-7B-Instruct_full_v1/analysis.json) | [summary](pilot/results_baseline/Qwen2.5-7B-Instruct_full_v1/summary.md) |
| Llama-3.1-8B | [prompts](pilot/results_baseline/Llama-3.1-8B-Instruct_full_v1/prompts.jsonl) | [raw](pilot/results_baseline/Llama-3.1-8B-Instruct_full_v1/raw.json) | [analysis](pilot/results_baseline/Llama-3.1-8B-Instruct_full_v1/analysis.json) | [summary](pilot/results_baseline/Llama-3.1-8B-Instruct_full_v1/summary.md) |
| Gemma-4-E4B | [prompts](pilot/results_baseline/gemma-4-E4B-it_full_v1/prompts.jsonl) | [raw](pilot/results_baseline/gemma-4-E4B-it_full_v1/raw.json) | [analysis](pilot/results_baseline/gemma-4-E4B-it_full_v1/analysis.json) | [summary](pilot/results_baseline/gemma-4-E4B-it_full_v1/summary.md) |

原始输出中的 `prob_a` / `prob_b` 是首个 token 的 A/B 分数只在两个答案 token 之间归一化后的概率。`revision_requested` 是请求的模型版本。总体备选概率接近 50% 不能单独证明两个值等可信；三个模型均有位置偏差。/ `prob_a` and `prob_b` are probabilities normalised only over the two answer-token scores at the first generation step. `revision_requested` records the requested model revision. Mean P(alternative) near 50% alone does not establish equal plausibility; all three models show position bias.

推理与分析实现：[`prompt_zh.py`](pilot/prompt_zh.py)、[`run_baseline.py`](pilot/run_baseline.py)、[`run_baseline_compat.py`](pilot/run_baseline_compat.py)、[`model_compat.py`](pilot/model_compat.py)、[`run_pilot.py`](pilot/run_pilot.py)、[`analyze_baseline.py`](pilot/analyze_baseline.py)。

Inference and analysis implementation: [`prompt_zh.py`](pilot/prompt_zh.py), [`run_baseline.py`](pilot/run_baseline.py), [`run_baseline_compat.py`](pilot/run_baseline_compat.py), [`model_compat.py`](pilot/model_compat.py), [`run_pilot.py`](pilot/run_pilot.py), [`analyze_baseline.py`](pilot/analyze_baseline.py).

