"""频率加权抽样、统一三池、配额和精确标题查重；默认离线，不改pilot原数据。"""

import argparse
import ast
import csv
import hashlib
import json
import math
import random
import re
import statistics
import urllib.request
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlencode


HERE = Path(__file__).resolve().parent
PILOT = HERE.parents[1]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def save_rows(path, rows):
    path.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows))


def old_pools():
    fields = {"NAME_ENTITY": "entity_people", "NAME_SOURCE": "individual_sources", "NAME_ATTR": "attribute_people"}
    pools = {}
    for node in ast.parse((PILOT / "build_data_zh.py").read_text()).body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id in fields:
                    pools[fields[target.id]] = ast.literal_eval(node.value)
    if len(pools) != 3 or sum(map(len, pools.values())) != 20:
        raise ValueError("Unexpected pilot name pools")
    return pools


def inputs(config):
    source = json.loads((HERE / "sources.json").read_text())
    for name, record in source["files"].items():
        if digest(HERE / "raw" / name) != record["sha256"]:
            raise ValueError(f"Input hash mismatch: {name}")
    tables = {}
    for filename in ["familyname.csv", "givenname.csv"]:
        with (HERE / "raw" / filename).open(encoding="utf-8-sig", newline="") as handle:
            tables[filename] = list(csv.DictReader(handle))
    if len(tables["familyname.csv"]) != 1806 or len(tables["givenname.csv"]) != 2614:
        raise ValueError("Unexpected frequency table size")
    surnames = tables["familyname.csv"]
    characters = tables["givenname.csv"]
    for rows, key, columns in [(surnames, "surname", [config["surname_weight_column"]]), (characters, "character", list(config["given_character_weight_columns"].values()))]:
        if len({row[key] for row in rows}) != len(rows):
            raise ValueError("Duplicate source entries")
        for row in rows:
            if not re.fullmatch(r"[\u4e00-\u9fff]{1,2}" if key == "surname" else r"[\u4e00-\u9fff]", row[key]):
                raise ValueError(f"Unexpected character entry: {row[key]}")
            for column in columns:
                weight = float(row[column])
                if not math.isfinite(weight) or weight < 0:
                    raise ValueError(f"Invalid frequency: {row[key]}, {column}")
    return surnames, characters, source


def load_wiki():
    path = HERE / "wiki_requests.json"
    requests = json.loads(path.read_text())["requests"] if path.exists() else []
    cache = {}
    for request in requests:
        response_path = HERE / request["file"]
        if digest(response_path) != request["sha256"]:
            raise ValueError("Wikipedia response hash mismatch")
        response = json.loads(response_path.read_text())
        if "query" not in response or "error" in response:
            raise ValueError("Wikipedia request failed; do not treat as missing")
        query = response["query"]
        normalized = {row["from"]: row["to"] for row in query.get("normalized", [])}
        redirects = {row["from"]: row["to"] for row in query.get("redirects", [])}
        pages = {row["title"]: row for row in query["pages"]}
        for title in request["titles"]:
            resolved = normalized.get(title, title)
            resolved = redirects.get(resolved, resolved)
            if resolved not in pages:
                raise ValueError(f"No result for requested title: {title}")
            page = pages[resolved]
            cache[title] = {"status": "missing_exact_title" if "missing" in page else "page_exists", "resolved_title": resolved, "pageid": page.get("pageid"), "file": request["file"], "retrieved_at_utc": request["retrieved_at_utc"], "sha256": request["sha256"]}
    return requests, cache


def wiki_url(titles):
    return "https://zh.wikipedia.org/w/api.php?" + urlencode({"action": "query", "format": "json", "formatversion": "2", "redirects": "1", "prop": "info", "titles": "|".join(titles)})


