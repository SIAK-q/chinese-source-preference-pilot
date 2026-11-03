# 中文pilot数据生成 / Chinese pilot data generation

本目录记录中文pilot数据的生成与修订，包括生成要求、模型输入、各版输出和修改指令。最终数据包含7类虚构实体，共30个实体、151项测试属性和20个信源。每项测试属性由1个原值和4个备选组成。

## 生成方法

数据结构参照WFW，实体名称、信源名称及属性取值按中文语境构造。模型先读取WFW的字段、示例和代码，随后在同一会话中生成并检查中文姓名、地名，再编写生成脚本。原值与备选写在同一份脚本中；现居城市等少量取值由代码从地名池按固定顺序填入。后续修订以前一轮脚本和数据为上下文。

## 生成与修订过程

| 阶段 | 主要工作 | 指令与产出 |
|---|---|---|
| 第一轮：生成初稿 | 建立中文实体与属性取值，生成并检查姓名、地名。 | [造名要求](2_place_names.md)；[第一版输出](output_round1.md)和[实体数据](output_round1.jsonl)，共30实体、169项属性。 |
| 第二轮：修改数据 | 修订机构和产品名称，删除总部所在地、制造商、国籍和所属国家属性，地点增加下辖乡镇数；调整为县市级地名，并分开不同用途的姓名池；部分取值也作了修订，如所属行业、员工人数、年营业额、主体结构和持续时间。 | [修改要求](3_corrections.md)；[第二版输出](output_round2.md)和[实体数据](output_round2.jsonl)，共30实体、151项属性。 |
| 第三轮：统一地名池 | 政府、报纸和实体共用一套虚构地名池，并更新数据中的地名。 | [地名池修改要求](4_shared_place_pool.md)；最终[实体数据](../../entities_zh.jsonl)和[信源名称](../../sources_zh.json)。 |

## 项目文件

| 文件 | 内容 |
|---|---|
| [生成指令](1_task.md) | 根据最终数据整理的生成要求，汇总实体结构、属性取值和命名方法。 |
| [数据中英对照表](../../conflict_pairs.md) | 最终数据的原值与备选，附英文释义。 |
| [地名生成记录](../place_names/README.md) | 虚构地名的构造、检查、最终名单及使用方式。 |

<details>
<summary>English version / 英文对照</summary>

This folder documents the generation and revision of the Chinese pilot data, including generation requirements, model inputs, versioned outputs and revision instructions. The final data contains 30 fictional entities across seven types, 151 test attributes and 20 sources. Each test attribute contains one original value and four alternatives.

### Generation method

The data follows WFW's structure, with entity names, source names and attribute values constructed for the Chinese setting. The model first read WFW fields, examples and code, then generated and checked Chinese person and place names in the same session before writing generation scripts. Originals and alternatives were written into the same script; a few values, such as cities of residence, were filled in by code in a fixed order from the place-name pool. Subsequent revisions used the preceding script and data as context.

### Generation and revision

| Stage | Work completed | Instructions and outputs |
|---|---|---|
| Round 1: first draft | Build Chinese entities and attribute values; generate and check person and place names. | [Naming requirements](2_place_names.md); [first output](output_round1.md) and [entity data](output_round1.jsonl), containing 30 entities and 169 attributes. |
| Round 2: revise the data | Revise organization and product names; remove headquarters, manufacturer, nationality and country attributes, and add the number of subordinate towns/townships for locations; adopt county/city-level place names and separate person-name pools by use; some values were also revised, e.g. industry, employee count, annual revenue, structural system and duration. | [Revision instructions](3_corrections.md); [second output](output_round2.md) and [entity data](output_round2.jsonl), containing 30 entities and 151 attributes. |
| Round 3: unify the place-name pool | Use a shared fictional place-name pool for government sources, newspapers and entities, updating place names in the data. | [Place-pool revision](4_shared_place_pool.md); final [entities](../../entities_zh.jsonl) and [source names](../../sources_zh.json). |

### Project files

| File | Content |
|---|---|
| [Generation instruction](1_task.md) | Requirements reconstructed from the final data, bringing together entity structure, attribute values and naming methods. |
| [Chinese–English data table](../../conflict_pairs.md) | Original values and alternatives in the final data, with English glosses. |
| [Place-name generation record](../place_names/README.md) | Construction, checks, final list and use of the fictional place names. |

</details>

<details>
<summary>输入材料与输出文件 / Inputs and output files</summary>

### 输入材料 / Input materials

初轮读取了英文实体文件的开头3,000字节，并统计实体类别及字段。中文姓名和地名随后在同一会话中生成、检查；模型将中文原值与备选写入生成脚本，后续轮次沿用已有脚本和结果。

The first round read the opening 3,000 bytes of the English entity file and counted entity classes and fields. Chinese person and place names were then generated and checked in the same session. The model wrote Chinese originals and alternatives into generation scripts, using the existing scripts and results in subsequent rounds.

### 输出文件与整理 / Output files and preparation

[首轮输出](output_round1.md)和[第二轮输出](output_round2.md)保存模型写出的脚本原文。两份JSONL实体导出由保存的历史脚本恢复，其中首轮导出包含同轮的名称修正。最终数据使用库中已有的实体和信源文件。早期各轮信源文件未单独留存。

The [first output](output_round1.md) and [second output](output_round2.md) preserve the scripts written by the model. The two JSONL entity exports were recovered from the saved historical scripts; the first includes a recorded name correction from the same round. The final data uses the entity and source files already in the repository. Earlier source-file versions were not saved separately.

[指令1](1_task.md)按最终采用的数据和方法回顾整理，尚未重新运行。

[Instruction 1](1_task.md) was retrospectively reconstructed from the adopted data and methods and has not been rerun.

</details>
