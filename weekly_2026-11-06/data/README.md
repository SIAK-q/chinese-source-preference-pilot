# 数据与修订 / Data and revisions

- **数据 / Data:** 30实体、151项属性；每项原值＋四备选。 / 30 entities, 151 attributes; one original and four alternatives each.
- [原始生成记录 / Original generation records](../../generation/MODEL_INPUT.md)：模型输入、三轮生成与修改。 / Model inputs and three rounds of generation and revision.
- [原始 → v1完整对照 / Original → v1 comparison](../pilot/data_review/value_revision/full_v1/DATA_V1_FULL_SUBMISSION_ZH_EN.md)：全部取值与修改说明。 / All values and revision rationales.
- [修订prompt与结果 / Revision prompts and results](../pilot/data_review/value_revision/PROMPTS_REVISION_SUBMISSION.md)：规则、审核与相容性检查。 / Rules, review and compatibility checks.

<details>
<summary>数据与处理文件 / Data and processing files</summary>

- [原始数据 / Original data](../pilot/data/entities_zh.jsonl) · [v1数据 / v1 data](../pilot/data_review/value_revision/full_v1/entities_full_v1.jsonl)。五值列表首项为原值。 / The first of each five-value list is the original.
- [修订脚本 / Revision script](../pilot/data_review/value_revision/full_v1/build_full_v1.py) · [变更记录 / Changes](../pilot/data_review/value_revision/full_v1/changes_from_draft.json) · [相容性检查 / Compatibility check](../pilot/data_review/value_revision/full_v1/compat_check_v1.json)。
- [基础脚本 / Base script](../pilot/data_review/value_revision/draftA_20261104_149/build_full_v1.py) · [中间数据 / Intermediate data](../pilot/data_review/value_revision/draftB_20261105_150/entities_full_v2.jsonl)。

</details>
