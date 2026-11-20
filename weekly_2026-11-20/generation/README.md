# 数据生成过程 / How the data was generated

- **数据 / Data:** 70实体、380属性，每项原值＋四备选。 / 70 entities, 380 attributes, one original and four alternatives each.
- **模型 / Model:** `gpt-6.1-sol`.
- **贯穿例子 / Worked example:** 《双陵晨光图》 / Morning Light in Shuangling.

## ① 准备输入 / Prepare inputs

- 确定实体、字段、作品类型和可用姓名。 / Specify the entity, fields, artwork type and available names.

<details>
<summary>实际输入与姓名名单 / Actual input and candidate names</summary>

```json
{
  "date": "2026-11-18",
  "id": "ART-01",
  "name": "《双陵晨光图》",
  "fixed_art_type": "架上绘画",
  "creator_candidates": [
    "林逢江",
    "梁江文",
    "汪仁维",
    "曹峰彦",
    "陈竹才"
  ],
  "entity_class": "art",
  "creator_rule": "属性姓名池后50名分为十组，每组首名作原值、另四名作备选；与建筑前50名不重叠。",
  "fixed_creator": "林逢江",
  "type_definition": "架上绘画或人物雕塑；类型为固定背景，在组装表中显示，不作为冲突属性。",
  "dimensions": "作品本体高度、宽度，不含画框或雕塑底座。",
  "previous_same_type_originals": [],
  "references": []
}
```

</details>

↓

## ② 生成原值表 / Generate the original table

- 用`gpt-6.1-sol`生成完整原值表。 / Generate the complete original table using `gpt-6.1-sol`.

<details>
<summary>生成原值：实际中文prompt / Original-table task prompt</summary>

```text
你正在为中文知识冲突实验生成一个虚构的艺术作品实体原值表，暂不生成备选。
实际输入：
{
  "date": "2026-11-18",
  "id": "ART-01",
  "name": "《双陵晨光图》",
  "fixed_art_type": "架上绘画",
  "creator_candidates": [
    "林逢江",
    "梁江文",
    "汪仁维",
    "曹峰彦",
    "陈竹才"
  ],
  "entity_class": "art",
  "creator_rule": "属性姓名池后50名分为十组，每组首名作原值、另四名作备选；与建筑前50名不重叠。",
  "fixed_creator": "林逢江",
  "type_definition": "架上绘画或人物雕塑；类型为固定背景，在组装表中显示，不作为冲突属性。",
  "dimensions": "作品本体高度、宽度，不含画框或雕塑底座。",
  "previous_same_type_originals": [],
  "references": []
}

填写字段：创作者、创作年份、高度、宽度、材料。每项只给一个值，属性值均为字符串。
使用中文、中文日期和公制单位，字段名及取值自然、直白；日期不晚于输入的生成日。
相关属性须同时考虑，整表搭配合理；与此前同类原值保持合理差异。姓名、地名只用提供的池；不按名字猜性别。
不要声称已查网页、外部查重或取得人工认可；无法合理填写时具体报告问题。
固定输入的作品类型，不将它作为冲突字段。创作者仅取属性姓名池。高度、宽度指作品本体，单位厘米，材料符合该作品类型。题名不直接提示材料和创作者。
只输出一个JSON对象，含id、name、entity_class及全部测试字段；人物另含固定性别，艺术作品另含description说明固定作品类型。
```

</details>

<details>
<summary>生成原值：原始输出 / Raw original-table output</summary>

```json
{"id":"ART-01","name":"《双陵晨光图》","entity_class":"art","description":"架上绘画","创作者":"林逢江","创作年份":"2017年","高度":"85厘米","宽度":"115厘米","材料":"布面油彩"}
```

</details>

↓

## ③ 补四个备选 / Add four alternatives

- **模型 / Model:** 根据完整原表生成材料备选。 / Generate material alternatives from the complete original table.
- **脚本 / Script:** 生成年份与尺寸备选，从预先分配名单取创作者。 / Generate year and dimension alternatives; take creators from the preassigned list.

<details>
<summary>材料备选：实际中文prompt / Material-alternative task prompt</summary>

```text
给定虚构实体的完整原值表：
{
  "id": "ART-01",
  "name": "《双陵晨光图》",
  "entity_class": "art",
  "description": "架上绘画",
  "创作者": "林逢江",
  "创作年份": "2017年",
  "高度": "85厘米",
  "宽度": "115厘米",
  "材料": "布面油彩"
}

为目标属性材料生成四个不同备选，不重复原值；每个备选单独替换入原表，其余字段保持原值时仍应合理。
使用自然、直白的中文，与原值单位和含义一致；只输出四个字符串的JSON数组。
作品类型固定为架上绘画；尺寸是作品本体，不含框或底座。四种材料各自替换后应仍与类型、题名和本体尺寸相容；绘画材料可包含载体与颜料，不以仅调整词序制造差异。
```

