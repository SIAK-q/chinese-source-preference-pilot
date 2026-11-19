# 本批数据的生成过程

- **定稿更新（11-18）**：原批次生成后，按用户决定仅删除人物“籍贯”；其他属性不重生成。当前final70_20261118_v2为70实体、人物8项、3040题／模型；下文保留当时生成过程。
- **当前**：新批次七类各10，共70个候选；每项原值＋四备选；11-18用户确认70实体定稿，活动主办方及3个月保修保留；完整baseline未跑。
- **本页怎么读**：先看步骤，再展开《双陵晨光图》的真实prompt、输出和脚本处理；下面用的是已经保存的记录。
- **生成方式**：Codex在当前会话读已存任务prompt后撰写输出；任务prompt不是完整聊天上下文，具体模型版本与参数不可见。

- **1．定规则**：确定七类、39种属性、姓名地名池及备选规则。艺术类型沿用准备设定；创作者姓名先分配，不让模型另起姓名。
- **2．写模板**：Codex按规程编写各类原值模板；产品使用已审模板，其他模板不记为用户逐句审核通过。11-16保存冻结记录。
- **3．填实际输入**：逐实体填名称、固定背景、候选名单和此前同类原值；先存input和prompt，再生成该实体原值。
- **4．生成原值**：当前会话生成完整表；固定提供的姓名、性别或作品类型沿用输入，其余内容同时考虑整表搭配。保存raw后再处理下个实体。
- **5．补四备选**：文本内容带完整原表生成；名单、日期、数值等由脚本按规则补齐。每项实验只替换一个属性。
- **6．检查**：检查五值互异、单位、范围、行序、单属性差异和双表顺序；格式检查不算用户审核，也不证明等可信。
- **7．处理修改**：另存新版及修改前后、原因、谁作决定。机构规模、活动删“周”、制造商及保修措辞修改均保留旧版。
- **8．交付**：说明与Obsidian同步后按类给用户看；CURRENT_DATA.json指向当前各组件及70个合并候选。

| 内容 | 实际怎样得到 |
|---|---|
| 各类原值 | 当前会话按保存的任务prompt生成，固定名单与背景沿用输入 |
| 人物职业＋学历、身高＋体重备选 | 两组成对生成；实验仍只改一个属性 |
| 行业、建筑/艺术材料、活动主办方、产品制造商备选 | 读完整原表后，当前会话撰写四个备选 |
| 创作者、设计师及城市等 | 从已准备名单按保存的规则分配或抽取 |
| 日期、数值、保修月数等 | 脚本按已定区间、幅度或档位生成 |

<details>
<summary>真实样例①：生成前保存的原值prompt（原文）</summary>

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
<summary>真实样例②：当前会话随后写出的原始输出（原文）</summary>

```json
{"id":"ART-01","name":"《双陵晨光图》","entity_class":"art","description":"架上绘画","创作者":"林逢江","创作年份":"2017年","高度":"85厘米","宽度":"115厘米","材料":"布面油彩"}
```

</details>

<details>
<summary>真实样例③：材料备选的实际prompt和原始输出</summary>

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

```json
[
  "布面丙烯",
  "纸本水彩",
  "纸本水粉",
  "纸本水墨"
]
```

</details>

- **样例中脚本补的部分**：创作者用预分配五人；年份取−2、−1、+1、+2年；85厘米高度取81、83、87、89厘米；115厘米宽度取110、112、118、120厘米。
- **固定背景处理**：把description中的“架上绘画”复制成可显示的“作品类型”行；不作为冲突属性。

| 属性 | 原值 | 备选1 | 备选2 | 备选3 | 备选4 |
|---|---|---|---|---|---|
| 创作者 | 林逢江 | 梁江文 | 汪仁维 | 曹峰彦 | 陈竹才 |
| 创作年份 | 2017年 | 2015年 | 2016年 | 2018年 | 2019年 |
| 高度 | 85厘米 | 81厘米 | 83厘米 | 87厘米 | 89厘米 |
| 宽度 | 115厘米 | 110厘米 | 112厘米 | 118厘米 | 120厘米 |
| 材料 | 布面油彩 | 布面丙烯 | 纸本水彩 | 纸本水粉 | 纸本水墨 |

<details>
<summary>真实样例④：脚本执行前的输入与执行后记录（原文）</summary>

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
<summary>真实修改样例：保修措辞的决定与前后对照</summary>

- **用户要求**：保修值直接写“N个月”；prompt不额外定义“均指整机保修”。
- **实际修改**：50个值删除固定前缀，月数不变；这不是重生成。

```json
{
  "date": "2026-11-18T14:08:37.077820+01:00",
  "actor": "用户决定；Codex执行",
  "user_messages": [
    "提问，保修期为什么一定要强调整机保修，直接写xx个月不可以。？",
    "[prompt注明“均指整机保修”。]会否有些咬文嚼字",
    "好的继续"
  ],
  "decision": "属性保修期保留，所有取值仅写N个月；prompt只说改变保修月数，不添加配件或其他条件，不追加均指整机的定义。",
  "scope": "仅删除10产品50个保修取值的固定前缀整机保修；月数、档位、其他字段、行序均不变。两项3个月的相容性标记仍未处理。",
  "input": "product.entities.pending_review.jsonl",
  "input_sha256": "93844b4b5729040e3b8d245cc3f331116d9d08febd9ddd7a3e3bf8048e11cfac",
  "templates": {
    "original": {
      "source": "templates/product.original.txt",
      "source_sha256": "ffc7acc690458488da332aa7e9c19527023c8f5494a5035733d007277b458179",
      "new": "product_warranty_wording_20261118/templates/product.original.txt",
      "new_sha256": "6d8e2dbe92206fe59f3fc3108b261d7905657f88a042ee30860b81a0be55d13a",
      "wording_changed": true
    },
    "alternatives": {
      "source": "templates/product.alternatives.txt",
      "source_sha256": "64a6b4025f666bc10970b4ddf74c4ac8450f8098795748c706dd1929b83398f8",
      "new": "product_warranty_wording_20261118/templates/product.alternatives.txt",
      "new_sha256": "7175830a8abf717dc27e5fe67a515f9e221f26f0a30457535d87d40066aad667",
      "wording_changed": true
    },
    "revision": {
      "source": "templates/product.revision.txt",
      "source_sha256": "398af273b6142e22b0751bdef50468c56b7f74b5d267493bb9039148657b8668",
      "new": "product_warranty_wording_20261118/templates/product.revision.txt",
      "new_sha256": "398af273b6142e22b0751bdef50468c56b7f74b5d267493bb9039148657b8668",
      "wording_changed": false
    }
  },
  "method": "格式转换脚本；不调用模型、不重新生成属性值。"
}
```

| 产品 | 位置 | 修改前 | 修改后 |
|---|---|---|---|
| PRODUCT-01 | 原值 | 整机保修24个月 | 24个月 |
| PRODUCT-01 | 备选1 | 整机保修12个月 | 12个月 |
| PRODUCT-01 | 备选2 | 整机保修18个月 | 18个月 |
| PRODUCT-01 | 备选3 | 整机保修36个月 | 36个月 |
| PRODUCT-01 | 备选4 | 整机保修48个月 | 48个月 |

</details>

- **全批记录位置**：`pilot/data_generation/new_batch_20261116_v2/`；各实体过程在`entities/实体ID/`，当前版本以`CURRENT_DATA.json`为准。
- **这次只展示过程**：没有改实体数据，没有重新调用模型，也没有跑baseline。
