"""Read-only audit of the November 20 report against saved data and probabilities."""
import hashlib
import json
import math
import re
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path
from statistics import mean

ROOT = Path(__file__).resolve().parents[3]
P = ROOT / 'pilot'
OUT = Path(__file__).parent

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def number(s):
    m = re.fullmatch(r'(\d{4})年(\d+)月(\d+)日', s)
    if m:
        return date(*map(int, m.groups())).toordinal()
    m = re.fullmatch(r'(\d{4})年(\d+)月', s)
    if m:
        return int(m[1])*12+int(m[2])
    m = re.fullmatch(r'(\d+)小时(?:(\d+)分钟)?', s)
    if m:
        return int(m[1])*60+int(m[2] or 0)
    m = re.fullmatch(r'(\d+(?:\.\d+)?)(万|亿)?(年|人次|人|元人民币|元|厘米|公斤|克|吨|平方公里|米|层|天|个乡镇|个|个月)', s)
    if m:
        return float(m[1])*{'万':10000, '亿':100000000, None:1}[m[2]]
    return None

def main():
    data = P/'data_generation/final70_20261118_v2/entities_zh.jsonl'
    entities = [json.loads(l) for l in data.read_text().splitlines()]
    expected, numeric, exceptions = {}, [], []
    for e in entities:
        fields = {k:v for k,v in e.items() if isinstance(v,list) and k!='row_order'}
        assert set(e['row_order']) == set(fields) | ({'性别'} if '性别' in e else set()) | ({'作品类型'} if '作品类型' in e else set())
        for f, vals in fields.items():
            assert len(vals)==len(set(vals))==5
            ns = [number(v) for v in vals]
            if all(v is not None for v in ns):
                low, high = sum(v<ns[0] for v in ns[1:]), sum(v>ns[0] for v in ns[1:])
                numeric.append((e['id'],f,low,high))
                if (low,high)!=(2,2):exceptions.append((e['id'],f,vals,low,high))
            for i in range(1,5):
                for order in (0,1):
                    expected[e['id'],f,i,order] = (vals[0],vals[i],e)
    runs = sorted(P.glob('results_baseline/kaggle_final70_20261118/*/raw.json'))
    runs += [P/f'results_baseline/Qwen2.5-{n}B-Instruct_autodl_bf16_final70_v2/raw.json' for n in (14,32)]
    metrics, strong_sets, prompt_reference = [], [], None
    for rawfile in runs:
        raw = json.loads(rawfile.read_text())
        if raw.get('n_records')!=3040:continue
        assert raw['data_sha256']==sha(data)
        assert raw['revision_requested']==raw['revision_loaded']
        rows = raw['results']; seen=set(); pairs=defaultdict(dict)
        for r in rows:
            key=(r['entity_id'],r['field'],r['alt_index'],r['order'])
            assert key not in seen;seen.add(key)
            orig, alt, e = expected[key]
            assert (r['original'],r['alternative'])==(orig,alt)
            assert (r['value_a'],r['value_b']) == ((orig,alt) if r['order']==0 else (alt,orig))
            assert all(math.isfinite(r[k]) and 0<=r[k]<=1 for k in ('prob_a','prob_b'))
            assert abs(r['prob_a']+r['prob_b']-1)<1e-5
            pairs[key[:3]][r['order']]=r['prob_b'] if r['order']==0 else r['prob_a']
        assert seen==set(expected)
        prompts_file=rawfile.parent/'prompts.jsonl'
        assert sha(prompts_file)==raw['prompts_sha256']
        prompts=[json.loads(l) for l in prompts_file.read_text().splitlines()]
        assert len(prompts)==3040
        for r in prompts:
            key=(r['entity_id'],r['field'],r['alt_index'],r['order'])
            orig,alt,e=expected[key]
            tables=re.findall(r'\| 名称 \|.*?(?=\n\n)',r['user'],re.S)
            assert len(tables)==2
            for t in tables:
                table_rows=[l.split('|')[1:3] for l in t.splitlines()]
                assert [a.strip() for a,b in table_rows]==['名称']+e['row_order']
                for a,b in table_rows:
                    f,v=a.strip(),b.strip()
                    if f=='名称':assert v==e['name']
                    elif f!=key[1]:assert v==(e[f][0] if isinstance(e[f],list) else e[f])
            vals=[dict((a.strip(),b.strip()) for a,b in [l.split('|')[1:3] for l in t.splitlines()])[key[1]] for t in tables]
            assert tuple(vals)==((orig,alt) if key[3]==0 else (alt,orig))
        canonical=[{k:r[k] for k in ('entity_id','field','alt_index','order','system','user')} for r in prompts]
        if prompt_reference is None:prompt_reference=canonical
        else:assert canonical==prompt_reference
        exact={k:('alternative' if min(v.values())>.8 else 'original') for k,v in pairs.items() if min(v.values())>.8 or max(v.values())<.2}
        rounded={k:('alternative' if min(round(x,3) for x in v.values())>.8 else 'original') for k,v in pairs.items() if min(round(x,3) for x in v.values())>.8 or max(round(x,3) for x in v.values())<.2}
        strong_sets.append(rounded)
        directions=defaultdict(list)
        for k,v in pairs.items():
            orig,alt,_=expected[k+(0,)]
            no,na=number(orig),number(alt)
            if no is not None and na is not None:
                directions['higher_later' if na>no else 'lower_earlier'].append(mean(v.values()))
        metrics.append({'model':raw['model'],'revision':raw['revision_loaded'],'dtype':raw['dtype'],
            'raw_file':str(rawfile.relative_to(ROOT)),'raw_sha256':sha(rawfile),
            'prompts_sha256':sha(prompts_file),'n_prompts':len(rows),'n_pairs':len(pairs),
            'mean_P_alternative_pct':round(100*mean(x for v in pairs.values() for x in v.values()),1),
            'mean_P_table2_pct':round(100*mean(r['prob_b'] for r in rows),1),
            'strong_report_rounded':len(rounded),'strong_unrounded':len(exact),
            'strong_original':sum(v=='original' for v in rounded.values()),'strong_alternative':sum(v=='alternative' for v in rounded.values()),
            'directions_all_numeric_including_warranty':{k:{'n_pairs':len(v),'mean_P_alternative_pct':round(mean(v)*100,1)} for k,v in directions.items()},
            'rounding_boundary_keys':[list(k) for k in exact.keys()-rounded.keys()]})
    shared=[{'entity_id':k[0],'field':k[1],'alt_index':k[2],'preferred':v} for k,v in strong_sets[0].items() if all(s.get(k)==v for s in strong_sets)]
    result={'date':'2026-11-20','actor':'Codex','checks':'Assertions in audit.py; no inference or dataset edits',
        'data_sha256':sha(data),'entities':len(entities),'by_type':dict(Counter(e['entity_class'] for e in entities)),
        'attribute_instances':len(expected)//8,'pairs':len(expected)//2,'prompts':len(expected),
        'numeric_date_and_duration_attributes':len(numeric),'two_below_two_above':len(numeric)-len(exceptions),
        'numeric_exceptions':exceptions,'numeric_by_field':dict(Counter(x[1] for x in numeric)),
        'runs':metrics,'identical_baseline_prompts_across_runs':True,'shared_strong_pairs':shared,
        'shared_by_field':dict(Counter(x['field'] for x in shared))}
    (OUT/'audit_results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('shared_strong_pairs',)},ensure_ascii=False,indent=2))

if __name__=='__main__':main()
