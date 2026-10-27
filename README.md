# Chinese source-preference pilot: data

This repository contains the pilot data of my MA thesis on how LLMs weigh different types of sources (government, newspaper, person, social media) when two Chinese-language materials conflict. The measurement setup follows Schuster, Gautam & Markert (2026); the entities, attribute values and source names were built for Chinese.

The pilot was a feasibility check: it tested whether the procedure runs in Chinese, not which sources models prefer. This release is for reviewing the data before it is extended.

30 fictional entities in 7 types, 151 entity–attribute items, 5 values each (index 0 = original, 1–4 = alternatives).

## Files

| File | Content |
|---|---|
| `conflict_pairs.md` | All 604 conflict pairs (original vs. one alternative), Chinese with English gloss; easiest to read |
| `conflict_pairs.csv` | Same pairs as a table |
| `entities_zh.jsonl` | Original Chinese data, one entity per line |
| `sources_zh.json` | The 20 Chinese source names (4 types × 5) |

## Notes

- Only alternative 1 was tested in the pilot (`tested_in_pilot = yes`).
- English glosses were machine-translated.
- Gender is fixed context, not a conflict attribute.

## Known issues

1. **One entity name overlaps with an alternative value.** EVENT-3 通溪非物质文化遗产展演 vs organiser alternative 通溪市非物质文化遗产保护中心 (a tested pair). The name check in the pilot only tested one direction.
2. **Numerical alternatives were written without a set range.** Schuster et al. (2026) vary numerical values by up to ±20%; 177 of the 296 numerical pairs here differ by more than 20%, e.g. marathon duration 1 day → 5 days (EVENT-2), elevation 58 m → 184 m (LOCATION-2). The range for the Chinese data is still to be decided.
