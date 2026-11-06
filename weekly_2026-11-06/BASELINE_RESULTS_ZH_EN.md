# 无信源 baseline 结果 / Source-free baseline results

三个模型使用同一份 v1 数据。每组原值和备选交换表序，各测一次；两张表均不标注信源。

Three models were tested on the same v1 data. Each original–alternative pair was tested in both table orders, without source labels.

| 模型 / Model | 备选的平均概率 / Mean P(alternative) | 表二的平均概率 / Mean P(Table 2) | 两种表序均偏向同一值 / Same value preferred in both orders |
| --- | ---: | ---: | ---: |
| Qwen2.5-7B-Instruct | 49.9% | 63.2% | 126 / 604 |
| Llama-3.1-8B-Instruct | 50.6% | 71.9% | 96 / 604 |
| Gemma-4-E4B-it | 51.7% | 58.8% | 284 / 604 |

- 三个模型都偏向表二；备选的平均概率接近 50%，不能单独证明每对值同样可信。
  
  All three models favour Table 2. A mean alternative probability near 50% does not by itself establish equal plausibility for each pair.
- 最后一列统计：交换表序前后，模型给同一个值的概率两次都超过 80% 的值对。
  
  The last column counts pairs where the same value receives a probability above 80% in both table orders. 

## 三个模型共同偏向同一值的 22 对 / The 22 pairs where all three models favour the same value

三个模型都满足上述条件的 22 对如下，按属性排列：学历偏向较高学历，人数偏向较大备选，婚姻状况偏向“已婚”。加粗表示共同偏向的值；概率为备选在两种表序下的平均概率，四舍五入至整数。

The 22 pairs meeting this condition for all three models are grouped by attribute: higher education, larger counts and “Married” are favoured. Bold marks the value favoured by all three models; probabilities are the alternative’s mean across both table orders, rounded to whole percentages.

| 实体 / Entity | 属性 / Attribute | 原值 / Original | 备选 / Alternative | P(备选) Qwen / Llama / Gemma |
|---|---|---|---|---:|
| PERSON-1 | 学历 / Education | 本科（汉语言文学） / Bachelor's, Chinese Language and Literature | **硕士研究生（学科教学·语文） / Master's, Subject Teaching: Chinese** | 100% / 98% / 100% |
| PERSON-1 |  | 本科（汉语言文学） / Bachelor's, Chinese Language and Literature | **硕士研究生（课程与教学论） / Master's, Curriculum and Instruction** | 100% / 98% / 100% |
| PERSON-3 |  | 本科（护理学） / Bachelor's, Nursing | **硕士研究生（护理学） / Master's, Nursing** | 100% / 100% / 100% |
| PERSON-4 |  | 大专（作物生产技术） / College diploma (dazhuan), Crop Production Technology | **硕士研究生（作物栽培学） / Master's, Crop Cultivation** | 100% / 99% / 100% |
| PERSON-5 |  | 本科（会计学） / Bachelor's, Accounting | **硕士研究生（会计硕士MPAcc） / Master's, Professional Accounting (MPAcc)** | 100% / 100% / 100% |
| PERSON-6 |  | **硕士研究生（桥梁与隧道工程） / Master's, Bridge and Tunnel Engineering** | 本科（土木工程） / Bachelor's, Civil Engineering | 0% / 1% / 0% |
| PERSON-6 |  | 硕士研究生（桥梁与隧道工程） / Master's, Bridge and Tunnel Engineering | **博士研究生（结构工程） / Doctorate, Structural Engineering** | 100% / 100% / 100% |
| PERSON-6 |  | **硕士研究生（桥梁与隧道工程） / Master's, Bridge and Tunnel Engineering** | 本科（道路桥梁与渡河工程） / Bachelor's, Road, Bridge and River-crossing Engineering | 0% / 3% / 0% |
| PERSON-6 |  | **硕士研究生（桥梁与隧道工程） / Master's, Bridge and Tunnel Engineering** | 大专（建筑工程技术） / College diploma (dazhuan), Building Construction Technology | 0% / 0% / 0% |
| PERSON-8 |  | 本科（市场营销） / Bachelor's, Marketing | **硕士研究生（工商管理MBA） / Master's, Business Administration (MBA)** | 100% / 100% / 100% |
| ORGANIZATION-1 | 员工人数 / Number of employees | 1,200 | **1,230** | 100% / 93% / 99% |
| ORGANIZATION-6 |  | 950 | **970** | 100% / 91% / 99% |
| ORGANIZATION-6 |  | 950 | **990** | 100% / 89% / 99% |
| BUILDING-1 | 容纳人数 / Capacity | 6,000 | **6,150** | 98% / 98% / 99% |
| BUILDING-1 |  | 6,000 | **6,300** | 100% / 98% / 98% |
| BUILDING-3 |  | 12,000 | **12,300** | 100% / 98% / 98% |
| BUILDING-3 |  | 12,000 | **12,600** | 100% / 97% / 99% |
| PERSON-2 | 婚姻状况 / Marital status | **已婚 / Married** | 未婚 / Never married | 0% / 0% / 2% |
| PERSON-4 |  | **已婚 / Married** | 未婚 / Never married | 0% / 0% / 3% |
| PERSON-6 |  | **已婚 / Married** | 未婚 / Never married | 0% / 0% / 4% |
| PERSON-2 | 出生日期 / Date of birth | 1975-02-22 | **1974-09-23** | 98% / 99% / 90% |
| ORGANIZATION-6 | 所属行业 / Industry | **软件和信息技术服务 / Software and IT services** | 计算机整机制造 / Computer manufacturing (complete systems) | 0% / 11% / 9% |

