# 本周进展与材料 / Progress and materials · 20 November 2026

- **数据 / Data:** 从30扩至70个实体，冲突对从604增至1,520。 / Expanded from 30 to 70 entities and from 604 to 1,520 conflict pairs.
- **Baseline:** 五个模型已完成，每模型3,040题；72B待完成。 / Five models complete, with 3,040 prompts each; 72B remains.
- **信源 / Sources:** 补全11月9日草稿的命名、抽样和筛查规则。 / Developed the naming, sampling and screening rules from the 9 November draft.

| 材料 / Material | 内容 / Contents |
|---|---|
| ① [完整数据表 / Full data table](data/REVIEW_TABLE.md) | 七类各10个实体；中文实验数据与英文阅读译文。 / Ten entities per type; Chinese experimental data with English reading translations. |
| ② [数据生成过程 / Data generation](generation/README.md) | 五步流程，附实际prompt、原始输出、脚本与检查。 / Five steps with actual prompts, raw outputs, scripts and checks. |
| ③ [Baseline结果 / Baseline results](baseline/README.md) | 位置偏好、取值偏好、属性差异与补充检查。 / Position preferences, value preferences, attribute differences and additional checks. |
| ④ [信源名称生成规程 / Source-name generation](sources/SOURCE_GENERATION_PROTOCOL.md) | 地名、政府、报纸、个人及社媒名称的生成方法与依据。 / Methods and supporting sources for place, government, newspaper, individual and social-media names. |

<details>
<summary>代码、输入与结果 / Code, inputs and results</summary>

- [Baseline运行记录 / Baseline run records](baseline/results/README.md)：五模型逐题输出与分析。 / Item-level outputs and analyses for five models.
- [Baseline脚本 / Baseline scripts](baseline/code/) · [中文题目 / Chinese prompts](baseline/prompts.jsonl) · [检查 / Checks](baseline/checks/)。
- [信源代码与输入 / Source-generation code and inputs](sources/SOURCE_GENERATION_PROTOCOL.md#附件--files)。

</details>
