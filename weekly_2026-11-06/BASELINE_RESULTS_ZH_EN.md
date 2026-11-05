# 无信源 baseline：三模型结果说明 / Source-free baseline: results for three models

本页保留原中文结果，并补充英文说明。三个模型都使用相同的 v1 数据，604 对、两种表序共 1208 题。P(A)、P(B) 是仅在两个答案 token 上归一化的首 token 概率。表序 0 是原值在表一，表序 1 是原值在表二。

This page retains the original Chinese summaries and adds English explanations. All three models use the same v1 data: 604 pairs and 1,208 items in both table orders. P(A) and P(B) are first-token probabilities normalised over the two answer tokens. In order 0 the original is in Table 1; in order 1 it is in Table 2.

## Qwen2.5-7B-Instruct

### 中文原记录

数据 `pilot/data_review/value_revision/full_v1/entities_full_v1.jsonl`（SHA256 2888f2ade9e864dc…），备选 [1, 2, 3, 4]，604 对 × 2 种表序 = 1208 题。

- 位置偏差：P(选表二) = 63.2%（95%区间 [60.0, 66.4]；表序0 63.1%，表序1 63.2%）。WFW口径：选项B硬胜率 63.0%，平局 0.2%。
- 备选胜率（概率平均）：合并 49.9%（95%区间 [48.0, 51.8]；表序0 63.1%，表序1 36.8%）；硬计数合并 49.6%（每题P(选备选)>0.5计一胜，仅参照；WFW附录C未写明用哪种算法）。
- 每题模式：两种表序都选原值 81（13.4%）；两种表序都选备选 78（12.9%）；两种表序都选表一 142（23.5%）；两种表序都选表二 300（49.7%）；至少一种表序平局 3（0.5%）。
- 值方向：备选更大/更晚 200题，P(选备选) 54.4%；备选更小/更早 196题，P(选备选) 47.4%；不可比（类别、保修） 208题。
- 两种表序都强烈偏向同一值（>0.8）：126 题，清单见 analysis.json。

备选胜率约50%本身不能证明两个值同样可信：纯位置策略也会得到约50%。看每题模式和逐题清单。

### English translation

- Position: mean P(Table 2) = 63.2% (95% interval: 60.0–66.4%; order 0: 63.1%, order 1: 63.2%). Hard choice of option B: 63.0%; ties: 0.2%.
- Alternative: mean P(alternative) = 49.9% (95% interval: 48.0–51.8%; order 0: 63.1%, order 1: 36.8%). The pooled hard win rate is 49.6%: a win is counted when P(alternative) > 0.5; it is reported as a reference because WFW Appendix C does not specify this calculation.
- Pair patterns: original in both orders 81 (13.4%); alternative in both 78 (12.9%); Table 1 in both 142 (23.5%); Table 2 in both 300 (49.7%); at least one tie 3 (0.5%).
- Direction: 200 pairs have a larger/later alternative, with mean P(alternative) 54.4%; 196 have a smaller/earlier alternative, with 47.4%; 208 categorical or warranty pairs are not comparable in this way.
- Strong same-value preference in both orders (>0.8): 126 pairs; see the model's analysis.json for the list.

## Llama-3.1-8B-Instruct

### 中文原记录

数据 `pilot/data_review/value_revision/full_v1/entities_full_v1.jsonl`（SHA256 2888f2ade9e864dc…），备选 [1, 2, 3, 4]，604 对 × 2 种表序 = 1208 题。

- 位置偏差：P(选表二) = 71.9%（95%区间 [69.7, 74.1]；表序0 72.5%，表序1 71.3%）。WFW口径：选项B硬胜率 74.5%，平局 0.1%。
- 备选胜率（概率平均）：合并 50.6%（95%区间 [48.8, 52.4]；表序0 72.5%，表序1 28.7%）；硬计数合并 51.7%（每题P(选备选)>0.5计一胜，仅参照；WFW附录C未写明用哪种算法）。
- 每题模式：两种表序都选原值 91（15.1%）；两种表序都选备选 111（18.4%）；两种表序都选表一 52（8.6%）；两种表序都选表二 349（57.8%）；至少一种表序平局 1（0.2%）。
- 值方向：备选更大/更晚 200题，P(选备选) 48.8%；备选更小/更早 196题，P(选备选) 50.9%；不可比（类别、保修） 208题。
- 两种表序都强烈偏向同一值（>0.8）：96 题，清单见 analysis.json。