</details>

<details>
<summary>材料备选：原始输出 / Raw material alternatives</summary>

```json
[
  "布面丙烯",
  "纸本水彩",
  "纸本水粉",
  "纸本水墨"
]
```

</details>

<details>
<summary>数值、日期与名单：实际参数 / Actual numeric, date and name-selection parameters</summary>

```json
{
  "date": "2026-11-18T14:13:13.434524+01:00",
  "actor": "Codex",
  "step": "rule_inputs_saved_before_generation",
  "script_sha256": "9177e80301d0883963b70d1d761f4e88b43c611d27942a3cba0d05f55ebd3a89",
  "original": {
    "id": "ART-01",
    "name": "《双陵晨光图》",
    "entity_class": "art",
    "description": "架上绘画",
    "创作者": "林逢江",
    "创作年份": "2017年",
    "高度": "85厘米",
    "宽度": "115厘米",
    "材料": "布面油彩"
  },
  "original_sha256": "f502d5803dc6099fea7d4234601325331fb57cd4d6d2e81ea83f8f49d03ea202",
  "material_sha256": "931d370b564bfcfa8ebaa5324a9a6e6dd577c0e6bbd8d98480ea06eaf36a2ae2",
  "creator_candidates": [
    "林逢江",
    "梁江文",
    "汪仁维",
    "曹峰彦",
    "陈竹才"
  ],
  "year_offsets": [
    -2,
    -1,
    1,
    2
  ],
  "numeric_percent": 5,
  "numeric_precision": "整数厘米，两低两高",
  "row_order_seed": "42:ART-01",
  "fixed_type_rendering": "description保留，同时复制为标量作品类型以显示在两张表；不改类型、不作冲突属性。"
}
```

</details>

<details>
<summary>备选生成与组装：实际脚本 / Actual alternative-generation and assembly script</summary>

