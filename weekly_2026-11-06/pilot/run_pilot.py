# -*- coding: utf-8 -*-
"""跑中文 pilot 实验，产出原始概率 -> pilot/results_raw.json。

测量方法完全照搬 helpers/model_inference.py：
  - forced choice，max_new_tokens=1，do_sample=False
  - 取 outputs.scores[0]，即最后一个位置的 logits
  - 只在答案 token A/B 的 id 上做 softmax 归一化（所以 prob_a + prob_b = 1）
  - apply_chat_template + 左 padding + add_special_tokens=False

每条数据跑两种表格顺序，照搬论文 §3.3 的 C'_rev = (T_B^y, T_A^x)
以及仓库 helpers/runner.py:411-419 的 reverse_tables 逻辑：

  order 0: 表一=(v0, 信源x)  表二=(v1, 信源y)   选项 (A)v0 (B)v1
  order 1: 表一=(v1, 信源y)  表二=(v0, 信源x)   选项 (A)v1 (B)v0

关键：**信源和它承载的取值绑在一起、整体换到另一个位置**。
所以信源 x 在 order 0 里坐 A 位、在 order 1 里坐 B 位，两次平均才真正抵消位置偏差。

（本文件的初版写错了：只交换取值、把信源焊死在原位，导致信源 x 永远在 A 位，
  SP 与位置偏差完全混杂。本机实测该模型位置/token 偏差达 25-35 个百分点，
  这个错误足以让 SP 不可解读。）

因为信源换了位置，group_a / group_b 也要跟着换，SP 按**信源类别**累积
而不是按固定位置累积——与 helpers/evaluation.py 的 group_diffs 一致。

条件：
  baseline        两张表都不给信源      -> P(A|无信源)
  gov_vs_social   表一政府  表二社交媒体
  gov_vs_person   表一政府  表二个人
  news_vs_social  表一报纸  表二社交媒体
  none_vs_gov     表一不标信源 表二政府

SP = P(A|有信源) - P(A|无信源)，按 (entity_id, pair_id, value_a, value_b) 配对，
与 helpers/evaluation.py::calculate_reference_comparison 的配对键一致。
"""

import argparse, json, logging, sys, time
from pathlib import Path

import torch

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
from prompt_zh import (build_two_table_prompt, get_question, SYSTEM_MESSAGE,
                       ANSWER_TOKENS, NO_SOURCE)

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s", datefmt="%H:%M:%S")
log = logging.getLogger("pilot")

EXCLUDED = {"id", "name", "entity_class", "description", "timeline_id"}


def pick_device_dtype():
    """按 cuda > mps > cpu 选设备，并挑合适的 dtype。

    A40 / A100 支持 bfloat16，数值范围比 fp16 大，长 prompt 上更稳；
    Apple MPS 上 bfloat16 支持不全，用 fp16。
    """
    if torch.cuda.is_available():
        dtype = torch.bfloat16 if torch.cuda.is_bf16_supported() else torch.float16
        return "cuda", dtype
    if torch.backends.mps.is_available():
        return "mps", torch.float16
    return "cpu", torch.float32

# 值为 (表一信源类别, 表二信源类别)；None 表示完全不标注信源
CONDITIONS = {
    "baseline":       (None, None),          # 论文的 C，两表都无信源标注
    "gov_vs_social":  ("government", "social_media"),
    "gov_vs_person":  ("government", "person"),
    "news_vs_social": ("newspaper", "social_media"),
    "none_vs_gov":    ("no_source", "government"),   # 论文的 x = "No source available"
}


def load_data():
    ents = [json.loads(l) for l in (HERE / "data/entities_zh.jsonl").open(encoding="utf-8")]
    srcs = json.loads((HERE / "data/sources_zh.json").read_text(encoding="utf-8"))
    return ents, srcs


def build_items(entities):
    """每个实体的每个冲突字段取一对 (values[0], values[1])。"""
    items = []
    for e in entities:
        for field, values in e.items():
            if field in EXCLUDED or not isinstance(values, list) or len(values) < 2:
                continue
            items.append({
                "entity_id": e["id"],
                "entity_name": e["name"],
                "entity_class": e["entity_class"],
                "field": field,
                "pair_id": f"{field}:0-1",
                "v0": values[0],
                "v1": values[1],
                "entity": e,
            })
    return items


def pick_source(srcs, category, idx):
    """从该类信源里按序轮取，保证各类信源被均匀使用。

    category 为 None -> 该表完全不标注信源（基线条件）
    category 为 "no_source" -> 显式标注"无可用信源"（论文 §3.3 的 No source available）
    """
    if category is None:
        return None
    if category == "no_source":
        return NO_SOURCE
    lst = srcs[category]
    return lst[idx % len(lst)]["name"]


