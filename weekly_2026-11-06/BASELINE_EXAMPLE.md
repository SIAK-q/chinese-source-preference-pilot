# 无信源 baseline：一道实际题 / One source-free baseline pair

原值和备选在两种表序下互换。下面的输入与输出取自三个模型的实际 v1 运行（PERSON-1，出生日期，备选1），不是手写示例。系统消息虽然提及信息源，两张表本身均不标注来源。

The original and alternative switch positions in the two table orders. Inputs and outputs below are from the actual v1 runs (PERSON-1, date of birth, alternative 1), not a handwritten example. The system message mentions sources, but neither table carries a source label.

## 系统消息 / System message

```text
以下是单项选择题。题目会提供来自不同信息源的表格数据。只回答正确答案对应的字母，不要输出任何其他内容。
```

**英文释义（非模型输入）/ English reading translation (not model input):** These are single-choice questions. The question provides tabular data from different sources. Answer only with the letter corresponding to the correct answer, with no other output.

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
（A）1987年8月14日
（B）1986年10月27日
```

**英文释义（非模型输入）/ English reading translation (not model input):**

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
（A）1986年10月27日
（B）1987年8月14日
```

**英文释义（非模型输入）/ English reading translation (not model input):**

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

首 token 的 A/B 条件概率；不是完整生成回答。/ First-token A/B conditional probabilities, not full generated answers.

| 模型 / Model | 表序 / Order | P(A) | P(B) |
|---|---:|---:|---:|
| Qwen2.5-7B-Instruct | 0 | 0.023655 | 0.976345 |
| Qwen2.5-7B-Instruct | 1 | 0.999990 | 0.000010 |
| Llama-3.1-8B-Instruct | 0 | 0.022629 | 0.977371 |
| Llama-3.1-8B-Instruct | 1 | 0.927363 | 0.072637 |
| gemma-4-E4B-it | 0 | 0.715424 | 0.284576 |
| gemma-4-E4B-it | 1 | 0.894789 | 0.105211 |
