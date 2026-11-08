# Data revision and source-free baseline

本目录包含原始 pilot 数据的 v1 修订记录及五模型无信源 baseline。数据共30个实体、151项冲突属性，展开为604对、1208题。

This directory contains the v1 revision records for the original pilot data and the source-free baseline for five models. The data cover 30 entities and 151 conflict attributes, giving 604 pairs and 1,208 items.

## Materials

- [原始生成记录 / Original generation records](../generation/MODEL_INPUT.md)：模型输入、三轮生成与修改，以及对应脚本和数据。<br>Model inputs, three rounds of generation and revision, and the corresponding scripts and data.

- [原始数据 → v1 完整对照 / Full original → v1 comparison](pilot/data_review/value_revision/full_v1/DATA_V1_FULL_SUBMISSION_ZH_EN.md)：151项属性的原值、四个备选及修订说明。<br>Original values, four alternatives and revision rationales for all 151 attributes.

- [数据修订 prompt 与结果 / Data revision prompts and results](pilot/data_review/value_revision/PROMPTS_REVISION_SUBMISSION.md)：取值规则、审核过程和相容性检查。<br>Value rules, review steps and compatibility checks.

- [WFW 与中文测试 prompt 对照 / WFW–Chinese test-prompt comparison](PROMPT_COMPARISON.md)：system prompt 与题目格式。<br>System prompts and item format.

- [实际输入与输出例题 / Actual input and output example](BASELINE_EXAMPLE.md)：一道题的两个表序、英文释义及五模型输出。<br>One pair in both table orders, an English reading translation and outputs from five models.

- [信源名称生成规程草稿 / Draft source-name generation protocol](SOURCE_GENERATION_PROTOCOL_DRAFT.md)：四类信源的命名方法、例子和依据。<br>Naming methods, examples and supporting sources for the four source types.

## Source-free baseline

[五模型结果与分析 / Results and analysis for five models](BASELINE_RESULTS_ZH_EN.md)

- **P(备选) / P(alternative)**：选择备选值的平均概率，用于观察模型偏向原值还是备选。<br>The mean probability of choosing the alternative, indicating preference for the original versus the alternative.

- **P(表二) / P(Table 2)**：选择第二张表所含值的平均概率，用于观察位置偏好。<br>The mean probability of choosing the value in the second table, indicating position preference.

- **两种表序均偏向同一值（>80%） / Same value preferred in both orders (>80%)**：换位前后，对同一个值的概率均超过80%的值对数量；80%为本项目暂用的筛查门槛。<br>The number of pairs where the same value receives more than 80% probability in each order; 80% is a provisional screening threshold for this project.

<details>
<summary>全部输入、输出与分析文件 / All inputs, outputs and analysis files</summary>

- `prompts.jsonl` 保存实际输入，`raw.json` 保存逐题结果，按题目编号 `i` 对应。<br>`prompts.jsonl` contains the actual inputs and `raw.json` the item-level results, matched by item number `i`.

- `prob_a` 和 `prob_b` 为生成第一步的A/B分数仅在这两个答案token之间归一化后的概率；`revision_requested` 为请求的模型版本。<br>`prob_a` and `prob_b` are probabilities normalised over only the A/B answer-token scores at the first generation step; `revision_requested` records the requested model revision.

| 模型 / Model | 输入 / Inputs | 输出 / Outputs | 分析 / Analysis | 汇总 / Summary |
|---|---|---|---|---|
| Qwen2.5-7B | [prompts](pilot/results_baseline/Qwen2.5-7B-Instruct_full_v1/prompts.jsonl) | [raw](pilot/results_baseline/Qwen2.5-7B-Instruct_full_v1/raw.json) | [analysis](pilot/results_baseline/Qwen2.5-7B-Instruct_full_v1/analysis.json) | [summary](pilot/results_baseline/Qwen2.5-7B-Instruct_full_v1/summary.md) |
| Qwen2.5-14B | [prompts](pilot/results_baseline/Qwen2.5-14B-Instruct_full_v1/prompts.jsonl) | [raw](pilot/results_baseline/Qwen2.5-14B-Instruct_full_v1/raw.json) | [analysis](pilot/results_baseline/Qwen2.5-14B-Instruct_full_v1/analysis.json) | [summary](pilot/results_baseline/Qwen2.5-14B-Instruct_full_v1/summary.md) |
| Llama-3.1-8B | [prompts](pilot/results_baseline/Llama-3.1-8B-Instruct_full_v1/prompts.jsonl) | [raw](pilot/results_baseline/Llama-3.1-8B-Instruct_full_v1/raw.json) | [analysis](pilot/results_baseline/Llama-3.1-8B-Instruct_full_v1/analysis.json) | [summary](pilot/results_baseline/Llama-3.1-8B-Instruct_full_v1/summary.md) |
| Gemma-4-E4B | [prompts](pilot/results_baseline/gemma-4-E4B-it_full_v1/prompts.jsonl) | [raw](pilot/results_baseline/gemma-4-E4B-it_full_v1/raw.json) | [analysis](pilot/results_baseline/gemma-4-E4B-it_full_v1/analysis.json) | [summary](pilot/results_baseline/gemma-4-E4B-it_full_v1/summary.md) |
| Gemma-4-12B | [prompts](pilot/results_baseline/gemma-4-12B-it_full_v1/prompts.jsonl) | [raw](pilot/results_baseline/gemma-4-12B-it_full_v1/raw.json) | [analysis](pilot/results_baseline/gemma-4-12B-it_full_v1/analysis.json) | [summary](pilot/results_baseline/gemma-4-12B-it_full_v1/summary.md) |

</details>

<details>
<summary>数据与代码文件 / Data and code files</summary>

- [原始 pilot 数据 / Original pilot data](pilot/data/entities_zh.jsonl) · [v1 数据 / Revised v1 data](pilot/data_review/value_revision/full_v1/entities_full_v1.jsonl)。每个属性的五值列表中，第一个为原值，其余四个为备选。<br>Each attribute has a five-value list: the first is the original and the remaining four are alternatives.

- [修订脚本 / Revision script](pilot/data_review/value_revision/full_v1/build_full_v1.py) · [变更记录 / Change record](pilot/data_review/value_revision/full_v1/changes_from_draft.json) · [相容性筛查 / Compatibility screen](pilot/data_review/value_revision/full_v1/compat_check_v1.json)。

- [基础生成脚本 / Base-generation script](pilot/data_review/value_revision/draftA_20261104_149/build_full_v1.py) · [最终修订脚本读取的中间数据 / Intermediate data read by the final revision script](pilot/data_review/value_revision/draftB_20261105_150/entities_full_v2.jsonl)。

- 推理与分析代码 / Inference and analysis code：[`prompt_zh.py`](pilot/prompt_zh.py) · [`run_baseline.py`](pilot/run_baseline.py) · [`run_baseline_compat.py`](pilot/run_baseline_compat.py) · [`model_compat.py`](pilot/model_compat.py) · [`run_pilot.py`](pilot/run_pilot.py) · [`analyze_baseline.py`](pilot/analyze_baseline.py)。

</details>
