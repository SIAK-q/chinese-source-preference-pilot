# -*- coding: utf-8 -*-
"""Check candidate Chinese names/places against zh.wikipedia for contamination."""
import json, sys, time, urllib.parse, urllib.request

API = "https://zh.wikipedia.org/w/api.php"
HDR = {"User-Agent": "MAThesisPilot/1.0 (research)"}

def query(titles):
    q = urllib.parse.urlencode({
        "action": "query", "format": "json", "titles": "|".join(titles),
        "redirects": 1,
    })
    req = urllib.request.Request(API + "?" + q, headers=HDR)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)

def search(term):
    q = urllib.parse.urlencode({
        "action": "query", "format": "json", "list": "search",
        "srsearch": term, "srlimit": 3,
    })
    req = urllib.request.Request(API + "?" + q, headers=HDR)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)["query"]["search"]

names = [l.strip() for l in open(sys.argv[1], encoding="utf-8") if l.strip()]
hits, clean = [], []
for i in range(0, len(names), 20):
    batch = names[i:i+20]
    d = query(batch)
    pages = d["query"]["pages"]
    norm = {}
    for n in d["query"].get("normalized", []): norm[n["to"]] = n["from"]
    for n in d["query"].get("redirects", []): norm[n["to"]] = n["from"]
    exists = set()
    for pid, p in pages.items():
        if int(pid) > 0:
            t = p["title"]
            exists.add(norm.get(t, t))
    for b in batch:
        (hits if b in exists else clean).append(b)
    time.sleep(0.3)

print("=== 有维基条目 (撞车) ===")
for h in hits: print(" ", h)
print("=== 无条目 ===")
print(" ", " ".join(clean))
print(f"\n撞车率: {len(hits)}/{len(names)} = {len(hits)/len(names):.0%}")
