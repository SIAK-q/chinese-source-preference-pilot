pool=[l.strip() for l in open("pool50.txt",encoding="utf-8") if l.strip()]
DIR=set("东西南北中上下")
BADWORD={"高中","上原","南都","大水","东化","金西","北口","白林","建定","市城","市阳","市安","市江","市宁","南中","高南","长南","永南"}
used=set(); sel=[]
for n in pool:
    if n[0] in DIR and n[1] in DIR: continue
    if n in BADWORD: continue
    if n[0]=="市" or n[1]=="市": continue
    if n[0] in used or n[1] in used: continue
    sel.append(n); used|={n[0],n[1]}
    if len(sel)==40: break
for i in range(0,len(sel),8): print(" ".join(sel[i:i+8]))
open("sel40.txt","w").write("\n".join(sel))

# ---- Output printed when this code was run on 2026-09-17 ----
# 新山 广城 临阳 永江 青安 平宁 武河 南化
# 兴川 大西 东德 海水 长溪 龙北 高源 天昌
# 金丰 宜湖 石都 双陵 黄台 通中 云口 上泉
# 建林 白原 和定 清田 镇华 宝门 乐泽 盐远
# 开庆 三邑 铁兰 惠明
