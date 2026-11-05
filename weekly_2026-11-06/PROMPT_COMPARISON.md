# WFW 与中文测试 prompt 对照 / WFW and Chinese test-prompt comparison

下方展示无信源 baseline 使用的系统指令与题目结构。完整的中文实际输入、两种表序和模型输出见[真实例题](BASELINE_EXAMPLE.md)；全部 1208 题的输入见[结果入口](README.md#无信源-baseline--source-free-baseline)。

This page compares the system instruction and item structure used for the source-free baseline. See the [actual example](BASELINE_EXAMPLE.md) for the full Chinese input in both orders and model outputs, and the [results index](README.md#无信源-baseline--source-free-baseline) for all 1,208 inputs.

## 系统指令 / System instruction

WFW 英文原始指令（[upstream `helpers/config.py`](https://github.com/JaSchuste/llm-source-preference/blob/main/helpers/config.py)）：

```text
The following are multiple choice questions. You are provided tabular data from sources. Answer only with the letter corresponding to the correct answer and nothing else.
```

中文实现（[`prompt_zh.py`](pilot/prompt_zh.py)）：

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
| 答案 / Options | `(A)`、`(B)` | `（A）`、`（B）` |

两版的系统指令都提到来源；在此无信源 baseline 条件下，**两张表均不显示来源标签**。中文使用“表一／表二”与答案 A/B 区分；答案 token 仍为 A/B。中文“不同信息源”中的“不同”比英文原指令更明确，这是一处措辞差异。

Both system instructions mention sources; in this source-free baseline, **neither table displays a source label**. Chinese uses “表一／表二” to distinguish table labels from answer tokens A/B, which remain unchanged. The Chinese instruction explicitly says “different” sources, which is an additional wording choice relative to the English instruction.

每题只改变一个属性，其他属性保持原值。原值与每个备选以两种表序分别展示。模型推理取第一个 token 的 A/B 分数，并仅在两个答案 token 之间归一化；模型不生成完整解释。

Each item changes one attribute while retaining the other original attributes. Each original–alternative pair appears in both table orders. Inference uses first-token A/B scores normalised only over the two answer tokens; no full explanation is generated.
