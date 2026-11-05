# -*- coding: utf-8 -*-
"""整批修订 v1：按已定规则为旧 pilot 全部 30 个实体重新生成数值／日期备选（2026-11-04）。

用途：在调整后的数据上跑无信源 baseline（用户 11-04 要求）。不是最终数据：
营收 ±10%、乡镇数 4→2 这类计数改动是暂定参数，11-06 会上问老师后可能改。

规则来源：《数值合理性检查（自用参考）》§7.1–7.3（用户 11-01 确认）；任务2页 11-04 决定。
- 数值：原值 ±w%（营收 10%，其余 5%）。候选 = 原值 + k×步长（步长按 §7.2 精度，锚定原值，
  所以价格尾数等随原值保留）；取 k = −K, −⌈K/2⌉, +⌈K/2⌉, +K（K = 窗口内最大步数），两侧各两个。
  K < 2 时步长细一位（§7.1 第3条），原值显示同步补一位小数并留痕。
- 完整日期：±365 天，四个区间（−365…−183、−182…−30、30…182、183…365）各随机取一天；举办日期保持星期几不变、月份差 ≤1 个月（§7.2）。
- 年月：±12 个月，四个区间各取一个。纯年份：−2, −1, +1, +2。日期不晚于 2025-12-31。
- 计数（乡镇数、层数、天数）：n−2, n−1, n+1, n+2，去掉 ≤0；不足 4 个 → 该字段转为背景。
- 保修期：结构不变，每个备选只改一个分量，取相邻常用档位。
- 类别字段：沿用旧备选；只应用已定的个别替换（REPLACE）。
- 固定停用：EVENT-2 马拉松不设持续时间（§7.3-2）；BUILDING-2 层数转背景（演示同；下一版重建原表）。
随机数：每个 (实体, 字段) 用 random.Random(f"42:{实体}:{字段}")，与处理顺序无关，可复现。

输入：pilot/data/entities_zh.jsonl（只读，前后核 SHA256）
输出（本目录）：entities_full_v1.jsonl、changes_full_v1.json
运行：.venv/bin/python pilot/data_review/value_revision/full_v1/build_full_v1.py
"""
import copy
import hashlib
import json
import math
import random
import re
import sys
from datetime import date, timedelta
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

HERE = Path(__file__).resolve().parent
PILOT = HERE.parents[2]
SRC = PILOT / "data" / "entities_zh.jsonl"
OUT_ENT = HERE / "entities_full_v1.jsonl"
OUT_CHG = HERE / "changes_full_v1.json"
DATE_MAX = date(2025, 12, 31)
SEED = 42

# 字段 → (类型, 窗口%或参数, 步长)。步长单位同显示单位（"万""亿"按显示数字算）
PCT = {
    "身高": (5, "1"), "体重": (5, "1"), "员工人数": (5, "10"), "年营业额": (10, "0.1"),
    "人口": (5, "0.1"), "面积": (5, "1"), "海拔": (5, "1"), "高度": (5, "1"),
    "容纳人数": (5, "10"), "参与人数": (5, None), "预算": (5, "10"),
    "价格": (5, None), "重量": (5, None),
}
DATE_FIELDS = {"出生日期", "发布日期", "举办日期"}
YM_FIELDS = {"成立时间"}
YEAR_FIELDS = {"建成年份", "创作年份"}
COUNT_FIELDS = {"下辖乡镇数", "层数", "持续时间"}
WARRANTY_FIELDS = {"保修期"}
SKIP = {"id", "name", "entity_class", "description", "timeline_id"}

DISABLE = {
    ("EVENT-2", "持续时间"): ("drop", "马拉松比赛本身一天，凑不出4个可信备选（10-30 14:06；§7.3-2）"),
    ("BUILDING-2", "层数"): ("background", "24米/3层比值待核，原表下一版重建；本版层数只作背景（任务2页 11-04）"),
}
REPLACE = {  # (实体, 字段, 备选序号) → (新值, 理由)
    ("PERSON-1", "学历", 3): ("本科（古典文献学）",
        "初等教育是小学方向，与中学语文教师不配；不用“本科（汉语言）”，因与原值只差两字（任务2页 11-04）"),
    ("BUILDING-2", "主体结构", 4): ("框架-剪力墙结构",
        "“预应力混凝土”是工艺，不与砖混、框架、钢结构并列；候选统一为结构体系（任务2页 11-04）"),
}