def fetch_wiki(titles, config, requests):
    for start in range(0, len(titles), config["wiki_batch_size"]):
        batch = titles[start:start + config["wiki_batch_size"]]
        url = wiki_url(batch)
        filename = f"raw/wiki_{len(requests):03d}.json"
        destination = HERE / filename
        if destination.exists():
            raise ValueError("Refusing to overwrite an existing Wikipedia response")
        request = urllib.request.Request(url, headers={"User-Agent": "LLMSourcePreferenceResearch/0.1 (small exact-title audit)"})
        with urllib.request.urlopen(request, timeout=60) as handle:
            content = handle.read()
        response = json.loads(content)
        if "query" not in response or "error" in response:
            raise ValueError("Wikipedia returned an error; no names approved")
        destination.write_bytes(content)
        requests.append({"url": url, "titles": batch, "file": filename, "retrieved_at_utc": datetime.now(timezone.utc).isoformat(), "sha256": digest(destination)})
        save_json(HERE / "wiki_requests.json", {"scope": config["wiki_scope"], "requests": requests})


def draw_batch(config, surnames, characters, cache, original_names):
    per_pool = config["names_per_pool"]
    if per_pool <= 0 or per_pool % 2:
        raise ValueError("names_per_pool must be a positive even number for exact quotas")
    quota = len(config["pool_names"]) * per_pool // 2
    rng = random.Random(config["sampling_seed"])
    surname_weights = [int(row[config["surname_weight_column"]]) for row in surnames]
    names = []
    seen = set()
    log = []
    for stratum, column in config["given_character_weight_columns"].items():
        weights = [int(row[column]) for row in characters]
        accepted = 0
        while accepted < quota:
            if len(log) >= config["max_sampling_attempts"]:
                raise ValueError("Sampling attempt limit reached")
            surname_row = rng.choices(surnames, weights=surname_weights, k=1)[0]
            given_rows = rng.choices(characters, weights=weights, k=config["given_name_characters"])
            given_name = "".join(row["character"] for row in given_rows)
            full_name = surname_row["surname"] + given_name
            reason = "proposed"
            if full_name in seen:
                reason = "duplicate_full_name"
            elif config["avoid_existing_pilot_full_names"] and full_name in original_names:
                reason = "existing_pilot_name"
            elif cache.get(full_name, {}).get("status") == "page_exists":
                reason = "wikipedia_page_exists"
            record = {"draw_id": len(log) + 1, "name": full_name, "surname": surname_row["surname"], "given_name": given_name, "usage_stratum": stratum, "surname_weight": int(surname_row[config["surname_weight_column"]]), "given_character_weights": [int(row[column]) for row in given_rows], "decision": reason}
            log.append(record)
            if reason != "proposed":
                continue
            accepted += 1
            seen.add(full_name)
            names.append({**record, "wiki": cache.get(full_name, {"status": "not_checked"}), "human_review": None, "final_approved": False})
    partition_rng = random.Random(config["partition_seed"])
    pools = {pool: [] for pool in config["pool_names"]}
    for stratum in config["given_character_weight_columns"]:
        stratum_names = [row for row in names if row["usage_stratum"] == stratum]
        partition_rng.shuffle(stratum_names)
        for index, pool in enumerate(config["pool_names"]):
            start = index * per_pool // 2
            pools[pool].extend({**row, "pool": pool} for row in stratum_names[start:start + per_pool // 2])
    for pool in pools.values():
        partition_rng.shuffle(pool)
    return names, pools, log


def pilot_comparison(original_pools, surnames, config):
    frequencies = {row["surname"]: int(row[config["surname_weight_column"]]) for row in surnames}
    sorted_counts = sorted(frequencies.values(), reverse=True)
    ranks = {surname: 1 + sum(count > frequency for count in sorted_counts) for surname, frequency in frequencies.items()}
    rows = []
    summaries = {}
    for pool, names in original_pools.items():
        for name in names:
            surname = name[0]
            if surname not in frequencies:
                raise ValueError(f"Pilot surname absent: {name}")
            rows.append({"pool": pool, "name": name, "surname": surname, "parse_rule": "existing pilot uses single-character surnames", "surname_rank": ranks[surname], "surname_population_count_in_source": frequencies[surname]})
        group = [row for row in rows if row["pool"] == pool]
        summaries[pool] = {"n": len(group), "mean_rank": statistics.mean(row["surname_rank"] for row in group), "median_rank": statistics.median(row["surname_rank"] for row in group), "rank_range": [min(row["surname_rank"] for row in group), max(row["surname_rank"] for row in group)], "mean_log10_source_count": statistics.mean(math.log10(row["surname_population_count_in_source"]) for row in group)}
    return rows, summaries


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fetch-wiki", action="store_true", help="Explicit network mode: fetch pending exact-title checks and replacements")
    args = parser.parse_args()
    config = json.loads((HERE / "config.json").read_text())
    protected_paths = [PILOT / "places_zh.py", PILOT / "build_data_zh.py", PILOT / "data" / "entities_zh.jsonl", PILOT / "data" / "sources_zh.json"]
    protected = {str(path.relative_to(PILOT)): digest(path) for path in protected_paths}
    original_pools = old_pools()
    original_names = {name for names in original_pools.values() for name in names}
    surnames, characters, source = inputs(config)
    for round_index in range(config["max_wiki_rounds"] + 1):
        requests, cache = load_wiki()
        names, pools, log = draw_batch(config, surnames, characters, cache, original_names)
        pending = [name for name in dict.fromkeys(list(original_names) + [row["name"] for row in names]) if name not in cache]
        pending.sort()
        if not args.fetch_wiki or not pending:
            break
        if round_index == config["max_wiki_rounds"]:
            raise ValueError("Wikipedia replacement rounds exhausted")
        fetch_wiki(pending, config, requests)
    reports = HERE / "reports"
    reports.mkdir(exist_ok=True)
    save_rows(reports / "sampling_log.jsonl", log)
    save_rows(reports / "unified_batch.jsonl", names)
    for pool, rows in pools.items():
        save_rows(reports / f"{pool}.jsonl", rows)
    comparison, old_summary = pilot_comparison(original_pools, surnames, config)
    save_rows(reports / "pilot_surname_ranks.jsonl", comparison)
    save_json(reports / "pilot_surname_summary.json", {"groups": old_summary, "interpretation": "Descriptive differences in this frequency source, not a significance test, a current-population estimate, or evidence of an SP effect."})
    save_json(reports / "pending_wiki_requests.json", {"requests": [{"titles": pending[start:start + config["wiki_batch_size"]], "url": wiki_url(pending[start:start + config["wiki_batch_size"]])} for start in range(0, len(pending), config["wiki_batch_size"])]})
    assert len(names) == len({row["name"] for row in names}) == len(config["pool_names"]) * config["names_per_pool"]
    assert {row["name"] for pool in pools.values() for row in pool} == {row["name"] for row in names}
    assert all(Counter(row["usage_stratum"] for row in pool) == {"male_usage": config["names_per_pool"] // 2, "female_usage": config["names_per_pool"] // 2} for pool in pools.values())
    assert protected == {str(path.relative_to(PILOT)): digest(path) for path in protected_paths}
    summary = {"status": "screened_draft_not_approved" if not pending else "pending_wiki_checks", "source_commit": source["commit"], "source_package_version": source["package_version"], "source_files_sha256": {name: record["sha256"] for name, record in source["files"].items()}, "config_sha256": digest(HERE / "config.json"), "unified_batch_size": len(names), "pool_sizes": {pool: len(rows) for pool, rows in pools.items()}, "pool_usage_quotas": {pool: dict(Counter(row["usage_stratum"] for row in rows)) for pool, rows in pools.items()}, "shared_sampling_frame_not_identical_empirical_pool_frequencies": True, "wikipedia_queries": len(requests), "queried_titles": len(cache), "pending_titles": len(pending), "excluded_page_titles": [name for name, entry in cache.items() if entry["status"] == "page_exists" and name not in original_names], "final_names_with_confirmed_missing_titles": sum(row["wiki"]["status"] == "missing_exact_title" for row in names), "human_review": None, "final_approved": False, "original_pilot_files": protected}
    save_json(reports / "summary.json", summary)
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
