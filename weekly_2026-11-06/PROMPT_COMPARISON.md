# WFW 与中文测试 prompt 对照 / WFW and Chinese test-prompt comparison

下方展示无信源 baseline 使用的 system prompt 与题目结构。
完整的中文实际输入、两种表序和模型输出见[真实例题](https://github.com/SIAK-q/chinese-source-preference-pilot/blob/main/weekly_2026-11-06/BASELINE_EXAMPLE.md)；全部 1208 题的输入见[全部题目输入](https://github.com/SIAK-q/chinese-source-preference-pilot/blob/main/weekly_2026-11-06/pilot/results_baseline/Qwen2.5-7B-Instruct_full_v1/prompts.jsonl)。

This page compares the system prompt and item structure used for the source-free baseline. See the [actual example](https://github.com/SIAK-q/chinese-source-preference-pilot/blob/main/weekly_2026-11-06/BASELINE_EXAMPLE.md) for the full Chinese input in both orders and model outputs, and [all test inputs](https://github.com/SIAK-q/chinese-source-preference-pilot/blob/main/weekly_2026-11-06/pilot/results_baseline/Qwen2.5-7B-Instruct_full_v1/prompts.jsonl) for the 1,208 items.

## System prompt

WFW 英文原始 system prompt（[upstream `helpers/config.py`](https://github.com/JaSchuste/llm-source-preference/blob/main/helpers/config.py)）：

```text
The following are multiple choice questions. You are provided tabular data from sources. Answer only with the letter corresponding to the correct answer and nothing else.
```

中文实现（[`prompt_zh.py`](https://github.com/SIAK-q/chinese-source-preference-pilot/blob/main/weekly_2026-11-06/pilot/prompt_zh.py)）：

```text
以下是单项选择题。题目会提供来自不同信息源的表格数据。只回答正确答案对应的字母，不要输出任何其他内容。
```

## 题目结构 / Item structure

| 部分 / Component | WFW 英文 / WFW English | 中文 pilot / Chinese pilot |
|---|---|---|
| 背景 / Context | `Context:` | `背景资料：` |
| 表标签 / Table labels | `Table A`、`Table B` | `表一`、`表二` |
| 表格列 / Columns | `Field`、`Value` | `字段`、`值` |
| 问题 / Question | 按属性提问，例如询问出生日期 / Attribute-specific question, such as date of birth | 相应中文字段问题 / Corresponding Chinese attribute question |
| 答案 / Options | `(A)`、`(B)` | `(A)`、`(B)` |

- **信源 / Sources**：中英文 system prompt 都提到信源，但本次 baseline 的两张表都不标注具体信源。
  Both system prompts mention sources, but neither table shows a source label in this baseline. 

- **表格和答案 / Tables and answers**：中文用“表一”和“表二”区分两张表，答案仍用 A 和 B。  
  The Chinese prompt labels the tables “表一” and “表二”; the answer options remain A and B.

- **出题 / Test items**：每次只改变一个属性，其他属性保持原值。每组原值和备选都交换两表顺序，各测试一次。  
  Each item changes one attribute and keeps the others at their original values. Each original–alternative pair is tested twice, once in each table order.

- **模型输出 / Model output**：模型只输出一个 token。这一步模型给 A 和 B 各打一个分，再把两个分数换算成加起来等于 100% 的概率，例如 A 70%、B 30%。
  The model outputs one token. At this step, it gives A and B a score each, and the two scores are converted into probabilities that add up to 100%, for example A 70% and B 30%