NUM_RE = re.compile(r"^(下辖)?(\d+(?:\.\d+)?)(万|亿)?(.*)$")


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def rng(eid, field):
    return random.Random(f"{SEED}:{eid}:{field}")


# ------------------------------------------------------------------ 数值
def parse_num(s):
    m = NUM_RE.match(s)
    if not m:
        raise ValueError(s)
    return m.group(1) or "", Decimal(m.group(2)), m.group(3) or "", m.group(4)


def decimals_of(d):
    return max(0, -d.as_tuple().exponent)


def fmt(prefix, x, mult, suffix, dec):
    q = Decimal(1).scaleb(-dec)
    return f"{prefix}{x.quantize(q, rounding=ROUND_HALF_UP)}{mult}{suffix}"


def gen_pct(eid, field, orig):
    w, step_s = PCT[field]
    prefix, o, mult, suffix = parse_num(orig)
    dec = decimals_of(o)
    if field == "参与人数" and mult == "万":   # §7.2：满万用“万”并细一位
        dec += 1
    step = Decimal(step_s) if step_s else Decimal(1).scaleb(-dec)
    if not step_s and mult == "" and dec == 0 and o >= 1000:
        step = Decimal(10)                       # 价格、人次等整数 ≥1000：到十位，锚定原值保留尾数（§7.2 价格惯用尾数）
    dec = max(dec, decimals_of(step))
    rewrite = None
    for attempt in range(2):
        K = int((o * w / 100) / step)
        if K >= 2:
            break
        step = step / 10                         # §7.1 第3条：细一位
        dec = max(dec, decimals_of(step))
    else:
        return None, None, f"细一位后仍凑不出两侧各两个（K={K}）"
    ks = [-K, -math.ceil(K / 2), math.ceil(K / 2), K]
    vals = [o + k * step for k in ks]
    new_orig = fmt(prefix, o, mult, suffix, dec)
    if new_orig != orig:
        rewrite = {"from": orig, "to": new_orig, "reason": "备选需细一位，原值补零统一精度（§7.1 第2、3条），数值不变"}
    alts = [fmt(prefix, v, mult, suffix, dec) for v in vals]
    changes = [f"{(v - o) / o * 100:+.1f}%" for v in vals]
    return [new_orig] + alts, (changes, rewrite, f"原值±{w}%，步长{step}{mult}，k={ks}"), None


# ------------------------------------------------------------------ 日期
def pdate(s):
    m = re.fullmatch(r"(\d{4})年(\d{1,2})月(\d{1,2})日", s)
    return date(int(m[1]), int(m[2]), int(m[3]))


def fdate(d):
    return f"{d.year}年{d.month}月{d.day}日"


def gen_date(eid, field, orig):
    r = rng(eid, field)
    o = pdate(orig)
    if field == "举办日期":                      # 保持星期几；月份差 ≤1；跨年用 ±52 周
        bands = [(-52, -48), (-4, -1), (1, 4), (48, 52)]
        out = []
        for lo, hi in bands:
            for _ in range(200):
                d = o + timedelta(weeks=r.randint(lo, hi))
                mdiff = min((d.month - o.month) % 12, (o.month - d.month) % 12)
                if mdiff <= 1 and d <= DATE_MAX and d not in out and d != o:
                    out.append(d)
                    break
            else:
                return None, None, f"区间{lo}..{hi}周内找不到合规日期"
    else:
        bands = [(-365, -183), (-182, -30), (30, 182), (183, 365)]   # 至少差 30 天，避免与原值几乎相同
        out = []
        for lo, hi in bands:
            hi2 = min(hi, (DATE_MAX - o).days)
            if hi2 < lo:
                lo, hi2 = -365, -1                 # 原值离上限太近时改取前侧
            out.append(o + timedelta(days=r.randint(lo, hi2)))
        if len(set(out)) < 4:
            return None, None, "日期重复"
    out.sort()
    return [orig] + [fdate(d) for d in out], ([f"{(d - o).days:+d}天" for d in out], None,
                                                "±365天" + ("，保持星期几、月份差≤1" if field == "举办日期" else "")), None


