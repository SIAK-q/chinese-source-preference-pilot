# 无信源 baseline 结果 / Source-free baseline results

五个模型使用同一份 v1 数据。每组原值和备选交换表序，各测一次；两张表均不标注信源。

Five models were tested on the same v1 data. Each original–alternative pair was tested in both table orders, without source labels.

| 模型 / Model | 运行 / Run | P(备选) / Mean P(alternative) | P(表二) / Mean P(Table 2) | 两种表序均偏向同一值（>80%） / Same value preferred in both orders (>80%) | 首 token 不是 A 或 B / First token not A or B |
|---|---|---:|---:|---:|---:|
| Qwen2.5-7B-Instruct | bwUniCluster, BF16 | 50.2% | 66.2% | 118 / 604 | 34 / 1,208 |
| Qwen2.5-14B-Instruct | bwUniCluster, BF16 | 47.6% | 59.0% | 244 / 604 | 0 / 1,208 |
| Llama-3.1-8B-Instruct | Kaggle, FP16 | 50.7% | 72.1% | 104 / 604 | 0 / 1,208 |
| Gemma-4-E4B-it | Kaggle, FP16 | 51.3% | 61.5% | 254 / 604 | 418 / 1,208 |
| Gemma-4-12B-it | Kaggle, FP16 | 53.7% | 45.5% | 132 / 604 | 355 / 1,208 |

- 五个模型中有四个平均偏向表二（59.0%–72.1%），Gemma-4-12B 略偏向表一（表二为 45.5%）。备选的平均概率接近 50%，不能单独证明每对值同样可信。

  Four of the five models favour Table 2 on average (59.0%–72.1%), while Gemma-4-12B slightly favours Table 1 (45.5% for Table 2). A mean alternative probability near 50% does not by itself establish equal plausibility for each pair.
- “两种表序均偏向同一值”统计：交换表序前后，模型给同一个值的概率两次都超过 80% 的值对。

  This column counts pairs where the same value receives a probability above 80% in both table orders.

## 首 token / First token

