# -*- coding: utf-8 -*-
"""任务6：分析无信源 baseline（run_baseline.py 的输出）。

做法见 data_review/prompt_translation/COMPARE.md 末节（WFW附录B、C）：
  1. 位置偏差：P(选表二) 的平均，全部和分表序；
  2. 备选胜率：P(选备选) 按概率平均，分表序和合并都报，另附硬计数作参照；
  3. 每题四种模式：两种表序都选表一 / 都选表二（看位置）、都选备选 / 都选原值（看内容）；
  4. 按值的大小方向拆分（备选比原值大/晚 vs 小/早）；
  5. 逐题清单：两种表序都强烈偏向同一个值的题，提示取值可能不合理（阈值是本项目建议，不是WFW规定）。

运行：python pilot/analyze_baseline.py pilot/results_baseline/Qwen2.5-3B-Instruct/raw.json
"""
import json
import re
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path
from statistics import mean

STRONG = 0.8   # 两种表序都 >0.8（或都 <0.2）才列入逐题清单；本项目建议值
N_BOOT = 10000  # 置信区间：按“原值–备选对”重抽样；次数同WFW的bootstrap（§3.3，helpers/evaluation.py:253 b=10_000）


def boot_ci(vals, seed=0):
    """95% bootstrap 区间（百分数），重抽样单位是原值–备选对。"""
    import random
    rnd, m = random.Random(seed), len(vals)
    means = sorted(sum(vals[rnd.randrange(m)] for _ in range(m)) / m for _ in range(N_BOOT))
    return [round(100 * means[int(0.025 * N_BOOT)], 1), round(100 * means[int(0.975 * N_BOOT)], 1)]


def wfw_position_bias(rows):
    """对应 WFW helpers/evaluation.py:84 calculate_position_bias（两选项、无中立项）。"""
    n = len(rows)
    return {"选项A硬胜率%": pct(sum(r["prob_a"] > r["prob_b"] for r in rows) / n),
            "选项B硬胜率%": pct(sum(r["prob_b"] > r["prob_a"] for r in rows) / n),
            "平局率%": pct(sum(r["prob_a"] == r["prob_b"] for r in rows) / n),
            "选项A平均概率%": pct(mean(r["prob_a"] for r in rows)),
            "选项B平均概率%": pct(mean(r["prob_b"] for r in rows)),
            "题数": n}

UNIT = {"万": 10 ** 4, "亿": 10 ** 8}


def to_number(s):
    """数值/日期/年月/年份 → 可比较的数；不能比较（类别、保修）返回 None。"""
    m = re.fullmatch(r"(\d+)小时(?:(\d+)分钟)?", s)
    if m:
        return int(m[1]) * 60 + int(m[2] or 0)
    m = re.fullmatch(r"(\d{4})年(\d{1,2})月(\d{1,2})日", s)
    if m:
        return date(int(m[1]), int(m[2]), int(m[3])).toordinal()
    m = re.fullmatch(r"(\d{4})年(\d{1,2})月", s)
    if m:
        return int(m[1]) * 12 + int(m[2])
    m = re.fullmatch(r"(\d{4})年", s)
    if m:
        return int(m[1])
    m = re.fullmatch(r"(?:下辖)?(\d+(?:\.\d+)?)(万|亿)?(人次|人|元人民币|厘米|公斤|吨|平方公里|米|层|天|个乡镇)", s)
    if m:
        return float(m[1]) * UNIT.get(m[2] or "", 1)
    return None


def pct(x):
    return round(100 * x, 1)


