"""按预存规则补建筑备选；原始输出不变，精度例外留档。"""
import hashlib
import json
import math
import re
import sys
from datetime import datetime
from decimal import Decimal, ROUND_FLOOR
from pathlib import Path
from prepare_person import BASE, read, save_new
sys.path.insert(0, str(BASE.parents[1]))
from data_review.validate_entity_batch import check
from prompt_zh import create_entity_table, make_row_order
from run_baseline import build_records

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def alternatives(value):
    m=re.fullmatch(r'(\d+(?:\.\d+)?)(.+)',value)
    number,unit=Decimal(m[1]),m[2]
    precision=max(0,-number.as_tuple().exponent)
    step=Decimal(1).scaleb(-precision)
    n=int((number*Decimal('.05')/step).to_integral_value(rounding=ROUND_FLOOR))
    exception=n<2
    n=max(2,n)
    offsets=[-n,-math.ceil(n/2),math.ceil(n/2),n]
    nums=[number+step*k for k in offsets]
    assert min(nums)>0
    return [value,*[f'{v:.{precision}f}{unit}' for v in nums]],{'offsets_in_steps':offsets,'step':str(step),'precision_exception':exception,'actual_maximum_percent':str(max(abs(v-number)/number*100 for v in nums))}

inputs=read(BASE/'building.input.json')
fields=read(BASE/'fields.json')['building']
script_hash=sha(Path(__file__))
rows=[]
originals=[]
exceptions=[]
for identity in inputs['identities']:
    folder=BASE/'entities'/identity['id']
    raw=read(folder/'original.raw.json')
    assert read(folder/'original.input.json')['previous_same_type_originals']==originals
    raw_hash=sha(folder/'original.raw.json')
    material=read(folder/'alternatives.material.raw.json')
    assert len({frozenset(re.split('[、和]',v)) for v in [raw['主要材料'],*material]})==5
    save_new(folder/'05_rule_inputs.execution_record.json',{'date':datetime.now().astimezone().isoformat(),'actor':'Codex','step':'inputs_saved_before_rule_generation','script':'../../assemble_building.py','script_sha256':script_hash,'original':raw,'original_sha256':raw_hash,'material_raw_sha256':sha(folder/'alternatives.material.raw.json'),'designer_candidates':identity['architect_candidates'],'year_offsets':[-2,-1,1,2],'floor_offsets':[-2,-1,1,2],'numeric_rule':'约±5%，两低两高，保持精度；不足四值时取相邻两档并记录幅度。','row_order_seed':f"42:{raw['id']}"})
    entity={k:v for k,v in raw.items() if k not in fields}
    entity['设计师']=identity['architect_candidates']
    assert entity['设计师'][0]==raw['设计师']
    year=int(raw['建成年份'].removesuffix('年'))
    assert year+2<=2026
    entity['建成年份']=[raw['建成年份'],*[f'{year+k}年' for k in [-2,-1,1,2]]]
    floor=int(raw['层数'].removesuffix('层'))
    assert floor-2>=1
    entity['层数']=[raw['层数'],*[f'{floor+k}层' for k in [-2,-1,1,2]]]
    entity['主要材料']=[raw['主要材料'],*material]
    steps=[]
    for field in ['高度','容纳人数']:
        entity[field],detail=alternatives(raw[field])
        steps.append({'field':field,**detail})
        if detail['precision_exception']: exceptions.append({'id':raw['id'],'field':field,'values':entity[field],**detail})
    entity['row_order']=make_row_order(entity)
    assert all(len(entity[f])==len(set(entity[f]))==5 and entity[f][0]==raw[f] for f in fields)
    assert sha(folder/'original.raw.json')==raw_hash
    save_new(folder/'entity.pending_review.json',entity)
    save_new(folder/'06_assembly.execution_record.json',{'date':datetime.now().astimezone().isoformat(),'actor':'Codex','script_sha256':script_hash,'steps':steps,'designer_rule':'预分配五名；无模型调用','years_and_floors_offsets':[-2,-1,1,2],'output':'entity.pending_review.json','checks':{'five_distinct_values':True,'originals_unchanged':True},'user_review':'候选待审','edits_to_raw_outputs':[]})
    rows.append(entity)
    originals.append(raw)
validation=check(rows,require_row_order=True,per_type={'building':10})
assert not validation['errors'],validation
records=build_records(rows,(1,2,3,4))
assert len(records)==480
for n in range(0,len(records),2):
    a,b=records[n:n+2]
    assert (a['value_a'],a['value_b'])==(b['value_b'],b['value_a'])
for entity in rows:
    for field in fields:
        a=create_entity_table(entity,field,entity[field][0])
        for alt in entity[field][1:]:
            b=create_entity_table(entity,field,alt)
            assert [k for k in a if a[k]!=b[k]]==[field]
assert len(exceptions)==9
for filename,values in [('building.entities.pending_review.jsonl',rows),('building.originals.pending_review.jsonl',originals),('building.baseline_prompt_preview.jsonl',records)]:
    with (BASE/filename).open('x') as f: f.write(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in values))
save_new(BASE/'13_building_complete.execution_record.json',{'date':datetime.now().astimezone().isoformat(),'actor':'Codex','script_sha256':script_hash,'validation':validation,'precision_exceptions':exceptions,'checks':{'originals_unchanged':True,'prior_inputs_match_outputs':True,'single_field_differs':True,'both_orders_reverse_values':True,'480_prompts_previewed':True},'data_sha256':sha(BASE/'building.entities.pending_review.jsonl'),'generation_boundary':'原值与材料备选在当前会话生成，具体模型版本参数不可见；其他备选由已保存脚本规则生成。','model_inference_run':False,'user_review':'建筑候选待审'})
print(json.dumps({'entities':10,'attributes':60,'previews':len(records),'precision_exceptions':len(exceptions),'validation':validation},ensure_ascii=False))
