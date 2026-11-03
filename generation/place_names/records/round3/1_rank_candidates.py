# -*- coding: utf-8 -*-
"""县市级两字地名：top50 字池 + 全局不重复用字，提高多样性。"""
import json,re,collections,itertools,random
SUF=re.compile(r'(自治州|自治县|自治区|地区|街道办事处|街道|镇|乡|区|县|市|州|盟|旗)$')
def stem(n):
    s=n
    for _ in range(3): s=SUF.sub("",s)
    return s
real=set()
for f in ["areas.json","cities.json","streets.json"]:
    for d in json.load(open(f)):
        real.add(d["name"])
        s=stem(d["name"])
        if s: real.add(s)
real|=set("北京 天津 上海 重庆 河北 山西 辽宁 吉林 黑龙江 江苏 浙江 安徽 福建 江西 山东 河南 湖北 湖南 广东 海南 四川 贵州 云南 陕西 甘肃 青海 台湾 内蒙 广西 西藏 宁夏 新疆 香港 澳门".split())
two=[stem(d["name"]) for f in ["areas.json","cities.json"] for d in json.load(open(f)) if len(stem(d["name"]))==2]
c1=collections.Counter(s[0] for s in two); c2=collections.Counter(s[1] for s in two)
A=[ch for ch,_ in c1.most_common(50)]; B=[ch for ch,_ in c2.most_common(50)]
free=["".join(p) for p in itertools.product(A,B) if p[0]!=p[1] and "".join(p) not in real]
print(f"top50×top50 候选 {len(A)*len(B)}, 未撞真实地名 {len(free)}")
# 按"两字在真实地名中的该位置频次之和"排序，频次越高越像真地名
free.sort(key=lambda x:-(c1[x[0]]+c2[x[1]]))
print("\n按典型度排序的前 150 个：")
for i in range(0,150,10):
    print(" ".join(free[i:i+10]))
open("pool50.txt","w").write("\n".join(free))

# ---- Output printed when this code was run on 2026-09-17 ----
# top50×top50 候选 2500, 未撞真实地名 1402
#
# 按典型度排序的前 150 个：
# 新山 永山 宁山 广山 广城 临阳 上山 和山 清山 镇山
# 昌山 黄城 和城 镇城 河城 市城 兴阳 天阳 石阳 黄阳
# 上阳 通阳 清阳 定阳 昌阳 宝阳 乐阳 盐阳 铁阳 市阳
# 永江 青安 白安 清安 城安 河安 盐安 三安 铁安 市安
# 广江 高江 天江 宜江 平宁 云江 白江 建江 新川 和江
# 城江 临宁 河江 宝江 盐江 铁江 惠江 华江 市江 南东
# 龙宁 新水 永南 永河 安河 龙平 金宁 南西 安川 武河
# 南都 新西 长南 新陵 临东 海平 南化 高宁 南德 南中
# 大水 阳宁 石宁 东西 永东 永水 安水 黄宁 宜宁 临源
# 兴河 双宁 德宁 临昌 宁川 兴川 高南 天南 北宁 云宁
# 上宁 白宁 通宁 南原 新口 永溪 阳南 和宁 清宁 镇宁
# 城宁 西东 黄南 宜南 河宁 宝宁 开宁 乐宁 盐宁 三宁
# 铁宁 惠宁 市宁 石平 双南 青南 德南 南泽 南远 东化
# 临陵 大西 江水 天川 阳河 宜平 北南 上南 白南 南庆
# 南清 南邑 南兰 新定 东德 东中 平化 临都 永西 武源