@torch.inference_mode()
def get_answer_probabilities(model, tokenizer, prompts, system_message):
    """照搬 helpers/model_inference.py::_run_inference。"""
    target_ids = [tokenizer.encode(t, add_special_tokens=False)[-1] for t in ANSWER_TOKENS]

    chat_inputs = [
        tokenizer.apply_chat_template(
            [{"role": "system", "content": system_message},
             {"role": "user", "content": p}],
            tokenize=False, add_generation_prompt=True,
        ) for p in prompts
    ]
    tokenizer.padding_side = "left"
    tok = tokenizer(chat_inputs, return_tensors="pt", padding=True,
                    truncation=False, add_special_tokens=False)
    device = next(model.parameters()).device
    tok = {k: v.to(device) for k, v in tok.items()}

    out = model.generate(**tok, max_new_tokens=1, return_dict_in_generate=True,
                         output_scores=True, do_sample=False,
                         pad_token_id=tokenizer.pad_token_id)
    logits = out.scores[0]                                  # (batch, vocab)
    tgt = logits[:, torch.tensor(target_ids, device=logits.device)]
    probs = torch.nn.functional.softmax(tgt.float(), dim=-1).cpu().numpy()
    return [(float(r[0]), float(r[1])) for r in probs]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="Qwen/Qwen2.5-3B-Instruct")
    ap.add_argument("--batch-size", type=int, default=8)
    ap.add_argument("--out", default=str(HERE / "results_raw.json"))
    args = ap.parse_args()

    entities, srcs = load_data()
    items = build_items(entities)
    log.info("实体 %d 个，冲突条目 %d 条", len(entities), len(items))

    from transformers import AutoTokenizer, AutoModelForCausalLM
    device, dtype = pick_device_dtype()
    log.info("加载 %s 到 %s (%s) ...", args.model, device, dtype)
    if device == "cuda":
        log.info("GPU: %s", torch.cuda.get_device_name(0))
    tokenizer = AutoTokenizer.from_pretrained(args.model)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    model = AutoModelForCausalLM.from_pretrained(args.model, dtype=dtype).to(device)
    model.eval()

    # 检查答案 token 是否真是单 token（中文实验里这点必须验，见 RESULTS.md 的坑）
    tokcheck = {t: tokenizer.encode(t, add_special_tokens=False) for t in ANSWER_TOKENS}
    log.info("答案 token 编码: %s", tokcheck)

    # ---- 组装所有 prompt ----
    records = []
    for cond, (cat_a, cat_b) in CONDITIONS.items():
        for i, it in enumerate(items):
            sa = pick_source(srcs, cat_a, i)
            sb = pick_source(srcs, cat_b, i)
            ga0 = cat_a or "no_source"
            gb0 = cat_b or "no_source"
            for order in (0, 1):
                if order == 0:
                    va, vb, src_a, src_b, ga, gb = it["v0"], it["v1"], sa, sb, ga0, gb0
                else:
                    # 信源连同取值整体换位（论文的 reverse_tables）
                    va, vb, src_a, src_b, ga, gb = it["v1"], it["v0"], sb, sa, gb0, ga0
                q = get_question(it["entity_class"], it["field"], it["entity_name"])
                prompt = build_two_table_prompt(it["entity"], it["field"], va, vb,
                                                src_a, src_b, q)
                records.append({
                    "condition": cond, "entity_id": it["entity_id"],
                    "entity_name": it["entity_name"], "entity_class": it["entity_class"],
                    "field": it["field"], "pair_id": it["pair_id"],
                    "order": order, "value_a": va, "value_b": vb,
                    "source_a": src_a, "source_b": src_b,
                    "group_a": ga, "group_b": gb,
                    "prompt": prompt,
                })
    log.info("共 %d 条 prompt（%d 条件 × %d 条目 × 2 顺序）",
             len(records), len(CONDITIONS), len(items))

    # ---- 分批推理 ----
    t0 = time.time()
    for s in range(0, len(records), args.batch_size):
        batch = records[s:s + args.batch_size]
        probs = get_answer_probabilities(model, tokenizer,
                                         [r["prompt"] for r in batch], SYSTEM_MESSAGE)
        for r, (pa, pb) in zip(batch, probs):
            r["prob_a"], r["prob_b"] = pa, pb
        done = s + len(batch)
        if (s // args.batch_size) % 20 == 0 or done == len(records):
            el = time.time() - t0
            log.info("%d/%d  用时 %.0fs  预计剩余 %.0fs",
                     done, len(records), el, el / done * (len(records) - done))

    for r in records:
        r.pop("prompt", None)     # 原始文件不存 prompt，太大

    out = {
        "model": args.model, "device": device, "dtype": str(dtype),
        "n_entities": len(entities), "n_items": len(items),
        "answer_token_ids": {t: tokenizer.encode(t, add_special_tokens=False) for t in ANSWER_TOKENS},
        "results": records,
    }
    Path(args.out).write_text(json.dumps(out, ensure_ascii=False), encoding="utf-8")
    log.info("写出 %s（%d 条）", args.out, len(records))


if __name__ == "__main__":
    main()
