# 无信源baseline / Source-free baseline

- 70个实体，1520个冲突对，每个模型3040题（两种表序）；五个模型已完成，Qwen2.5-72B在跑。 / 70 entities, 1,520 conflict pairs, 3,040 questions per model (both table orders); five models complete, Qwen2.5-72B running.


## ① 位置偏好 / Table-position preferences

<details>
<summary>五模型位置偏好 / Table-position preferences of all five models</summary>

| 模型 / Model | 平均选表二概率<br>Mean P(Table 2) |
|---|---|
| GLM-4-9B-0414 | 16.1% |
| Llama-3.1-8B-Instruct | 61.1% |
| Qwen2.5-7B-Instruct | 64.4% |
| Qwen2.5-14B-Instruct | 61.1% |
| Qwen2.5-32B-Instruct | 48.3% |

</details>

## ② 取值偏好 / Value preferences

- 五模型共同强偏19对，主要是较长保修期和较高学历。 / All five share 19 strong-preference pairs, mainly longer warranties and higher education.

<details>
<summary>五模型取值偏好：每模型1520对 / Value preferences: 1,520 pairs per model</summary>

- **强偏好 / Strong preference:** 两种表序下，同一个值的概率都超过80%。 / The same value receives over 80% probability in both table orders.
- **Qwen规模 / Qwen sizes:** 强偏好对数：7B 315 → 14B 533 → 32B 712。 / Strong-preference pairs: 7B 315 → 14B 533 → 32B 712.
- 共同19对：保修期10、学历6、容纳人数2、身高1。 / Shared 19 pairs: warranty 10, education 6, capacity 2, height 1.

| 模型 / Model | 运行 / Run | 平均选备选概率<br>Mean P(alternative) | 强偏原值<br>Strong original | 强偏备选<br>Strong alternative | 合计<br>Total |
|---|---|---|---|---|---|
| GLM-4-9B-0414 | Kaggle, FP16 | 50.0% | 74 | 83 | 157 |
| Llama-3.1-8B-Instruct | Kaggle, FP16 | 50.2% | 123 | 127 | 250 |
| Qwen2.5-7B-Instruct | Kaggle, FP16 | 49.6% | 167 | 148 | 315 |
| Qwen2.5-14B-Instruct | AutoDL, BF16 | 50.2% | 257 | 276 | 533 |
| Qwen2.5-32B-Instruct | AutoDL, BF16 | 50.4% | 339 | 373 | 712 |

</details>



## 补充检查 / Additional checks

<details>
<summary>冲突行在第几行 / Position of the conflicting row</summary>

- 全部7类实体（人物、地点、机构、活动、产品、建筑、艺术作品）均按冲突行的相对位置分为上、中、下三组，不计名称行。 / All seven entity types (people, locations, organisations, events, products, buildings and artworks) are grouped by the conflicting row’s relative position: top, middle or bottom, excluding the name row.
- 各组平均选备选概率为48.4–52.3%。这是不同题目分组的比较。 / Mean P(alternative) is 48.4–52.3% across the groups. The groups contain different items.

| 模型 / Model | 上段 / Top | 中段 / Middle | 下段 / Bottom |
|---|---|---|---|
| GLM-4-9B-0414 | 49.6% | 50.3% | 50.1% |
| Llama-3.1-8B-Instruct | 50.4% | 50.8% | 49.6% |
| Qwen2.5-7B-Instruct | 49.5% | 49.6% | 49.8% |
| Qwen2.5-14B-Instruct | 52.3% | 48.4% | 49.8% |
| Qwen2.5-32B-Instruct | 50.7% | 50.7% | 49.8% |

</details>

<details>
<summary>表有多长 / Table length</summary>

- **行数 / Rows:** 不含名称行：地点4；机构、活动、产品5；建筑、艺术6；人物9。 / Excluding the name: locations 4; organisations, events and products 5; buildings and art 6; people 9.
- **发现 / Observation:** 地点题上，Llama和Qwen7B更偏表二，平均概率如下。 / Llama and Qwen7B favour Table 2 more on location items, with the mean probabilities below.

| 模型 / Model | 地点题<br>Location items | 其他题组<br>Other item groups |
|---|---|---|
| Llama-3.1-8B | 92.5% | 47.5%–72.9% |
| Qwen2.5-7B | 90.5% | 54.5%–69.9% |


</details>

