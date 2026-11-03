# Chinese source-preference pilot: data

This repository contains the pilot data of my MA thesis on how LLMs weigh different types of sources (government, newspaper, person, social media) when two Chinese-language materials conflict. The measurement setup follows Schuster, Gautam & Markert (2026); the entities, attribute values and source names were built for Chinese.

The pilot was a feasibility check: it tested whether the procedure runs in Chinese, not which sources models prefer. This release is for reviewing the data before it is extended.

30 fictional entities in 7 types, 151 entity–attribute items, 5 values each (index 0 = original, 1–4 = alternatives).

## How the data was generated

The data was generated on 2026-09-17 in one session with Claude Opus 5 (`claude-opus-5`) in Claude Code. The data was made and revised over three rounds; the four instruction files below describe them. There was no separate prompt per entity or per attribute.

**What the model saw.** The instructions, the earlier rounds of the session, and parts of the Schuster et al. (2026) repository: the field names of each entity type, the source templates, the code, and the first 3,000 bytes of the English entity file (PERSON-1 and PERSON-2 complete, the start of PERSON-3). 14 birth dates are identical to those three English records; the instructions did not ask for this.

**How originals and alternatives were made.** The model wrote the values directly into Python scripts, almost all as fixed lists (a few, such as city of residence, were filled in by code from the place-name list). The original and its four alternatives were written together, and all attributes of an entity were written in the same script.

**What changed afterwards.**

| Round | Instruction | What changed |
|---|---|---|
| 1 | Initial request (original wording in the session records), [2: how to make place names](generation/prompts/2_place_names.md) | First complete data |
| 2 | [3: five problems in the first data](generation/prompts/3_corrections.md) | Organization and product names revised and the headquarters and manufacturer attributes removed; nationality and country removed, number of towns/townships added for locations; some values revised (e.g. industry, revenue, structural system, duration); county/city-level place names; separate person-name pools |
| 3 | [4: one shared place-name pool](generation/prompts/4_shared_place_pool.md) | One pool of 20 place names for all sources and entities |

Values were revised only in round 2; round 3 updated place names and the fields that contain them. How the place names were made: [`generation/place_names/`](generation/place_names/).

**Final data.** Running the final scripts produced [`entities_zh.jsonl`](entities_zh.jsonl) and [`sources_zh.json`](sources_zh.json). [Instruction 1](generation/prompts/1_task.md) is a generation prompt reconstructed from this final data and the methods described in the proposal and the 23 October slides; it has not been rerun. The easiest way to read the originals and alternatives side by side is [`conflict_pairs.md`](conflict_pairs.md).

**Reading the prompt files.** Each file presents a Chinese version and an English translation. Instructions 2–4 keep the original Chinese excerpt folded below; Instruction 1's original wording is in the session records. Instruction 1 names Weibo, the platform chosen in the implementation; the original instruction asked the model to choose a platform and explain its choice.

## Files

| File | Content |
|---|---|
| `conflict_pairs.md` | All 604 conflict pairs (original vs. one alternative), Chinese with English gloss; easiest to read |
| `conflict_pairs.csv` | Same pairs as a table |
| `entities_zh.jsonl` | Original Chinese data, one entity per line |
| `sources_zh.json` | The 20 Chinese source names (4 types × 5) |
| `generation/prompts/` | The four instructions (edited or reconstructed Chinese text, English translation; original wording for 2–4) |
| `generation/place_names/` | How the place names were made, with the original code and output |

## Notes

- Only alternative 1 was tested in the pilot (`tested_in_pilot = yes`).
- English glosses were machine-translated.
- Gender is fixed context, not a conflict attribute.

## Known issues

1. **One entity name overlaps with an alternative value.** EVENT-3 通溪非物质文化遗产展演 vs organiser alternative 通溪市非物质文化遗产保护中心 (a tested pair). The name check in the pilot only tested one direction.
2. **Numerical alternatives were written without a set range.** Schuster et al. (2026) vary numerical values by up to ±20%; 177 of the 296 numerical pairs here differ by more than 20%, e.g. marathon duration 1 day → 5 days (EVENT-2), elevation 58 m → 184 m (LOCATION-2). The range for the Chinese data is still to be decided.
