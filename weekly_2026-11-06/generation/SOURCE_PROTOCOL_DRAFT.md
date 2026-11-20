# Source-name generation protocol (draft)
中文：信源名称生成规程（草稿）

生成政府、报纸、个人和社媒用户四类信源名称。数据扩充后，再确定每类需要多少个名称。

Generate names for government, newspaper, individual and social media sources. Decide how many names each type needs when expanding the dataset.

地名和人名查中文维基；政府、报纸和个人名称检查是否自然。

Check place names and person names against Chinese Wikipedia, and review government, newspaper and individual names for naturalness.

## Fictional place names / 虚构地名

- **怎么造地名**：统计真实县名、市名的第一个字和第二个字分别常用哪些字，再把常用字两两组合，例如“平”＋“宁”得到“平宁”；和真实行政区划或中文维基条目同名的删掉。<br>**How names are made:** Count which characters are most common in the first and second positions of real county and city names, then combine them, for example 平 + 宁 gives 平宁 (Pingning). Names matching a real administrative division or a Chinese Wikipedia title are removed.
- **政府和报纸**：从同一批地名里各抽各的，所以“平宁市民政局”和“平宁晚报”可能同时出现。<br>**Government and newspapers:** Each source draws from the same list independently, so 平宁市民政局 (Pingning Civil Affairs Bureau) and 平宁晚报 (Pingning Evening News) may both appear.
- **实体**：实体用另一批地名，不和信源地名重复。<br>**Entities:** Entities use a separate list that does not overlap with source place names. 

<details>
<summary>地名数据与版本 / Place-name data and version</summary>

