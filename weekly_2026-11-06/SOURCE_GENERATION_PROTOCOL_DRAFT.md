# Source-name generation protocol (draft)
中文：信源名称生成规程（草稿）

## Overview

- Each source belongs to one of four types: government, newspaper, individual, social media user.
    - 中文：每个信源属于四类之一：政府、报纸、个人、社交媒体用户。
- Pool sizes will follow the size of the expanded dataset.
    - 中文：各名称池的规模按扩充后的数据量确定。

## Fictional place names

- Government and newspaper sources draw from one shared pool of fictional place names; entity places come from a separate list.
    - 中文：政府和报纸信源共用一个虚构地名池；实体地名使用单独的名单。
- Place names are drawn independently for each source.
    - 中文：每个信源的地名各自随机抽取。
- Method: count character frequencies by position in real county- and prefecture-level names, combine frequent characters, then remove names matching real administrative divisions or Chinese Wikipedia titles.
    - 中文：方法：按位置统计真实县级、地级名称的用字频率，组合高频字，再排除与真实行政区划或中文维基条目相同的名称。

## Government

- Format: fictional place + 市(city) + real agency name, e.g. 广城市民政局 (Guangcheng Civil Affairs Bureau).
    - 中文：格式：虚构地名 + 市 + 真实机构名，例如广城市民政局。
- Each entity type has its own list of agencies. A government source combines one randomly drawn agency from that list with one randomly drawn place.
    - 中文：每类实体有各自的机构列表。每个政府信源从对应列表随机抽取一个机构，再随机配一个地名。

| Entity type 实体类型  | Agencies 机构                                                                                     |
| ----------------- | ----------------------------------------------------------------------------------------------- |
| Person 人物         | 公安局 (Public Security Bureau), 民政局 (Civil Affairs Bureau), 人力资源和社会保障局 (Human Resources and Social Security Bureau)    |
| Organisation 机构   | 市场监督管理局 (Administration for Market Regulation), 统计局 (Statistics Bureau), 人力资源和社会保障局 (Human Resources and Social Security Bureau) |
| Location 地点       | 统计局 (Statistics Bureau), 民政局 (Civil Affairs Bureau), 规划和自然资源局 (Planning and Natural Resources Bureau)                |
| Building 建筑       | 住房和城乡建设局 (Housing and Urban-Rural Development Bureau)                                                  |
| Event 活动          | 文化和旅游局 (Culture and Tourism Bureau), 商务局 (Commerce Bureau)                                                    |
| Sports event 体育活动 | 体育局 (Sports Bureau)                                                                                    |
| Product 产品        | 市场监督管理局 (Administration for Market Regulation), 商务局 (Commerce Bureau)                                                     |
| Artwork 艺术作品      | 文化和旅游局 (Culture and Tourism Bureau)                                                                    |

- Agencies are drawn from the municipal government departments of Beijing and Shanghai, two representative Chinese cities, and matched to entity types according to their official functions. Department names use a standard form.
    - 中文：机构选自北京、上海这两个具有代表性的城市的市级政府部门，并根据官方职能与实体类型对应。部门名称采用通用形式。
- Official lists: [Beijing](https://www.beijing.gov.cn/gongkai/zfxxgk/fdzdgknr/jgzn/), [Shanghai](https://www.shanghai.gov.cn/nw2405/).
    - 中文：官方名单见北京、上海市政府网站链接。

## Newspapers

- Format: fictional place + suffix, e.g. 临阳晚报 (Linyang Evening News).
    - 中文：格式：虚构地名 + 后缀，例如临阳晚报。
- Suffixes: the six most frequent endings among the 428 newspaper titles in the [2025 list of internet news sources](https://www.cac.gov.cn/rootimages/uploadimg/1756886952378281/1756886952378281.pdf) published by the Cyberspace Administration of China: 日报 (daily, 238), 晚报 (evening news, 29), 时报 (times, 15), 商报 (business news, 14), 晨报 (morning news, 11), 都市报 (metropolitan news, 9).
    - 中文：后缀：国家网信办《2025 版互联网新闻信息稿源单位名单》中 428 个报纸名称里最常见的六种结尾：日报（238）、晚报（29）、时报（15）、商报（14）、晨报（11）、都市报（9）。
- Each suffix is drawn with equal probability.
    - 中文：六种后缀等概率抽取。

## Individuals

- Common Chinese full names without a Chinese Wikipedia page, balanced between male- and female-usage names.
    - 中文：常见中文姓名，排除有中文维基页面的姓名，男性和女性常用名各半。
- Proposed method: surnames weighted by a published surname-frequency table; two given-name characters drawn from gendered character frequencies.
    - 中文：拟用方法：姓氏按已发表的姓氏频率表加权；名字的两个字按分性别的用字频率抽取。
- Individual-source names, entity names and names inside attribute values stay in three separate pools.
    - 中文：个人信源、实体人物和属性值中的人名分属三个互不重复的名单。

## Social media users

- Handles are displayed as 用户 @昵称 (User @handle), e.g. 用户 @热心的枫叶4655 (User @warm-hearted maple leaf 4655).
    - 中文：昵称显示为“用户 @昵称”，例如用户 @热心的枫叶4655。
- WFW combines a random adjective, noun and four digits, modelled on Reddit's suggested usernames. A direct Chinese translation does not read like a Chinese handle.
    - 中文：WFW 用随机形容词、名词加四位数字，模仿 Reddit 的推荐用户名。直译成中文不像中文网名。
- The same structure is used here: a random adjective + 的 + a random noun + four random digits (1000–9999). 的 links the adjective and noun, as is usual in Chinese.
    - 中文：这里采用相同的结构：随机形容词 + 的 + 随机名词 + 四位随机数字（1000–9999）。形容词和名词之间加“的”，符合中文的表达习惯。
- Word lists: candidate words come from the open-source Chinese nickname generator [chinayin/random-nickname](https://github.com/chinayin/random-nickname) (Apache-2.0, commit 26f0b9c). Only words found in the [SUBTLEX-CH](https://www.ugent.be/pp/experimentele-psychologie/en/research/documents/subtlexch) word-frequency list (Cai & Brysbaert, 2010) are kept, giving 217 adjectives and 198 nouns.
    - 中文：词表：候选词来自开源中文昵称生成器 chinayin/random-nickname（Apache-2.0，commit 26f0b9c），只保留 SUBTLEX-CH 词频表（Cai & Brysbaert, 2010）收录的词，共 217 个形容词和 198 个名词。
- As in WFW, words are drawn at random, with no selection by meaning.
    - 中文：与 WFW 一样，随机抽词，不按词义筛选。
