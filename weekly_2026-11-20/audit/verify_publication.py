"""Run from the public weekly folder: python3 audit/verify_publication.py."""
import gzip
import hashlib
import json
import math
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean
sys.dont_write_bytecode = True
from audit_source_workspace import number

ROOT=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    for line in (ROOT/'SHA256SUMS').read_text().splitlines():
        digest,rel=line.split('  ',1)
        assert sha(ROOT/rel)==digest,rel
    for item in json.loads((ROOT/'audit/publication_manifest.json').read_text())['copies']:
        assert sha(ROOT/item['published'])==item['sha256'],item['published']
    data=ROOT/'data/entities_zh.jsonl'
    saved=json.loads((ROOT/'audit/results.json').read_text())
    assert sha(data)==saved['data_sha256']
    entities=[json.loads(l) for l in data.read_text().splitlines()]
    assert len(entities)==70
    expected={};numeric=0
    for e in entities:
        for field,values in e.items():
            if not isinstance(values,list) or field=='row_order':continue
            assert len(values)==len(set(values))==5
            ns=[number(x) for x in values]
            if all(x is not None for x in ns):
                assert sum(x<ns[0] for x in ns[1:])==sum(x>ns[0] for x in ns[1:])==2
                numeric+=1
            for alt in range(1,5):
                for order in (0,1):expected[e['id'],field,alt,order]=(values[0],values[alt])
    assert len(expected)==3040 and numeric==250
    prompts=[json.loads(l) for l in (ROOT/'baseline/prompts.jsonl').read_text().splitlines()]
    assert {(x['entity_id'],x['field'],x['alt_index'],x['order']) for x in prompts}==set(expected)
    strongs=[]
    for metric in saved['runs']:
        raw=json.loads((ROOT/'baseline/raw'/ (metric['model'].split('/')[-1]+'.json')).read_text())
        assert raw['revision_loaded']==raw['revision_requested']==metric['revision']
        assert raw['data_sha256']==sha(data)
        assert raw['prompts_sha256']==sha(ROOT/'baseline/prompts.jsonl')
        pairs=defaultdict(dict);keys=[]
        for row in raw['results']:
            key=(row['entity_id'],row['field'],row['alt_index'],row['order']);keys.append(key)
            orig,alt=expected[key]
            assert (row['original'],row['alternative'])==(orig,alt)
            assert (row['value_a'],row['value_b'])==((orig,alt) if key[-1]==0 else (alt,orig))
            assert all(math.isfinite(row[p]) and 0<=row[p]<=1 for p in ('prob_a','prob_b'))
            assert abs(row['prob_a']+row['prob_b']-1)<1e-5
            pairs[key[:3]][key[-1]]=row['prob_b'] if key[-1]==0 else row['prob_a']
        assert len(keys)==len(set(keys))==3040 and set(keys)==set(expected)
        assert round(100*mean(x['prob_b'] for x in raw['results']),1)==metric['mean_P_table2_pct']
        assert round(100*mean(x for v in pairs.values() for x in v.values()),1)==metric['mean_P_alternative_pct']
        strong={k:('alternative' if min(v.values())>.8 else 'original') for k,v in pairs.items() if min(v.values())>.8 or max(v.values())<.2}
        assert len(strong)==metric['strong_unrounded']==metric['strong_report_rounded']
        assert sum(v=='original' for v in strong.values())==metric['strong_original']
        assert sum(v=='alternative' for v in strong.values())==metric['strong_alternative']
        direction=defaultdict(list)
        for k,v in pairs.items():
            orig,alt=expected[k+(0,)];no,na=number(orig),number(alt)
            if no is not None and na is not None:direction['higher_later' if na>no else 'lower_earlier'].append(mean(v.values()))
        for k,v in direction.items():
            assert len(v)==metric['directions_all_numeric_including_warranty'][k]['n_pairs']==500
            assert round(mean(v)*100,1)==metric['directions_all_numeric_including_warranty'][k]['mean_P_alternative_pct']
        strongs.append(strong)
    shared={k:v for k,v in strongs[0].items() if all(s.get(k)==v for s in strongs)}
    assert len(shared)==19
    assert shared=={(x['entity_id'],x['field'],x['alt_index']):x['preferred'] for x in saved['shared_strong_pairs']}
    manifest=json.loads((ROOT/'sources/manifest.json').read_text())
    full=gzip.decompress((ROOT/'sources/prompts.jsonl.gz').read_bytes())
    assert hashlib.sha256(full).hexdigest()==manifest['prompts_sha256']
    source_rows=[json.loads(l) for l in full.splitlines()]
    assert Counter(x['condition'] for x in source_rows)==dict.fromkeys(manifest['conditions'],3040)
    paired=defaultdict(dict)
    for x in source_rows:
        paired[x['condition'],x['entity_id'],x['field'],x['alt_index']][x['order']]=x
    assert len(paired)==7600
    for a in paired.values():
        x,y=a[0],a[1]
        assert (x['value_a'],x['value_b'],x['source_a'],x['source_b'])==(y['value_b'],y['value_a'],y['source_b'],y['source_a'])
    # Resolve exact-title Wikipedia checks using the saved API response bodies.
    requests=json.loads((ROOT/'sources/wiki/wiki_requests.json').read_text())['requests']
    status={}
    for req in requests:
        response=ROOT/'sources/wiki'/req['file']
        assert sha(response)==req['sha256']
        q=json.loads(response.read_text())['query']
        norm={x['from']:x['to'] for x in q.get('normalized',[])}
        redirects={x['from']:x['to'] for x in q.get('redirects',[])}
        pages={x['title']:x for x in q['pages']}
        for title in req['titles']:
            resolved=norm.get(title,title)
            seen=set()
            while resolved in redirects and resolved not in seen:
                seen.add(resolved);resolved=redirects[resolved]
            page=pages.get(resolved)
            if page is not None:status[title]='missing' not in page
    kept=manifest['sampling']['person_names']
    assert len(kept)==len({x['name'] for x in kept})==1520
    assert all(status[x['name']] is False for x in kept)
    skipped=manifest['sampling']['person_wiki']['skipped_page_exists']
    assert len(skipped)==36 and all(status[n] for n in skipped)
    for path in ROOT.rglob('*.md'):
        for link in re.findall(r'\]\(([^)]+)\)',path.read_text()):
            if link.startswith(('http:','https:','#','obsidian:')):continue
            assert (path.parent/link.split('#')[0].strip('<>')).exists(),(str(path),link)
    print('PASS: file hashes; 70 entities/380 items; 250 numeric/date/duration items; five 3040-prompt baselines; 19 shared pairs; 15200 prepared source prompts; 1520 retained names and 36 rejected draws; local Markdown links.')

if __name__=='__main__':main()
