# 本周工作：数据修订与无信源 baseline / Weekly work: data revision and source-free baseline

本目录汇集 11 月 6 日会议的完整数据与实验材料。当前为 30 个虚构实体、151 个冲突属性；Original 保留不变，修订版 v1 用于下述无信源诊断。这是小规模 pilot，不用于解释信源偏好。

This directory contains the data and experiment materials for the 6 November meeting. It covers 30 fictional entities and 151 conflict attributes; Original is retained and the revised v1 was used for the source-free diagnostics below. This is a small pilot, not an analysis of source preferences.

## 从哪里看 / Where to start

1. [原始生成过程、指令、输入与输出 / Original generation process, instructions, inputs and outputs](../generation/)：此前已整理的 Original 生成记录。/ The previously shared generation records for Original.
2. [Original → v1 完整对照表 / Full Original → v1 comparison](pilot/data_review/value_revision/full_v1/DATA_V1_FULL_SUBMISSION_ZH_EN.md)：全部 30 个实体、151 个属性、每项原值与四个备选，中英对照及修订说明。英文是阅读辅助，中文是实验数据。/ All 30 entities and 151 attributes, with original values, four alternatives and revision rationales in Chinese and English. English is a reading gloss; Chinese is the experimental data.
3. [修订阶段指令与结果 / Revision instructions and results](pilot/data_review/value_revision/PROMPTS_REVISION_SUBMISSION.md)：修订规则、相容性检查及修改。/ Revision rules, compatibility screening and changes.
4. [WFW 与中文测试 prompt 对照 / WFW–Chinese prompt comparison](PROMPT_COMPARISON.md)：系统指令与测试形式。/ System instructions and test format.
5. [无信源输入与输出示例 / Example input and output](BASELINE_EXAMPLE.md)：一道真实题的两个表序、英文释义及三个模型输出。/ One actual pair in both table orders, an English reading translation and the three models' outputs.
6. [baseline 结果与全部文件 / Baseline results and complete files](#无信源-baseline--source-free-baseline)：逐模型输入、原始输出、分析和汇总。/ Complete model inputs, raw outputs, analysis and summaries.

## 数据与方法 / Data and method

- [Original 数据 / Original data](pilot/data/entities_zh.jsonl)；[v1 数据 / Revised v1 data](pilot/data_review/value_revision/full_v1/entities_full_v1.jsonl)。每组五值中，第一个是原值，其余四个是备选。/ Each five-value list contains an original value and four alternatives.
- 修订后每道题仅改变一个属性，其他属性保持原值；每个原值与四个备选配对，每对交换表序，共 604 对、1208 题。/ Each test item changes one attribute while retaining the others' original values; each original–alternative pair is shown in both orders, for 604 pairs and 1,208 items.
- [修订生成脚本 / Revision generation script](pilot/data_review/value_revision/full_v1/build_full_v1.py)、[变更记录 / Change record](pilot/data_review/value_revision/full_v1/changes_from_draft.json)、[相容性筛查 / Compatibility screen](pilot/data_review/value_revision/full_v1/compat_check_v1.json)。身高和体重备选在 v1 中分别生成，之后按实际题目搭配筛查。/ Height and weight alternatives in v1 were generated separately and screened afterwards against the fixed original context used in each item.
- 基础生成规则见[脚本](pilot/data_review/value_revision/draftA_20261104_149/build_full_v1.py)；最终修订脚本读取的[中间输入](pilot/data_review/value_revision/draftB_20261105_150/entities_full_v2.jsonl)也保留，供复核生成过程。/ The [base-generation script](pilot/data_review/value_revision/draftA_20261104_149/build_full_v1.py) and the [intermediate input](pilot/data_review/value_revision/draftB_20261105_150/entities_full_v2.jsonl) consumed by the final revision script are retained for verification.

## 无信源 baseline / Source-free baseline

三次运行使用同一版 v1 数据、1208 题。表中的“强同值”指两种表序下对同一个值的概率均大于 0.8；这是本项目的诊断阈值。/ All three runs use the same v1 data and 1,208 items. A strong same-value pair has probability greater than 0.8 for the same value in both table orders; this is a project diagnostic threshold.

| 模型 / Model | P(备选) / P(alternative) | P(表二) / P(Table 2) | 强同值 / Strong same-value |
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

原始输出中的 `prob_a` / `prob_b` 是首个 token 的 A/B 分数只在两个答案 token 之间归一化后的概率，并非模型生成的完整解释。`revision_requested` 是请求的模型版本；结果中的 `revision_loaded=null`，不将其写成已独立核实的实际加载版本。总体备选概率接近 50% 不能单独证明两个值等可信；三个模型均有位置偏差。/ `prob_a` and `prob_b` are probabilities normalised only over the two answer-token scores at the first generation step, not full generated explanations. `revision_requested` records the requested model revision; `revision_loaded=null`, so the loaded revision is not independently confirmed by the result file. Mean P(alternative) near 50% alone does not establish equal plausibility; all three models show position bias.

推理与分析实现：[`prompt_zh.py`](pilot/prompt_zh.py)、[`run_baseline.py`](pilot/run_baseline.py)、[`run_baseline_compat.py`](pilot/run_baseline_compat.py)、[`model_compat.py`](pilot/model_compat.py)、[`run_pilot.py`](pilot/run_pilot.py)、[`analyze_baseline.py`](pilot/analyze_baseline.py)。[SHA256 清单](SHA256.json)记录本目录材料哈希。结果文件保留运行时记录的原路径，作为历史元数据，不保证在本目录中可直接复用。

Inference and analysis implementation: [`prompt_zh.py`](pilot/prompt_zh.py), [`run_baseline.py`](pilot/run_baseline.py), [`run_baseline_compat.py`](pilot/run_baseline_compat.py), [`model_compat.py`](pilot/model_compat.py), [`run_pilot.py`](pilot/run_pilot.py), [`analyze_baseline.py`](pilot/analyze_baseline.py). The [SHA256 manifest](SHA256.json) records file hashes. Paths in the result files are preserved as run metadata and are not guaranteed to run directly from this directory.

Qwen2.5-14B 的全量结果尚待取得及核验，因此未列入本目录。/ The full Qwen2.5-14B result is not included because it has not yet been retrieved and verified.
