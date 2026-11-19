# Publication audit / 上传审核

- Data: 70 entities, 380 attribute instances, 1,520 pairs; all 250 numeric/date/duration items, including warranty months, have two lower and two higher alternatives.
- Five complete runs: 3,040 valid probability records each, matching data SHA256, fixed loaded revision, complete two-order pairing, correct value swapping and identical prompts.
- Recomputed the five main-table rows, strong-preference counts and shared 19 pairs from raw probabilities.
- Corrected report claims: source effects use each item’s own baseline; the size comparison is within Qwen; the 72B baseline is incomplete. Updated source-name sampling and distinguished the explicit missing-source label from baseline.
- **审核结果：** 主表数字通过；改正数值字段漏计和旧规程，保留数据与原始结果。

[Machine-readable results](results.json) include all run hashes and the shared pair list. [Original audit script](audit_source_workspace.py) uses the original research workspace paths. The portable `verify_publication.py` checks this public folder. [Manifest](publication_manifest.json) maps each copied file back to its research-workspace source. Code/scripts in historical records are original snapshots; relative paths may depend on the original workspace.
