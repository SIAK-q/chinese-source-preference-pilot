# 数据修订记录 / Data revision record

本页按实施顺序整理原始 pilot 数据到v1的修订。

This page presents the revision from the original pilot data to v1. 

原始数据与v1均含30个实体、151项冲突属性。每项有四个备选，每对值使用两种表序，共1208题。

Both versions contain 30 entities and 151 conflict attributes. Each attribute has four alternatives, tested in both table orders, giving 1,208 items.

## 1. 试做 / Trial

**Prompt**：

- 缩小数值备选与原值的差距，制定取值和检查规则。<br>Reduce numerical differences and set value and checking rules.
- 七类实体各试做一个；每次只改一个属性，其他属性保持原值。<br>Prepare one example per entity type; change one attribute at a time and retain the other original values.
- 示例另存，旧数据不覆盖。<br>Save examples separately; retain the original data.

**结果 / Result**：完成七类实体各一个示例及对应检查记录。

One example from each of the seven entity types, with checking records.

<details>
<summary>示例与检查记录 / Examples and checking records</summary>

- [示例数据 / Example data](demo_entities.jsonl) · [示例变更 / Example changes](demo_changes.json)
- 检查记录 / Checking records：[2ab](acceptance_2ab.json) · [2c](acceptance_2c.json) · [2d](acceptance_2d.json)

</details>

## 2. 批量修订 / Batch revision

**Prompt**：

- 将规则用于全部30个实体。<br>Apply the rules to all 30 entities.
- 记录新旧值、修改方法和理由；未定参数标为暂定。<br>Record old and new values, methods and reasons; mark unsettled parameters as provisional.

**脚本规则 / Script rules**（`draftA_20261104_149/build_full_v1.py`，固定随机种子 / fixed random seed）：

| 属性类型 / Type       | 规则 / Rule                                                                                                                                                                                                                                                                                                                                                                              |
| ----------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 连续数值 / Continuous | 原值 ±5%，两低两高 / ±5%, two lower and two higher                                                                                                                                                                                                                                                                                                                                            |
| 年营业额 / Revenue    | ±10%                                                                                                                                                                                                                                                                                                                                                                                   |
| 完整日期 / Full dates | • 前后一年内分四个区间，各抽一天，两早两晚。<br>One date from each of four intervals within one year: two earlier and two later.<br><br>• 出生和发布日期：前后30–182天、183–365天。<br>Birth and release dates: 30–182 and 183–365 days before or after.<br><br>• 举办日期：前后1–4周、48–52周，保持星期几，月份相差不超过1个月。<br>Event dates: 1–4 and 48–52 weeks before or after, keeping the weekday, with the month differing by at most one. |
| 年月 / Year–month   | ±12 个月 / ±12 months                                                                                                                                                                                                                                                                                                                                                                    |
| 年份 / Years        | −2、−1、+1、+2                                                                                                                                                                                                                                                                                                                                                                            |
| 计数 / Counts       | n−2、n−1、n+1、n+2                                                                                                                                                                                                                                                                                                                                                                        |
| 保修期 / Warranty    | 结构不变，每个备选只改一项条件，取相邻常用档位 / Same structure; each alternative changes one component to an adjacent common level                                                                                                                                                                                                                                                                           |
| 类别 / Categories   | 沿用旧备选 / Keep original alternatives                                                                                                                                                                                                                                                                                                                                                     |

以上为批量生成规则；逐字段调整见第3—5步。

These are the batch-generation rules; attribute-specific adjustments follow in steps 3–5.

## 3. 字段检查 / Attribute review

**Prompt**：

- 列出规则未定或可能与背景冲突的字段。<br>List attributes with unsettled rules or potential conflicts with background information.
- 定义字段含义，查中文资料，提出原值和备选方案。<br>Define each attribute, consult Chinese sources and propose values.
- 将每个备选与同一实体的其他原值搭配检查。<br>Check each alternative against the entity’s other original values.

**主要结果 / Main outcomes**：

