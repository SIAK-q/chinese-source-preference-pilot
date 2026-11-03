# -*- coding: utf-8 -*-
import json,re,collections,random
SUF=re.compile(r'(自治州|自治县|自治区|地区|街道办事处|街道|镇|乡|区|县|市|州|盟|旗)$')
def stem(n):
    s=n
    for _ in range(3): s=SUF.sub("",s)
    return s
# 只用县级区划 + 地级市，不用街道（街道是乡镇级，register 太低）
county=[]
for f in ["areas.json","cities.json"]:
    for d in json.load(open(f)):
        s=stem(d["name"])
        if s: county.append(s)
two=[s for s in county if len(s)==2]
print("县市级两字词干:",len(two),"/",len(county))
random.seed(1); print("\n真实样例:"," ".join(random.sample(two,50)))
for pos in range(2):
    c=collections.Counter(s[pos] for s in two)
    print(f"\n第{pos+1}字 top50:"," ".join(f"{ch}{n}" for ch,n in c.most_common(50)))

# ---- Output printed when this code was run on 2026-09-17 ----
# 县市级两字词干: 2529 / 3319
#
# 真实样例: 泉山 营口 松山 罗庄 新兴 措勤 望谟 弥勒 蒙山 上杭 集安 墨脱 怀安 兴宾 道孚 保山 大兴 大方 巩义 铜鼓 荆门 巴彦 天门 隆化 满城 博野 囊谦 灵寿 上思 濂溪 长宁 涿鹿 华池 上犹 金阳 新城 乌恰 铅山 武江 崇仁 彭泽 麒麟 平桥 沙河 市中 于田 道外 颍泉 江岸 逊克
#
# 第1字 top50: 南45 新42 东37 平36 临33 大31 永30 安30 龙29 武27 西26 江24 海23 长23 金23 宁20 兴20 广18 高16 天16 阳15 石15 黄14 宜14 双13 青13 德13 北12 云12 上12 白12 建12 通12 和11 清11 定11 中11 镇11 城11 昌10 河10 宝10 开10 乐10 盐10 三10 铁10 惠10 华10 市10
#
# 第2字 top50: 山133 城128 阳112 安83 江72 宁49 南45 平43 河42 川41 东33 水33 溪30 源29 昌28 西26 海25 湖25 陵24 都23 兴21 台20 化20 德19 中19 北18 口18 丰18 泉16 林16 原15 定14 田14 龙14 华13 和13 门13 泽12 远12 庆11 清11 邑11 兰11 明11 云10 桥10 乐10 顺10 关10 武10
