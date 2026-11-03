# 模型输入与输出 / Model input and output

中文 pilot 参照 WFW 构造实体、属性值和信源。下表展示数据生成过程。

The Chinese pilot follows WFW to construct entities, attribute values and sources. The table shows the data-generation process.

## 模型看到了什么 / What the model saw

模型根据以下任务要求及会话中获得的材料，生成整批中文 pilot 数据。

The model generated the Chinese pilot data as a batch, using the task requirements and material obtained during the session.

| 输入 / Input                                    | 模型获得的信息 / Information available to the model                                                                                                                                                                             | 记录 / Record                                                            |
| --------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------- |
| **生成要求**<br>Task requirements                 | 按 WFW 的结构生成中文实体、属性原值和备选，以及信源名称；使用中文名称、公制单位和中文日期。<br>Generate Chinese entities, original and alternative attribute values, and source names following WFW's structure; use Chinese names, metric units and Chinese dates. | [生成要求 / Generation requirements](prompts/2_task.md)                    |
| **WFW 实体结构**<br>WFW entity structure          | 各类实体的数量和字段；每个测试属性使用原值和4个备选的列表。<br>Entity counts and fields by type; each test attribute uses a list containing an original and four alternatives.                                                                        | 文件读取明细见页底 / File-reading details below                                 |
| **WFW 英文实体**<br>WFW English entities          | 两个人物的完整记录及第三个人物记录的开头，包含姓名、属性及其原值和备选。<br>Two complete person records and the beginning of a third, containing names, attributes, originals and alternatives.                                                              | 读取英文实体文件开头3,000字节 / First 3,000 bytes of the English entity file       |
| **WFW 信源与代码**<br>WFW sources and code         | 政府和报纸信源模板、姓名和地名列表示例、问题模板，以及相关代码。<br>Government and newspaper source templates, samples of person-name and place-name lists, question templates, and relevant code.                                                       | 文件读取明细见页底 / File-reading details below                                 |
| **中文姓名和地名**<br>Chinese person and place names | 数据生成前，模型写出常见中文姓名并查询中文维基。一批15个常见姓名中有2个查到词条，未用于后续名单；提交的20个姓名均未查到同名词条。地名的生成见下表。<br>Before data generation, the model wrote common Chinese names and checked them against Chinese Wikipedia. Two of a batch of 15 common names had matching pages and were not included in the later list; none of the 20 submitted names had a matching page. Place-name generation is described below. | [姓名与地名要求 / Name and place-name requirements](prompts/1_place_names.md) |

## 模型写出了什么 / What the model wrote

模型在同一份脚本中写出整批实体的原值和备选。第一版共30个实体、169项测试属性。

The model wrote the originals and alternatives for the batch of entities in one script. The first version contains 30 entities and 169 test attributes.

[第一版脚本 / First script](prompts/output_round1.md) · [第一版数据 / First data](prompts/output_round1.jsonl)

### 属性的写入顺序 / Attribute order in the script

第一版脚本按属性组织数据。人物部分的排列如下：

The first script organises data by attribute. The person section is arranged as follows:

| 顺序 / Order | 内容 / Content |
|---|---|
| 1 | 姓名、性别、原职业 / Name, gender and original occupation |
| 2 | 职业原值和备选 / Original occupation and alternatives |
| 3 | 出生日期、学历、身高、体重、婚姻状况 / Date of birth, education, height, weight and marital status |
| 4 | 现居城市、国籍：代码按固定规则填入 / City of residence and nationality: filled by code using fixed rules |

其他实体类型的写入顺序 / Writing order for the other entity types:

| 实体类型 / Entity type | 写入顺序 / Order |
|---|---|
| 机构 / Organization | 名称与原行业 → 成立时间 → 员工人数 → 年营业额 → 所属行业（5个值）/ name and original industry → founding date → employees → annual revenue → industry (5 values) |
| 地点 / Location | 名称 → 人口 → 面积 → 海拔 / name → population → area → elevation |
| 建筑 / Building | 名称 → 设计师 → 建成年份 → 高度 → 层数 → 主体结构 → 容纳人数 / name → architect → completion year → height → floors → structural system → capacity |
| 事件 / Event | 名称 → 举办日期 → 持续时间 → 参与人数 → 主办方 → 预算 / name → date → duration → participants → organizer → budget |
| 产品 / Product | 名称 → 制造商 → 发布日期 → 价格 → 重量 → 保修期 / name → manufacturer → release date → price → weight → warranty |
| 艺术作品 / Artwork | 名称 → 创作者 → 创作年份 / name → creator → creation year |

第二版修改时，模型参考第一版脚本和结果，重写数据脚本；机构和产品的新品牌名、地点的下辖乡镇数在这一版写入。人名明确分为三个互不重叠的名单：8个人物实体、5个个人信源、7个设计师和创作者。

For the second version, the model used the first script and results as context and rewrote the data script. The new organization and product brand names and the location town/township counts were written in this version. Person names were explicitly divided into three non-overlapping lists: 8 person entities, 5 individual sources, and 7 architects and creators.

## 修改及最终结果 / Revisions and final data