| 字段 / Attribute              | 修订后取值或规则 / Revised values or rule                                                                                                                                                          |
| --------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 马拉松持续时间 / Marathon duration | 单位由天改为小时；原值 6小时15分钟，备选 6小时、6小时5分钟、6小时25分钟、6小时30分钟。/ Unit changed from days to hours; original 6 h 15 min, alternatives 6 h, 6 h 5 min, 6 h 25 min, 6 h 30 min. |
| 图书馆高度 / Library height      | 原值 24 米；备选 22、23、25、26 米。/ Original 24 m; alternatives 22, 23, 25, 26 m.                                                                                                                   |
| 图书馆层数 / Library floors      | 原值 3 层；备选 4、5、6、7 层。/ Original 3 floors; alternatives 4, 5, 6, 7 floors.                                                                                                                   |
| 年营业额 / Revenue              | ±10%；屹嘉股份采用一位小数。/ ±10%; one decimal place for Yijia.                                                                                                                                       |
| 下辖乡镇数 / Towns               | 原值保留；备选按 ±1、±2。/ Keep the original; alternatives ±1 and ±2.                                                                                                                                |
| 公司成立时间 / Founding date      | 年月格式，±12 个月。/ Year–month format, ±12 months.                                                                                                                                               |

## 4. 全表审核 / Full review

**Prompt**：

- 逐项审核拟修改值；类别备选在明显反直觉时修改。<br>Review proposed changes; revise categorical alternatives when clearly counter-intuitive.
- 保留原值的自然写法，数值备选兼顾合理性与精度。<br>Retain natural original wording; choose plausible numerical alternatives with appropriate precision.

**结果 / Result**：职业备选“社区卫生服务中心全科医生”改为“社区卫生服务中心护士”。

The occupation alternative “Community health-centre general practitioner” was replaced with “Community health-centre nurse”.

通溪体育馆高度38米、清山图书馆高度24米、长源农业机械博览会参与人数2.3万人次、惠明国际马拉松赛参与人数1.2万人保持原写法，备选取同精度的自然值；四项备选与原值的最大差距分别为5.3%、8.3%、8.7%和16.7%。

The original written forms were kept for Tongxi Gymnasium height (38 m), Qingshan Library height (24 m), Changyuan Agricultural Machinery Expo attendance (23,000) and Huiming International Marathon participants (12,000), with alternatives at the same precision. Their largest differences from the originals are 5.3%, 8.3%, 8.7% and 16.7%.

## 5. 相容性检查 / Compatibility check

**Prompt**：

- 将原值和每个备选分别与同一实体的其他原值搭配检查。<br>Check each original and alternative against the entity’s other original values.
- 对明确的相容性疑点提出修改，并记录理由。<br>Propose changes for identified compatibility issues and record the reasons.

**结果 / Result**：

- 蒋雨柔职业备选：“县医院药剂师”→“县医院ICU护士”，以改善与原护理学历的搭配。
  Jiang Yurou’s occupation alternative: “County-hospital pharmacist” → “County-hospital ICU nurse”, to better fit the original nursing qualification.

- 蒋雨柔学历备选：“大专（医学检验技术）”→“大专（助产）”，以改善与原护士长职业的搭配。
  Jiang Yurou’s education alternative: “College diploma in Medical Laboratory Technology” → “College diploma in Midwifery”, to better fit the original head-nurse occupation.

- 新定会展中心主体结构备选：“膜结构”→“框架-剪力墙结构”，以改善与多层建筑背景的搭配。
  Xinding Convention and Exhibition Centre’s structural alternative: “Membrane structure” → “Frame–shear-wall structure”, to better fit the multi-storey building context.

## 文件入口 / Files

- [原始数据 / Original data](../../data/entities_zh.jsonl) · [v1数据 / Revised v1 data](full_v1/entities_full_v1.jsonl)
- [151项完整对照 / Full comparison of 151 attributes](full_v1/DATA_V1_FULL_SUBMISSION_ZH_EN.md)
- [最终修订脚本 / Final revision script](full_v1/build_full_v1.py) · [变更记录 / Change record](full_v1/changes_from_draft.json)
- [五模型baseline结果 / Five-model baseline results](../../../BASELINE_RESULTS_ZH_EN.md)
