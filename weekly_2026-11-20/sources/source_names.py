# -*- coding: utf-8 -*-
"""信源名生成（按 SOURCE_GENERATION_PROTOCOL_DRAFT.md，11-09 版）。旧 source_sampling.py 不动。

四类信源，每题现抽（WFW 也是逐题抽信源，helpers/source_generator.py）：
- 政府：{地名}市{机构}；机构按实体类型从规程表里随机抽一个，地名从信源地名池抽。
- 报纸：{地名}＋日报／晚报／时报／晨报／都市报，五种等概率；不用“商报”（11-09 会议）。
- 个人：每对现抽（11-16 用户定，同 WFW helpers/runner.py:391-392 "fresh per pair"）。
    规则同 name_generation/person/sample_person_names.py：姓按 n.1930_2008 加权，名两字按 n.male 或 n.female 加权，
    男女用字各半；同批不重名；排除实体人物、属性值人物、旧个人信源及旧 pilot 名字。people 传名单时仍按名单抽（旧用法）。
- 社媒：用户 @{昵称}。两种昵称交替使用，各占一半（11-12 用户定，按 11-09 会议“mix it up”）：
    形容词＋的＋名词＋四位数字（1000–9999），词表 name_generation/social/wordlists.json（217 形容词、198 名词）；
    用户＋10位数字（微博新账号默认昵称，首位非0），例如“用户 @用户7829104852”。
- 无信源：固定写“无可用信源”。

政府和报纸从同一个地名池各抽各的；地名池须与实体地名不重叠（--exclude-places 检查）。
同一批内社媒昵称不重复。

预览：
  python3 data_generation/source_names.py --places P.txt --people N.txt --preview 8 \
      [--exclude-places E.txt] [--out X.json]
名单文件：每行一个名称，或 jsonl（取 "name" 字段）。
"""
import argparse
import hashlib
import json
import random
from pathlib import Path

HERE = Path(__file__).resolve().parent
PILOT = HERE.parent
HANDLE_DIGITS = 10
PERSON_DIR = PILOT / "name_generation/person"
PERSON_POOLS = PERSON_DIR / "reports_extended_20261115"

WORDLISTS = PILOT / "name_generation/social/wordlists.json"

SUFFIXES = ("日报", "晚报", "时报", "晨报", "都市报")
AGENCIES = {
    "person": ("公安局", "民政局", "人力资源和社会保障局"),
    "organization": ("市场监督管理局", "统计局", "人力资源和社会保障局"),
    "location": ("统计局", "民政局", "规划和自然资源局"),
    "building": ("住房和城乡建设局", "规划和自然资源局"),
    "event": ("文化和旅游局", "商务局"),
    "event_sports": ("体育局", "文化和旅游局"),
    "product": ("市场监督管理局", "商务局"),
    "art": ("文化和旅游局", "版权局"),  # 两个机构由 random.choice 等概率抽取
}
SPORTS_WORDS = ("马拉松", "运动会", "体育", "联赛", "锦标赛", "龙舟")   # 活动名含这些词 → 体育活动
NO_SOURCE = "无可用信源"


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read_names(path):
    names = []
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            names.append(json.loads(line)["name"] if line.startswith("{") else line)
    if len(set(names)) != len(names):
        raise ValueError(f"{path} 有重复名称")
    return names


def entity_type(entity):
    cls = entity["entity_class"]
    if cls == "event" and any(w in entity["name"] for w in SPORTS_WORDS):
        return "event_sports"
    return cls


