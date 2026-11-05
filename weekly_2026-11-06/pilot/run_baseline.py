# -*- coding: utf-8 -*-
"""任务6：无信源 baseline（两张表都不标来源）。

和 run_pilot.py 的区别只在组题：
  - 原值和每个备选都配对（默认 4 个备选全用，对应 WFW 的 get_pairs，helpers/models.py:218–224）；
  - 每对两种表序：order 0 = 表一原值/表二备选，order 1 = 对调；
  - 只有无信源条件。
测量契约不变：直接复用 run_pilot.get_answer_probabilities
（max_new_tokens=1、do_sample=False、只在 A/B 两个 token 上 softmax）。

运行：
  .venv/bin/python pilot/run_baseline.py --model Qwen/Qwen2.5-3B-Instruct --limit 16   # 冒烟测试
  .venv/bin/python pilot/run_baseline.py --model Qwen/Qwen2.5-3B-Instruct              # 全量
  # Kaggle（两张 T4）：模型分到两张卡，T4 用 fp16
  python pilot/run_baseline.py --model Qwen/Qwen2.5-7B-Instruct --device-map auto --dtype float16
"""
import argparse
import hashlib
import json
import logging
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from prompt_zh import build_two_table_prompt, get_question, SYSTEM_MESSAGE, ANSWER_TOKENS  # noqa: E402

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s", datefmt="%H:%M:%S")
log = logging.getLogger("baseline")

EXCLUDED = {"id", "name", "entity_class", "description", "timeline_id"}


def build_records(entities, alts):
    recs = []
    for e in entities:
        for field, vals in e.items():
            if field in EXCLUDED or not isinstance(vals, list) or len(vals) < 2:
                continue
            q = get_question(e["entity_class"], field, e["name"])
            for i in alts:
                if i >= len(vals):
                    continue
                for order in (0, 1):
                    va, vb = (vals[0], vals[i]) if order == 0 else (vals[i], vals[0])
                    recs.append({
                        "entity_id": e["id"], "entity_class": e["entity_class"], "field": field,
                        "alt_index": i, "order": order,
                        "original": vals[0], "alternative": vals[i],
                        "value_a": va, "value_b": vb,
                        "prompt": build_two_table_prompt(e, field, va, vb, None, None, q),
                    })
    return recs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="Qwen/Qwen2.5-3B-Instruct")
    ap.add_argument("--data", default=str(HERE / "data" / "entities_zh.jsonl"))
    ap.add_argument("--alts", default="1,2,3,4", help="用哪些备选，逗号分隔；旧pilot只用了 1")
    ap.add_argument("--batch-size", type=int, default=8)
    ap.add_argument("--limit", type=int, default=0, help="只跑前 N 条（冒烟测试）")
    ap.add_argument("--out", default="")
    ap.add_argument("--device-map", default="", help="多卡时填 auto，把模型分到几张卡上")
    ap.add_argument("--dtype", default="auto", choices=["auto", "float16", "bfloat16", "float32"],
                    help="auto = 按设备自动选；T4 不原生支持 bf16，用 float16")
    ap.add_argument("--revision", default=None, help="固定模型版本（HF commit）；不填则用最新版，版本号仍会记录")
    args = ap.parse_args()

    data = Path(args.data)
    entities = [json.loads(l) for l in data.open(encoding="utf-8") if l.strip()]
    alts = [int(x) for x in args.alts.split(",")]
    recs = build_records(entities, alts)
    if args.limit:
        recs = recs[:args.limit]
    log.info("实体 %d 个，题目 %d 条（备选 %s × 两种表序）", len(entities), len(recs), alts)

    import torch
    from transformers import AutoTokenizer, AutoModelForCausalLM
    from run_pilot import get_answer_probabilities, pick_device_dtype

    import transformers
    device, dtype = pick_device_dtype()
    if args.dtype != "auto":
        dtype = getattr(torch, args.dtype)
    log.info("加载 %s 到 %s (%s，device_map=%s)", args.model, device, dtype, args.device_map or "单卡")
    tok = AutoTokenizer.from_pretrained(args.model, revision=args.revision)
    if tok.pad_token is None:
        tok.pad_token = tok.eos_token
    kw = {"dtype": dtype, "revision": args.revision}
    if args.device_map:
        kw["device_map"] = args.device_map
    model = AutoModelForCausalLM.from_pretrained(args.model, **kw)
    if not args.device_map:
        model = model.to(device)
    model.eval()
    if next(model.parameters()).dtype != dtype:
        raise SystemExit(f"模型精度是 {next(model.parameters()).dtype}，不是 {dtype}；请用 transformers 5.x")
    gpus = [torch.cuda.get_device_name(i) for i in range(torch.cuda.device_count())] if device == "cuda" else []
    tokcheck = {t: tok.encode(t, add_special_tokens=False) for t in ANSWER_TOKENS}
    log.info("答案 token 编码: %s", tokcheck)
    if any(len(v) != 1 for v in tokcheck.values()):
        raise SystemExit("答案 token 不是单 token，测量契约不成立")

    t0 = time.time()
    for s in range(0, len(recs), args.batch_size):
        batch = recs[s:s + args.batch_size]
        probs = get_answer_probabilities(model, tok, [r["prompt"] for r in batch], SYSTEM_MESSAGE)
        for r, (pa, pb) in zip(batch, probs):
            r["prob_a"], r["prob_b"] = pa, pb
        done = s + len(batch)
        if (s // args.batch_size) % 20 == 0 or done == len(recs):
            el = time.time() - t0
            log.info("%d/%d  用时 %.0fs  预计剩余 %.0fs", done, len(recs), el, el / done * (len(recs) - done))

    tag = args.model.split("/")[-1]
    out = Path(args.out) if args.out else HERE / "results_baseline" / tag / ("raw_limit.json" if args.limit else "raw.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    # 实际发给模型的完整 prompt 另存一份（附录用），raw 里只留序号
    prompts_path = out.with_name(out.stem.replace("raw", "prompts") + ".jsonl")
    with prompts_path.open("w", encoding="utf-8") as fh:
        for i, r in enumerate(recs):
            fh.write(json.dumps({"i": i, "entity_id": r["entity_id"], "field": r["field"], "alt_index": r["alt_index"],
                                 "order": r["order"], "system": SYSTEM_MESSAGE, "user": r.pop("prompt")},
                                ensure_ascii=False) + "\n")
            r["i"] = i
    out.write_text(json.dumps({
        "model": args.model, "revision_requested": args.revision,
        "revision_loaded": getattr(model.config, "_commit_hash", None), "device": device, "dtype": str(dtype), "device_map": args.device_map or None,
        "gpus": gpus, "torch": torch.__version__, "transformers": transformers.__version__,
        "data": str(data.relative_to(HERE.parent)) if data.is_relative_to(HERE.parent) else str(data),
        "data_sha256": hashlib.sha256(data.read_bytes()).hexdigest(),
        "alts": alts, "limit": args.limit, "n_records": len(recs),
        "answer_token_ids": tokcheck, "system_message": SYSTEM_MESSAGE,
        "command": " ".join(sys.argv), "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "prompts_file": prompts_path.name, "prompts_sha256": hashlib.sha256(prompts_path.read_bytes()).hexdigest(),
        "seconds": round(time.time() - t0, 1),
        "results": recs,
    }, ensure_ascii=False), encoding="utf-8")
    log.info("写出 %s", out)


if __name__ == "__main__":
    main()
