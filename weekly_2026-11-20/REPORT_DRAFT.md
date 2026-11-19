# Weekly progress report（草稿，2026-11-20；中英对照，发老师时只取英文）

## Goal of this stage｜本阶段目标

Source preference is measured against a source-free baseline. This stage therefore builds the expanded dataset, fixes the models and runs the full baseline, so that the source experiments can start from a stable reference.

信源偏好要和无信源baseline比较。所以这一阶段完成三件事：扩充数据、确定模型、跑完整baseline，为信源实验提供稳定的参照。

## 1. Data｜数据

- **Size:** 70 entities (10 per type) and 380 attributes. Each original value has four alternatives, giving 1,520 conflict pairs and 3,040 prompts per model in both table orders.
  - **规模：** 70个实体（每类10个），380个属性。每个原值配4个备选，共1520个冲突对；两种表序下每个模型3040题。
- **Alternatives:** All 250 numeric, date and duration attributes (including warranty months) have two alternatives above and two below the original, e.g. height 174 cm → 166, 170, 178, 182 cm.
  - **备选：** 250个数值、日期和时长属性（含保修月数）都是两个备选高于原值、两个低于原值，如身高174厘米→166、170、178、182厘米。
- **Row order:** Rows are shuffled across entities, so the conflict row appears in different positions; both tables in a question keep the same order.
  - **行序：** 不同实体间打乱行序，冲突行出现在不同位置；同一道题的两张表行序相同。
- **Records:** Prompts, raw outputs and revisions are saved for each generation step.
  - **记录：** 每一步生成都保留prompt、原始输出和修改记录。

| Type<br>类型 | Attributes<br>属性 |
|---|---|
| Person<br>人物 | occupation, education, date of birth, place of birth, current city, height, weight, marital status<br>职业、学历、出生日期、出生地、现居城市、身高、体重、婚姻状况 |
| Organisation<br>机构 | founding date, headquarters, industry, employees, annual revenue<br>成立时间、总部所在地、所属行业、员工人数、年营业额 |
| Location<br>地点 | population, area, elevation, number of townships<br>人口、面积、海拔、下辖乡镇数 |
| Building<br>建筑 | completion year, height, floors, capacity, main material, architect<br>建成年份、高度、层数、容纳人数、主要材料、设计师 |
| Event<br>活动 | date, duration, participants, budget, organiser<br>举办日期、持续时间、参与人数、预算、主办方 |
| Product<br>产品 | release date, price, weight, warranty, manufacturer<br>发布日期、价格、重量、保修期、制造商 |
| Art<br>艺术作品 | creation year, creator, height, width, material<br>创作年份、创作者、高度、宽度、材料 |

## 2. Models｜模型

Six models: Qwen2.5-Instruct 7B, 14B, 32B and 72B (one family across sizes); Llama-3.1-8B-Instruct (a second family); GLM-4-9B-0414 (a Chinese-developed model, replacing Gemma). Answers are read as A/B probabilities at the first generation step.

六个模型：Qwen2.5-Instruct 7B、14B、32B、72B（同一系列不同规模）；Llama-3.1-8B-Instruct（另一系列）；GLM-4-9B-0414（国产模型，替换Gemma）。答案取第一步生成时A和B的概率。

## 3. Baseline results｜baseline结果

Five of six models are complete; the Qwen2.5-72B baseline remains to be completed.

六个模型已完成五个；Qwen2.5-72B baseline尚未完成。

| Model<br>模型 | Run<br>运行 | Mean P(alternative)<br>平均选备选概率 | Mean P(Table 2)<br>平均选表二概率 | Strong same-value pairs<br>强烈偏向同一值 |
| --- | --- | ---: | ---: | ---: |
| GLM-4-9B-0414 | Kaggle, FP16 | 50.0% | 16.1% | 157 / 1,520 |
| Llama-3.1-8B-Instruct | Kaggle, FP16 | 50.2% | 61.1% | 250 / 1,520 |
| Qwen2.5-7B-Instruct | Kaggle, FP16 | 49.6% | 64.4% | 315 / 1,520 |
| Qwen2.5-14B-Instruct | AutoDL, BF16 | 50.2% | 61.1% | 533 / 1,520 |
| Qwen2.5-32B-Instruct | AutoDL, BF16 | 50.4% | 48.3% | 712 / 1,520 |

Strong preference: even if the two tables switch places, the model still gives the same value with more than 80% probability.

强烈偏向：两张表对调后，模型仍以80%以上的概率选同一个值。