| 阶段 / Stage | 修改 / Revision | 输出 / Output |
|---|---|---|
| **数据修改**<br>Data revision | 根据[指令3](prompts/3_corrections.md)修改名称、字段和部分取值。<br>Following [Instruction 3](prompts/3_corrections.md), revise names, fields and some values. | [第二版脚本 / Second script](prompts/output_round2.md) · [第二版数据 / Second data](prompts/output_round2.jsonl)：30实体、151项属性 / 30 entities, 151 attributes |
| **统一地名池**<br>Shared place-name pool | 根据[指令4](prompts/4_shared_place_pool.md)统一地名池并更新相关名称。<br>Following [Instruction 4](prompts/4_shared_place_pool.md), unify the place-name pool and update the relevant names. | [地名方法 / Place-name method](place_names/README.md) · [最终实体 / Final entities](../entities_zh.jsonl) · [信源 / Sources](../sources_zh.json) |

三轮先后用过三批地名。每一轮都是先定下当轮的地名，再写入数据；只有第三轮才是政府、报纸和实体共用的一个地名池。

Three successive sets of place names were used. In each round, the names were fixed before they were written into the data; only in round 3 did government sources, newspapers and entities share one pool.

| 轮次 / Round    | 地名怎么来 / How the names were made                                                                                                                                                                                                                                                                                                                                                                                 | 怎么分配 / How they were assigned                                                                                                          | 写入数据 / Used in data                                                                                                                                                                                                                                                                                         |
| ------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 第一轮 / Round 1 | [指令1](prompts/1_place_names.md)后，模型先交一批三字名（如青鹤城），被指出像武侠小说；按真实三字地名字频重做（如北马坪、南头堡），后确认。<br>After [Instruction 1](prompts/1_place_names.md), a first batch (e.g. 青鹤城) was rejected as sounding like martial-arts fiction; the names were redone from the character frequencies of real three-character place names (e.g. 北马坪, 南头堡) and confirmed.                                                                   | 按用途分开：政府5个、报纸5个、实体10个。<br>Separate lists: 5 for government, 5 for newspapers, 10 for entities.                                         | 第一版脚本<br>first script                                                                                                                                                                                                                                                                                       |
| 第二轮 / Round 2 | [指令3](prompts/3_corrections.md)要求改用县市级两字地名；模型生成（如平宁、临源）。<br>[Instruction 3](prompts/3_corrections.md) asked for two-character county/city-level names; the model made them (e.g. 平宁, 临源).                                                                                                                                                                                                                       | 仍按用途分开：政府、报纸、地点实体、其他实体各5个。<br>Still separate lists: 5 each for government, newspapers, location entities and other entities.           | 第二版脚本（整份重写）<br>second script (rewritten in full)                                                                                                                                                                                                                                                            |
| 第三轮 / Round 3 | [指令4](prompts/4_shared_place_pool.md)要求共用一个地名池；模型统计真实县市地名的用字频率，组合候选并查重，得到最终20个（如双陵、通溪），方法见[地名生成](place_names/README.md)。<br>[Instruction 4](prompts/4_shared_place_pool.md) asked for one shared pool; the model counted character frequencies in real county/city names, combined and checked candidates, and arrived at the final 20 names (e.g. 双陵, 通溪); see [place-name generation](place_names/README.md). | 共用一个池：前10个交错分给政府和报纸，后10个给实体。<br>One shared pool: the first 10 alternate between government and newspapers, the last 10 go to entities. | 在第二版脚本上更新地名：用这个地名池生成政府和报纸信源名称（如广城市民政局、临阳日报），并更新实体名称、现居城市和主办方中的地名；其他取值不变<br>The second script was updated: government and newspaper source names were built from this pool (e.g. 广城市民政局, 临阳日报), and the place names in entity names, cities of residence and organizers were updated; other values unchanged |

模型读过的英文实体示例中，有14个生日值也出现在中文 pilot 数据中。现居城市由脚本按固定规则从地名池填入；最终版活动主办方由代码组合地名和机构名称。

Fourteen birth-date values from the English entity examples also appear in the Chinese pilot data. The script fills cities of residence from the place-name pool using a fixed rule; in the final version, code combines place names and institution names for event organizers.

<details>
<summary>WFW参考材料读取明细 / WFW reference files read</summary>

| 文件 / File | 读取范围 / Portion read |
|---|---|
| `data/neoqa_entities_counterfactual.jsonl` | 开头3,000字节及类别/字段统计 / first 3,000 bytes and class/field counts |
| `data/government_template.jsonl`; `data/newspaper_templates.txt` | 政府模板前2,000字节；报纸模板全文 / first 2,000 bytes of government templates; full newspaper templates |
| `data/names_last.txt`; `data/names_first_male.json` | 前20行；前400字节 / first 20 lines; first 400 bytes |
| `data/timeline_locations.json`; `data/circulation_values.json`; `data/question_cache.json` | 前1,200、1,000、1,500字节 / first 1,200, 1,000 and 1,500 bytes |
| `data/explicit_questions.txt` | 全文 / full file |
| `helpers/config.py`; `helpers/models.py`; `helpers/model_inference.py` | 全文 / full files |
| `helpers/prompt_builder.py`; `helpers/evaluation.py` | 部分内容 / selected portions |
| `helpers/source_generator.py` | 函数名检索 / function-name search |

</details>
