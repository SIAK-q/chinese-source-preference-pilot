---
status: current source-name rules; prepared prompts, baseline discussion precedes source inference
updated: 2026-11-20
---
# Source-name generation protocol (draft)
中文：信源名称生成规程

## Fictional place names / 虚构地名

- **怎么造地名**：统计真实县名、市名的第一个字和第二个字分别常用哪些字，再把常用字两两组合，例如“平”＋“宁”得到“平宁”；和真实行政区划或中文维基条目同名的删掉。<br>**How names are made:** Count which characters are most common in the first and second positions of real county and city names, then combine them, for example 平 + 宁 gives 平宁 (Pingning). Names matching a real administrative division or a Chinese Wikipedia title are removed.
- **政府和报纸**：从同一批地名里各抽各的，所以“平宁市民政局”和“平宁晚报”可能同时出现。<br>**Government and newspapers:** Each source draws from the same list independently, so 平宁市民政局 (Pingning Civil Affairs Bureau) and 平宁晚报 (Pingning Evening News) may both appear.
- **人工筛选**：组合后读一遍，删除读起来不自然或像小说地名的组合，记录名称和理由。<br>**Manual screening:** Read the combinations, remove unnatural or novel-like names, and record each removal and its reason.
- **实体**：实体用另一批地名，不和信源地名重复。<br>**Entities:** Entities use a separate list that does not overlap with source place names. 

<details>
<summary>地名数据与版本 / Place-name data and version</summary>