class SourceNamer:
    def __init__(self, places, people, seed=20261111, exclude_places=()):
        overlap = set(places) & set(exclude_places)
        if overlap:
            raise ValueError(f"信源地名与实体地名重叠：{sorted(overlap)}")
        self.places = list(places)
        self.people = list(people) if people is not None else None   # None = 每对现抽
        self.seed = seed
        self.rng = random.Random(seed)
        self.seen_handles = set()
        self.n_handles = 0   # 偶数次→形容词式，奇数次→用户＋数字，保证各占一半
        words = json.loads(WORDLISTS.read_text(encoding="utf-8"))
        self.adjectives, self.nouns = words["adjectives"], words["nouns"]
        if (len(self.adjectives), len(self.nouns)) != (217, 198):
            raise ValueError("昵称词表数量不是 217/198，与规程不符")
        self.person_log = []
        if self.people is None:
            self._init_person_sampler()

    def _init_person_sampler(self):
        import sys
        sys.path.insert(0, str(PERSON_DIR))
        import sample_person_names as base
        config = json.loads((PERSON_DIR / "config.json").read_text())
        self.surnames, self.characters, _ = base.inputs(config)
        self.surname_weights = [int(r[config["surname_weight_column"]]) for r in self.surnames]
        self.char_columns = config["given_character_weight_columns"]
        self.char_weights = {k: [int(r[c]) for r in self.characters] for k, c in self.char_columns.items()}
        blocked = {n for names in base.old_pools().values() for n in names}
        for pool in ("entity_people", "attribute_people", "individual_sources"):
            for line in (PERSON_POOLS / f"{pool}.jsonl").read_text().splitlines():
                blocked.add(json.loads(line)["name"])
        self.person_blocked = blocked
        self.person_seen = set()
        self.person_rng = random.Random(f"person-source:{self.seed}")
        # 11-19 补：同 WFW helpers/source_generator.py:276-353，现抽姓名查中文维基精确标题，有页面即跳过重抽。
        self.wiki_base, self.person_config = base, config
        _, self.wiki_cache = base.load_wiki()
        self.person_wiki_skipped = []

    def fresh_person(self, pair_key=None):
        for _ in range(100000):
            stratum = self.person_rng.choice(sorted(self.char_columns))
            surname = self.person_rng.choices(self.surnames, weights=self.surname_weights, k=1)[0]["surname"]
            given = "".join(r["character"] for r in self.person_rng.choices(
                self.characters, weights=self.char_weights[stratum], k=2))
            name = surname + given
            if name in self.person_blocked or name in self.person_seen:
                continue
            if self.wiki_cache.get(name, {}).get("status") == "page_exists":
                self.person_wiki_skipped.append(name)
                continue
            self.person_seen.add(name)
            item = {"name": name, "category": "person", "surname": surname, "given_name": given,
                    "usage_stratum": stratum, "pair_key": pair_key}
            self.person_log.append(item)
            return dict(item)
        raise RuntimeError("找不到新的不重复人名")

    def wiki_pending(self):
        """已抽出、但还没查过中文维基的个人信源名。"""
        return sorted({x["name"] for x in self.person_log} - set(self.wiki_cache))

    def wiki_fetch(self, names):
        """分批查询（每批50个），批间停3秒；遇429限流等60秒重试。"""
        import time
        import urllib.error
        names, size = list(names), self.person_config["wiki_batch_size"]
        for start in range(0, len(names), size):
            for attempt in range(6):
                try:
                    requests, _ = self.wiki_base.load_wiki()
                    self.wiki_base.fetch_wiki(names[start:start + size], self.person_config, requests)
                    break
                except urllib.error.HTTPError as e:
                    if e.code != 429 or attempt == 5:
                        raise
                    time.sleep(60)
            time.sleep(3)

    def handle(self):
        plain = self.n_handles % 2 == 1
        for _ in range(100000):
            if plain:
                h, form = "用户" + str(self.rng.randint(10 ** (HANDLE_DIGITS - 1), 10 ** HANDLE_DIGITS - 1)), "用户+数字"
            else:
                h = f"{self.rng.choice(self.adjectives)}的{self.rng.choice(self.nouns)}{self.rng.randint(1000, 9999)}"
                form = "形容词的名词+四位数"
            if h not in self.seen_handles:
                self.seen_handles.add(h)
                self.n_handles += 1
                return h, form
        raise RuntimeError("找不到新的不重复昵称")

    def draw(self, category, entity, pair_key=None):
        if category is None:
            return None
        if category == "no_source":
            return {"name": NO_SOURCE, "category": category}
        if category == "government":
            key = entity_type(entity)
            agency, place = self.rng.choice(AGENCIES[key]), self.rng.choice(self.places)
            return {"name": f"{place}市{agency}", "category": category,
                    "place": place, "agency": agency, "entity_type": key}
        if category == "newspaper":
            place, suffix = self.rng.choice(self.places), self.rng.choice(SUFFIXES)
            return {"name": place + suffix, "category": category, "place": place, "suffix": suffix}
        if category == "person":
            if self.people is None:
                return self.fresh_person(pair_key)
            return {"name": self.rng.choice(self.people), "category": category}
        if category == "social_media":
            h, form = self.handle()
            return {"name": f"用户 @{h}", "category": category, "handle": h, "form": form}
        raise ValueError(f"未知信源类别：{category}")

    def provenance(self, places_file=None, people_file=None):
        return {"protocol": "SOURCE_GENERATION_PROTOCOL_DRAFT.md (2026-11-09)", "seed": self.seed,
                "handle_format": f"alternate 1:1: adjective+的+noun+4 digits / 用户 + {HANDLE_DIGITS} digits, first non-zero",
                "wordlists_sha256": sha(WORDLISTS),
                "suffixes": SUFFIXES, "agencies": AGENCIES, "sports_words": SPORTS_WORDS,
                "script_sha256": sha(__file__),
                "places_file_sha256": sha(places_file) if places_file else None,
                "people_file_sha256": sha(people_file) if people_file else None,
                "n_places": len(self.places),
                "person_mode": "fresh_per_pair" if self.people is None else "list",
                "n_people": None if self.people is None else len(self.people),
                "person_pools_sha256": {p: sha(PERSON_POOLS / f"{p}.jsonl") for p in
                                        ("entity_people", "attribute_people", "individual_sources")},
                "person_names": self.person_log,
                "person_wiki": None if self.people is not None else {
                    "rule": "exact zh.wikipedia title (redirects followed); page exists -> skip and redraw",
                    "drawn_checked": sum(1 for x in self.person_log if x["name"] in self.wiki_cache),
                    "drawn_total": len(self.person_log),
                    "skipped_page_exists": self.person_wiki_skipped,
                    "wiki_requests_sha256": sha(PERSON_DIR / "wiki_requests.json")}}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--places", required=True)
    ap.add_argument("--people", required=True)
    ap.add_argument("--exclude-places", help="实体地名名单，须与信源地名不重叠")
    ap.add_argument("--seed", type=int, default=20261111)
    ap.add_argument("--preview", type=int, default=8, help="每类预览几个")
    ap.add_argument("--out")
    a = ap.parse_args()
    namer = SourceNamer(read_names(a.places), read_names(a.people), a.seed, read_names(a.exclude_places) if a.exclude_places else ())
    demo = [{"name": "示例人物", "entity_class": "person"}, {"name": "示例建筑", "entity_class": "building"},
            {"name": "示例国际马拉松赛", "entity_class": "event"}]
    out = {"provenance": namer.provenance(a.places, a.people), "preview": {}}
    for cat in ("government", "newspaper", "person", "social_media"):
        out["preview"][cat] = [namer.draw(cat, demo[i % len(demo)]) for i in range(a.preview)]
        print(cat, "：", "、".join(x["name"] for x in out["preview"][cat]))
    if a.out:
        Path(a.out).write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
