# Entity generation protocol (draft)
中文：实体生成规程（草稿）

下一批按三步生成：先写一个实体的完整原值表，再逐个属性制作4个备选，最后检查并保存。

Create the next batch in three steps: write a complete original table for one entity, make four alternatives for each attribute, then check and save the data.

**规模**：人物、机构、地点和建筑各约30个。活动、产品和艺术作品待定：保持3、3、1个（共约127个实体，按现有属性约659项，每个模型5,272题），或各10个（共约150个实体，约740项，每个模型5,920题）。

**Scale:** About 30 each for person, organisation, location and building entities. Event, product and artwork counts are to be decided: keep 3, 3 and 1 (about 127 entities; with the current attributes, about 659 attributes and 5,272 items per model), or use 10 each (about 150 entities, 740 attributes and 5,920 items per model).

## 1. 生成原值表 / Create the original table

- **输入**：实体类型、属性清单和已准备的姓名或地名。<br>**Input:** The entity type, attribute list and prepared person or place names.
- **操作**：模型写出每项属性的一个原值，使用中文、公制单位和中文日期。整张表要合理，例如中学语文教师配本科（汉语言文学），身高162厘米配体重54公斤。<br>**Action:** The model writes one original value per attribute, using Chinese, metric units and Chinese dates. Values should fit together, such as a secondary-school Chinese teacher with a bachelor’s degree in Chinese Language and Literature, or height 162 cm with weight 54 kg.
- **多样性**：生成时列出同类实体已用过的职业、行业或活动类型，尽量不重复；每批统计各类取值的分布。<br>**Diversity:** List the occupations, industries or event types already used by entities of the same type and avoid repeating them; report the distribution of values for each batch.
- **输出**：一个实体的完整原值表，此时不生成备选。<br>**Output:** A complete original table for one entity, without alternatives yet.

<details>
<summary>七类实体、名称与属性 / Entity types, names and attributes</summary>

| Type 类型 | Name format 名称格式 | Test attributes 测试属性 |
|---|---|---|
| Person 人物 | 中文姓名，例如“郑淑芬” / Chinese full name | 出生日期、职业、学历、身高、体重、婚姻状况、现居城市 / birth date, occupation, education, height, weight, marital status, city of residence |
| Organisation 机构 | 两字名称＋集团／股份有限公司／实业集团，例如“晟远集团” / brand + company form | 成立时间、所属行业、员工人数、年营业额 / founding date, industry, employees, annual revenue |
| Location 地点 | 虚构地名，例如“双陵” / fictional place | 人口、面积、海拔、下辖乡镇数 / population, area, elevation, number of towns |
| Building 建筑 | 地名＋建筑类型，例如“通溪体育馆” / place + building type | 设计师、建成年份、高度、层数、主体结构、容纳人数 / architect, completion year, height, floors, structure, capacity |
| Event 活动 | 地名＋活动类型，例如“惠明国际马拉松赛” / place + event type | 举办日期、持续时间、参与人数、主办方、预算 / date, duration, participants, organizer, budget |
| Product 产品 | 品牌名＋型号＋产品类型，例如“昱腾 ZL-40 装载机” / brand + model + product type | 发布日期、价格、重量、保修期 / release date, price, weight, warranty |
| Artwork 艺术作品 | 《地名＋题名》，例如《白原晚渡图》 / place + title | 创作者、创作年份 / creator, year of creation |

- 实体地名不与信源地名重复，生成方法见[信源规程](SOURCE_GENERATION_PROTOCOL_DRAFT.md)。<br>Entity place names do not overlap with source place names; see the [source-name protocol](SOURCE_GENERATION_PROTOCOL_DRAFT.md) for the method.
- 从ChineseNames抽取三份互不重名的姓名名单，分别用于人物实体、个人信源，以及实体属性中的设计师和创作者。<br>Draw three non-overlapping name lists from ChineseNames: for person entities, individual sources, and entity attribute values such as architects and creators. 抽取和筛查方法见信源规程。<br>See the source-name protocol for sampling and screening.
- 模型给公司起两字名称，例如“晟远”，再加“集团”等字样；给产品起两字品牌名，例如“昱腾”，再加型号和产品类型，组成“昱腾 ZL-40 装载机”。这两个字不带地名，也不提示行业或产品类型；与中文维基已有名称重名的换掉。<br>The model creates a two-character company name, such as 晟远, followed by a company form such as 集团 (Group). For a product, it creates a two-character brand, such as 昱腾, and adds a model and product type, giving 昱腾 ZL-40 装载机 (Yuteng ZL-40 Loader). The two-character name should contain no place name or clue to the industry or product type. Replace names already found on Chinese Wikipedia.
- 与WFW相比，不设总部所在地和制造商：早期公司名带地名（如“北马坪纺织集团”），会直接透露总部；产品名里的品牌会透露制造商。这两项在v1中删除，这里沿用。<br>Unlike WFW, the data do not include headquarters or manufacturer. Early company names contained places (e.g. 北马坪纺织集团), revealing the headquarters, and brand names in product names can reveal the manufacturer. Both attributes were removed in v1 and remain excluded.
- 人物性别由姓名所属的男性或女性使用组决定，只作固定背景。现居城市、设计师、创作者和主办方按第2步的名单或组合规则填写。<br>A person’s gender follows the male- or female-usage group of the name and is fixed background. Fill cities of residence, architect and creator names, and organizers using the list or combination rules in step 2.