- [modood/Administrative-divisions-of-China](https://github.com/modood/Administrative-divisions-of-China)：commit c49d495，数据截至2023-06-30，WTFPL。<br>[modood/Administrative-divisions-of-China](https://github.com/modood/Administrative-divisions-of-China): commit c49d495, data as of 30 June 2023, WTFPL.
- 字频：取市级和县级名称，去掉“市、县、区”等后缀，保留两字名（2,529条），第一个字和第二个字各取最常用的50个。<br>Frequencies: Take city- and county-level names, remove endings such as 市, 县 and 区, keep two-character names (2,529 entries), and take the 50 most common characters in each position.
- 组合与查重：50×50共2,500个组合，删去两字相同或与真实市、县、乡镇街道名、省名相同的组合；pilot中剩1,402个候选；人工筛选删去75个（如“市城”“黄泉”“镇宁”），留1,327个；配信源时再排除11个实体地名，可用1,316个。<br>Combination and checks: The 50 × 50 combinations give 2,500 names. Names with identical characters or matching real city, county, township, street or province names are removed, leaving 1,402 candidates in the pilot. Manual screening removed 75 more (e.g. 市城, 黄泉, 镇宁), leaving 1,327. Source sampling excludes 11 entity place names, leaving 1,316 available.

</details>

## Government / 政府

- **格式**：虚构地名＋市＋机构名，例如“广城市民政局”。<br>**Format:** Fictional place + 市 (city) + agency name, e.g. 广城市民政局 (Guangcheng Civil Affairs Bureau).
- **抽取**：按实体类型从下表抽一个机构，再从信源地名池抽一个地名。<br>**Sampling:** Draw an agency for the entity type from the table below, then draw a place name from the source pool.

| Entity type 实体类型 | Agencies 机构 |
|---|---|
| Person 人物 | 公安局 (Public Security), 民政局 (Civil Affairs), 人力资源和社会保障局 (Human Resources and Social Security) |
| Organisation 机构 | 市场监督管理局 (Market Regulation), 统计局 (Statistics), 人力资源和社会保障局 (Human Resources and Social Security) |
| Location 地点 | 统计局 (Statistics), 民政局 (Civil Affairs), 规划和自然资源局 (Planning and Natural Resources) |
| Building 建筑 | 住房和城乡建设局 (Housing and Urban-Rural Development), 规划和自然资源局 (Planning and Natural Resources) |
| Event 活动 | 文化和旅游局 (Culture and Tourism), 商务局 (Commerce) |
| Sports event 体育活动 | 体育局 (Sports), 文化和旅游局 (Culture and Tourism; event and sports-tourism information) |
| Product 产品 | 市场监督管理局 (Market Regulation), 商务局 (Commerce) |
| Artwork 艺术作品 | 文化和旅游局 (Culture and Tourism), 版权局 (Copyright); each 50% |

机构选自北京、上海均设置的市级部门，按官方职能或实际发布的信息匹配实体类型，名称采用通用形式。官方名单：[北京](https://www.beijing.gov.cn/gongkai/zfxxgk/fdzdgknr/jgzn/) · [上海](https://www.shanghai.gov.cn/nw2405/)。

Agencies are selected from municipal departments present in both Beijing and Shanghai, matched to entity types by their official functions or the information they publish, and given standard names. Official lists: [Beijing](https://www.beijing.gov.cn/gongkai/zfxxgk/fdzdgknr/jgzn/) · [Shanghai](https://www.shanghai.gov.cn/nw2405/).

<details>
<summary>新增机构的依据 / Evidence for additional agencies</summary>

- **建筑—规划和自然资源局**：[北京部门职责](https://www.beijing.gov.cn/gongkai/caizheng/czzt/2024ys/202402/t20240222_3567448.html)包括工程建设项目规划和用地管理；[上海部门职责](https://www.shanghai.gov.cn/nw2405/20201030/b0ed17bf3451450db9f75e6d73790b51.html)包括建设工程规划土地管理及竣工前监督。<br>**Buildings—Planning and Natural Resources:** Both Beijing and Shanghai assign construction planning and land management to these departments.
- **体育活动—文化和旅游局**：[北京文旅部门网站](https://whlyj.beijing.gov.cn/zwgk/xwzx/gwyxx/202505/t20250506_4081841.html)转载赛事旅游报道；[上海文旅部门](https://whlyj.sh.gov.cn/wlyw/20260904/ce63f9f285264b84ae14123b057206b2.html)发布的旅游节活动包含体育赛事。据此，将文旅部门加入赛事及体旅活动信息的信源。<br>**Sports events—Culture and Tourism:** Beijing publishes sports-tourism coverage, and Shanghai announces sports events within its tourism festival. This supports using the department as a publisher of event and sports-tourism information.

</details>

## Newspapers / 报纸

- **格式**：虚构地名＋后缀，例如“临阳晚报”。<br>**Format:** Fictional place + suffix, e.g. 临阳晚报 (Linyang Evening News).
- **抽取**：从信源地名池抽一个地名；日报、晚报、时报、晨报、都市报五种后缀等概率抽取。<br>**Sampling:** Draw a place from the source pool and draw one of five suffixes with equal probability: 日报 (daily), 晚报 (evening news), 时报 (times), 晨报 (morning news), 都市报 (metropolitan news).

<details>
<summary>后缀统计与依据 / Suffix counts and source</summary>

从国家网信办[《2025版互联网新闻信息稿源单位名单》](https://www.cac.gov.cn/rootimages/uploadimg/1756886952378281/1756886952378281.pdf)的428个报纸名称中，选取六种常见、可用于命名的后缀：日报238、晚报29、时报15、商报14、晨报11、都市报9。

11月9日会议决定不使用“商报”，其余五种等概率抽取。<br>The 9 November meeting excluded 商报; the remaining five endings are sampled equally.

Six common endings suitable for naming were selected from 428 newspaper titles in the Cyberspace Administration of China’s [2025 list of internet news sources](https://www.cac.gov.cn/rootimages/uploadimg/1756886952378281/1756886952378281.pdf): 日报 (238), 晚报 (29), 时报 (15), 商报 (14), 晨报 (11) and 都市报 (9).

</details>

## Individuals / 个人


- **抽法**：从ChineseNames数据按姓氏人数频率抽姓；每个姓名等概率选择男性或女性用字组，再按该组字频独立抽两个名用字。<br>**Sampling:** Draw the surname using population-frequency weights from ChineseNames. For each name, choose the male- or female-usage character distribution with equal probability, then independently draw two given-name characters using its frequency weights.
- **查重**：有中文维基精确标题页面的姓名跳过重抽；排除已有三个人名池，且本批个人信源不重名。<br>**Checks:** Redraw names with an exact-title Chinese Wikipedia page; exclude the three existing person-name pools and duplicate names within this source batch.
- **已保存批次**：定稿70实体配五条件共15,200题（含baseline）；1,520个个人信源姓名均已查中文维基并无精确标题页面，因有页面跳过36次。<br>**Saved batch:** The final 70 entities have 15,200 prepared prompts across five conditions, including baseline. All 1,520 retained individual-source names were checked and had no exact-title Chinese Wikipedia page; 36 draws were skipped because a page existed.
- **复用**：两种表序及不同被测模型使用同一份已保存信源，不在模型运行时重抽；保存种子、规则版本、配题键及结果。<br>**Reuse:** Use the same saved sources for both table orders and all evaluated models, without drawing again during inference. Log the seed, rule version, pair key and result.

<details>
<summary>数据库、版本与许可 / Database, version and licence</summary>

- [ChineseNames](https://github.com/psychbruce/ChineseNames)：commit dd948e7，版本2025.8。<br>[ChineseNames](https://github.com/psychbruce/ChineseNames): commit dd948e7, version 2025.8.
- 数据为1930–2008年出生、2008年在世的户籍汉族人口的姓名聚合频率，不含个人记录。<br>The data provide aggregate name frequencies for Han Chinese household-registered people born in 1930–2008 and alive in 2008, not individual records.
- 引用Bao (2023)和Bao et al. (2021)，按数据库的GPL-3和CC BY-NC-SA条款作非商业使用。<br>Cite Bao (2023) and Bao et al. (2021), and use the database non-commercially under its GPL-3 and CC BY-NC-SA terms.

</details>

## Social media users / 社媒用户

- **显示格式**：“用户 @昵称”，例如“用户 @热心的枫叶4655”“用户 @用户7829104852”。<br>**Display:** 用户 @handle, e.g. 用户 @热心的枫叶4655 and 用户 @用户7829104852.
- **昵称两种，各占一半**：①形容词＋的＋名词＋四位数字（1000–9999），如“热心的枫叶4655”，形容词从217个、名词从198个中随机抽（词表来源见下方折叠块）；②微博新账号默认昵称“用户＋10位数字”（首位不为0），如“用户7829104852”。两种交替生成，同一批内不重复。<br>**Two handle forms, half each:** (1) adjective + 的 + noun + four digits (1000–9999), e.g. 热心的枫叶4655, with the adjective drawn from 217 and the noun from 198 candidates (sources in the fold below); (2) Weibo's default handle for new accounts, 用户 plus ten digits (first digit non-zero), e.g. 用户7829104852. The two forms alternate, and handles do not repeat within a batch.
- **依据**：11月9日会议上，老师认可第一种“possible”，并建议加入微博默认格式：“you could mix it up, you could use that as well”。<br>**Basis:** At the 9 November meeting, the supervisor found the first form possible and suggested adding Weibo's default format: "you could mix it up, you could use that as well".

<details>
<summary>词表来源与筛选 / Word-list sources and filtering</summary>

- 候选词来自开源中文昵称生成器[chinayin/random-nickname](https://github.com/chinayin/random-nickname)，Apache-2.0，commit 26f0b9c。<br>Candidate words come from the open-source Chinese nickname generator [chinayin/random-nickname](https://github.com/chinayin/random-nickname), Apache-2.0, commit 26f0b9c.
- 只保留[SUBTLEX-CH](https://www.ugent.be/pp/experimentele-psychologie/en/research/documents/subtlexch)词频表（Cai & Brysbaert, 2010）收录的词，得到217个形容词和198个名词。<br>Keep only words found in the [SUBTLEX-CH](https://www.ugent.be/pp/experimentele-psychologie/en/research/documents/subtlexch) frequency list (Cai & Brysbaert, 2010), giving 217 adjectives and 198 nouns.

</details>
