"""Baseline诊断（Claude，2026-11-20）：属性层面的偏好值分布、冲突行位置、表长。
只读已有baseline结果，不跑推理、不改数据。
用法（在 pilot/ 下）：python work_records/2026-11-19-claude-baseline-diagnostics/diagnostics.py
输出：同目录 per_pair.csv、by_field.csv、by_position.csv、by_length.csv、summary.json
"""
import csv, hashlib, json, re, sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
PILOT = HERE.parents[1]
DATA = PILOT / "data_generation/final70_20261118_v2/entities_zh.jsonl"
DATA_SHA = "80f71b7a27ab91017ea78da350849d0f3176b80a1cd0ea56ebb4301a4a64ca38"
RUNS = {
    "GLM-4-9B (Kaggle FP16)": "results_baseline/kaggle_final70_20261118/GLM-4-9B-0414_kaggle_fp16_final70_v2",
    "Llama-3.1-8B (Kaggle FP16)": "results_baseline/kaggle_final70_20261118/Llama-3.1-8B-Instruct_kaggle_fp16_final70_v2",
    "Qwen2.5-7B (Kaggle FP16)": "results_baseline/kaggle_final70_20261118/Qwen2.5-7B-Instruct_kaggle_fp16_final70_v2",
    "Qwen2.5-14B (AutoDL BF16)": "results_baseline/Qwen2.5-14B-Instruct_autodl_bf16_final70_v2",
    "Qwen2.5-32B (AutoDL BF16)": "results_baseline/Qwen2.5-32B-Instruct_autodl_bf16_final70_v2",
}
STRONG = 0.8          # 两种表序都以>80%概率选同一值
# 预先定的位置三段：冲突行在非"名称"数据行中的序号k（1..m），相对位置 r=(k-1)/(m-1)
# 上段 r<1/3，中段 1/3<=r<=2/3，下段 r>2/3
EDU = {"中专": 1, "大专": 2, "本科": 3, "硕士研究生": 4}


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def order_value(field, v):
    """可比较大小的值 → 数字；不可比返回None。日期按年月日，保修按月，学历按层级。"""
    s = str(v)
    if field == "学历":
        return EDU.get(s.split("（")[0])
    m = re.fullmatch(r"(\d{4})年(?:(\d{1,2})月)?(?:(\d{1,2})日)?", s)
    if m:
        return int(m[1]) * 10000 + int(m[2] or 0) * 100 + int(m[3] or 0)
    nums = re.findall(r"\d+(?:\.\d+)?", s.replace(",", ""))
    if len(nums) == 1 and re.fullmatch(r"[\d.,]+\s*[^\d\s（）()]*", s):
        x = float(nums[0])
        if "万" in s:
            x *= 1e4
        if "亿" in s:
            x *= 1e8
        if field == "保修期" and "年" in s:
            x *= 12
        return x
    return None


def table_rows(user):
    """表一的数据行（字段名列表），不含表头和分隔行。"""
    t1 = user.split("表一：", 1)[1].split("表二：", 1)[0]
    rows = []
    for line in t1.strip().splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) != 2 or cells[0] in ("字段",) or set(cells[0]) <= set("-"):
            continue
        rows.append(cells[0])
    return rows