</details>

<details>
<summary>原值生成prompt（拟用） / Proposed original-value prompt</summary>

- 为一个虚构的【实体类型】填写原值表，字段为【属性清单】。人名和地名使用已准备的名单；公司名和产品名按上表格式起名。<br>Complete an original table for one fictional [entity type] using [attribute list]. Use the prepared lists for person and place names; create company and product names using the formats above.
- 职业、行业或活动类型尽量不与【同类实体已用的值】重复。<br>Avoid repeating [values already used by entities of the same type] for occupation, industry or event type.
- 每个字段只给一个值，不给备选。使用中文、公制单位和中文日期；相关属性要搭配合理。<br>Give one value per field, without alternatives. Use Chinese, metric units and Chinese dates, with related attributes fitting together.
- 输出完整表格。<br>Return the complete table.

</details>

## 2. 生成四个备选 / Create four alternatives

- **输入**：完整原值表和一个待修改的属性。<br>**Input:** The complete original table and one target attribute.
- **操作**：按下表制作4个备选；每个备选都不同于原值，四个备选互不相同。<br>**Action:** Make four alternatives using the methods below. All four must differ from each other and from the original.
- **只改一个属性**：每道题只改一个属性，其他属性保持原值。两个备选不会同时出现在一张表里，所以每个备选只需和其他原值相配。<br>**One attribute per item:** Each item changes one attribute and keeps the other original values. Two alternatives never appear in the same table, so each alternative only needs to fit the other originals.
- **输出**：该属性的“1个原值＋4个备选”，再处理下一个属性。<br>**Output:** One original value and four alternatives for that attribute, then move to the next attribute.

以同一个人物为例：

For the same person:

| 方法 / Method | 做法与例子 / Procedure and example |
|---|---|
| 代码调整 / Adjust with code | 身高原值162厘米，由代码生成154、158、166、170厘米；体重仍为54公斤。<br>From an original height of 162 cm, code produces 154, 158, 166 and 170 cm; weight stays at 54 kg. |
| 名单抽取 / Draw from a list | 婚姻状况原值为“已婚”，取“未婚、离异、再婚、丧偶”作备选。<br>For an original marital status of “Married”, use “Never married”, “Divorced”, “Remarried” and “Widowed”. |
| 模型生成 / Generate with a model | 输入整张人物原值表，让模型生成4个职业备选，均须与原学历“本科（汉语言文学）”相配。<br>Provide the complete original person table and ask the model for four occupation alternatives compatible with the original bachelor’s degree in Chinese Language and Literature. |

<details>
<summary>代码调整的具体规则 / Rules for code-based adjustments</summary>

| 属性 / Attribute | 规则 / Rule |
|---|---|
| 一般数值 / General numbers | 两低两高，最大差距约±5%，一组约为最大差距的一半，另一组接近最大差距，按原值精度取整。<br>Two lower and two higher values, up to about ±5%; one pair at about half the maximum difference and the other near the maximum, rounded to the original precision. |
| 年营业额 / Revenue | 同上，最大差距约±10%。<br>Same method, up to about ±10%. |
| 出生及发布日期 / Birth and release dates | 四个区间各抽一天：前183–365天、前30–182天、后30–182天、后183–365天。<br>Sample one date from each interval: 183–365 days earlier, 30–182 days earlier, 30–182 days later, 183–365 days later. |
| 举办日期 / Event dates | 四个区间各抽一天：前48–52周、前1–4周、后1–4周、后48–52周；保持星期几，月份相差不超过1个月。<br>Sample one date from each interval: 48–52 weeks earlier, 1–4 weeks earlier, 1–4 weeks later, 48–52 weeks later. Keep the weekday and a month difference of at most one. |
| 年月 / Year–month | 前后12个月内，两早两晚。<br>Two earlier and two later dates within 12 months. |
| 年份 / Years | −2、−1、+1、+2。 |
| 小计数 / Small counts | n−2、n−1、n+1、n+2。n−2小于1或结果不合理时，改用大于n的整数补足四个备选，例如3层用4、5、6、7层。<br>If n−2 is below 1 or implausible, use integers above n to reach four alternatives; for example, 3 floors takes 4, 5, 6 and 7. |
| 持续时间 / Duration | 先换算成统一单位生成备选，再转回自然写法：按天计的用小计数规则，按小时和分钟计的换算成分钟后用一般数值规则。例如6小时15分钟：6小时、6小时5分钟、6小时25分钟、6小时30分钟。<br>Convert to one unit, generate the alternatives, then convert back to natural wording. Durations in days use the small-count rule; durations in hours and minutes are converted to minutes and use the general-number rule. For 6 h 15 min: 6 h, 6 h 5 min, 6 h 25 min, 6 h 30 min. |
| 保修期 / Warranty | 每个备选只改一项条件，取相邻常用档位。<br>Change one component per alternative to an adjacent common level. |

