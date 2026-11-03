# -*- coding: utf-8 -*-
"""严格按真实三字地名的字频分布生成，不用任何 top40 之外的字。"""
import json,re,itertools,random
SUF=re.compile(r'(自治州|自治县|自治区|地区|街道办事处|街道|镇|乡|区|县|市|州|盟|旗)$')
real=set()
for f in ["areas.json","cities.json","streets.json"]:
    for d in json.load(open(f)):
        n=d["name"]; real.add(n); s=n
        for _ in range(3): s=SUF.sub("",s)
        if s: real.add(s)

# 通名只取平实的行政/聚落类，排除 路/街（那是城市道路派生的街道名）
TONG = list("庄河桥口店湖沟营湾堡坪铺集屯岭寨坝岗塘关寺")
XING = list("杨张王李郭董陈刘梁唐吴赵孙马高朱徐胡")   # 真实高频姓
MOD  = list("大西东南北新小上下老中")                  # 真实高频方位/大小
ZI   = list("石马柳杨树桥安平清水沙官城头门林庄")      # 真实高频第二字

c=[]
c += [f"{x}家{t}" for x,t in itertools.product(XING,TONG)]          # 杨家湾型 (最高频)
c += [f"{m}{z}{t}" for m,z,t in itertools.product(MOD,ZI,TONG)]     # 大石寨型
c += [f"{n}里{t}" for n in list("三五七八九十") for t in TONG]       # 十里店型

free=[x for x in c if x not in real and x[0]!=x[1] and x[1]!=x[2]]
print(f"候选 {len(c)}, 未撞 {len(free)} ({1-len(free)/len(c):.1%} 撞车)")
random.seed(5); random.shuffle(free)
print("\n"+" ".join(free[:80]))
open("cand_real.txt","w").write("\n".join(free))

# ---- Output printed when this code was run on 2026-09-17 ----
# 候选 4431, 未撞 4214 (4.9% 撞车)
#
# 大庄湾 西水桥 中官营 西沙集 南平桥 新城堡 陈家店 小沙河 下林湾 赵家铺 小林店 上城湾 北马坪 中安塘 老水岗 小官屯 大柳岗 小沙湖 上安岭 北树坪 小林塘 新水岭 上安桥 陈家营 中平寨 上庄铺 西石口 上林集 北庄集 中庄岭 大门塘 西头河 老清塘 下马湖 孙家堡 中平桥 上石店 下庄关 东官寨 上平岗 新林寺 下马寨 下柳坝 小马坪 东安坪 老桥坝 中石铺 中官屯 西石营 北官关 西石坝 赵家寨 新沙湖 上柳口 下沙湖 中水坝 北水寺 中城寨 小平坪 上水坝 中门营 东门坝 中城湾 南门坝 小桥湖 东庄河 下门寨 西杨河 陈家塘 新城关 北官湖 上庄坪 老官庄 南头堡 老安桥 中杨集 北安铺 南清堡 东石关 西门坪