```python
"""按预存规则补艺术备选，并将固定作品类型显示为背景行。"""
import hashlib,json,math,re,sys
from datetime import datetime
from decimal import Decimal,ROUND_FLOOR
from pathlib import Path
from prepare_person import BASE,read,save_new
sys.path.insert(0,str(BASE.parents[1]))
from data_review.validate_entity_batch import check
from prompt_zh import create_entity_table,make_row_order
from run_baseline import build_records

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dimensions(value):
    n=Decimal(value.removesuffix('厘米'));maximum=int((n*Decimal('.05')).to_integral_value(rounding=ROUND_FLOOR));assert maximum>=2
    offsets=[-maximum,-math.ceil(maximum/2),math.ceil(maximum/2),maximum]
    return [value,*[f'{n+k:.0f}厘米' for k in offsets]],{'offsets_cm':offsets,'actual_maximum_percent':str(max(Decimal(abs(k))/n*100 for k in offsets)),'precision_exception':False}

fields=read(BASE/'fields.json')['art'];config=read(BASE/'art.input.json');script_hash=sha(Path(__file__));rows=[];originals=[]
for identity in config['identities']:
    folder=BASE/'entities'/identity['id'];raw=read(folder/'original.raw.json');saved=read(folder/'03_material_input.execution_record.json')
    assert read(folder/'original.input.json')['previous_same_type_originals']==originals
    assert sha(folder/'original.raw.json')==saved['original_sha256']
    materials=read(folder/'alternatives.material.raw.json')
    save_new(folder/'05_rule_inputs.execution_record.json',{'date':datetime.now().astimezone().isoformat(),'actor':'Codex','step':'rule_inputs_saved_before_generation','script_sha256':script_hash,'original':raw,'original_sha256':sha(folder/'original.raw.json'),'material_sha256':sha(folder/'alternatives.material.raw.json'),'creator_candidates':identity['creator_candidates'],'year_offsets':[-2,-1,1,2],'numeric_percent':5,'numeric_precision':'整数厘米，两低两高','row_order_seed':f"42:{raw['id']}",'fixed_type_rendering':'description保留，同时复制为标量作品类型以显示在两张表；不改类型、不作冲突属性。'})
    entity={k:v for k,v in raw.items() if k not in fields};entity['作品类型']=raw['description']
    entity['创作者']=identity['creator_candidates'];assert entity['创作者'][0]==raw['创作者']
    year=int(raw['创作年份'].removesuffix('年'));assert year+2<=2026
    entity['创作年份']=[raw['创作年份'],*[f'{year+k}年' for k in [-2,-1,1,2]]]
    entity['材料']=[raw['材料'],*materials];steps=[]
    for field in ['高度','宽度']:
        entity[field],detail=dimensions(raw[field]);steps.append({'field':field,**detail})
    entity['row_order']=make_row_order(entity)
    assert all(len(entity[f])==len(set(entity[f]))==5 and entity[f][0]==raw[f] for f in fields)
    assert sha(folder/'original.raw.json')==saved['original_sha256']
    save_new(folder/'entity.pending_review.json',entity)
    save_new(folder/'06_assembly.execution_record.json',{'date':datetime.now().astimezone().isoformat(),'actor':'Codex','script_sha256':script_hash,'steps':steps,'creator_rule':'预分配五名，首名原值，后四名备选','year_offsets':[-2,-1,1,2],'fixed_type':raw['description'],'derived_field':'作品类型由description复制，用于两表显示','checks':{'five_distinct':True,'raw_originals_unchanged':True,'type_unchanged':True,'all_attributes_original_values_unchanged':True},'user_review':'候选待审','output':'entity.pending_review.json'})
    rows.append(entity);originals.append(raw)
validation=check(rows,require_row_order=True,per_type={'art':10});assert not validation['errors'],validation
records=build_records(rows,(1,2,3,4));assert len(records)==400
for i in range(0,len(records),2):
    a,b=records[i:i+2];assert (a['value_a'],a['value_b'])==(b['value_b'],b['value_a'])
    assert a['field']!='作品类型' and b['field']!='作品类型'
for entity in rows:
    for field in fields:
        a=create_entity_table(entity,field,entity[field][0])
        for alt in entity[field][1:]:
            b=create_entity_table(entity,field,alt);assert [k for k in a if a[k]!=b[k]]==[field]
            assert a['作品类型']==b['作品类型']==entity['description']
creators=[v for e in rows for v in e['创作者']];assert len(set(creators))==50
buildings=[json.loads(s) for s in (BASE/'building.entities.pending_review.jsonl').read_text().splitlines()]
assert not set(creators)&{v for e in buildings for v in e['设计师']}
for filename,data in [('art.entities.pending_review.jsonl',rows),('art.originals.pending_review.jsonl',originals),('art.baseline_prompt_preview.jsonl',records)]:
    with (BASE/filename).open('x') as f:f.write(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in data))
save_new(BASE/'20_art_complete.execution_record.json',{'date':datetime.now().astimezone().isoformat(),'actor':'Codex','script_sha256':script_hash,'validation':validation,'data_sha256':sha(BASE/'art.entities.pending_review.jsonl'),'precision_exceptions':[],'checks':{'prior_inputs_match_raw_outputs':True,'raw_originals_unchanged':True,'fixed_type_displayed_in_both_tables':True,'type_not_tested_as_conflict':True,'only_one_attribute_differs':True,'both_orders_reverse_values':True,'100_building_and_art_names_unique':True,'400_prompts_previewed':True},'generation_boundary':'原值和材料备选由当前会话撰写，模型版本参数不可见；创作者按已准备名单，年份尺寸由脚本生成。','model_inference_run':False,'user_review':'候选待审'})
print(json.dumps({'entities':10,'validation':validation,'type_fixed_and_visible':True,'precision_exceptions':0},ensure_ascii=False))
```

</details>

↓

## ④ 组装与检查 / Assemble and check

- 每题只改一个属性，组装两种表序；检查五值互异、原值保留和单属性差异。 / Change one attribute per question, build both table orders, and check distinct values, preserved originals and single-attribute differences.

<details>
<summary>脚本处理：原始记录 / Original assembly record</summary>

```json
{
  "date": "2026-11-18T14:13:13.436366+01:00",
  "actor": "Codex",
  "script_sha256": "9177e80301d0883963b70d1d761f4e88b43c611d27942a3cba0d05f55ebd3a89",
  "steps": [
    {
      "field": "高度",
      "offsets_cm": [
        -4,
        -2,
        2,
        4
      ],
      "actual_maximum_percent": "4.705882352941176470588235294",
      "precision_exception": false
    },
    {
      "field": "宽度",
      "offsets_cm": [
        -5,
        -3,
        3,
        5
      ],
      "actual_maximum_percent": "4.347826086956521739130434783",
      "precision_exception": false
    }
  ],
  "creator_rule": "预分配五名，首名原值，后四名备选",
  "year_offsets": [
    -2,
    -1,
    1,
    2
  ],
  "fixed_type": "架上绘画",
  "derived_field": "作品类型由description复制，用于两表显示",
  "checks": {
    "five_distinct": true,
    "raw_originals_unchanged": true,
    "type_unchanged": true,
    "all_attributes_original_values_unchanged": true
  },
  "user_review": "候选待审",
  "output": "entity.pending_review.json"
}
```

</details>

<details>
<summary>整批艺术数据：检查结果 / Checks for the artwork batch</summary>