def main():
    assert sha(DATA) == DATA_SHA, "数据SHA不符"
    ents = {e["id"]: e for e in map(json.loads, DATA.open(encoding="utf-8"))}
    inputs = {"data": DATA_SHA}
    per_pair = []
    for model, d in RUNS.items():
        d = PILOT / d
        raw = json.loads((d / "raw.json").read_text())
        assert raw["data_sha256"] == DATA_SHA and raw["n_records"] == 3040, model
        inputs[model] = {"raw.json": sha(d / "raw.json"), "prompts.jsonl": sha(d / "prompts.jsonl")}
        prompts = {}
        for line in (d / "prompts.jsonl").open(encoding="utf-8"):
            p = json.loads(line)
            prompts[(p["entity_id"], p["field"], p["alt_index"], p["order"])] = p["user"]
        pairs = defaultdict(dict)
        for r in raw["results"]:
            pairs[(r["entity_id"], r["field"], r["alt_index"])][r["order"]] = r
        for (eid, field, ai), o in pairs.items():
            assert set(o) == {0, 1}
            r0, r1 = o[0], o[1]
            assert r0["value_a"] == r0["original"] and r1["value_b"] == r1["original"]
            p_alt0, p_alt1 = r0["prob_b"], r1["prob_a"]          # 两种表序下选备选的概率
            rows0 = table_rows(prompts[(eid, field, ai, 0)])
            rows1 = table_rows(prompts[(eid, field, ai, 1)])
            assert rows0 == rows1 == ["名称"] + ents[eid]["row_order"], (model, eid)
            m = len(rows0) - 1                                   # 不含"名称"的数据行
            k = rows0.index(field)                               # 名称为第0行，故k即非名称序号1..m
            rel = (k - 1) / (m - 1)
            seg = "上" if rel < 1 / 3 else ("下" if rel > 2 / 3 else "中")
            vo, va = order_value(field, r0["original"]), order_value(field, r0["alternative"])
            direction = None
            if vo is not None and va is not None and vo != va:
                direction = "备选更高" if va > vo else "备选更低"
            strong = "原值" if max(p_alt0, p_alt1) < 1 - STRONG else ("备选" if min(p_alt0, p_alt1) > STRONG else "")
            per_pair.append({
                "model": model, "entity_id": eid, "entity_class": ents[eid]["entity_class"], "field": field,
                "alt_index": ai, "original": r0["original"], "alternative": r0["alternative"],
                "p_alt_order0": round(p_alt0, 4), "p_alt_order1": round(p_alt1, 4),
                "p_alt_mean": round((p_alt0 + p_alt1) / 2, 4),
                "p_table2_mean": round((r0["prob_b"] + r1["prob_b"]) / 2, 4),
                "strong": strong, "direction": direction or "",
                "rows_data": m, "conflict_row": k, "segment": seg,
            })

    # 复算锚点
    anchors = {"GLM-4-9B (Kaggle FP16)": (74, 83), "Llama-3.1-8B (Kaggle FP16)": (123, 127),
               "Qwen2.5-7B (Kaggle FP16)": (167, 148), "Qwen2.5-14B (AutoDL BF16)": (257, 276),
               "Qwen2.5-32B (AutoDL BF16)": (339, 373)}
    check = {}
    for model, (a, b) in anchors.items():
        got = (sum(1 for x in per_pair if x["model"] == model and x["strong"] == "原值"),
               sum(1 for x in per_pair if x["model"] == model and x["strong"] == "备选"))
        check[model] = {"expected": [a, b], "got": list(got), "ok": got == (a, b)}

    def agg(rows):
        n = len(rows)
        return {"pairs": n,
                "entities": len({x["entity_id"] for x in rows}),
                "mean_p_alt": round(sum(x["p_alt_mean"] for x in rows) / n, 3) if n else None,
                "mean_p_table2": round(sum(x["p_table2_mean"] for x in rows) / n, 3) if n else None,
                "strong_orig": sum(x["strong"] == "原值" for x in rows),
                "strong_alt": sum(x["strong"] == "备选" for x in rows),
                "strong_share": round(sum(bool(x["strong"]) for x in rows) / n, 3) if n else None}

    by_field, by_pos, by_len = [], [], []
    for model in RUNS:
        mrows = [x for x in per_pair if x["model"] == model]
        groups = defaultdict(list)
        for x in mrows:
            groups[(x["entity_class"], x["field"])].append(x)
        for (cls, field), rows in sorted(groups.items()):
            a = agg(rows)
            up = [x for x in rows if x["direction"] == "备选更高"]
            dn = [x for x in rows if x["direction"] == "备选更低"]
            # 强偏好题中被偏好的值是"较高"还是"较低"
            pref_high = sum(1 for x in rows if x["strong"] and x["direction"] and
                            ((x["strong"] == "备选") == (x["direction"] == "备选更高")))
            pref_low = sum(1 for x in rows if x["strong"] and x["direction"]) - pref_high
            by_field.append({"model": model, "entity_class": cls, "field": field, **a,
                             "p_alt_when_alt_higher": round(sum(x["p_alt_mean"] for x in up) / len(up), 3) if up else "",
                             "p_alt_when_alt_lower": round(sum(x["p_alt_mean"] for x in dn) / len(dn), 3) if dn else "",
                             "strong_pref_higher": pref_high if (up or dn) else "",
                             "strong_pref_lower": pref_low if (up or dn) else ""})
        for seg in "上中下":
            rows = [x for x in mrows if x["segment"] == seg]
            by_pos.append({"model": model, "entity_class": "全部", "segment": seg, **agg(rows)})
            for cls in sorted({x["entity_class"] for x in rows}):
                by_pos.append({"model": model, "entity_class": cls, "segment": seg,
                               **agg([x for x in rows if x["entity_class"] == cls])})
        for m in sorted({x["rows_data"] for x in mrows}):
            rows = [x for x in mrows if x["rows_data"] == m]
            by_len.append({"model": model, "rows_data": m,
                           "classes": "、".join(sorted({x["entity_class"] for x in rows})), **agg(rows)})

    def write(name, rows):
        with (HERE / name).open("w", encoding="utf-8-sig", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            w.writeheader()
            w.writerows(rows)

    write("per_pair.csv", per_pair)
    write("by_field.csv", by_field)
    write("by_position.csv", by_pos)
    write("by_length.csv", by_len)
    out = {"date": "2026-11-20", "actor": "Claude", "script_sha256": sha(__file__), "inputs": inputs,
           "strong_threshold": STRONG, "segments": "非名称数据行相对位置 r=(k-1)/(m-1)：上 r<1/3，中 1/3–2/3，下 r>2/3",
           "anchor_check": check}
    (HERE / "summary.json").write_text(json.dumps(out, ensure_ascii=False, indent=1))
    print(json.dumps(check, ensure_ascii=False))
    if not all(v["ok"] for v in check.values()):
        sys.exit("锚点不符")


if __name__ == "__main__":
    main()
