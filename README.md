# Chinese source-preference pilot: data

Pilot data for a Chinese adaptation of Schuster, Gautam & Markert (2026), *Whose Facts Win?*.
30 fictional entities in 7 types, 151 entity–attribute items, 5 values each (index 0 = original, 1–4 = alternatives).

| File | Content |
|---|---|
| `conflict_pairs.md` | All 604 conflict pairs (original vs. one alternative), Chinese with English gloss; easiest to read |
| `conflict_pairs.csv` | Same pairs as a table |
| `entities_zh.jsonl` | Original Chinese data, one entity per line |
| `sources_zh.json` | The 20 Chinese source names (4 types × 5) |

Notes
- Only alternative 1 was tested in the pilot (`tested_in_pilot = yes`).
- English glosses were machine-translated and AI-checked, not independently human-reviewed.
- Gender is fixed context, not a conflict attribute.
