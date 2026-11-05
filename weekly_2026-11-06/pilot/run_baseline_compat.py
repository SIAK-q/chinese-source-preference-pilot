# -*- coding: utf-8 -*-
"""无信源 baseline 的通用入口：题目和输出格式与 run_baseline.py 完全相同，推理改用 model_compat.ModelBundle。

为什么另起一个入口：Gemma 4 必须用 AutoProcessor + AutoModelForMultimodalLM 加载，并关闭思考模式
（enable_thinking=False），run_baseline.py 的 AutoModelForCausalLM 路径不适用。run_baseline.py 本身不改，
历史结果继续对应原脚本。

测量契约不变：max_new_tokens=1、do_sample=False、取 scores[0]，只在 A/B 两个答案 token 上 softmax；
每题两种表序，来源（此处无）与值一起换位。题目由 run_baseline.build_records 生成，逐字相同。

运行：python pilot/run_baseline_compat.py --model google/gemma-4-E4B-it --dtype float16 --device-map auto \
        --data pilot/data_review/value_revision/full_v1/entities_full_v1.jsonl --out <目录>/raw.json
"""
import argparse
import hashlib
import json
import logging
import math
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from prompt_zh import SYSTEM_MESSAGE, ANSWER_TOKENS  # noqa: E402
from run_baseline import build_records  # noqa: E402
from model_compat import ModelBundle, PINNED  # noqa: E402

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s", datefmt="%H:%M:%S")
log = logging.getLogger("baseline_compat")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    ap.add_argument("--revision", default=None, help="不填则用 model_compat.PINNED")
    ap.add_argument("--data", required=True)
    ap.add_argument("--alts", default="1,2,3,4")
    ap.add_argument("--batch-size", type=int, default=8)
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--out", required=True)
    ap.add_argument("--device-map", default="")
    ap.add_argument("--dtype", default="auto", choices=["auto", "float16", "bfloat16", "float32"])
    args = ap.parse_args()

    data = Path(args.data)
    entities = [json.loads(l) for l in data.open(encoding="utf-8") if l.strip()]
    alts = [int(x) for x in args.alts.split(",")]
    recs = build_records(entities, alts)
    if args.limit:
        recs = recs[:args.limit]
    log.info("实体 %d 个，题目 %d 条", len(entities), len(recs))

    revision = args.revision or PINNED.get(args.model)
    m = ModelBundle(args.model, revision, args.dtype, args.device_map)
    tokcheck = {t: m.tokenizer.encode(t, add_special_tokens=False) for t in ANSWER_TOKENS}
    log.info("模型 %s；答案 token 编码 %s", m.metadata(), tokcheck)

    t0 = time.time()
    first_tokens = []
    for s in range(0, len(recs), args.batch_size):
        batch = recs[s:s + args.batch_size]
        probs, decoded = m.probabilities(SYSTEM_MESSAGE, [r["prompt"] for r in batch], letters=tuple(ANSWER_TOKENS))
        for r, (pa, pb), d in zip(batch, probs, decoded):
            if not (math.isfinite(pa) and math.isfinite(pb)):
                raise SystemExit(f"概率不是有限数（{pa}, {pb}），可能是精度溢出；换 --dtype 再试")
            r["prob_a"], r["prob_b"] = pa, pb
            first_tokens.append(d)
        done = s + len(batch)
        if (s // args.batch_size) % 20 == 0 or done == len(recs):
            el = time.time() - t0
            log.info("%d/%d  用时 %.0fs", done, len(recs), el)

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    prompts_path = out.with_name(out.stem.replace("raw", "prompts") + ".jsonl")
    with prompts_path.open("w", encoding="utf-8") as fh:
        for i, r in enumerate(recs):
            fh.write(json.dumps({"i": i, "entity_id": r["entity_id"], "field": r["field"], "alt_index": r["alt_index"],
                                 "order": r["order"], "system": SYSTEM_MESSAGE, "user": r.pop("prompt")},
                                ensure_ascii=False) + "\n")
            r["i"] = i
    meta = m.metadata()
    pilot = HERE
    out.write_text(json.dumps({
        "model": args.model, "revision_requested": revision, "revision_loaded": meta.get("revision_resolved"),
        "architecture": meta.get("architecture"), "device": meta.get("device"), "dtype": meta.get("dtype"),
        "device_map": args.device_map or None, "torch": meta.get("torch"), "transformers": meta.get("transformers"),
        "thinking_disabled": meta.get("thinking_disabled"),
        "data": str(data), "data_sha256": hashlib.sha256(data.read_bytes()).hexdigest(),
        "alts": alts, "limit": args.limit, "n_records": len(recs),
        "answer_token_ids": tokcheck, "system_message": SYSTEM_MESSAGE,
        "first_generated_token_counts": {t: first_tokens.count(t) for t in sorted(set(first_tokens))},
        "command": " ".join(sys.argv),
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "model_compat_sha256": hashlib.sha256((pilot / "model_compat.py").read_bytes()).hexdigest(),
        "prompts_file": prompts_path.name, "prompts_sha256": hashlib.sha256(prompts_path.read_bytes()).hexdigest(),
        "seconds": round(time.time() - t0, 1),
        "results": recs,
    }, ensure_ascii=False), encoding="utf-8")
    log.info("写出 %s", out)


if __name__ == "__main__":
    main()
