# 运行记录 / Run records

<details>
<summary>全部输入、输出与分析文件 / All inputs, outputs and analysis files</summary>

- `prompts.jsonl` 保存实际输入，`raw.json` 保存逐题结果，按题目编号 `i` 对应。<br>`prompts.jsonl` contains the actual inputs and `raw.json` the item-level results, matched by item number `i`.

- `prob_a` 和 `prob_b` 为生成第一步的A/B分数仅在这两个答案token之间归一化后的概率；`revision_requested` 为请求的模型版本。<br>`prob_a` and `prob_b` are probabilities normalised over only the A/B answer-token scores at the first generation step; `revision_requested` records the requested model revision.

| 模型 / Model | 输入 / Inputs | 输出 / Outputs | 分析 / Analysis | 汇总 / Summary |
|---|---|---|---|---|
| Qwen2.5-7B | [prompts](../pilot/results_baseline/Qwen2.5-7B-Instruct_full_v1/prompts.jsonl) | [raw](../pilot/results_baseline/Qwen2.5-7B-Instruct_full_v1/raw.json) | [analysis](../pilot/results_baseline/Qwen2.5-7B-Instruct_full_v1/analysis.json) | [summary](../pilot/results_baseline/Qwen2.5-7B-Instruct_full_v1/summary.md) |
| Qwen2.5-14B | [prompts](../pilot/results_baseline/Qwen2.5-14B-Instruct_full_v1/prompts.jsonl) | [raw](../pilot/results_baseline/Qwen2.5-14B-Instruct_full_v1/raw.json) | [analysis](../pilot/results_baseline/Qwen2.5-14B-Instruct_full_v1/analysis.json) | [summary](../pilot/results_baseline/Qwen2.5-14B-Instruct_full_v1/summary.md) |
| Llama-3.1-8B | [prompts](../pilot/results_baseline/Llama-3.1-8B-Instruct_full_v1/prompts.jsonl) | [raw](../pilot/results_baseline/Llama-3.1-8B-Instruct_full_v1/raw.json) | [analysis](../pilot/results_baseline/Llama-3.1-8B-Instruct_full_v1/analysis.json) | [summary](../pilot/results_baseline/Llama-3.1-8B-Instruct_full_v1/summary.md) |
| Gemma-4-E4B | [prompts](../pilot/results_baseline/gemma-4-E4B-it_full_v1/prompts.jsonl) | [raw](../pilot/results_baseline/gemma-4-E4B-it_full_v1/raw.json) | [analysis](../pilot/results_baseline/gemma-4-E4B-it_full_v1/analysis.json) | [summary](../pilot/results_baseline/gemma-4-E4B-it_full_v1/summary.md) |
| Gemma-4-12B | [prompts](../pilot/results_baseline/gemma-4-12B-it_full_v1/prompts.jsonl) | [raw](../pilot/results_baseline/gemma-4-12B-it_full_v1/raw.json) | [analysis](../pilot/results_baseline/gemma-4-12B-it_full_v1/analysis.json) | [summary](../pilot/results_baseline/gemma-4-12B-it_full_v1/summary.md) |

</details>


- [推理与分析代码 / Inference and analysis code](../pilot/)。
