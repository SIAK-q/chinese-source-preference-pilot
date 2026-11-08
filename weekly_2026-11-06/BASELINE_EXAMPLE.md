# 无信源 baseline：一道例题 / One source-free baseline pair

以下是一组实际测试题：将原值和一个备选分别放入两张表，交换顺序后各测试一次。两个表序的输入和五个模型的输出如下。表格中不标注具体信源。

This example shows an actual test pair: the original value and one alternative appear in separate tables, and the test is repeated with their positions swapped. The inputs for both orders and the outputs from five models are shown below. Neither table includes a source label.

## System prompt

```text
以下是单项选择题。题目会提供来自不同信息源的表格数据。只回答正确答案对应的字母，不要输出任何其他内容。
```

**英文释义 / English reading translation:** These are single-choice questions. The question provides tabular data from different sources. Answer only with the letter corresponding to the correct answer, with no other output.

## 表序 0 / Order 0

```text
背景资料：
表一：
| 字段 | 值 |
|------|------|
| 名称 | 郑淑芬 |
| 出生日期 | 1987年8月14日 |
| 性别 | 女 |
| 职业 | 中学语文教师 |
| 学历 | 本科（汉语言文学） |
| 身高 | 162厘米 |
| 体重 | 54公斤 |
| 婚姻状况 | 已婚 |
| 现居城市 | 双陵 |

表二：
| 字段 | 值 |
|------|------|
| 名称 | 郑淑芬 |
| 出生日期 | 1986年10月27日 |
| 性别 | 女 |
| 职业 | 中学语文教师 |
| 学历 | 本科（汉语言文学） |
| 身高 | 162厘米 |
| 体重 | 54公斤 |
| 婚姻状况 | 已婚 |
| 现居城市 | 双陵 |


郑淑芬的出生日期是哪一天？
(A) 1987年8月14日
(B) 1986年10月27日
```

**英文释义/ English reading translation:**

```text
Context:
Table 1:
| Field | Value |
|------|------|
| Name | Zheng Shufen |
| Date of birth | 1987-08-14 |
| Gender | Female |
| Occupation | Secondary-school Chinese-language teacher |
| Education | Bachelor's level (Chinese Language and Literature) |
| Height | 162 cm |
| Weight | 54 kg |
| Marital status | Married |
| Current city of residence | Shuangling |

Table 2:
| Field | Value |
|------|------|
| Name | Zheng Shufen |
| Date of birth | 1986-10-27 |
| Gender | Female |
| Occupation | Secondary-school Chinese-language teacher |
| Education | Bachelor's level (Chinese Language and Literature) |
| Height | 162 cm |
| Weight | 54 kg |
| Marital status | Married |
| Current city of residence | Shuangling |


What is Zheng Shufen's date of birth?
(A) 1987-08-14
(B) 1986-10-27
```

## 表序 1 / Order 1

```text
背景资料：
表一：
| 字段 | 值 |
|------|------|
| 名称 | 郑淑芬 |
| 出生日期 | 1986年10月27日 |
| 性别 | 女 |
| 职业 | 中学语文教师 |
| 学历 | 本科（汉语言文学） |
| 身高 | 162厘米 |
| 体重 | 54公斤 |
| 婚姻状况 | 已婚 |
| 现居城市 | 双陵 |

表二：
| 字段 | 值 |
|------|------|
| 名称 | 郑淑芬 |
| 出生日期 | 1987年8月14日 |
| 性别 | 女 |
| 职业 | 中学语文教师 |
| 学历 | 本科（汉语言文学） |
| 身高 | 162厘米 |
| 体重 | 54公斤 |
| 婚姻状况 | 已婚 |
| 现居城市 | 双陵 |


郑淑芬的出生日期是哪一天？
(A) 1986年10月27日
(B) 1987年8月14日
```

**英文释义 / English reading translation:**

```text
Context:
Table 1:
| Field | Value |
|------|------|
| Name | Zheng Shufen |
| Date of birth | 1986-10-27 |
| Gender | Female |
| Occupation | Secondary-school Chinese-language teacher |
| Education | Bachelor's level (Chinese Language and Literature) |
| Height | 162 cm |
| Weight | 54 kg |
| Marital status | Married |
| Current city of residence | Shuangling |

Table 2:
| Field | Value |
|------|------|
| Name | Zheng Shufen |
| Date of birth | 1987-08-14 |
| Gender | Female |
| Occupation | Secondary-school Chinese-language teacher |
| Education | Bachelor's level (Chinese Language and Literature) |
| Height | 162 cm |
| Weight | 54 kg |
| Marital status | Married |
| Current city of residence | Shuangling |


What is Zheng Shufen's date of birth?
(A) 1986-10-27
(B) 1987-08-14
```

