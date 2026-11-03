# 指令1：生成数据 / Instruction 1: generate the data


## 中文 / Chinese

```text
【生成中文知识冲突测试数据】
参照WFW的数据结构，为中文设置生成实体、属性取值和信源名称。

一、实体和属性
按WFW的7类实体生成30个实体：人物8个、机构7个、地点5个、建筑3个、事件3个、
产品3个、艺术作品1个。各类测试属性如下：
- 人物：出生日期、职业、学历、身高、体重、婚姻状况、现居城市。
- 机构：成立时间、所属行业、员工人数、年营业额。
- 地点：人口、面积、海拔、下辖乡镇数。
- 建筑：设计师、建成年份、高度、层数、主体结构、容纳人数。
- 事件：举办日期、持续时间、参与人数、主办方、预算。
- 产品：发布日期、价格、重量、保修期。
- 艺术作品：创作者、创作年份。
相对WFW，删去眼睛颜色、头发颜色和国籍，新增现居城市；机构不设总部所在地，
产品不设制造商，因为名称中的地名或行业会泄露答案。

二、取值
每项测试属性写成长度为5的固定列表：第1项为原始值，第2–5项为同样合理的备选值。
按实体逐个写出原始值和4个备选，不设数值变化范围。
单位使用公制，日期使用中文格式，取值按中国实际情况确定：
- 学历使用中国学历层次，需要时附专业；婚姻状况为户籍口径的5个类别，每人都包含这5类，顺序可以不同。
- 同一人物的5个职业属于同一领域。
- 地点的人口、面积等量级参照中国县级市。
- 人物性别按女、男交替，作为固定背景信息，不作测试属性。

三、名称
地名从已确认的20个虚构地名池中取用：5个给政府信源，5个给报纸信源，10个用于实体。
- 地点实体直接使用地名；建筑、事件和艺术作品名称由地名加类型词构成，如“通溪体育馆”。
- 人物现居城市按固定顺序从实体地名中轮流取值。
- 事件主办方由事件所在地加5类机构构成，如“通溪市文化和旅游局”。
- 机构和产品使用不含地名或行业的两字品牌，如“晟远集团”。
人名使用常见中文姓名，有中文维基词条的删去并替换。实体人物、个人信源、
设计师及创作者分别使用互不重叠的三组姓名；设计师和创作者共用一组7个姓名。
生成后检查：任何取值都不出现在实体名称中。

四、信源名称
生成20个信源名称，四类各5个，按中文命名习惯构造：
- 政府机构：虚构地名＋5类真实机构，即民政局、公安局、卫生健康委员会、
  市场监督管理局、统计局，如“广城市民政局”。
- 报纸：虚构地名＋日报、晚报、都市报、时报或商报，不加“市”“县”，如“临阳日报”。
- 社交媒体：5个微博风格的虚构昵称，以“微博用户 @昵称”呈现；照搬已有作品名的昵称替换。
- 个人：从个人信源专用姓名池取名。
信源只区分以上四种类型，不加入发行量、粉丝数、职称、性别或年龄等类型内特征。

五、输出
实体保存为entities_zh.jsonl，保留id、name、entity_class、description和timeline_id等字段。
信源按四类保存为sources_zh.json，并记录政府、报纸的地名和社交媒体平台信息。
```

## English translation

**[Generate Chinese data for knowledge-conflict tests]**

Follow WFW's data structure to create entities, attribute values and source names for the Chinese setting.

**I. Entities and attributes**

Generate 30 entities in WFW's seven entity types: 8 people, 7 organizations, 5 locations, 3 buildings, 3 events, 3 products and 1 artwork. The test attributes are:

- People: date of birth, occupation, education, height, weight, marital status and current city of residence.
- Organizations: founding date, industry, employee count and annual revenue.
- Locations: population, area, elevation and number of subordinate towns/townships.
- Buildings: architect, completion year, height, floor count, main structural system and capacity.
- Events: date, duration, participant count, organizer and budget.
- Products: release date, price, weight and warranty.
- Artwork: creator and creation year.

Compared with WFW, drop eye colour, hair colour and nationality, and add current city of residence. Do not give organizations a headquarters attribute or products a manufacturer attribute, because a place or industry in the name would reveal the answer.

**II. Values**

Write each test attribute as a fixed list of five values: the first is the original value, and the remaining four are equally plausible alternatives. Write the original value and the four alternatives entity by entity, without a set numerical range. Use metric units and Chinese date formats, and fit the values to China:

- Education uses Chinese degree levels, with a major where applicable. Marital status uses the five household-registration categories; each person has all five, and the order may differ.
- The five occupations of one person belong to the same field.
- Location sizes such as population and area are on the scale of Chinese county-level cities.
- Gender alternates female/male and is fixed background information, not a test attribute.

**III. Names**

Take place names from the confirmed pool of 20 fictional names: 5 for government sources, 5 for newspaper sources and 10 for entities.

- Locations use a place name directly; building, event and artwork names combine a place name with a type term, such as 通溪体育馆 (Tongxi Gymnasium).
- People's current city of residence is taken from the entity place names in a fixed rotation.
- Event organizers combine the event's place with five types of institutions, such as 通溪市文化和旅游局 (Tongxi Culture and Tourism Bureau).
- Organizations and products use two-character brand names without place or industry, such as 晟远集团 (Shengyuan Group).

Use common Chinese person names; drop and replace names that have a Chinese Wikipedia entry. Use three mutually disjoint name pools for entity people, individual sources, and architects/creators; architects and creators share one list of 7 names. After generation, check that no value appears inside an entity name.

**IV. Source names**

Generate 20 source names, five in each category, following Chinese naming conventions:

- Government agencies: fictional place name + one of five real agency types, namely 民政局 (civil affairs bureau), 公安局 (public security bureau), 卫生健康委员会 (health commission), 市场监督管理局 (market regulation bureau) and 统计局 (statistics bureau), such as 广城市民政局 (Guangcheng Civil Affairs Bureau).
- Newspapers: fictional place name + 日报, 晚报, 都市报, 时报 or 商报 (daily, evening paper, metropolitan paper, times or business paper), without 市 (city) or 县 (county), such as 临阳日报 (Linyang Daily).
- Social media: five fictional Weibo-style nicknames, presented as “微博用户 @nickname”; replace nicknames that copy the title of an existing work.
- Individuals: names from the dedicated individual-source pool.

Distinguish sources only by these four categories. Do not add within-category features such as circulation, follower count, professional title, gender or age.

**V. Output**

Save entities as entities_zh.jsonl, retaining fields such as id, name, entity_class, description and timeline_id. Save sources by category as sources_zh.json, recording place names for government/newspaper sources and platform information for social media.
