# 无信源 baseline 结果 / Source-free baseline results

五个模型使用同一份 v1 数据。每组原值和备选交换表序，各测一次；两张表均不标注信源。

Five models were tested on the same v1 data. Each original–alternative pair was tested in both table orders, without source labels.

| 模型 / Model | 运行 / Run | P(备选) / Mean P(alternative) | P(表二) / Mean P(Table 2) | 两种表序均偏向同一值（>80%） / Same value preferred in both orders (>80%) |
|---|---|---:|---:|---:|
| Qwen2.5-7B-Instruct | bwUniCluster, BF16 | 50.2% | 66.2% | 118 / 604 |
| Qwen2.5-14B-Instruct | bwUniCluster, BF16 | 47.6% | 59.0% | 244 / 604 |
| Llama-3.1-8B-Instruct | Kaggle, FP16 | 50.7% | 72.1% | 104 / 604 |
| Gemma-4-E4B-it | Kaggle, FP16 | 51.3% | 61.5% | 254 / 604 |
| Gemma-4-12B-it | Kaggle, FP16 | 53.7% | 45.5% | 132 / 604 |

- **P(备选) / P(alternative)**：选择备选值的平均概率，用于观察模型偏向原值还是备选。<br>The mean probability of choosing the alternative, indicating preference for the original versus the alternative.

- **P(表二) / P(Table 2)**：选择第二张表所含值的平均概率，用于观察位置偏好。<br>The mean probability of choosing the value in the second table, indicating position preference.

- **两种表序均偏向同一值（>80%） / Same value preferred in both orders (>80%)**：换位前后，同一个值的概率均超过80%的值对数量。<br>The number of pairs where the same value receives more than 80% probability in each table order.

五个模型中有四个平均偏向表二（59.0%–72.1%），Gemma-4-12B略偏向表一（表二为45.5%）。

Four of the five models favour Table 2 on average (59.0%–72.1%), while Gemma-4-12B slightly favours Table 1 (45.5% for Table 2).

## 首 token / First token

每个模型共1208题，实际生成的首token如下。

First tokens across 1,208 items per model:

| 模型 / Model | A或B / A or B | 其他 / Other |
|---|---:|---|
| Qwen2.5-7B | 1,174 | `(A` / `(B`: 34 |
| Qwen2.5-14B | 1,208 | 0 |
| Llama-3.1-8B | 1,208 | 0 |
| Gemma-4-E4B | 790 | `(`: 418 |
| Gemma-4-12B | 853 | 无法 (unable): 170; `(`: 127; `thought`: 40; 由于 (because): 10; `<\|channel>`: 4; `1`: 4 |

