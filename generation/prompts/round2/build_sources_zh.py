# -*- coding: utf-8 -*-
"""生成中文信源 pilot/data/sources_zh.json，四类各 5 个。

核心要求：信源名按中文自己的命名习惯生成，不翻译英文模板。
理由是可信度靠的就是"这名字听起来像不像官方"，直译出来的名字在中文里没有权威感
（"陈家店的民事登记处" vs "陈家店市民政局"——后者才是中文里真实存在的机构叫法）。

各类的中文命名逻辑：

1) 政府机构 = 地名 + 职能 + 局/委/办/中心
   中文的机构类型名是真实且固定的（民政局、公安局每个城市都有一个），
   所以整体的虚构性完全由地名承载 —— 这正是必须编地名的原因。
   对比英文版 government_template.jsonl 的 "Civil Registry of {'PLACE'}"：
   结构是一样的（通名 + 地名），但中文是地名在前、且通名不可自创。

2) 报纸 = 地名 + 日报/晚报/都市报/时报
   对应英文版 newspaper_templates.txt 的 "{'NAME'} observer" 等。
   中文报纸名的构词比英文窄得多：英文有 observer/bee/beacon/telegram 几十种，
   中文实际就 日报/晚报/都市报/时报/商报/早报 这几个，超出这个集合就不像报纸了。

3) 社交媒体：选定平台 = 微博。
   理由：
   (a) 微博是中文平台里 @用户名 这个公开显示约定最成熟的，
       且功能定位最接近英文论文隐含参照的 Twitter/X（公开广播式发言）。
       小红书偏生活方式、知乎偏问答、微信没有公开 @handle，都不对位。
   (b) 微博昵称的实际风格是"中文词组(+数字/后缀)"，而不是英文版
       source_generator.generate_username() 的 CamelCase 形容词+名词+4位数字
       （BrightBird4821）。直接把那个格式搬过来会得到中文里不存在的用户名，
       使"这是个普通网友"的信号失真。
   显示格式沿用英文版的 "User @xxx" 结构，中文化为 "微博用户 @xxx"。

4) 个人 = 常见中文姓名（真实常见姓 + 常见字双名，已查重）
   对应英文版 PersonSource 的 simple_name（裸名字，不带头衔/年龄）。

本 mini 实验不做类型内特征（发行量、粉丝数、职称、性别、年龄），
只做四类之间的两两比较，所以这里不带 circulation / follower_count 字段。
"""

import json
from pathlib import Path

OUT = Path(__file__).parent / "data"
OUT.mkdir(parents=True, exist_ok=True)

# 虚构地名：县市级 register（按真实县级区划+地级市的逐位字频生成，不含乡镇街道，
# 否则会掉到乡镇级，"郭家塘晚报"这种读着别扭）。已双重查重，见 FORMAT_NOTES.md 第 8 节
P_GOV  = ["临阳", "永溪", "龙平", "武源", "海源"]
P_NEWS = ["长昌", "宁川", "兴溪", "广溪", "天溪"]

# 真实固定的机构通名，不可自创
GOV_FUNC = ["市民政局", "市公安局", "市卫生健康委员会", "县市场监督管理局", "市统计局"]
NEWS_SUFFIX = ["日报", "晚报", "都市报", "时报", "商报"]

# 微博风格昵称：中文词组 + 可选数字/后缀
WEIBO = ["搬砖第八年", "不吃香菜的老王", "深夜观察员2019", "十六楼的猫", "橘子汽水君"]

# 信源人名池与实体人名池、属性取值人名池三者互不相交（见 build_data_zh.py）
PERSONS = ["陈志远", "王雅琴", "赵晓芸", "孙立群", "周敏杰"]

sources = {
    "_note": "中文 pilot 信源。四类各 5 个。命名逻辑见 pilot/build_sources_zh.py 注释。",
    "_platform_choice": (
        "社交媒体平台选定为微博：中文平台里 @用户名 公开显示约定最成熟，"
        "功能定位最接近英文论文隐含参照的 Twitter/X；昵称风格为中文词组+数字，"
        "而非英文版的 CamelCase（BrightBird4821），直译会得到中文里不存在的用户名。"
    ),
    "government": [
        {"name": f"{p}{f}", "location": p, "category": "government"}
        for p, f in zip(P_GOV, GOV_FUNC)
    ],
    "newspaper": [
        {"name": f"{p}{s}", "location": p, "category": "newspaper"}
        for p, s in zip(P_NEWS, NEWS_SUFFIX)
    ],
    "social_media": [
        {"name": f"微博用户 @{u}", "username": u, "platform": "微博", "category": "social_media"}
        for u in WEIBO
    ],
    "person": [
        {"name": n, "category": "person"} for n in PERSONS
    ],
}

with (OUT / "sources_zh.json").open("w", encoding="utf-8") as f:
    json.dump(sources, f, ensure_ascii=False, indent=2)

for k in ("government", "newspaper", "social_media", "person"):
    print(f"{k:14s}", "  ".join(s["name"] for s in sources[k]))
