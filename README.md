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

## Known issues (pilot data, kept as generated)
1. **Numerical alternatives are not range-controlled.** 121 of the numerical pairs differ from the original by more than 30% (years: more than 15 years), e.g. marathon duration 1 day → 5 days (EVENT-2), elevation 58 m → 184 m (LOCATION-2). A plausibility check is in progress.
2. **Inconsistent number formats within a list.** EVENT-2 participation mixes 万 and plain numbers (1.2万人 vs 8600人; this was the tested pair); PRODUCT-1 warranty sometimes adds an hour limit and sometimes not. A model could tell values apart by form alone.
3. **One entity name overlaps with an alternative value.** EVENT-3 通溪非物质文化遗产展演 vs organiser alternative 通溪市非物质文化遗产保护中心.