def main(raw_path):
    raw_path = Path(raw_path)
    d = json.loads(raw_path.read_text(encoding="utf-8"))
    rows = d["results"]
    for r in rows:
        r["p_alt"] = r["prob_b"] if r["order"] == 0 else r["prob_a"]

    # 1–2. 位置偏差、备选胜率
    by_order = {o: [r for r in rows if r["order"] == o] for o in (0, 1)}
    position = {"全部": pct(mean(r["prob_b"] for r in rows)),
                **{f"表序{o}": pct(mean(r["prob_b"] for r in by_order[o])) for o in (0, 1)}}
    alt_soft = {"合并": pct(mean(r["p_alt"] for r in rows)),
                **{f"表序{o}": pct(mean(r["p_alt"] for r in by_order[o])) for o in (0, 1)}}
    alt_hard = {"合并": pct(mean(r["p_alt"] > 0.5 for r in rows)),
                **{f"表序{o}": pct(mean(r["p_alt"] > 0.5 for r in by_order[o])) for o in (0, 1)}}

    # 3. 每题（原值–备选对）两种表序
    pairs = defaultdict(dict)
    for r in rows:
        pairs[(r["entity_id"], r["field"], r["alt_index"])][r["order"]] = r
    items, modes = [], defaultdict(int)
    for (eid, f, i), od in pairs.items():
        if set(od) != {0, 1}:
            continue
        p0, p1 = od[0]["p_alt"], od[1]["p_alt"]
        if p0 == 0.5 or p1 == 0.5:
            mode = "至少一种表序平局"
        elif p0 > 0.5 and p1 > 0.5:
            mode = "两种表序都选备选"
        elif p0 < 0.5 and p1 < 0.5:
            mode = "两种表序都选原值"
        elif p0 > 0.5 and p1 < 0.5:
            mode = "两种表序都选表二"
        else:
            mode = "两种表序都选表一"
        modes[mode] += 1
        o, a = od[0]["original"], od[0]["alternative"]
        no, na = to_number(o), to_number(a)
        direction = None if no is None or na is None else ("备选更大/更晚" if na > no else "备选更小/更早")
        items.append({"entity_id": eid, "entity_class": od[0]["entity_class"], "field": f, "alt_index": i,
                      "original": o, "alternative": a, "p_alt_order0": round(p0, 3), "p_alt_order1": round(p1, 3),
                      "content_pref_alt": round((p0 + p1) / 2, 3), "position_pref_table2": round((p0 + 1 - p1) / 2, 3),
                      "mode": mode, "direction": direction})
    n_items = len(items)

    # 4. 方向拆分
    direction = {}
    for k in ("备选更大/更晚", "备选更小/更早"):
        sub = [x for x in items if x["direction"] == k]
        if sub:
            direction[k] = {"题数": len(sub), "P(选备选)均值": pct(mean(x["content_pref_alt"] for x in sub))}
    direction["不可比（类别、保修）"] = {"题数": sum(x["direction"] is None for x in items)}

    # 按备选序号、实体类型
    by_alt = {i: pct(mean(x["content_pref_alt"] for x in items if x["alt_index"] == i))
              for i in sorted({x["alt_index"] for x in items})}
    by_class = {c: pct(mean(x["content_pref_alt"] for x in items if x["entity_class"] == c))
                for c in sorted({x["entity_class"] for x in items})}

    # WFW 口径（附录B、C）＋置信区间＋按字段
    wfw = {"位置偏差_WFW口径": {"全部": wfw_position_bias(rows),
                              **{f"表序{o}": wfw_position_bias(by_order[o]) for o in (0, 1)}},
           "P选表二_95%区间": boot_ci([x["position_pref_table2"] for x in items]),
           "P选备选_95%区间": boot_ci([x["content_pref_alt"] for x in items])}
    by_field = {}
    for f in sorted({x["field"] for x in items}):
        sub = [x for x in items if x["field"] == f]
        by_field[f] = {"对数": len(sub), "P选备选%": pct(mean(x["content_pref_alt"] for x in sub)),
                       "P选表二%": pct(mean(x["position_pref_table2"] for x in sub))}

    # 5. 逐题清单
    strong = [x for x in items if (x["p_alt_order0"] > STRONG and x["p_alt_order1"] > STRONG)
              or (x["p_alt_order0"] < 1 - STRONG and x["p_alt_order1"] < 1 - STRONG)]

    result = {
        "model": d["model"], "data": d["data"], "data_sha256": d["data_sha256"], "alts": d["alts"],
        "n_prompts": len(rows), "n_pairs": n_items,
        "位置偏差_P选表二": position,
        "备选胜率_概率平均": alt_soft,
        "备选胜率_硬计数_仅参照": alt_hard,
        "每题模式": {k: {"题数": v, "占比": pct(v / n_items)} for k, v in sorted(modes.items())},
        "值方向": direction,
        "按备选序号_P选备选": by_alt,
        "按实体类型_P选备选": by_class,
        **wfw,
        "按字段": by_field,
        "两种表序都强烈偏向同一值": {"阈值": STRONG, "题数": len(strong),
                               "清单": sorted(strong, key=lambda x: x["content_pref_alt"])},
        "逐题": items,
        "说明": "备选胜率约50%本身不能证明两个值同样可信：纯位置策略也会得到约50%。看每题模式和逐题清单。",
    }
    out_dir = raw_path.parent
    sfx = "" if raw_path.stem == "raw" else f"_{raw_path.stem}"   # 试跑的 raw_limit.json 不覆盖全量结果
    (out_dir / f"analysis{sfx}.json").write_text(json.dumps(result, ensure_ascii=False, indent=1), encoding="utf-8")

    m = result["每题模式"]
    lines = [
        f"# 无信源 baseline：{d['model']}",
        "",
        f"数据 `{d['data']}`（SHA256 {d['data_sha256'][:16]}…），备选 {d['alts']}，{n_items} 对 × 2 种表序 = {len(rows)} 题。",
        "",
        f"- 位置偏差：P(选表二) = {position['全部']}%（95%区间 {wfw['P选表二_95%区间']}；表序0 {position['表序0']}%，表序1 {position['表序1']}%）。"
        f"WFW口径：选项B硬胜率 {wfw['位置偏差_WFW口径']['全部']['选项B硬胜率%']}%，平局 {wfw['位置偏差_WFW口径']['全部']['平局率%']}%。",
        f"- 备选胜率（概率平均）：合并 {alt_soft['合并']}%（95%区间 {wfw['P选备选_95%区间']}；表序0 {alt_soft['表序0']}%，表序1 {alt_soft['表序1']}%）；"
        f"硬计数合并 {alt_hard['合并']}%（每题P(选备选)>0.5计一胜，仅参照；WFW附录C未写明用哪种算法）。",
        "- 每题模式：" + "；".join(f"{k} {v['题数']}（{v['占比']}%）" for k, v in m.items()) + "。",
        "- 值方向：" + "；".join(f"{k} {v['题数']}题" + (f"，P(选备选) {v['P(选备选)均值']}%" if "P(选备选)均值" in v else "")
                               for k, v in direction.items()) + "。",
        f"- 两种表序都强烈偏向同一值（>{STRONG}）：{len(strong)} 题，清单见 analysis.json。",
        "",
        result["说明"],
    ]
    (out_dir / f"summary{sfx}.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "pilot/results_baseline/Qwen2.5-3B-Instruct/raw.json")
