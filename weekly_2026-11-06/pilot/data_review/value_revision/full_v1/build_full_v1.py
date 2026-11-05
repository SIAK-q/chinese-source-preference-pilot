# -*- coding: utf-8 -*-
"""修订数据 v1（定稿，151 属性）= 草稿B ＋ 恢复清山图书馆“层数”为冲突属性（用户 11-05 选方案 A）＋ 11-05 送审审核。

命名说明（11-05 用户定）：对外只有“原始数据 → v1”。中间两版改称草稿：草稿A（原 full_v1，149 属性，
draftA_20261104_149/）、草稿B（原 full_v2 草稿，150 属性，draftB_20261105_150/）。本版此前曾称 v3、v2。
3B／7B／Gemma／Llama 的 baseline 运行11–14 用的是草稿B。

依据：notes《修订版数据与baseline》“图书馆层数：恢复方案”节。高度固定 24 米时，按“平均每层高度”
落在三个官方实例（每层约 4.3–7.4 米）附近来选：4 层 6.0 米、5 层 4.8 米、6 层 4.0 米、7 层 3.4 米。
原值 3 层保留。
11-05 送审表审核（用户定“明显反直觉才改”）：4 个补小数的原值恢复旧写法、备选改为同精度自然值；
7 处类别待审建议撤回、恢复草稿前原备选，只保留“全科医生→社区卫生服务中心护士”。见 REVIEW_EDITS。
11-05 全实体相容性筛查后（用户同意三项，codex§349）：在 REVIEW_EDITS 之后再改三个备选，见 COMPAT_EDITS。
输入：draftB_20261105_150/entities_full_v2.jsonl（只读）；输出：entities_full_v1.jsonl、changes_from_draft.json
"""
import copy, hashlib, json
from pathlib import Path
HERE = Path(__file__).resolve().parent
SRC = HERE.parent / "draftB_20261105_150" / "entities_full_v2.jsonl"
OUT = HERE / "entities_full_v1.jsonl"
CHG = HERE / "changes_from_draft.json"
NEW = ["3层", "4层", "5层", "6层", "7层"]
R = "11-05送审审核：只有明显反直觉才改（用户定）"
REVIEW_EDITS = [  # (entity_id, field, new_list, reason)
    ("BUILDING-1", "高度", ["38米", "36米", "37米", "39米", "40米"], "恢复原写法38米，备选取整数米；" + R),
    ("BUILDING-2", "高度", ["24米", "22米", "23米", "25米", "26米"], "恢复原写法24米，备选取整数米；" + R),
    ("EVENT-1", "参与人数", ["2.3万人次", "2.1万人次", "2.2万人次", "2.4万人次", "2.5万人次"], "恢复原写法2.3万人次，备选同为一位小数；" + R),
    ("EVENT-2", "参与人数", ["1.2万人", "1.0万人", "1.1万人", "1.3万人", "1.4万人"], "恢复原写法1.2万人，备选同为一位小数；" + R),
    ("PERSON-1", "学历", ["本科（汉语言文学）", "硕士研究生（学科教学·语文）", "本科（教育学）", "大专（初等教育）", "硕士研究生（课程与教学论）"], "撤回古典文献学替换，恢复大专（初等教育）；" + R),
    ("PERSON-3", "职业", ["三甲医院护士长", "社区卫生服务中心护士", "县医院药剂师", "妇幼保健院助产士", "疾控中心流调员"], "保留全科医生→社区卫生服务中心护士（护理本科任医生明显不对）；撤回ICU护士替换，恢复县医院药剂师；" + R),
    ("PERSON-3", "学历", ["本科（护理学）", "大专（护理）", "硕士研究生（护理学）", "本科（助产学）", "大专（医学检验技术）"], "撤回助产替换，恢复大专（医学检验技术）；" + R),
    ("BUILDING-1", "主体结构", ["钢筋混凝土框架", "钢结构", "钢筋混凝土剪力墙", "预应力混凝土", "钢混组合结构"], "撤回框架-剪力墙替换，恢复预应力混凝土（专业细节，非明显反直觉）；" + R),
    ("BUILDING-2", "主体结构", ["砖混结构", "钢筋混凝土框架", "钢结构", "钢混组合结构", "预应力混凝土"], "同上；" + R),
    ("BUILDING-3", "主体结构", ["钢结构", "钢筋混凝土框架", "预应力混凝土", "钢混组合结构", "膜结构"], "撤回两处替换，恢复预应力混凝土、膜结构；" + R),
]
C = "11-05全实体相容性筛查，用户同意修改（codex§349）"
COMPAT_EDITS = [  # (entity_id, field, old_alt, new_alt, reason)：只换一个备选，原值和其他备选不动
    ("PERSON-3", "职业", "县医院药剂师", "县医院ICU护士",
     "原学历本科（护理学）配药剂师不对口：药剂岗位通常要求药学类专业（未查条文）；换为护理岗位；" + C),
    ("PERSON-3", "学历", "大专（医学检验技术）", "大专（助产）",
     "原职业三甲医院护士长须护士执业注册，《护士条例》第七条（二）要求护理、助产专业课程；医学检验技术不符；" + C),
    ("BUILDING-3", "主体结构", "膜结构", "框架-剪力墙结构",
     "膜结构一般用于屋盖或大跨度围护，不作8层61米建筑的主体结构；框架-剪力墙是常见多高层结构体系；" + C),
]
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
before = sha(SRC)
ents = [json.loads(l) for l in SRC.open(encoding="utf-8") if l.strip()]
out = []
for e in ents:
    e = copy.deepcopy(e)
    if e["id"] == "BUILDING-2":
        assert e["层数"] == "3层", e["层数"]
        e["层数"] = NEW
    for eid, fld, new, _ in REVIEW_EDITS:
        if e["id"] == eid:
            assert fld in e and len(e[fld]) == 5, (eid, fld)
            e[fld] = new
    for eid, fld, old, new, _ in COMPAT_EDITS:
        if e["id"] == eid:
            assert old in e[fld] and e[fld][0] != old, (eid, fld, old)
            e[fld] = [new if v == old else v for v in e[fld]]
    out.append(e)
