# 模型输入与输出 / Model input and output

模型分三轮写出脚本和数据，最终得到30个实体、151项测试属性。[最终实体 / Final entities](prompts/round3/entities_zh.jsonl) · [信源 / Sources](prompts/round3/sources_zh.json)

The model wrote the scripts and data in three rounds, ending with 30 entities and 151 test attributes.

## 模型看到了什么 / What the model saw

| 输入 / Input                                  | 模型获得的信息 / Information available to the model                                                                                                                                                                                                                                                                                                                                                  | 记录 / Record                                                            |
| ------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------- |
| **任务要求**<br>Task requirements               | 按 WFW 的结构生成中文实体、属性原值和备选，以及信源名称；使用中文名称、公制单位和中文日期。<br>Generate Chinese entities, original and alternative attribute values, and source names following WFW's structure; use Chinese names, metric units and Chinese dates.                                                                                                                                                                      | [生成要求 / Generation requirements](prompts/2_task.md)                    |
| **WFW 结构与示例**<br>WFW structure and examples | 各类实体的数量和字段；每个测试属性使用原值和4个备选的列表；两个完整人物记录及第三个记录的开头；政府和报纸信源模板、姓名和地名列表示例、问题模板及相关代码。<br>Entity counts and fields by type; each test attribute uses a list of an original and four alternatives; two complete person records and the beginning of a third; government and newspaper templates, samples of person-name and place-name lists, question templates and relevant code.                    | 读取明细见页底 / File-reading details below                                   |
| **姓名和地名准备**<br>Person and place names       | 模型写出常见中文姓名并查询中文维基，查到词条的姓名不用；提交的20个姓名均未查到词条。地名见下表。<br>The model wrote common Chinese names and checked them against Chinese Wikipedia; names with a page were not used, and none of the 20 submitted names had a page. Place names are described below. | [姓名与地名要求 / Name and place-name requirements](prompts/1_place_names.md) |

## 三轮生成和修改 / Three rounds of generation and revision

| 轮次 / Round | 输入要求 / Input | 主要改动 / Main changes | 脚本与输出 / Scripts and output |
|---|---|---|---|
| **第一轮**<br>Round 1 | [生成要求](prompts/2_task.md)；地名按[指令1](prompts/1_place_names.md)。<br>[Generation requirements](prompts/2_task.md); place names from [prompt 1](prompts/1_place_names.md). | 在同一份脚本中写出整批原值和备选。地名为三字名（如北马坪、南头堡），政府5个、报纸5个、实体10个，分开使用。<br>All originals and alternatives were written in one script. Place names had three characters (e.g. 北马坪, 南头堡), in separate lists: 5 for government, 5 for newspapers and 10 for entities. | [第一版脚本 / First script](prompts/round1/output_round1.md) · [第一版数据 / First data](prompts/round1/output_round1.jsonl)：30实体、169项属性 / 30 entities, 169 attributes |
| **第二轮**<br>Round 2 | [指令3](prompts/3_corrections.md)。<br>[Prompt 3](prompts/3_corrections.md). | 参考第一版重写脚本，修改名称、字段和部分取值；写入机构和产品的新品牌名、地点的下辖乡镇数。人名分为三个互不重叠的名单：8个人物实体、5个个人信源、7个设计师和创作者。地名改为县市级两字名（如平宁、临源），政府、报纸、地点实体、其他实体各5个。<br>The script was rewritten with the first version as context, revising names, fields and some values, and adding new organization and product brand names and location town/township counts. Person names were divided into three non-overlapping lists: 8 person entities, 5 individual sources, and 7 architects and creators. Place names became two-character county/city-level names (e.g. 平宁, 临源), 5 each for government, newspapers, location entities and other entities. | [第二版脚本 / Second script](prompts/round2/output_round2.md) · [第二版数据 / Second data](prompts/round2/output_round2.jsonl)：30实体、151项属性 / 30 entities, 151 attributes |
| **第三轮**<br>Round 3 | [指令4](prompts/4_shared_place_pool.md)。<br>[Prompt 4](prompts/4_shared_place_pool.md). | 政府、报纸和实体共用20个地名（如双陵、通溪）：前10个交错分给政府和报纸，后10个给实体。据此生成政府和报纸信源名称，并更新实体名称、现居城市和主办方中的地名；其他取值不变。[地名方法](place_names/README.md)。<br>Government, newspapers and entities share 20 place names (e.g. 双陵, 通溪): the first 10 alternate between government and newspapers, and the last 10 go to entities. Government and newspaper source names were built from this pool, and place names in entity names, cities of residence and organizers were updated; other values are unchanged. [Place-name method](place_names/README.md). | [第三轮脚本与数据 / Round 3 scripts and data](prompts/round3/README.md) |

## 哪些值由模型写，哪些由代码填 / Values written by the model and filled by code

- 原值和备选由模型写入脚本。人物部分先写职业，后写学历。

  The model wrote originals and alternatives in the script. In the person section, occupation comes before education.
- 模型读过的英文实体示例中，有14个生日值也出现在中文 pilot 数据中。

  Fourteen birth-date values from the English entity examples also appear in the Chinese pilot data.
- 现居城市由脚本按固定规则从地名池填入；最终版活动主办方由代码组合地名和机构名称。

  The script fills cities of residence from the place-name pool using a fixed rule; in the final version, code combines place names and institution names for event organizers.

<details>
<summary>第一版脚本的属性写入顺序 / Attribute order in the first script</summary>

| 顺序 / Order | 人物 / Person |
|---|---|
| 1 | 姓名、性别、原职业 / Name, gender and original occupation |
| 2 | 职业原值和备选 / Original occupation and alternatives |
| 3 | 出生日期、学历、身高、体重、婚姻状况 / Date of birth, education, height, weight and marital status |
| 4 | 现居城市、国籍：代码按固定规则填入 / City of residence and nationality: filled by code using fixed rules |


| 实体类型 / Entity type | 写入顺序 / Order |
|---|---|
| 机构 / Organization | 名称与原行业 → 成立时间 → 员工人数 → 年营业额 → 所属行业（5个值）/ name and original industry → founding date → employees → annual revenue → industry (5 values) |
| 地点 / Location | 名称 → 人口 → 面积 → 海拔 / name → population → area → elevation |
| 建筑 / Building | 名称 → 设计师 → 建成年份 → 高度 → 层数 → 主体结构 → 容纳人数 / name → architect → completion year → height → floors → structural system → capacity |
| 事件 / Event | 名称 → 举办日期 → 持续时间 → 参与人数 → 主办方 → 预算 / name → date → duration → participants → organizer → budget |
| 产品 / Product | 名称 → 制造商 → 发布日期 → 价格 → 重量 → 保修期 / name → manufacturer → release date → price → weight → warranty |
| 艺术作品 / Artwork | 名称 → 创作者 → 创作年份 / name → creator → creation year |

</details>

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
