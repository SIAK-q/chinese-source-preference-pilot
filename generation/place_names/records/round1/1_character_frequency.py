# -*- coding: utf-8 -*-
import json,re,collections
SUF=re.compile(r'(自治州|自治县|自治区|地区|街道办事处|街道|镇|乡|区|县|市|州|盟|旗)$')
stems=[]
for f in ["areas.json","cities.json","streets.json"]:
    for d in json.load(open(f)):
        s=d["name"]
        for _ in range(3): s=SUF.sub("",s)
        if s: stems.append(s)
three=[s for s in stems if len(s)==3]
print("三字词干数:",len(three),"占比 %.0f%%"%(100*len(three)/len(stems)))
print("\n随机真实三字样例:")
import random; random.seed(3)
print(" ".join(random.sample(three,60)))
for pos in range(3):
    c=collections.Counter(s[pos] for s in three)
    print(f"\n第{pos+1}字 top40:", " ".join(f"{ch}{n}" for ch,n in c.most_common(40)))

# ---- Output printed when this code was run on 2026-09-17 ----
# 三字词干数: 7958 占比 18%
#
# 随机真实三字样例:
# 贝子府 大箕铺 中同街 西湾子 西岗子 盐州路 石桥驿 即墨路 马王堆 新安店 马头铺 东马坊 龙马潭 小苏莽 骆家坝 吴家堡 大石寨 任丘路 碧流台 石门口 金钟山 王舍人 八里营 董家营 嘉应观 兴华路 陈家港 广东路 南宽坪 张百湾 梁家沟 泰山路 郭家屯 宁远堡 羊毛工 狼城岗 金龙湖 河门口 浪卡子 利福塔 构皮滩 新垒头 杨树岭 甲根坝 阿日希 新下陆 唐家口 唐马寨 杨家湾 青龙桥 红旗街 十里店 慈恩寺 金湖路 均州路 七连屿 长江路 东北街 北大街 箭盘山
#
# 第1字 top40: 大381 西168 东157 三144 南136 新132 白120 黄119 小113 石106 北105 五94 马94 金83 张80 王79 高74 龙72 青72 太71 杨71 八70 四60 中60 下59 阿59 红58 长56 上56 沙55 七53 老51 双47 天47 李44 清41 刘41 水38 十38 黑36
#
# 第2字 top40: 家735 里163 山156 河155 子146 龙97 马93 阳90 石87 水84 尔79 道72 平69 花68 官65 城64 大61 华58 王55 头54 门52 沙52 拉51 林48 安47 江45 西43 木42 庄40 各36 海35 桥35 溪35 北33 兴33 树33 台32 南32 营32 东31
#
# 第3字 top40: 路645 山411 庄345 河304 子272 桥249 口210 店187 街186 湖167 沟165 营150 湾141 堡141 坪140 铺125 集116 寺111 屯109 岭100 场91 寨85 坝80 城79 庙78 头76 村74 园73 岗66 塘66 关63 门61 台61 滩58 江55 港45 楼42 里39 川38 溪37
