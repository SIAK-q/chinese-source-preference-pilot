# 中文虚构地名 / Invented Chinese place names

本次pilot使用一个包含20个虚构两字地名的地名池。这些名字由真实县、市级地名中的常用字组合而成，经过真实名称查重，并确保最终池中的汉字不重复。政府信源、报纸和实体分别使用池中的不同部分。

The pilot uses a pool of 20 invented two-character place names. They were constructed from characters frequent in real county- and city-level names, checked against real names, and selected so that no character occurs twice in the final pool. Government sources, newspapers and entities use separate parts of this pool.

## 最终采用的地名 / Final names

| 用途 / Use | 地名 / Names |
|---|---|
| 政府信源 / Government sources | 广城 永江 平宁 兴川 金丰 |
| 报纸 / Newspapers | 临阳 青安 武河 天昌 宜湖 |
| 实体 / Entities | 双陵 上泉 白原 龙泽 乐水 通溪 清山 新定 长源 惠明 |

最终地名保存在[`places_zh.py`](places_zh.py)。政府和报纸交错使用前10个地名，实体使用后10个。交错取用是本次pilot采用的分配方式。

The final file is [`places_zh.py`](places_zh.py). Government and newspaper names were taken alternately from the first ten entries; entities use the last ten. Alternating the entries is the arrangement used in this pilot.

信源和实体分别使用不同的子集，以避免信源标签中的地名与实体名称或属性值中的地名重合。

The source and entity subsets are kept separate to avoid place-name overlap between source labels and entity names or attribute values.

## 最终地名池怎样生成 / How the final pool was made

以下是收到[指令4](../prompts/4_shared_place_pool.md)之后，第三轮生成最终地名池的做法；`records/round3/`保存的就是这一轮的代码。前两轮的地名见下文“此前的修改”，代码未收入。

The steps below were carried out in round 3, after [Instruction 4](../prompts/4_shared_place_pool.md); `records/round3/` holds the code of this round. The earlier rounds are summarised under “Earlier revisions”; their code is not included.

1. **以真实县、市名称为基础。** 使用[中国行政区划数据](https://github.com/modood/Administrative-divisions-of-China)，去掉行政区划后缀后，得到2,529条两字地名词干。

    **Start from real county and city names.** An administrative-division list from [modood/Administrative-divisions-of-China](https://github.com/modood/Administrative-divisions-of-China) supplied 2,529 two-character name stems after administrative endings were removed.

2. **组合候选并排序。** 分别取第一、第二个位置上出现频率最高的50个字，交叉组合。排除两个字相同的组合，以及与行政区划表中的名称（包括乡镇、街道）或所列省级名称重合的组合，剩下1,402个候选。按两个字在各自位置上的出现次数之和排序。

    **Construct and rank candidates.** The 50 most frequent characters at each position were combined. Identical-character pairs and names matching the administrative-division list (including townships and streets) or the listed province names were excluded, leaving 1,402 candidates. Candidates were ranked by the sum of the two characters' frequencies at their respective positions.

3. **增加用字多样性。** 代码选择名字时，不重复使用其他已选名字中的字；排除两个方位字相连、含“市”字的组合，并应用模型指定的排除词表。这一步得到36个候选。

    **Make the selection more varied.** Code selected names without reusing a character across names, excluded pairs of direction characters and names containing 市, and applied a model-specified exclusion list. This produced 36 candidates.

4. **选定最终20个名字。** 模型从上述候选中挑选，并从排序后的候选池中补充名字，调用维基检查程序，替换已有词条的名称。当时最后一次检查中，选定的20个名字均未查到中文维基页面；这20个名字共使用40个不同的汉字。

    **Select the final 20.** The model selected names from these candidates, supplemented them from the ranked pool, and used the Wikipedia checker to replace names with an existing page. The final recorded check found no Chinese Wikipedia page for the 20 selected names; the pool contains 40 different characters.

我也检查了这些名字的读音和自然度，判断它们是否像中文县、市级地名。

I also reviewed the names for pronounceability and whether they sounded like plausible Chinese county or city names.

候选的组合和筛选由代码完成；排除词表的指定及最终名单的选择由模型完成。

The code constructed and filtered the candidates. The model specified the exclusion list and made the final selection.

## 此前的修改 / Earlier revisions

第一版使用三字地名，但这些名字并不自然。下一版改用县、市地名的字频，但分别选出的政府和报纸名单中，不同的字各自集中重复出现。最终版保留县、市级地名作为基础，改为使用一个汉字不重复的共同地名池。对应的修改要求见[指令1](../prompts/1_place_names.md)、[3](../prompts/3_corrections.md)、[4](../prompts/4_shared_place_pool.md)。

The first version used three-character names, but these names did not sound natural. The next version used county/city character frequencies, but the separately selected government and newspaper lists repeated different characters. The final version kept the county/city basis and used one pool with no repeated characters. The corresponding requests are in [Instructions 1](../prompts/1_place_names.md), [3](../prompts/3_corrections.md) and [4](../prompts/4_shared_place_pool.md).

<details>
<summary>最终方法的历史代码 / Historical code for the final method</summary>

- [生成1,402个候选并排序 / Construct and rank the 1,402 candidates](records/round3/1_rank_candidates.py)。
- [应用用字多样性约束和词项过滤规则 / Apply the character-diversity and word filters](records/round3/2_select_filtered.py)。
- [查询中文维基标题，并跟随重定向 / Check Chinese Wikipedia titles, following redirects](records/check_names.py)。


</details>