- [modood/Administrative-divisions-of-China](https://github.com/modood/Administrative-divisions-of-China)：commit c49d495，数据截至2023-06-30，WTFPL。<br>[modood/Administrative-divisions-of-China](https://github.com/modood/Administrative-divisions-of-China): commit c49d495, data as of 30 June 2023, WTFPL.
- 字频：取市级和县级名称，去掉“市、县、区”等后缀，保留两字名（2,529条），第一个字和第二个字各取最常用的50个。<br>Frequencies: Take city- and county-level names, remove endings such as 市, 县 and 区, keep two-character names (2,529 entries), and take the 50 most common characters in each position.
- 组合与查重：50×50共2,500个组合，删去两字相同或与真实市、县、乡镇街道名、省名相同的组合；pilot中剩1,402个候选。<br>Combination and checks: The 50 × 50 combinations give 2,500 names. Names with identical characters or matching real city, county, township, street or province names are removed, leaving 1,402 candidates in the pilot.

</details>

## Government / 政府

- **格式**：虚构地名＋市＋机构名，例如“广城市民政局”。<br>**Format:** Fictional place + 市 (city) + agency name, e.g. 广城市民政局 (Guangcheng Civil Affairs Bureau).
- **抽取**：按实体类型从下表抽一个机构，再从信源地名池抽一个地名。<br>**Sampling:** Draw an agency for the entity type from the table below, then draw a place name from the source pool.

| Entity type 实体类型 | Agencies 机构 |
|---|---|
| Person 人物 | 公安局 (Public Security), 民政局 (Civil Affairs), 人力资源和社会保障局 (Human Resources and Social Security) |
| Organisation 机构 | 市场监督管理局 (Market Regulation), 统计局 (Statistics), 人力资源和社会保障局 (Human Resources and Social Security) |
| Location 地点 | 统计局 (Statistics), 民政局 (Civil Affairs), 规划和自然资源局 (Planning and Natural Resources) |
| Building 建筑 | 住房和城乡建设局 (Housing and Urban-Rural Development) |
| Event 活动 | 文化和旅游局 (Culture and Tourism), 商务局 (Commerce) |
| Sports event 体育活动 | 体育局 (Sports) |
| Product 产品 | 市场监督管理局 (Market Regulation), 商务局 (Commerce) |
| Artwork 艺术作品 | 文化和旅游局 (Culture and Tourism) |

机构选自北京、上海均设置的市级部门，按官方职能匹配实体类型，名称采用通用形式。官方名单：[北京](https://www.beijing.gov.cn/gongkai/zfxxgk/fdzdgknr/jgzn/) · [上海](https://www.shanghai.gov.cn/nw2405/)。

Agencies are selected from municipal departments present in both Beijing and Shanghai, matched to entity types by their official functions, and given standard names. Official lists: [Beijing](https://www.beijing.gov.cn/gongkai/zfxxgk/fdzdgknr/jgzn/) · [Shanghai](https://www.shanghai.gov.cn/nw2405/).

## Newspapers / 报纸

- **格式**：虚构地名＋后缀，例如“临阳晚报”。<br>**Format:** Fictional place + suffix, e.g. 临阳晚报 (Linyang Evening News).
- **抽取**：从信源地名池抽一个地名；日报、晚报、时报、商报、晨报、都市报六种后缀等概率抽取。<br>**Sampling:** Draw a place from the source pool and draw one of six suffixes with equal probability: 日报 (daily), 晚报 (evening news), 时报 (times), 商报 (business news), 晨报 (morning news), 都市报 (metropolitan news).

<details>
<summary>后缀统计与依据 / Suffix counts and source</summary>

从国家网信办[《2025版互联网新闻信息稿源单位名单》](https://www.cac.gov.cn/rootimages/uploadimg/1756886952378281/1756886952378281.pdf)的428个报纸名称中，选取六种常见、可用于命名的后缀：日报238、晚报29、时报15、商报14、晨报11、都市报9。

Six common endings suitable for naming were selected from 428 newspaper titles in the Cyberspace Administration of China’s [2025 list of internet news sources](https://www.cac.gov.cn/rootimages/uploadimg/1756886952378281/1756886952378281.pdf): 日报 (238), 晚报 (29), 时报 (15), 商报 (14), 晨报 (11) and 都市报 (9).

</details>

## Individuals / 个人


- 从ChineseNames最常见的200个姓中抽姓，从男性或女性使用组最常见的200个双字名中抽名；男女常用名各半。<br>Draw a surname from the 200 most frequent surnames in ChineseNames and a two-character given name from the 200 most frequent in the male- or female-usage group, with equal numbers from each group.
- 排除有中文维基页面的全名。<br>Exclude full names with a Chinese Wikipedia page.
- 人工筛查姓名自然度，并记录删除项。<br>Screen full names manually for naturalness and record removals.
- 个人信源、实体人物和属性值中的人名分属三个互不重叠的名单。<br>Keep individual-source names, person-entity names and names used as attribute values in three non-overlapping lists.

<details>
<summary>数据库、版本与许可 / Database, version and licence</summary>

- [ChineseNames](https://github.com/psychbruce/ChineseNames)：commit dd948e7，版本2025.8。<br>[ChineseNames](https://github.com/psychbruce/ChineseNames): commit dd948e7, version 2025.8.
- 数据为1930–2008年出生、2008年在世的户籍汉族人口的姓名聚合频率，不含个人记录。<br>The data provide aggregate name frequencies for Han Chinese household-registered people born in 1930–2008 and alive in 2008, not individual records.
- 引用Bao (2023)和Bao et al. (2021)，按数据库的GPL-3和CC BY-NC-SA条款作非商业使用。<br>Cite Bao (2023) and Bao et al. (2021), and use the database non-commercially under its GPL-3 and CC BY-NC-SA terms.

</details>

## Social media users / 社媒用户

- **显示格式**：“用户 @昵称”，例如“用户 @热心的枫叶4655”。<br>**Display:** 用户 @handle, e.g. 用户 @热心的枫叶4655 (User @warm-hearted maple leaf 4655).
- **组合规则**：形容词＋的＋名词＋四位数字（1000–9999），沿用WFW的“形容词＋名词＋数字”结构。<br>**Structure:** Adjective + 的 + noun + four digits (1000–9999), following WFW’s adjective–noun–digits structure.
- **抽取**：形容词、名词和数字分别随机抽取。<br>**Sampling:** Draw the adjective, noun and number at random.

<details>
<summary>词表来源与筛选 / Word-list sources and filtering</summary>

- 候选词来自开源中文昵称生成器[chinayin/random-nickname](https://github.com/chinayin/random-nickname)，Apache-2.0，commit 26f0b9c。<br>Candidate words come from the open-source Chinese nickname generator [chinayin/random-nickname](https://github.com/chinayin/random-nickname), Apache-2.0, commit 26f0b9c.
- 只保留[SUBTLEX-CH](https://www.ugent.be/pp/experimentele-psychologie/en/research/documents/subtlexch)词频表（Cai & Brysbaert, 2010）收录的词，得到217个形容词和198个名词。<br>Keep only words found in the [SUBTLEX-CH](https://www.ugent.be/pp/experimentele-psychologie/en/research/documents/subtlexch) frequency list (Cai & Brysbaert, 2010), giving 217 adjectives and 198 nouns.

</details>
