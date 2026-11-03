# 指令3：修改第一版数据的五个问题 / Instruction 3: five problems in the first dataset

## 中文 / Chinese

```
第一版数据中的以下问题需要修改：

1. 机构和产品的名称泄露了属性答案。例如北马坪纺织集团的总部所在地备选中有"北马坪"，
   而表格第一行始终显示实体名，模型看名称即可推出答案，违反"两边同样合理"的要求。
   产品的制造商同理。解决办法：机构和产品名称不含地名，或删去"总部所在地"和
   "制造商"两个属性。

2. 产品制造商的备选不合理。净水器的制造商备选中有医药公司和食品公司，并非同等合理。
   备选应属于同一行业。

3. 国籍不一致。人物使用中文姓名、居住在中式地名，国籍却是"瑟兰尼亚人"这类西式音译。
   应删去国籍属性，或统一整个设定。建议删去，人物属性已足够。

4. 地名层级：信源中的地名仍是乡镇级（如"陈家店市民政局""郭家塘晚报"），读起来不自然，
   需要另外生成一批县市级的两字地名。地点实体也有同样问题：五里营这类名称是村镇级的，
   而数据给它的是 73 万人口、2450 平方公里的县市级规模，名称与规模不符。

5. 社交媒体账号"@城南旧事本人"用了真实小说《城南旧事》（林海音）的书名，
   应换成不指向真实作品的虚构名称。
   另外，个人信源的姓名池和实体姓名池应分开，目前有重叠。

修改后再次提交。
```

## English translation

The following problems in the first dataset need to be fixed:

1. Organization and product names leak attribute answers. For example, the headquarters alternatives of 北马坪纺织集团 (Beimaping Textile Group) include 北马坪 (Beimaping), while the first row of the table always shows the entity name, so the model can infer the answer from the name, violating the requirement that "both sides are equally plausible". The same applies to product manufacturers. Fix: organization and product names should not contain place names, or drop the two attributes "headquarters" and "manufacturer".

2. The product manufacturer alternatives are not plausible. The manufacturer alternatives for a water purifier include pharmaceutical and food companies, which are not equally plausible. Alternatives should belong to the same industry.

3. Nationality is inconsistent. People with Chinese names living in Chinese-style places have a nationality like 瑟兰尼亚人 (a Western-style transliteration, "Seranian"). Either drop the nationality attribute or make the whole setting consistent. Dropping it is suggested; there are enough person attributes.

4. Place-name level: the place names in the sources are still township-level (e.g. 陈家店市民政局, 郭家塘晚报), which reads unnaturally; a separate batch of county/city-level two-character place names is needed. Location entities have the same problem: a name like 五里营 (Wuliying) is village/township-level, while the data gives it the scale of a county or city (730,000 inhabitants, 2,450 km²), so name and scale do not match.

5. The social media account @城南旧事本人 uses the title of a real novel, 城南旧事 (My Memories of Old Beijing, by Lin Haiyin); replace it with a fictional name that does not point to a real work. Also, the name pool for individual sources and the name pool for entities should be separate; they currently overlap.

Submit again after the fixes.