备选胜率约50%本身不能证明两个值同样可信：纯位置策略也会得到约50%。看每题模式和逐题清单。

### English translation

- Position: mean P(Table 2) = 71.9% (95% interval: 69.7–74.1%; order 0: 72.5%, order 1: 71.3%). Hard choice of option B: 74.5%; ties: 0.1%.
- Alternative: mean P(alternative) = 50.6% (95% interval: 48.8–52.4%; order 0: 72.5%, order 1: 28.7%). The pooled hard win rate is 51.7%, a reference count of cases where P(alternative) > 0.5.
- Pair patterns: original in both orders 91 (15.1%); alternative in both 111 (18.4%); Table 1 in both 52 (8.6%); Table 2 in both 349 (57.8%); at least one tie 1 (0.2%).
- Direction: 200 pairs have a larger/later alternative, with mean P(alternative) 48.8%; 196 have a smaller/earlier alternative, with 50.9%; 208 categorical or warranty pairs are not comparable in this way.
- Strong same-value preference in both orders (>0.8): 96 pairs; see the model's analysis.json for the list.

## gemma-4-E4B-it

### 中文原记录

数据 `pilot/data_review/value_revision/full_v1/entities_full_v1.jsonl`（SHA256 2888f2ade9e864dc…），备选 [1, 2, 3, 4]，604 对 × 2 种表序 = 1208 题。

- 位置偏差：P(选表二) = 58.8%（95%区间 [57.0, 60.7]；表序0 60.5%，表序1 57.1%）。WFW口径：选项B硬胜率 57.8%，平局 0.3%。
- 备选胜率（概率平均）：合并 51.7%（95%区间 [48.9, 54.5]；表序0 60.5%，表序1 42.9%）；硬计数合并 51.8%（每题P(选备选)>0.5计一胜，仅参照；WFW附录C未写明用哪种算法）。
- 每题模式：两种表序都选原值 177（29.3%）；两种表序都选备选 201（33.3%）；两种表序都选表一 63（10.4%）；两种表序都选表二 159（26.3%）；至少一种表序平局 4（0.7%）。
- 值方向：备选更大/更晚 200题，P(选备选) 79.0%；备选更小/更早 196题，P(选备选) 21.9%；不可比（类别、保修） 208题。
- 两种表序都强烈偏向同一值（>0.8）：284 题，清单见 analysis.json。

备选胜率约50%本身不能证明两个值同样可信：纯位置策略也会得到约50%。看每题模式和逐题清单。

### English translation

- Position: mean P(Table 2) = 58.8% (95% interval: 57.0–60.7%; order 0: 60.5%, order 1: 57.1%). Hard choice of option B: 57.8%; ties: 0.3%.
- Alternative: mean P(alternative) = 51.7% (95% interval: 48.9–54.5%; order 0: 60.5%, order 1: 42.9%). The pooled hard win rate is 51.8%, a reference count of cases where P(alternative) > 0.5.
- Pair patterns: original in both orders 177 (29.3%); alternative in both 201 (33.3%); Table 1 in both 63 (10.4%); Table 2 in both 159 (26.3%); at least one tie 4 (0.7%).
- Direction: 200 pairs have a larger/later alternative, with mean P(alternative) 79.0%; 196 have a smaller/earlier alternative, with 21.9%; 208 categorical or warranty pairs are not comparable in this way.
- Strong same-value preference in both orders (>0.8): 284 pairs; see the model's analysis.json for the list.

平均备选胜率接近 50% 不能单独证明等可信：纯位置策略也可能得到约 50%。需结合分表序及逐对结果解释。

A mean alternative win rate close to 50% does not by itself establish equal plausibility: a pure position strategy can also produce approximately 50%. Interpret it alongside the results by table order and by pair.