## 详细结果 / Detailed results

每个模型的完整输入、逐题概率和详细统计如下。

Full inputs, item-level probabilities and detailed statistics are linked below for each model. Inputs and item-level results are matched by item number i.

- Qwen2.5-7B：[输入 / Inputs](https://github.com/SIAK-q/chinese-source-preference-pilot/blob/main/weekly_2026-11-06/pilot/results_baseline/Qwen2.5-7B-Instruct_full_v1/prompts.jsonl) · [逐题结果 / Item-level results](https://github.com/SIAK-q/chinese-source-preference-pilot/blob/main/weekly_2026-11-06/pilot/results_baseline/Qwen2.5-7B-Instruct_full_v1/raw.json) · [详细统计 / Detailed statistics](https://github.com/SIAK-q/chinese-source-preference-pilot/blob/main/weekly_2026-11-06/pilot/results_baseline/Qwen2.5-7B-Instruct_full_v1/analysis.json)
- Llama-3.1-8B：[输入 / Inputs](https://github.com/SIAK-q/chinese-source-preference-pilot/blob/main/weekly_2026-11-06/pilot/results_baseline/Llama-3.1-8B-Instruct_full_v1/prompts.jsonl) · [逐题结果 / Item-level results](https://github.com/SIAK-q/chinese-source-preference-pilot/blob/main/weekly_2026-11-06/pilot/results_baseline/Llama-3.1-8B-Instruct_full_v1/raw.json) · [详细统计 / Detailed statistics](https://github.com/SIAK-q/chinese-source-preference-pilot/blob/main/weekly_2026-11-06/pilot/results_baseline/Llama-3.1-8B-Instruct_full_v1/analysis.json)
- Gemma-4-E4B：[输入 / Inputs](https://github.com/SIAK-q/chinese-source-preference-pilot/blob/main/weekly_2026-11-06/pilot/results_baseline/gemma-4-E4B-it_full_v1/prompts.jsonl) · [逐题结果 / Item-level results](https://github.com/SIAK-q/chinese-source-preference-pilot/blob/main/weekly_2026-11-06/pilot/results_baseline/gemma-4-E4B-it_full_v1/raw.json) · [详细统计 / Detailed statistics](https://github.com/SIAK-q/chinese-source-preference-pilot/blob/main/weekly_2026-11-06/pilot/results_baseline/gemma-4-E4B-it_full_v1/analysis.json)
