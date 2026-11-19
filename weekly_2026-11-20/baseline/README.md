# Models and source-free baseline / 模型与无信源baseline

- Five models completed the same 3,040 prompts on final70_20261118_v2. The model weights are fixed by the revisions below.
- Qwen2.5 provides four planned sizes; Llama and GLM add two model families. The 72B baseline is pending.
- Take first-step A/B scores, normalise over A/B only, with greedy generation and one generated token. Each conflict pair is tested in both table orders.
- 五模型共用同一份题目；备选概率按对应的值计算，位置概率按表二计算。

| Model | Precision | Mean P(alt) | Mean P(Table 2) | Strong original / alternative |
|---|---|---:|---:|---:|
| zai-org/GLM-4-9B-0414 | float16 | 50.0% | 16.1% | 74 / 83 |
| meta-llama/Llama-3.1-8B-Instruct | float16 | 50.2% | 61.1% | 123 / 127 |
| Qwen/Qwen2.5-7B-Instruct | float16 | 49.6% | 64.4% | 167 / 148 |
| Qwen/Qwen2.5-14B-Instruct | bfloat16 | 50.2% | 61.1% | 257 / 276 |
| Qwen/Qwen2.5-32B-Instruct | bfloat16 | 50.4% | 48.3% | 339 / 373 |

Strong: the same value has probability greater than 0.8 in each table order. The unrounded probabilities reproduce all reported counts. The five-model intersection contains 19 pairs, listed in [audit results](../audit/results.json).

The complete numeric/date/duration audit includes 250 attribute instances, including warranty months. Each has two smaller/earlier and two larger/later alternatives. For Qwen32B, mean P(alt) is 72.8% on 500 larger/later pairs and 31.0% on 500 smaller/earlier pairs. This replaces the older direction summary, whose unit parser omitted some fields.

| Model | Exact loaded revision |
|---|---|
| zai-org/GLM-4-9B-0414 | `645b8482494e31b6b752272bf7f7f273ef0f3caf` |
| meta-llama/Llama-3.1-8B-Instruct | `0e9e39f249a16976918f6564b8830bc894c89659` |
| Qwen/Qwen2.5-7B-Instruct | `a09a35458c702b33eeacc393d103063234e8bc28` |
| Qwen/Qwen2.5-14B-Instruct | `cf98f3b3bbb457ad9e2bb7baf9a0125b6b88caa8` |
| Qwen/Qwen2.5-32B-Instruct | `5ede1c97bbab6ce5cda5812749b4c0bdf79b18dd` |

The sixth planned model is Qwen/Qwen2.5-72B-Instruct, revision `495f39366efef23836d0cfae4fbe635880d2be31`; no completed 72B result is included. The [six-model manifest](planned_six_models.json) records the original UC3 BF16 submission plan; the table above records actual completed run precisions.

- [Raw probabilities and runtime metadata](raw/)
- [Identical saved system/user inputs](prompts.jsonl)
- [Inference and analysis code snapshots](code/): original workspace paths; `model_compat.py` also documents model-specific loading.
- The source effect is a change from the same value’s baseline probability, paired by item and table order, and grouped by source category. Overall P(alt) close to 50% is a descriptive average.