def gen_ym(eid, field, orig):
    r = rng(eid, field)
    m = re.fullmatch(r"(\d{4})年(\d{1,2})月", orig)
    y0, m0 = int(m[1]), int(m[2])
    offs = [r.randint(lo, hi) for lo, hi in [(-12, -7), (-6, -1), (1, 6), (7, 12)]]
    vals = []
    for k in offs:
        t = y0 * 12 + (m0 - 1) + k
        vals.append(f"{t // 12}年{t % 12 + 1}月")
    return [orig] + vals, ([f"{k:+d}个月" for k in offs], None, "±12个月，只写年月"), None


def gen_year(eid, field, orig):
    y = int(re.fullmatch(r"(\d{4})年", orig)[1])
    ks = [-2, -1, 1, 2]
    if y + 2 > DATE_MAX.year:
        return None, None, "+2年超过2025"
    return [orig] + [f"{y + k}年" for k in ks], ([f"{k:+d}年" for k in ks], None, "±2年逐年"), None


def gen_count(eid, field, orig):
    prefix, o, mult, suffix = parse_num(orig)
    n = int(o)
    cand = [n + k for k in (-2, -1, 1, 2) if n + k > 0]
    if len(cand) < 4:
        return None, None, f"n−2…n+2 内只有{len(cand)}个正整数"
    return [orig] + [f"{prefix}{c}{suffix}" for c in cand], (
        [f"{c - n:+d}（{(c - n) / n * 100:+.0f}%）" for c in cand], None, "计数：n−2,n−1,n+1,n+2"), None


# ------------------------------------------------------------------ 保修
MONTH_TIERS = [3, 6, 12, 18, 24, 36, 48, 60]
HOUR_TIERS = [1000, 2000, 3000, 4000, 5000, 6000, 8000, 10000]
COMP_RE = re.compile(r"(\d+)(年|个月|小时)")


def tier_neighbors(v, tiers):
    i = tiers.index(v)
    return [tiers[i - 1], tiers[i + 1]]


def fmt_months(mo):
    return f"{mo // 12}年" if mo % 12 == 0 else f"{mo}个月"


def gen_warranty(eid, field, orig):
    comps = list(COMP_RE.finditer(orig))
    alts, notes = [], []
    for c in comps:
        n, unit = int(c[1]), c[2]
        if unit == "小时":
            nbrs, f = tier_neighbors(n, HOUR_TIERS), (lambda x: f"{x}小时")
        else:
            mo = n * 12 if unit == "年" else n
            nbrs, f = tier_neighbors(mo, MONTH_TIERS), fmt_months
        for x in nbrs:
            alts.append(orig[:c.start()] + f(x) + orig[c.end():])
            notes.append(f"{c[0]}→{f(x)}")
    if len(alts) != 4 or len(set(alts)) != 4:
        return None, None, f"保修期分量数≠2（{len(comps)}）"
    return [orig] + alts, (notes, None, "结构不变，每个备选只改一个分量，取相邻常用档位"), None


GEN = {}
for f_ in PCT:
    GEN[f_] = gen_pct
for f_ in DATE_FIELDS:
    GEN[f_] = gen_date
for f_ in YM_FIELDS:
    GEN[f_] = gen_ym
for f_ in YEAR_FIELDS:
    GEN[f_] = gen_year
for f_ in COUNT_FIELDS:
    GEN[f_] = gen_count
for f_ in WARRANTY_FIELDS:
    GEN[f_] = gen_warranty


