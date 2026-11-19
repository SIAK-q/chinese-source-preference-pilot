# Supporting materials · 20 November 2026

- **Data:** 70 entities, 380 entity–attribute items, 1,520 conflict pairs and 3,040 prompts per model.
- **Baseline:** five completed models; the 72B baseline remains incomplete in this release.
- **Sources:** rules and 15,200 prepared prompts (including baseline); source comparisons follow discussion of the full baseline.
- **本周材料：** 数据、生成记录、五模型baseline、信源规程；先看下表。

| Material / 材料 | Review entry / 审阅入口 | Supporting records / 原始材料 |
|---|---|---|
| Progress report / report草稿 | [Bilingual draft](REPORT_DRAFT.md) | [Audit findings](audit/README.md) |
| Expanded data / 新70实体 | [Original + four alternatives](data/REVIEW_TABLE.md) | [Exact JSONL](data/entities_zh.jsonl), [user decisions](data/review_decisions.json) |
| Generation / 生成过程 | [Procedure and record map](generation/README.md) | [Per-entity prompts and raw outputs](generation/records/new_batch_20261116_v2/entities/) |
| Models and baseline / 模型与baseline | [Results and fixed model versions](baseline/README.md) | [Raw probabilities](baseline/raw/), [identical input prompts](baseline/prompts.jsonl) |
| Source setup / 信源设置 | [Current bilingual protocol](sources/PROTOCOL.md) | [Prepared batch and checks](sources/README.md) |

All filenames and hashes are listed in [SHA256SUMS](SHA256SUMS). Run `python3 audit/verify_publication.py` from this directory to check the release. Earlier weekly folders remain unchanged.