## 模型输出 / Model outputs

- **表序 / Order**：表序 0 中，A 是原日期（1987-08-14），B 是备选日期（1986-10-27）；表序 1 中，两者位置互换。  
  In order 0, A is the original date (1987-08-14) and B is the alternative (1986-10-27). Their positions are swapped in order 1.

- **P(A) 和 P(B)**：根据模型生成第一个 token 时 A、B 的分数，计算两者之间的相对概率；每行相加为 1。数值越高，表示模型越倾向该选项。  
  These are probabilities calculated from the model’s first-token scores for A and B, normalised over those two options; each row sums to 1. A higher value indicates a stronger preference for that option.

- **例如 / Example**：Qwen2.5-7B 在表序 0 中偏向 B（99.7%），在表序 1 中偏向 A（约 100%）。两次偏向的都是同一个日期：备选日期 1986-10-27。  
  Qwen2.5-7B favours B in order 0 (99.7%) and A in order 1 (approximately 100%). In both orders, it favours the same date: the alternative, 1986-10-27.

| 模型 / Model | 表序 / Order | P(A) | P(B) | 首 token / First token |
|---|---:|---:|---:|---|
| Qwen2.5-7B-Instruct | 0 | 0.003173 | 0.996827 | `B` |
| Qwen2.5-7B-Instruct | 1 | 0.999999 | 0.000001 | `A` |
| Qwen2.5-14B-Instruct | 0 | 0.999979 | 0.000021 | `A` |
| Qwen2.5-14B-Instruct | 1 | 1.000000 | 0.000000 | `A` |
| Llama-3.1-8B-Instruct | 0 | 0.007012 | 0.992988 | `B` |
| Llama-3.1-8B-Instruct | 1 | 0.757794 | 0.242206 | `A` |
| Gemma-4-E4B-it | 0 | 0.835484 | 0.164516 | `A` |
| Gemma-4-E4B-it | 1 | 0.872347 | 0.127653 | `A` |
| Gemma-4-12B-it | 0 | 0.905322 | 0.094678 | `(` |
| Gemma-4-12B-it | 1 | 0.488283 | 0.511717 | `无法` |

全部 1,208 题的输入见 prompts.jsonl，逐题的 P(A) 和 P(B) 见 raw.json，两者按题目编号 i 对应。

The inputs for all 1,208 items are in prompts.jsonl, and the item-level P(A) and P(B) are in raw.json; the two files are matched by item number i.

- Qwen2.5-7B：[输入 / Inputs](https://github.com/SIAK-q/chinese-source-preference-pilot/blob/main/weekly_2026-11-06/pilot/results_baseline/Qwen2.5-7B-Instruct_full_v1/prompts.jsonl) · [结果 / Results](https://github.com/SIAK-q/chinese-source-preference-pilot/blob/main/weekly_2026-11-06/pilot/results_baseline/Qwen2.5-7B-Instruct_full_v1/raw.json)
- Llama-3.1-8B：[输入 / Inputs](https://github.com/SIAK-q/chinese-source-preference-pilot/blob/main/weekly_2026-11-06/pilot/results_baseline/Llama-3.1-8B-Instruct_full_v1/prompts.jsonl) · [结果 / Results](https://github.com/SIAK-q/chinese-source-preference-pilot/blob/main/weekly_2026-11-06/pilot/results_baseline/Llama-3.1-8B-Instruct_full_v1/raw.json)
- Gemma-4-E4B：[输入 / Inputs](https://github.com/SIAK-q/chinese-source-preference-pilot/blob/main/weekly_2026-11-06/pilot/results_baseline/gemma-4-E4B-it_full_v1/prompts.jsonl) · [结果 / Results](https://github.com/SIAK-q/chinese-source-preference-pilot/blob/main/weekly_2026-11-06/pilot/results_baseline/gemma-4-E4B-it_full_v1/raw.json)
