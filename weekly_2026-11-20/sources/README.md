# Prepared source materials / 已准备的信源材料

- [Current bilingual rules](PROTOCOL.md): government, newspapers, individuals and social-media handles.
- [Manifest](manifest.json): 7,600 pairs and 15,200 prompts across baseline + four source comparisons, seed 20261111. Sources move with their values across table orders.
- [Full saved prompts, gzip](prompts.jsonl.gz); [ten readable sample prompts](sample_prompts.jsonl), two table orders per condition.
- All 1,520 retained individual-source names have no exact-title Chinese Wikipedia page in the saved checks; 36 draws were skipped because a page existed. [Raw Wikipedia responses and request metadata](wiki/) preserve the check date and hashes.
- Place pool: 1,327 after the 75 recorded removals; source sampling excludes 11 entity place names, leaving 1,316.
- The fourth comparison uses the explicit label “无可用信源” (“No source available”) against government. The baseline omits source labels from both tables.
- **当前阶段：** 配题完成；完整baseline先与老师讨论，再运行信源对比。

[Code snapshots](code/) preserve the source sampler and preparation logic. They use external naming resources cited in the protocol; third-party frequency tables are not redistributed here. Historical workspace paths in the snapshots are retained. All full prompts are saved, so the prepared batch can be inspected without re-sampling.
