# 指令2：生成并使用地名池 / Instruction 2: how to make and use the place-name pool

## 中文 / Chinese

```
重新生成人名和地名。地名按“组合候选→查重→确认地名池→从池中取名生成数据”的顺序处理：

1. 先用常见的地名用字组合出虚构地名候选。
2. 核对候选是否为真实存在的行政区划：对比中文维基，并与中国行政区划列表比对。
3. 与真实地名重合的，换一个常见组合，不改用生僻字。
4. 多次尝试仍重合的，可考虑三字地名：真实的三字县市名较少，编造空间大，读起来仍然自然。
5. 先提交20个地名和20个人名供我确认。确认后，将这批地名作为地名池；生成实体和信源数据时，从池中取名填入相应位置，例如政府和报纸名称中的地名、地点实体名称，以及人物的现居城市等属性。

```

## English translation

Regenerate person and place names. For place names, follow this sequence: combine candidates → check for existing names → confirm the place-name pool → take names from the pool to generate the data.

1. First combine common place-name characters into invented place-name candidates.
2. Check whether each candidate is a real administrative division by checking Chinese Wikipedia and comparing it with a list of Chinese administrative divisions.
3. If a candidate coincides with a real name, replace it with another common combination; do not resort to rare characters.
4. If repeated attempts still coincide with real names, consider three-character place names: real three-character county/city names are fewer, leaving more room to invent names that still sound natural.
5. First submit 20 place names and 20 person names for my confirmation. Once confirmed, use this set of place names as the pool. When generating entity and source data, take names from this pool for the relevant positions, such as the place-name component of government and newspaper names, location-entity names, and attributes such as a person's city of residence.
