# 模型输入与输出 / Model input and output

模型分三轮写出脚本和数据，最终得到30个实体、151项测试属性。[最终实体 / Final entities](prompts/round3/entities_zh.jsonl) · [信源 / Sources](prompts/round3/sources_zh.json)

The model wrote the scripts and data in three rounds, ending with 30 entities and 151 test attributes.

## 模型看到了什么 / What the model saw

| 输入 / Input                                  | 模型获得的信息 / Information available to the model                                                                                                                                                                             | 记录 / Record                                                            |
| ------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------- |
| **任务要求**<br>Task requirements               | 按 WFW 的结构生成中文实体、属性原值和备选，以及信源名称；使用中文名称、公制单位和中文日期。<br>Generate Chinese entities, original and alternative attribute values, and source names following WFW's structure; use Chinese names, metric units and Chinese dates. | [生成要求 / Generation requirements](prompts/2_task.md)                    |
| **WFW 结构与示例**<br>WFW structure and examples | 实体类别与字段、原值＋4个备选的结构、人物记录示例，以及信源和问题模板。<br>Entity classes and fields, the structure of one original plus four alternatives, sample person records, and source and question templates.                                       | 读取明细见页底 / File-reading details below                                   |
| **姓名和地名准备**<br>Person and place names       | 模型生成中文姓名，并排除中文维基已有词条的姓名。地名见下表。<br>The model generated Chinese names and excluded those with a Chinese Wikipedia page. Place names are covered below.                                                                     | [姓名与地名要求 / Name and place-name requirements](prompts/1_place_names.md) |

## 数据生成与修订 / Data generation and revision

| 轮次 / Round         | 输入要求 / Input                                                                                                                                                          | 主要改动 / Main changes                                                                                                                                                                                                                                                                                                                         | 脚本与输出 / Scripts and output                                                                                                                                     |
| ------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **第一轮**<br>Round 1 | [生成要求](prompts/2_task.md)；地名按[指令1](prompts/1_place_names.md)。<br>[Generation requirements](prompts/2_task.md); place names from [prompt 1](prompts/1_place_names.md). | 模型生成整批脚本和数据，原值和备选由模型写入脚本。<br>The model generated the full script and data, writing originals and alternatives in the script.                                                                                                                                                                                                                | [第一版脚本 / First script](prompts/round1/output_round1.md) · [第一版数据 / First data](prompts/round1/output_round1.jsonl)：30实体、169项属性 / 30 entities, 169 attributes   |
| **第二轮**<br>Round 2 | [指令3](prompts/3_corrections.md)。<br>[Prompt 3](prompts/3_corrections.md).                                                                                             | 修改机构和产品品牌名，将人物实体、个人信源、设计师及创作者的人名分为三个互不重叠的名单；调整属性和部分取值，属性总数从169项减至151项。

Organization and product brand names were revised. Three non-overlapping name lists were used for person entities, individual sources, and architects and creators. Fields and some values were revised, reducing the attribute count from 169 to 151.                                                                                                                                                                                                                                | [第二版脚本 / Second script](prompts/round2/output_round2.md) · [第二版数据 / Second data](prompts/round2/output_round2.jsonl)：30实体、151项属性 / 30 entities, 151 attributes |
| **第三轮**<br>Round 3 | [指令4](prompts/4_shared_place_pool.md)。<br>[Prompt 4](prompts/4_shared_place_pool.md).                                                                                 | 统一地名池并更新相关名称。现居城市由脚本按固定规则从地名池填入，活动主办方由代码组合地名和机构名称。[地名方法](place_names/README.md)。<br>The place-name pool was unified and related names updated. The script fills cities of residence from the pool using a fixed rule, and code combines place names and institution names for event organizers. [Place-name method](place_names/README.md). | [第三轮脚本与数据 / Round 3 scripts and data](prompts/round3/README.md)                                                                                                |

<details>
<summary>WFW参考材料读取明细 / WFW reference files read</summary>

模型读过的英文实体示例中，有14个生日值也出现在中文 pilot 数据中。

Fourteen birth-date values from the English entity examples also appear in the Chinese pilot data.

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