```json
{
  "date": "2026-11-18T14:13:13.484599+01:00",
  "actor": "Codex",
  "script_sha256": "9177e80301d0883963b70d1d761f4e88b43c611d27942a3cba0d05f55ebd3a89",
  "validation": {
    "entities": 10,
    "by_class": {
      "art": 10
    },
    "instances": 50,
    "pairs": 200,
    "items": 400,
    "spread": [
      [
        "较大数值·宽度",
        20,
        20
      ],
      [
        "较大数值·高度",
        20,
        20
      ]
    ],
    "errors": [],
    "review": []
  },
  "data_sha256": "d4dd8eac03acdcddf27e485b265659512c974e9f4af2fe9d0060092a23c19b49",
  "precision_exceptions": [],
  "checks": {
    "prior_inputs_match_raw_outputs": true,
    "raw_originals_unchanged": true,
    "fixed_type_displayed_in_both_tables": true,
    "type_not_tested_as_conflict": true,
    "only_one_attribute_differs": true,
    "both_orders_reverse_values": true,
    "100_building_and_art_names_unique": true,
    "400_prompts_previewed": true
  },
  "generation_boundary": "原值和材料备选由当前会话撰写，模型版本参数不可见；创作者按已准备名单，年份尺寸由脚本生成。",
  "model_inference_run": false,
  "user_review": "候选待审"
}
```

</details>

↓

## ⑤ 修改、定稿 / Revise and finalise

- 按检查和反馈修改，另存新版本；本例25个取值在最终版中保留。 / Revise following checks and feedback, saving a new version. All 25 values in this example are retained in the final version.

| 属性 / Attribute | 原值 / Original | 四个备选 / Four alternatives | 产生方式 / Method |
|---|---|---|---|
| 材料<br>Material | 布面油彩<br>Oil on canvas | 布面丙烯、纸本水彩、纸本水粉、纸本水墨<br>Acrylic on canvas; Watercolour on paper; Gouache on paper; Ink on paper | 模型生成<br>Model-generated |
| 创作年份<br>Year of creation | 2017年<br>2017 | 2015年、2016年、2018年、2019年<br>2015; 2016; 2018; 2019 | 脚本生成<br>Script-generated |
| 高度<br>Height | 85厘米<br>85 cm | 81厘米、83厘米、87厘米、89厘米<br>81 cm; 83 cm; 87 cm; 89 cm | 脚本生成<br>Script-generated |
| 宽度<br>Width | 115厘米<br>115 cm | 110厘米、112厘米、118厘米、120厘米<br>110 cm; 112 cm; 118 cm; 120 cm | 脚本生成<br>Script-generated |
| 创作者<br>Creator | 林逢江<br>Lin Fengjiang | 梁江文、汪仁维、曹峰彦、陈竹才<br>Liang Jiangwen; Wang Renwei; Cao Fengyan; Chen Zhucai | 从预先分配名单中取值<br>Taken from a preassigned list |

<details>
<summary>本例：组装输出与定稿数据对照 / This example: assembled and final data</summary>

```json
{
  "id": "ART-01",
  "name": "《双陵晨光图》",
  "entity_class": "art",
  "description": "架上绘画",
  "作品类型": "架上绘画",
  "创作者": [
    "林逢江",
    "梁江文",
    "汪仁维",
    "曹峰彦",
    "陈竹才"
  ],
  "创作年份": [
    "2017年",
    "2015年",
    "2016年",
    "2018年",
    "2019年"
  ],
  "材料": [
    "布面油彩",
    "布面丙烯",
    "纸本水彩",
    "纸本水粉",
    "纸本水墨"
  ],
  "高度": [
    "85厘米",
    "81厘米",
    "83厘米",
    "87厘米",
    "89厘米"
  ],
  "宽度": [
    "115厘米",
    "110厘米",
    "112厘米",
    "118厘米",
    "120厘米"
  ],
  "row_order": [
    "宽度",
    "高度",
    "作品类型",
    "创作年份",
    "创作者",
    "材料"
  ]
}
```


**定稿 / Final:**

```json
{
  "id": "ART-01",
  "name": "《双陵晨光图》",
  "entity_class": "art",
  "description": "架上绘画",
  "作品类型": "架上绘画",
  "创作者": [
    "林逢江",
    "梁江文",
    "汪仁维",
    "曹峰彦",
    "陈竹才"
  ],
  "创作年份": [
    "2017年",
    "2015年",
    "2016年",
    "2018年",
    "2019年"
  ],
  "材料": [
    "布面油彩",
    "布面丙烯",
    "纸本水彩",
    "纸本水粉",
    "纸本水墨"
  ],
  "高度": [
    "85厘米",
    "81厘米",
    "83厘米",
    "87厘米",
    "89厘米"
  ],
  "宽度": [
    "115厘米",
    "110厘米",
    "112厘米",
    "118厘米",
    "120厘米"
  ],
  "row_order": [
    "宽度",
    "高度",
    "作品类型",
    "创作年份",
    "创作者",
    "材料"
  ]
}
```

</details>