- Gemma-4-E4B：1208 题中有 418 题以 “(” 开头。这 418 题中有 82 题，“(” 后写的字母与第一步概率较高的选项不同（[核对结果](pilot/results_baseline/gemma-4-E4B-it_full_v1/second_token_check.json)）。
  Gemma-4-E4B began with "(" in 418 of 1,208 items. In 82 of these 418, the letter written after "(" differed from the option with the higher first-step probability ([check](pilot/results_baseline/gemma-4-E4B-it_full_v1/second_token_check.json)).
- Gemma-4-12B：1208 题中有 355 题的首 token 不是 A 或 B：“无法”170、“(”127、“thought”40、“由于”10、“<|channel>”4、“1”4。
  Gemma-4-12B gave a first token other than A or B in 355 of 1,208 items: "无法" ("unable") 170, "(" 127, "thought" 40, "由于" ("because") 10, "<|channel>" 4 and "1" 4.
- 两个 Gemma 4 模型的结果照常报告，测量方式待确认。Qwen2.5-7B 有 34/1208 题的首 token 是整体的 “(A” 或 “(B”。
  Results for both Gemma 4 models are reported with the measurement still to be confirmed. Qwen2.5-7B produced "(A" or "(B" as a single first token in 34 of 1,208 items.

## 三个模型共同偏向同一值的 23 对 / The 23 pairs where three models favour the same value

Qwen2.5-7B、Llama-3.1-8B 和 Gemma-4-E4B 都满足上述条件的 23 对如下，按属性排列：学历偏向较高学历，人数偏向较大备选，婚姻状况偏向“已婚”。这 23 对中，有 17 对在 Qwen2.5-14B 和 Gemma-4-12B 上也有同样的强偏好。加粗表示共同偏向的值；概率为备选在两种表序下的平均概率，四舍五入至整数。

The 23 pairs meeting this condition for Qwen2.5-7B, Llama-3.1-8B and Gemma-4-E4B are grouped by attribute: higher education, larger counts and “Married” are favoured. Of these 23, 17 show the same strong preference in both Qwen2.5-14B and Gemma-4-12B. Bold marks the value favoured by all three models; probabilities are the alternative’s mean across the two table orders, rounded to whole percentages.

| 实体 / Entity | 属性 / Attribute | 原值 / Original | 备选 / Alternative | P(备选) Qwen / Llama / Gemma |
|---|---|---|---|---:|
| PERSON-1 | 学历 / Education | 本科（汉语言文学） / Bachelor's, Chinese Language and Literature | **硕士研究生（学科教学·语文） / Master's, Subject Teaching: Chinese** | 100% / 97% / 100% |
| PERSON-1 |  | 本科（汉语言文学） / Bachelor's, Chinese Language and Literature | **硕士研究生（课程与教学论） / Master's, Curriculum and Instruction** | 100% / 99% / 100% |
| PERSON-3 |  | 本科（护理学） / Bachelor's, Nursing | **硕士研究生（护理学） / Master's, Nursing** | 100% / 100% / 100% |
| PERSON-4 |  | 大专（作物生产技术） / College diploma (dazhuan), Crop Production Technology | **硕士研究生（作物栽培学） / Master's, Crop Cultivation** | 100% / 99% / 100% |
| PERSON-5 |  | 本科（会计学） / Bachelor's, Accounting | **硕士研究生（会计硕士MPAcc） / Master's, Professional Accounting (MPAcc)** | 100% / 100% / 100% |
| PERSON-6 |  | **硕士研究生（桥梁与隧道工程） / Master's, Bridge and Tunnel Engineering** | 本科（土木工程） / Bachelor's, Civil Engineering | 0% / 1% / 0% |
| PERSON-6 |  | 硕士研究生（桥梁与隧道工程） / Master's, Bridge and Tunnel Engineering | **博士研究生（结构工程） / Doctorate, Structural Engineering** | 100% / 100% / 100% |
| PERSON-6 |  | **硕士研究生（桥梁与隧道工程） / Master's, Bridge and Tunnel Engineering** | 本科（道路桥梁与渡河工程） / Bachelor's, Road, Bridge and River-crossing Engineering | 0% / 1% / 0% |
| PERSON-6 |  | **硕士研究生（桥梁与隧道工程） / Master's, Bridge and Tunnel Engineering** | 大专（建筑工程技术） / College diploma (dazhuan), Building Construction Technology | 0% / 0% / 0% |
| PERSON-8 |  | 本科（市场营销） / Bachelor's, Marketing | **硕士研究生（工商管理MBA） / Master's, Business Administration (MBA)** | 100% / 100% / 100% |
| ORGANIZATION-1 | 员工人数 / Number of employees | 1,200 | **1,230** | 100% / 95% / 99% |
| ORGANIZATION-3 |  | 3,400 | **3,490** | 100% / 88% / 100% |
| ORGANIZATION-3 |  | 3,400 | **3,570** | 100% / 92% / 99% |
| ORGANIZATION-6 |  | 950 | **970** | 98% / 91% / 98% |
| ORGANIZATION-6 |  | 950 | **990** | 100% / 91% / 97% |
| BUILDING-1 | 容纳人数 / Capacity | 6,000 | **6,300** | 99% / 98% / 97% |
| BUILDING-3 |  | 12,000 | **12,300** | 100% / 97% / 96% |
| BUILDING-3 |  | 12,000 | **12,600** | 99% / 98% / 98% |
| PERSON-2 | 婚姻状况 / Marital status | **已婚 / Married** | 未婚 / Never married | 0% / 0% / 2% |
| PERSON-3 |  | 未婚 / Never married | **已婚 / Married** | 92% / 100% / 96% |
| PERSON-4 |  | **已婚 / Married** | 未婚 / Never married | 0% / 0% / 4% |
| PERSON-6 |  | **已婚 / Married** | 未婚 / Never married | 0% / 0% / 3% |
| PERSON-8 |  | 未婚 / Never married | **已婚 / Married** | 93% / 100% / 98% |

## 详细结果 / Detailed results

每个模型的完整输入、逐题概率和详细统计如下。

Full inputs, item-level probabilities and detailed statistics are linked below for each model. Inputs and item-level results are matched by item number i.

- Qwen2.5-7B：[输入 / Inputs](https://github.com/SIAK-q/chinese-source-preference-pilot/blob/main/weekly_2026-11-06/pilot/results_baseline/Qwen2.5-7B-Instruct_full_v1/prompts.jsonl) · [逐题结果 / Item-level results](https://github.com/SIAK-q/chinese-source-preference-pilot/blob/main/weekly_2026-11-06/pilot/results_baseline/Qwen2.5-7B-Instruct_full_v1/raw.json) · [详细统计 / Detailed statistics](https://github.com/SIAK-q/chinese-source-preference-pilot/blob/main/weekly_2026-11-06/pilot/results_baseline/Qwen2.5-7B-Instruct_full_v1/analysis.json)
- Qwen2.5-14B：[输入 / Inputs](https://github.com/SIAK-q/chinese-source-preference-pilot/blob/main/weekly_2026-11-06/pilot/results_baseline/Qwen2.5-14B-Instruct_full_v1/prompts.jsonl) · [逐题结果 / Item-level results](https://github.com/SIAK-q/chinese-source-preference-pilot/blob/main/weekly_2026-11-06/pilot/results_baseline/Qwen2.5-14B-Instruct_full_v1/raw.json) · [详细统计 / Detailed statistics](https://github.com/SIAK-q/chinese-source-preference-pilot/blob/main/weekly_2026-11-06/pilot/results_baseline/Qwen2.5-14B-Instruct_full_v1/analysis.json)
- Llama-3.1-8B：[输入 / Inputs](https://github.com/SIAK-q/chinese-source-preference-pilot/blob/main/weekly_2026-11-06/pilot/results_baseline/Llama-3.1-8B-Instruct_full_v1/prompts.jsonl) · [逐题结果 / Item-level results](https://github.com/SIAK-q/chinese-source-preference-pilot/blob/main/weekly_2026-11-06/pilot/results_baseline/Llama-3.1-8B-Instruct_full_v1/raw.json) · [详细统计 / Detailed statistics](https://github.com/SIAK-q/chinese-source-preference-pilot/blob/main/weekly_2026-11-06/pilot/results_baseline/Llama-3.1-8B-Instruct_full_v1/analysis.json)
- Gemma-4-E4B：[输入 / Inputs](https://github.com/SIAK-q/chinese-source-preference-pilot/blob/main/weekly_2026-11-06/pilot/results_baseline/gemma-4-E4B-it_full_v1/prompts.jsonl) · [逐题结果 / Item-level results](https://github.com/SIAK-q/chinese-source-preference-pilot/blob/main/weekly_2026-11-06/pilot/results_baseline/gemma-4-E4B-it_full_v1/raw.json) · [详细统计 / Detailed statistics](https://github.com/SIAK-q/chinese-source-preference-pilot/blob/main/weekly_2026-11-06/pilot/results_baseline/gemma-4-E4B-it_full_v1/analysis.json)
- Gemma-4-12B：[输入 / Inputs](https://github.com/SIAK-q/chinese-source-preference-pilot/blob/main/weekly_2026-11-06/pilot/results_baseline/gemma-4-12B-it_full_v1/prompts.jsonl) · [逐题结果 / Item-level results](https://github.com/SIAK-q/chinese-source-preference-pilot/blob/main/weekly_2026-11-06/pilot/results_baseline/gemma-4-12B-it_full_v1/raw.json) · [详细统计 / Detailed statistics](https://github.com/SIAK-q/chinese-source-preference-pilot/blob/main/weekly_2026-11-06/pilot/results_baseline/gemma-4-12B-it_full_v1/analysis.json)