- **The overall mean is close to 50%.** Mean P(alternative) is 49.6–50.4% for all five models.
  - **整体均值接近50%。** 五个模型平均选备选概率均为49.6–50.4%。
- **Within the tested Qwen models, more pairs retain a strong preference after switching table order.** Counts rise from 315 (7B) to 533 (14B) and 712 (32B). Qwen2.5-32B has a mean P(Table 2) of 48.3%; GLM chooses Table 1 in both orders for 77% of pairs.
  - **已测Qwen模型中，表序对调后仍强烈偏向同一值的题增多。** 7B为315对、14B为533对、32B为712对。Qwen2.5-32B平均选表二概率为48.3%；GLM在77%的题中两种表序都选表一。
- **Value preferences fall on both sides.** Among strongly preferred pairs, original/alternative: GLM 74/83, Llama 123/127, Qwen2.5-7B 167/148, 14B 257/276, 32B 339/373. Qwen2.5-32B prefers larger or later values (P(alternative) 72.8% vs 31.0%, across 500 larger/later and 500 smaller/earlier pairs); the strongly preferred values occur among both originals and alternatives.
  - **值偏好落在两边。** 强烈偏好题中偏原值／偏备选：GLM 74／83、Llama 123／127、Qwen2.5-7B 167／148、14B 257／276、32B 339／373。Qwen2.5-32B偏好更大或更晚的值（500对较大／较晚备选为72.8%，500对较小／较早备选为31.0%）；强烈偏好的值分散在原值和备选两边。
- **Shared value preferences.** All five models strongly favour the same value in 19 pairs: longer warranty (10), higher education (6), larger capacity (2) and height (1).
  - **共同值偏好。** 五个模型在19对上都强烈偏向同一个值：保修期更长10对、学历更高6对、容纳人数更多2对、身高1对。

## 4. Analysis plan｜分析方案

- For each conflict pair and table order, source preference is the change in the probability of choosing the same value, relative to its source-free baseline. These changes are then grouped by source category.
  - 逐冲突对、逐表序比较：加信源后，选择同一个值的概率相对无信源baseline改变多少；再按信源类别汇总。
- Position bias differs strongly between models, so source effects must be compared within each model, with both table orders.
  - 各模型位置偏差差别很大，信源效应需在每个模型内部、结合两种表序比较。
- Before the source runs, the baseline results will be used to check whether conflict-row position and table length affect choices.
  - 跑信源前，先用baseline结果检查冲突行位置和表长是否影响选择。

## 5. Source setup｜信源设置

Four comparisons are prepared: government vs social media, government vs individual, newspaper vs social media, and the explicit label “No source available” vs government. Sources move together with their values when the table order switches.

已准备四组对比：政府对社媒、政府对个人、报纸对社媒、“无可用信源”标签对政府。表序互换时，信源与取值一起移动。

| Source<br>信源 | Rule<br>规则 |
|---|---|
| Government<br>政府 | Two to three suitable agencies per entity type, e.g. sports bureau or culture and tourism bureau for sports events<br>每类2–3个合适机构，如体育活动用体育局或文旅局 |
| Newspaper<br>报纸 | Daily, evening, times, morning, metropolitan, equal probability<br>日报、晚报、时报、晨报、都市报等概率 |
| Individual<br>个人 | Surname by frequency, two given-name characters by male or female character frequency; names with a Chinese Wikipedia page redrawn<br>姓按频率，名两字按男女用字频率；有中文维基页面的重抽 |
| Social media<br>社交媒体 | Half adjective + “的” + noun + four digits; half “用户” + ten digits<br>一半“形容词＋的＋名词＋4位数”，一半“用户＋10位数” |

Place names for government and newspaper sources come from a shared pool of 1,327 names, after removing 75 unnatural ones; 11 entity place names are excluded from source sampling, leaving 1,316 available.

政府和报纸信源的地名来自共用地名池，删去75个不自然的名称后剩1327个；实际抽信源时再排除11个实体地名，可用1316个。

## Next steps｜下一步

1. Complete the Qwen2.5-72B baseline.
   - 完成Qwen2.5-72B baseline。
2. Check conflict-row position, table length and attribute-level preferences.
   - 检查冲突行位置、表长和各属性偏好。
3. Run the source experiments after discussing the full baseline.
   - 讨论完整baseline后，跑信源实验。

## Questions for discussion｜讨论问题

1. Does the full baseline support starting the source experiments with the four planned comparisons?
   - 完整baseline是否支持按计划的四组对比开始信源实验？
2. How should source, position and value preferences be analysed together? Would a mixed-effects model be useful?
   - 如何同时分析信源、位置和取值偏好？是否适合使用混合效应模型？