def main():
    sha_before = sha(SRC)
    old = [json.loads(l) for l in SRC.open(encoding="utf-8")]
    new_ents, changes, problems = [], [], []
    for e in old:
        ne = copy.deepcopy(e)
        eid = e["id"]
        for field, vals in e.items():
            if field in SKIP or not isinstance(vals, list):
                continue
            rec = {"entity_id": eid, "field": field, "old_values": vals}
            key = (eid, field)
            if key in DISABLE:
                mode, why = DISABLE[key]
                if mode == "drop":
                    del ne[field]
                    rec.update(decision="停用（不设字段）", background_value=None, reason=why)
                else:
                    ne[field] = vals[0]
                    rec.update(decision="停用（转背景标量）", background_value=vals[0], reason=why)
                changes.append(rec)
                continue
            if field in GEN:
                out, info, err = GEN[field](eid, field, vals[0])
                if err:
                    if field in COUNT_FIELDS:
                        ne[field] = vals[0]
                        rec.update(decision="停用（转背景标量）", background_value=vals[0],
                                   reason=f"{err}；按§7.1第4条只作背景")
                        changes.append(rec)
                        continue
                    problems.append(f"{eid} {field}: {err}")
                    out, info = vals, ([], None, "未能按规则生成，沿用旧值")
                deltas, rewrite, rule = info
                ne[field] = out
                rec.update(new_values=out, decision="修改", rule=rule,
                           alternatives=[{"index": i + 1, "old": vals[i + 1], "new": out[i + 1],
                                          "change": deltas[i] if deltas else ""} for i in range(4)])
                if rewrite:
                    rec["original_display_rewrite"] = rewrite
            else:
                out = list(vals)
                notes = []
                for (re_, rf, ri), (nv, why) in REPLACE.items():
                    if (re_, rf) == key:
                        notes.append({"index": ri, "old": out[ri], "new": nv, "reason": why})
                        out[ri] = nv
                ne[field] = out
                rec.update(new_values=out, decision="替换个别备选" if notes else "保留（类别值，沿用旧备选）",
                           rule="类别值：沿用旧备选", replacements=notes)
            if len(set(ne[field])) != 5:
                problems.append(f"{eid} {field}: 五个值有重复 {ne[field]}")
            changes.append(rec)
        new_ents.append(ne)

    assert sha(SRC) == sha_before, "原数据被改动"
    with OUT_ENT.open("w", encoding="utf-8") as f:
        for ne in new_ents:
            f.write(json.dumps(ne, ensure_ascii=False) + "\n")
    n_conf = sum(1 for e in new_ents for k, v in e.items() if k not in SKIP and isinstance(v, list))
    summary = {
        "entities": len(new_ents),
        "conflict_attributes": n_conf,
        "pairs": n_conf * 4,
        "prompts_both_orders": n_conf * 8,
        "decisions": {d: sum(1 for c in changes if c["decision"] == d) for d in sorted({c["decision"] for c in changes})},
    }
    meta = {
        "status": "整批修订 v1（暂定参数），用于 baseline 诊断；不是最终数据",
        "date": "2026-11-04",
        "script": "pilot/data_review/value_revision/full_v1/build_full_v1.py",
        "script_sha256": sha(Path(__file__)),
        "input": "pilot/data/entities_zh.jsonl",
        "input_sha256": sha_before,
        "output_sha256": sha(OUT_ENT),
        "seed": SEED,
        "parameters": {"默认数值窗口": "±5%", "年营业额": "±10%", "完整日期": "±365天",
                       "举办日期": "±365天，保持星期几，月份差≤1", "年月": "±12个月", "纯年份": "±2年",
                       "计数": "n−2…n+2，凑不齐转背景（4→2 这类大相对改动暂定，待问老师）",
                       "日期上限（演示配置）": str(DATE_MAX)},
        "provisional": ["年营业额 ±10%", "计数 n−2…n+2 中相对改动大的（如乡镇数 4→2）"],
        "rules": "《数值合理性检查（自用参考）》§7.1–7.3；任务2页 11-04 决定",
    }
    OUT_CHG.write_text(json.dumps({"meta": meta, "summary": summary, "problems": problems,
                                   "changes": changes}, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False))
    print("problems:", problems or "无")


if __name__ == "__main__":
    main()
