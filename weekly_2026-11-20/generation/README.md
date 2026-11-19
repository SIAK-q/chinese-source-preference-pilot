# How this batch was made / 本批如何生成

- **Generate originals:** Codex read the saved task prompt and wrote an original table in the ongoing conversation. Exact model version and sampling parameters were not visible.
- **Generate alternatives:** text alternatives were written with the complete original table in view; scripts supplied dates, numeric values and selections from prepared name/place lists.
- **Check and revise:** per-entity checks, user feedback and revised outputs are saved beside the inputs. Later revisions changed organisation scales, product warranty wording and removed the person hometown field.
- **Final version:** `final70_20261118_v2`, approved on 18 November; 70 entities and 380 attribute instances. Final data and the removal decision are under [data](../data/).
- **生成路线：** 先原值、再四备选、检查、按反馈修改；每个实体都有输入和原始输出。

| Record | Where to inspect |
|---|---|
| Current concise rules | [Chinese protocol](PROTOCOL_ZH.md) |
| Frozen original/alternative templates | [templates](records/new_batch_20261116_v2/templates/) |
| Every entity’s actual input, prompt, raw output and checks | [70 entity folders](records/new_batch_20261116_v2/entities/) |
| Example artwork | [ART-01](records/new_batch_20261116_v2/entities/ART-01/) |
| Revised organisation scale and industries | [revision records](records/new_batch_20261116_v2/organization_scale_revision_20261116/) |
| Warranty revision | [revision records](records/new_batch_20261116_v2/product_warranty_wording_20261118/) |
| Final components | [CURRENT_DATA.json](records/new_batch_20261116_v2/CURRENT_DATA.json) |
| Saved process explanation with verbatim example | [Chinese process record](PROCESS_RECORD_ZH.md) |

The saved process explanation describes the 18 November generation stage; its statement that baseline had not run belongs to that date. Current completion status is in the release index. Historical prompts and raw records are preserved verbatim. Task prompts are saved inputs within the conversation, not standalone API-call transcripts. Scripts and records are snapshots of their original workspace; paths in them refer to that workspace.