- **E4B核对：** 418道先输出“(”的题中，有82道出现这种情况：首步A/B分数更偏向一个选项，但接着写出的字母却是另一个。[核对记录](pilot/results_baseline/gemma-4-E4B-it_full_v1/second_token_check.json)
  **E4B check:** In 82 of the 418 items starting with “(”, the first-step A/B scores favoured one option, but the next letter indicated the other. [Check results](pilot/results_baseline/gemma-4-E4B-it_full_v1/second_token_check.json)

## 五个模型共同偏向同一值的 17 对 / The 17 pairs where all five models favour the same value

五模型在两种表序中都以超过80%的概率偏向同一个值的有17对：较高学历10对、较大人数4对、“已婚”3对。

Across all five models, 17 pairs show a preference above 80% for the same value in each table order: higher education (10), larger counts (4) and “Married” (3).

<details>
<summary>17对完整清单与读表示例 / All 17 pairs and a reading example</summary>

- 加粗为五模型共同偏好的值；概率为两种表序的平均P(备选)，取整。<br>Bold marks the value all five models favour; percentages are mean P(alternative) across both orders, rounded to whole percentages.

- 例如，PERSON-4的原值是“已婚”，备选是“未婚”。Gemma-12B两次选“未婚”的概率约为1%和10%，平均约5%，所以它偏向“已婚”。<br>For PERSON-4, the original is “Married” and the alternative is “Never married”. Gemma-12B assigns about 1% and 10% to “Never married” in the two orders, about 5% on average, so it favours “Married”.

| 实体 / Entity | 属性 / Attribute | 原值 / Original | 备选 / Alternative | Qwen-7B | Qwen-14B | Llama-8B | Gemma-E4B | Gemma-12B |
|---|---|---|---|---:|---:|---:|---:|---:|
| PERSON-1 | 学历 / Education | 本科（汉语言文学） / Bachelor's, Chinese Language and Literature | **硕士研究生（学科教学·语文） / Master's, Subject Teaching: Chinese** | 100% | 100% | 97% | 100% | 100% |
| PERSON-1 |  | 本科（汉语言文学） / Bachelor's, Chinese Language and Literature | **硕士研究生（课程与教学论） / Master's, Curriculum and Instruction** | 100% | 100% | 99% | 100% | 100% |
| PERSON-3 |  | 本科（护理学） / Bachelor's, Nursing | **硕士研究生（护理学） / Master's, Nursing** | 100% | 100% | 100% | 100% | 100% |
| PERSON-4 |  | 大专（作物生产技术） / College diploma (dazhuan), Crop Production Technology | **硕士研究生（作物栽培学） / Master's, Crop Cultivation** | 100% | 100% | 99% | 100% | 100% |
| PERSON-5 |  | 本科（会计学） / Bachelor's, Accounting | **硕士研究生（会计硕士MPAcc） / Master's, Professional Accounting (MPAcc)** | 100% | 100% | 100% | 100% | 100% |
| PERSON-6 |  | **硕士研究生（桥梁与隧道工程） / Master's, Bridge and Tunnel Engineering** | 本科（土木工程） / Bachelor's, Civil Engineering | 0% | 0% | 1% | 0% | 0% |
| PERSON-6 |  | 硕士研究生（桥梁与隧道工程） / Master's, Bridge and Tunnel Engineering | **博士研究生（结构工程） / Doctorate, Structural Engineering** | 100% | 100% | 100% | 100% | 100% |
| PERSON-6 |  | **硕士研究生（桥梁与隧道工程） / Master's, Bridge and Tunnel Engineering** | 本科（道路桥梁与渡河工程） / Bachelor's, Road, Bridge and River-crossing Engineering | 0% | 0% | 1% | 0% | 0% |
| PERSON-6 |  | **硕士研究生（桥梁与隧道工程） / Master's, Bridge and Tunnel Engineering** | 大专（建筑工程技术） / College diploma (dazhuan), Building Construction Technology | 0% | 0% | 0% | 0% | 0% |
| PERSON-8 |  | 本科（市场营销） / Bachelor's, Marketing | **硕士研究生（工商管理MBA） / Master's, Business Administration (MBA)** | 100% | 100% | 100% | 100% | 100% |
| ORGANIZATION-3 | 员工人数 / Number of employees | 3,400 | **3,490** | 100% | 100% | 88% | 100% | 100% |
| BUILDING-1 | 容纳人数 / Capacity | 6,000 | **6,300** | 99% | 100% | 98% | 97% | 90% |
| BUILDING-3 |  | 12,000 | **12,300** | 100% | 100% | 97% | 96% | 96% |
| BUILDING-3 |  | 12,000 | **12,600** | 99% | 100% | 98% | 98% | 91% |
| PERSON-3 | 婚姻状况 / Marital status | 未婚 / Never married | **已婚 / Married** | 92% | 100% | 100% | 96% | 91% |
| PERSON-4 |  | **已婚 / Married** | 未婚 / Never married | 0% | 0% | 0% | 4% | 5% |
| PERSON-8 |  | 未婚 / Never married | **已婚 / Married** | 93% | 100% | 100% | 99% | 96% |

</details>

全部输入、逐题结果与分析文件见[文件入口](README.md)。

See the [file index](README.md) for all inputs, item-level results and analysis files.
