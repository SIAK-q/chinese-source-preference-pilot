# -*- coding: utf-8 -*-
"""v1 全实体相容性筛查（codex§348，2026-11-05）。

按实际组题：每次只把一个属性换成一个备选，其他属性取原值；另查 30 个原始实体。
不做笛卡尔积，不按下标拼多个备选。只算筛查指标，不判定对错；类别关系由人工逐项看。
输入：full_v1/entities_full_v1.jsonl（只读）；输出：compat_check_v1.json
运行：python3 pilot/data_review/value_revision/full_v1/compat_check_v1.py
"""
import hashlib, json, re
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / "entities_full_v1.jsonl"
OUT = HERE / "compat_check_v1.json"
SK = {"id", "name", "entity_class", "description", "timeline_id"}
num = lambda s: float(re.search(r"[\d.]+", s).group())


def metrics(e):
    c = e["entity_class"]
    m = {}
    if c == "person":
        h, w = num(e["身高"]) / 100, num(e["体重"])
        m["BMI"] = round(w / h / h, 1)
        m["出生年"] = int(num(e["出生日期"]))
    elif c == "organization":
        m["人均营收_万元"] = round(num(e["年营业额"]) * 1e4 / num(e["员工人数"]), 1)
        m["行业"] = e["所属行业"]
    elif c == "location":
        m["人口密度_人每平方公里"] = round(num(e["人口"]) * 1e4 / num(e["面积"]))
        m["每乡镇面积_平方公里"] = round(num(e["面积"]) / num(e["下辖乡镇数"]))
    elif c == "building":
        m["平均层高_米"] = round(num(e["高度"]) / num(e["层数"]), 1)
        m["结构"] = e["主体结构"]
    elif c == "event":
        m["人均预算_元"] = round(num(e["预算"]) * 1e4 / (num(e["参与人数"]) * (1e4 if "万" in e["参与人数"] else 1)))
    return m


def orig(e):
    return {k: (v[0] if isinstance(v, list) else v) for k, v in e.items()}


ents = [json.loads(l) for l in SRC.open(encoding="utf-8") if l.strip()]
rows, n_combo = [], 0
for e in ents:
    base = orig(e)
    rows.append({"id": e["id"], "name": e["name"], "changed": None, "value": None, "metrics": metrics(base)})
    for k, v in e.items():
        if k in SK or not isinstance(v, list):
            continue
        for alt in v[1:]:
            x = dict(base); x[k] = alt
            rows.append({"id": e["id"], "name": e["name"], "changed": k, "value": alt, "metrics": metrics(x)})
            n_combo += 1


def rng(cls, key):
    vals = [r["metrics"][key] for r in rows if key in r["metrics"]]
    return [min(vals), max(vals)] if vals else None


summary = {"entities": len(ents), "single_alt_combos": n_combo, "original_entities": len(ents),
           "ranges": {k: rng(None, k) for k in ["BMI", "人均营收_万元", "人口密度_人每平方公里", "每乡镇面积_平方公里", "平均层高_米", "人均预算_元"]}}
OUT.write_text(json.dumps({"meta": {"date": "2026-11-05", "input": "full_v1/entities_full_v1.jsonl",
                                    "input_sha256": hashlib.sha256(SRC.read_bytes()).hexdigest(),
                                    "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},
                           "summary": summary, "rows": rows}, ensure_ascii=False, indent=1), encoding="utf-8")
print(json.dumps(summary, ensure_ascii=False))
for r in rows:
    if r["id"].startswith(("ORG", "BUILDING")) and r["changed"] in (None, "所属行业", "层数", "高度", "主体结构", "员工人数", "年营业额"):
        print(r["id"], r["changed"], r["value"], r["metrics"])
