# 指令4：统一地名池并更新数据 / Instruction 4: unify the place-name pool and update the data

## 中文整理版 / Chinese reconstructed version

```text
请将现有数据中的地名统一到一个共用的虚构地名池，并更新实体和信源文件。

1. 地名池：沿用前面基于真实县市地名用字统计、组合和查重的方法，整理出20个两字虚构地名。
   名称应适合县市语境；20个名称的40个汉字不重复，并完成行政区划表和中文维基查重。

2. 分配方式：政府和报纸从同一份有序地名池交错取名。前10个地名中，第1、3、5、7、9个
   用于政府，第2、4、6、8、10个用于报纸；后10个用于实体名称和地点属性。
   这样既共用一套地名生成方法，也使实体用地名与信源用地名不重叠。

3. 更新数据：将分配后的地名用于政府、报纸名称，以及实体名称和地点属性中相应的位置，
   保持同一地名在各文件中的使用一致。

请输出：
- 共用地名池及政府、报纸、实体三组的分配结果；
- 更新后的entities_zh.jsonl和sources_zh.json。

```

## English translation

```text
Unify the place names in the existing data through one shared fictional place-name pool,
and update the entity and source files.

1. Pool: use the earlier method of character-frequency analysis of real county and city names,
   combination, and duplicate checks to compile 20 fictional two-character place names.
   The names should suit a county or city context. Use 40 distinct characters across the
   20 names, and check them against the administrative-division list and Chinese Wikipedia.

2. Allocation: assign names to government and newspaper sources alternately from the same
   ordered pool. Among the first 10 names, use positions 1, 3, 5, 7, and 9 for government
   sources, and positions 2, 4, 6, 8, and 10 for newspapers. Reserve the remaining 10 names
   for entity names and location attributes. This shares one name-generation method while
   keeping entity place names separate from source place names. 

3. Update the data: apply the allocated names to government and newspaper names and to
   the relevant entity names and location attributes. Keep place-name usage consistent
   across the files.

Output:
- The shared place-name pool and its allocation to government, newspapers, and entities;
- The updated entities_zh.jsonl and sources_zh.json.

```

<details>
<summary>Original wording (verbatim from the session log, Chinese)</summary>

```
1.我觉得这一波地名没有上一波好。；2.地名池要共用，不要按信源类型分开。现在政府和报纸用的是不同的地名，
其中报纸有三个带溪、政府有两个带源，地名用字的差异会混进信源类型的对比里。
WFW用的是同一个地名池填所有信源模板（source_generator.py 里报纸和政府
都从NeoQA的locations抽），照这个改。

改完可以往下做prompt构造。
```

</details>
