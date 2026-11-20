# Source-name generation protocol
中文：信源名称生成规程

本页说明政府、报纸、个人和社媒用户四类信源名称的生成方法。

How names are generated for four source types: government, newspaper, individual and social media user.

## Fictional place names / 虚构地名

- **造法**：统计真实县、市名第一、二个字的常用字，两两组合，如“平”＋“宁”→“平宁”；与真实地名或中文维基条目同名的删掉。<br>**Method:** Combine the most common first and second characters of real county and city names, e.g. 平 + 宁 → 平宁; names matching a real place or Chinese Wikipedia title are removed.
- **人工筛选**：删去读起来不自然的75个，剩1,327个。<br>**Manual screening:** 75 unnatural names were removed, leaving 1,327.
- **使用**：政府和报纸各自从这批地名中抽，可能同名，如“平宁市民政局”与“平宁晚报”；实体另用一批地名，不重复。<br>**Use:** Government and newspaper sources draw from this list independently, so 平宁市民政局 and 平宁晚报 may both occur; entities use a separate, non-overlapping list.

<details>
<summary>地名数据与版本 / Place-name data and version</summary>

- [modood/Administrative-divisions-of-China](https://github.com/modood/Administrative-divisions-of-China)：commit c49d495，数据截至2023-06-30，WTFPL。<br>commit c49d495, data as of 30 June 2023, WTFPL.
- 取市、县级两字名（去“市、县、区”后2,529条），两个位置各取前50个常用字，组合得2,500个；去掉两字相同或与真实市、县、乡镇街道、省同名的，剩1,402个。<br>Two-character city and county names (2,529 after removing 市, 县, 区); the top 50 characters per position give 2,500 combinations; removing repeated characters and real city, county, township, street or province names leaves 1,402.

</details>

## Government / 政府

- **格式**：虚构地名＋市＋机构，如“广城市民政局”。<br>**Format:** Fictional place + 市 + agency, e.g. 广城市民政局 (Guangcheng Civil Affairs Bureau).
- **抽取**：按实体类型从下表等概率抽机构，再抽地名。<br>**Sampling:** Draw an agency for the entity type with equal probability, then a place name.

| Entity type 实体类型 | Agencies 机构 |
|---|---|
| Person 人物 | 公安局 (Public Security), 民政局 (Civil Affairs), 人力资源和社会保障局 (Human Resources and Social Security) |
| Organisation 机构 | 市场监督管理局 (Market Regulation), 统计局 (Statistics), 人力资源和社会保障局 (Human Resources and Social Security) |
| Location 地点 | 统计局 (Statistics), 民政局 (Civil Affairs), 规划和自然资源局 (Planning and Natural Resources) |
| Building 建筑 | 住房和城乡建设局 (Housing and Urban-Rural Development), 规划和自然资源局 (Planning and Natural Resources) |
| Event 活动 | 文化和旅游局 (Culture and Tourism), 商务局 (Commerce) |
| Sports event 体育活动 | 体育局 (Sports), 文化和旅游局 (Culture and Tourism) |
| Product 产品 | 市场监督管理局 (Market Regulation), 商务局 (Commerce) |
| Artwork 艺术作品 | 文化和旅游局 (Culture and Tourism), 版权局 (Copyright) |

机构均为北京、上海都设置的市级部门，按职能或实际发布的信息匹配实体类型。官方名单：[北京](https://www.beijing.gov.cn/gongkai/zfxxgk/fdzdgknr/jgzn/) · [上海](https://www.shanghai.gov.cn/nw2405/)。

All agencies exist at municipal level in both Beijing and Shanghai and are matched to entity types by function or published information. Official lists: [Beijing](https://www.beijing.gov.cn/gongkai/zfxxgk/fdzdgknr/jgzn/) · [Shanghai](https://www.shanghai.gov.cn/nw2405/).

<details>
<summary>新增机构的依据 / Evidence for added agencies</summary>

- **建筑—规划和自然资源局**：北京、上海该部门均负责建设项目规划和用地管理（[北京](https://www.beijing.gov.cn/gongkai/caizheng/czzt/2024ys/202402/t20240222_3567448.html) · [上海](https://www.shanghai.gov.cn/nw2405/20201030/b0ed17bf3451450db9f75e6d73790b51.html)）。<br>**Buildings:** In both cities this department handles construction planning and land use.
- **体育活动—文化和旅游局**：北京、上海文旅部门均发布赛事旅游信息（[北京](https://whlyj.beijing.gov.cn/zwgk/xwzx/gwyxx/202505/t20250506_4081841.html) · [上海](https://whlyj.sh.gov.cn/wlyw/20260904/ce63f9f285264b84ae14123b057206b2.html)）。<br>**Sports events:** Both cities' culture and tourism departments publish sports-tourism information.
- **艺术作品—版权局**：北京作品登记涵盖绘画、雕塑；国家版权局名录列有北京、上海市版权局（[北京](https://banshi.beijing.gov.cn/pubtask/task/1/110000000000/b59addd1-50b7-478f-bbe5-5c9a2b9f9169_app.html) · [名录](https://www.ncac.gov.cn/xxfb/bqshfw/bqdj/djjg/202410/t20241018_870052.html)）。<br>**Artworks:** Beijing's work registration covers paintings and sculptures; the national list includes Beijing and Shanghai copyright bureaus.

</details>

## Newspapers / 报纸

- **格式**：虚构地名＋后缀，如“临阳晚报”。<br>**Format:** Fictional place + suffix, e.g. 临阳晚报 (Linyang Evening News).
- **抽取**：日报、晚报、时报、晨报、都市报，等概率。<br>**Sampling:** 日报 (daily), 晚报 (evening), 时报 (times), 晨报 (morning), 都市报 (metropolitan), equal probability.

<details>
<summary>后缀依据 / Suffix source</summary>

国家网信办[《2025版互联网新闻信息稿源单位名单》](https://www.cac.gov.cn/rootimages/uploadimg/1756886952378281/1756886952378281.pdf)428个报纸名称中：日报238、晚报29、时报15、商报14、晨报11、都市报9。“商报”带行业指向，不用。

Counts in 428 newspaper titles from the [2025 list of internet news sources](https://www.cac.gov.cn/rootimages/uploadimg/1756886952378281/1756886952378281.pdf): 日报 238, 晚报 29, 时报 15, 商报 14, 晨报 11, 都市报 9. 商报 (business news) implies a domain and is not used.

</details>

## Individuals / 个人

- **抽法**：姓按人数频率抽；等概率选男性或女性用字组，再按该组字频独立抽两个名用字。<br>**Sampling:** Draw the surname by population frequency; choose the male- or female-usage distribution with equal probability, then independently draw two given-name characters by its frequencies.
- **查重**：有中文维基精确标题页面的姓名重抽。<br>**Checks:** Names with an exact-title Chinese Wikipedia page are redrawn.
- **名单分开**：个人信源、实体人物、属性值人名三者不重叠。<br>**Separate lists:** Source, entity and attribute-value names do not overlap.

<details>
<summary>数据库与许可 / Database and licence</summary>

- [ChineseNames](https://github.com/psychbruce/ChineseNames)：commit dd948e7，版本2025.8；1930–2008年出生、2008年在世户籍汉族人口的姓名聚合频率。<br>commit dd948e7, version 2025.8; aggregate name frequencies of Han Chinese registered residents born 1930–2008 and alive in 2008.
- 引用Bao (2023)、Bao et al. (2021)；按GPL-3和CC BY-NC-SA非商业使用。<br>Cite Bao (2023) and Bao et al. (2021); non-commercial use under GPL-3 and CC BY-NC-SA.

</details>

## Social media users / 社媒用户

- **格式**：“用户 @昵称”。<br>**Format:** 用户 @handle.
- **昵称**：一半为形容词＋的＋名词＋四位数，如“热心的枫叶4655”；一半为微博默认的“用户＋10位数”，如“用户7829104852”。同批不重复。<br>**Handles:** half adjective + 的 + noun + four digits, e.g. 热心的枫叶4655; half Weibo's default 用户 + ten digits, e.g. 用户7829104852. No repeats within a batch.

<details>
<summary>词表来源 / Word lists</summary>

- 候选词来自[chinayin/random-nickname](https://github.com/chinayin/random-nickname)（Apache-2.0，commit 26f0b9c），只保留[SUBTLEX-CH](https://www.ugent.be/pp/experimentele-psychologie/en/research/documents/subtlexch)（Cai & Brysbaert, 2010）收录的词：217个形容词、198个名词。<br>Words from [chinayin/random-nickname](https://github.com/chinayin/random-nickname) (Apache-2.0, commit 26f0b9c), kept only if listed in [SUBTLEX-CH](https://www.ugent.be/pp/experimentele-psychologie/en/research/documents/subtlexch) (Cai & Brysbaert, 2010): 217 adjectives, 198 nouns.

</details>

## 附件 / Files

<details>
<summary>代码与输入 / Code and inputs</summary>

- [source_names.py](source_names.py)：生成信源名称。 / Generates source names.
- [sample_person_names.py](sample_person_names.py)：抽取个人姓名，由上一个脚本调用。 / Samples person names; called by the script above.
- [inputs/](inputs/)：地名池、社媒词表、姓名抽样设置和三个人名池。ChineseNames原始数据未上传，见上方版本与许可。 / Place-name pool, social-media word lists, name-sampling settings and the three person-name pools. ChineseNames raw data are not included; see version and licence above.

</details>
