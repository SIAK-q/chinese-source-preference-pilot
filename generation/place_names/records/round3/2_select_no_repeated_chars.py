# -*- coding: utf-8 -*-
"""贪心选 20 个：全局不重复用字（40 个不同的字），按典型度优先。"""
pool=[l.strip() for l in open("pool50.txt",encoding="utf-8") if l.strip()]
# 排除方位字连用等不自然组合（南东/西东/东西/南西 这类）
DIR=set("东西南北中上下")
bad=lambda x: x[0] in DIR and x[1] in DIR
used=set(); sel=[]
for n in pool:
    if bad(n): continue
    if n[0] in used or n[1] in used: continue
    sel.append(n); used|={n[0],n[1]}
    if len(sel)==26: break
print("贪心结果(26个备选，用字全不重复):")
for i in range(0,len(sel),8): print(" ".join(sel[i:i+8]))
open("sel26.txt","w").write("\n".join(sel))

# ---- Output printed when this code was run on 2026-09-17 ----
# 贪心结果(26个备选，用字全不重复):
# 新山 广城 临阳 永江 青安 平宁 武河 南都
# 大水 兴川 东化 长溪 海源 金西 龙德 天昌
# 宜湖 双陵 高中 黄台 石丰 北口 云泉 白林
# 上原 建定
