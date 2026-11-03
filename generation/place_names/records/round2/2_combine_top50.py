# -*- coding: utf-8 -*-
import json,re,itertools,random
SUF=re.compile(r'(自治州|自治县|自治区|地区|街道办事处|街道|镇|乡|区|县|市|州|盟|旗)$')
real=set()
for f in ["areas.json","cities.json","streets.json"]:
    for d in json.load(open(f)):
        n=d["name"]; real.add(n); s=n
        for _ in range(3): s=SUF.sub("",s)
        if s: real.add(s)
# 再加省名和常见别称，避免撞
real |= set("北京 天津 上海 重庆 河北 山西 辽宁 吉林 黑龙江 江苏 浙江 安徽 福建 江西 山东 河南 湖北 湖南 广东 海南 四川 贵州 云南 陕西 甘肃 青海 台湾 内蒙 广西 西藏 宁夏 新疆 香港 澳门".split())

A=list("南新东平临大永安龙武西江海长金宁兴广高天阳石黄宜双青德北云上白建通和清定中镇城昌河宝开乐盐三")
B=list("山城阳安江宁南平河川东水溪源昌西海湖陵都兴台化德中北口丰泉林原定田龙华和门泽远庆清邑兰明云桥乐顺关")
cand=["".join(p) for p in itertools.product(A,B) if p[0]!=p[1]]
free=[c for c in cand if c not in real]
print(f"候选 {len(cand)}, 未撞 {len(free)} ({1-len(free)/len(cand):.0%} 撞车)")
random.seed(42); random.shuffle(free)
open("cand2_county.txt","w").write("\n".join(free))
print()
for i in range(0,120,12): print(" ".join(free[i:i+12]))

# ---- Output printed when this code was run on 2026-09-17 ----
# 候选 2232, 未撞 1212 (46% 撞车)
#
# 阳德 昌林 建兰 和湖 宁清 镇丰 江兰 南邑 中庆 宁口 城宁 开中
# 宜庆 通中 天泉 建江 盐定 兴湖 河海 东德 江林 昌水 高兰 临德
# 德南 白泽 通昌 清昌 云口 黄西 德云 镇顺 和都 清阳 城林 广门
# 黄宁 宜溪 长和 长都 北口 双中 城邑 德桥 盐德 乐东 清顺 中泽
# 德西 通泽 开关 开兰 天川 阳都 石远 永关 昌关 城和 城庆 乐云
# 城源 宝定 昌清 开陵 开桥 金德 建化 阳桥 云江 兴水 乐门 石华
# 三丰 宁丰 德田 新西 宜湖 上庆 临中 临兰 临阳 南兰 阳庆 龙平
# 河德 德林 南德 清山 白源 双宁 龙邑 德乐 城兴 石兴 白德 白华
# 建溪 乐林 清龙 平门 武泉 双南 盐水 建清 江丰 石原 开兴 三东
# 天远 和华 和江 三兰 通田 黄远 镇兰 宜顺 高庆 和山 云平 三北