assert sha(SRC) == before
with OUT.open("w", encoding="utf-8") as f:
    for e in out:
        f.write(json.dumps(e, ensure_ascii=False) + "\n")
SK = {"id", "name", "entity_class", "description", "timeline_id"}
n = sum(1 for e in out for k, v in e.items() if k not in SK and isinstance(v, list))
bad = [(e["id"], k) for e in out for k, v in e.items() if k not in SK and isinstance(v, list) and len(set(v)) != 5]
CHG.write_text(json.dumps({"meta": {"date": "2026-11-05", "input": "draftB_20261105_150/entities_full_v2.jsonl", "input_sha256": before,
    "output_sha256": sha(OUT), "script_sha256": sha(__file__)},
    "summary": {"entities": len(out), "conflict_attributes": n, "pairs": n * 4, "prompts_both_orders": n * 8},
    "problems": bad,
    "changes": [{"entity_id": "BUILDING-2", "name": "清山图书馆", "field": "层数", "draft": "3层（背景，不出题）", "final": NEW,
                 "reason": "恢复为冲突属性；高度固定24米，按平均每层高度接近官方实例（4.3–7.4米/层）选4–7层；1、2层在24米下每层24/12米，不合理",
                 "decided_by": "用户 11-05 选方案A"}]
    + [{"entity_id": eid, "field": fld, "final": new, "reason": why, "decided_by": "用户 11-05 送审表审核"} for eid, fld, new, why in REVIEW_EDITS]
    + [{"entity_id": eid, "field": fld, "old_alt": old, "new_alt": new, "reason": why, "decided_by": "用户 11-05 相容性筛查后同意（codex§349）"} for eid, fld, old, new, why in COMPAT_EDITS]}, ensure_ascii=False, indent=1), encoding="utf-8")
print(n, n * 8, "problems:", bad or "无")
