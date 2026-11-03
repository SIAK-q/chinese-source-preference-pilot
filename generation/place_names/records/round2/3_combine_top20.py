# -*- coding: utf-8 -*-
"""只保留两个字都在各自位置 top20 的组合（最典型的县市名构词）。"""
import json,re,collections,itertools
SUF=re.compile(r'(自治州|自治县|自治区|地区|街道办事处|街道|镇|乡|区|县|市|州|盟|旗)$')
def stem(n):
    s=n
    for _ in range(3): s=SUF.sub("",s)
    return s
real=set()
for f in ["areas.json","cities.json","streets.json"]:
    for d in json.load(open(f)):
        real.add(d["name"]); 
        s=stem(d["name"])
        if s: real.add(s)
real|=set("北京 天津 上海 重庆 河北 山西 辽宁 吉林 黑龙江 江苏 浙江 安徽 福建 江西 山东 河南 湖北 湖南 广东 海南 四川 贵州 云南 陕西 甘肃 青海 台湾 内蒙 广西 西藏 宁夏 新疆 香港 澳门".split())
two=[stem(d["name"]) for f in ["areas.json","cities.json"] for d in json.load(open(f)) if len(stem(d["name"]))==2]
c1=collections.Counter(s[0] for s in two); c2=collections.Counter(s[1] for s in two)
A=[ch for ch,_ in c1.most_common(20)]; B=[ch for ch,_ in c2.most_common(20)]
print("A(top20):"," ".join(A)); print("B(top20):"," ".join(B))
free=["".join(p) for p in itertools.product(A,B) if p[0]!=p[1] and "".join(p) not in real]
print(f"\n最典型组合 {len(A)*len(B)} 个, 未撞 {len(free)}")
print()
for i in range(0,len(free),12): print(" ".join(free[i:i+12]))
open("county_top.txt","w").write("\n".join(free))

# ---- Output printed when this code was run on 2026-09-17 ----
# A(top20): 南 新 东 平 临 大 永 安 龙 武 西 江 海 长 金 宁 兴 广 高 天
# B(top20): 山 城 阳 安 江 宁 南 平 河 川 东 水 溪 源 昌 西 海 湖 陵 都
#
# 最典型组合 400 个, 未撞 98
#
# 南东 南西 南都 新山 新川 新水 新西 新陵 东西 平宁 临阳 临宁
# 临东 临源 临昌 临陵 临都 大水 大西 大陵 大都 永山 永江 永南
# 永河 永东 永水 永溪 永西 永海 永都 安河 安川 安水 安湖 龙宁
# 龙平 武河 武源 武西 武海 西东 西都 江水 江昌 海平 海水 海源
# 海湖 海都 长南 长溪 长源 长昌 长都 金宁 金西 宁山 宁川 宁水
# 宁源 宁昌 宁湖 兴阳 兴河 兴川 兴水 兴溪 兴昌 兴西 兴湖 兴陵
# 兴都 广山 广城 广江 广溪 广湖 广都 高江 高宁 高南 高水 高源
# 高西 高海 天阳 天江 天南 天川 天东 天溪 天源 天昌 天西 天海
# 天陵 天都