- **数值精度**：若±5%内难以给出四个同精度的自然值，可调整幅度并记录最大差距。例如1.2万人的备选为1.0、1.1、1.3、1.4万人，最大差距16.7%。<br>**Precision:** If four natural alternatives at the original precision are difficult to obtain within ±5%, adjust the range and record the largest difference. For 12,000 people, alternatives of 10,000, 11,000, 13,000 and 14,000 differ by up to 16.7%.
- **保修期**：“整机2年或5000小时”可改为“整机18个月或5000小时”或“整机2年或4000小时”。<br>**Warranty:** “2 years or 5,000 hours” can become “18 months or 5,000 hours” or “2 years or 4,000 hours”.
- 日期抽样的随机种子由42、实体ID和属性名确定。<br>The date-sampling seed is derived from 42, the entity ID and attribute name.

</details>

<details>
<summary>名单抽取与组合的具体规则 / Rules for drawing and combining names and values</summary>

| 属性 / Attribute | 规则 / Rule |
|---|---|
| 婚姻状况 / Marital status | 已婚、未婚、离异、再婚、丧偶中，原值以外的四个。<br>The other four values among married, never married, divorced, remarried and widowed. |
| 现居城市 / City of residence | 保留原值，再从实体地名名单中选4个不同的备选。<br>Keep the original and choose four different alternatives from the entity place list. |
| 设计师、创作者 / Architect, creator | 保留原值，再从这两栏专用的人名名单中选4个不同的备选。<br>Keep the original and choose four different alternatives from the list reserved for these fields. |
| 主办方 / Organizer | 活动所在地名＋5个对该活动合适的单位；单位由模型按活动类型写出。<br>Combine the event location with five institutions suitable for that event, written by the model according to the event type. |

主办方例子：“惠明市体育局”“惠明市文化和旅游局”。

Organizer examples: Huiming Municipal Sports Bureau and Huiming Municipal Culture and Tourism Bureau.

</details>

<details>
<summary>模型生成备选的prompt（拟用） / Proposed alternative-value prompt</summary>

- 以下是一个实体的完整原值表：【原值表】。为【目标属性】生成4个不同的备选，不能重复原值。<br>Given the complete original table [original table], generate four distinct alternatives for [target attribute], none matching its original value.
- 每个备选都要与其他原值相配；其他属性不改。只输出这4个备选。<br>Each alternative must fit the other original values. Leave the other attributes unchanged and return only the four alternatives.

适用于职业、学历、所属行业和主体结构。生成职业备选时保留原学历；生成学历备选时保留原职业。

Use this for occupation, education, industry and structural system. Retain the original education when generating occupations, and the original occupation when generating education alternatives.

</details>

## 3. 检查并保存 / Check and save

- **输入**：原值表和各属性的4个备选。<br>**Input:** The original table and four alternatives per attribute.
- **操作**：按下面三项检查。发现问题时修改对应值，记录新旧值和理由，再检查一次。<br>**Action:** Perform the three checks below. Revise values with identified problems, record the old and new values and reasons, and check them again.
- **输出**：通过检查的数据、中英对照的“原值＋备选”表，以及生成输入、输出和修改记录。<br>**Output:** Checked data, a bilingual table of originals and alternatives, and generation inputs, outputs and revision records.

| 检查 / Check | 怎么检查 / Procedure |
|---|---|
| 数值与格式 / Values and format | 脚本检查数量、重复值、数值范围、单位和精度。<br>Scripts check counts, duplicates, ranges, units and precision. |
| 属性搭配 / Compatibility | 每次把一个属性换成一个备选，其他属性保持原值。例如身高154厘米仍配原体重54公斤，检查是否合理；数值用脚本辅助筛查，类别逐项人工看。同时比较原值和备选是否同样说得通，明显一边更合理的要修改。<br>Replace one attribute with one alternative while retaining the other originals. For example, check height 154 cm against the original weight of 54 kg. Scripts assist with numerical checks; review categorical relationships manually. Also compare whether the original and the alternative are equally plausible, and revise pairs where one is clearly more plausible. |
| 名称提示答案 / Answer clues in names | 实体名和取值有连续两个相同汉字就标出人工看，判断名称是否提示答案；标出不等于有错。<br>Flag two consecutive Han characters shared by an entity name and a value, then review whether the name suggests the answer; a flag does not itself indicate an error. |

全部数据生成并检查后，每个模型运行一次无信源baseline；模型总选同一个值的题，逐项复查取值是否不合理，查出明确问题才修改，修改后只重跑受影响的题。

After all data are generated and checked, run the source-free baseline once per model. Pairs where models consistently prefer one value are reviewed individually for implausible values and changed only if a clear problem is found; only the affected items are rerun.

