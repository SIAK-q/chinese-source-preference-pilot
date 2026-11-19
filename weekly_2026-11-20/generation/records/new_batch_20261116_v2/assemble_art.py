"""按预存规则补艺术备选，并将固定作品类型显示为背景行。"""
import hashlib,json,math,re,sys
from datetime import datetime
from decimal import Decimal,ROUND_FLOOR
from pathlib import Path
from prepare_person import BASE,read,save_new
sys.path.insert(0,str(BASE.parents[1]))
from data_review.validate_entity_batch import check
from prompt_zh import create_entity_table,make_row_order
from run_baseline import build_records

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dimensions(value):
    n=Decimal(value.removesuffix('厘米'));maximum=int((n*Decimal('.05')).to_integral_value(rounding=ROUND_FLOOR));assert maximum>=2
    offsets=[-maximum,-math.ceil(maximum/2),math.ceil(maximum/2),maximum]
    return [value,*[f'{n+k:.0f}厘米' for k in offsets]],{'offsets_cm':offsets,'actual_maximum_percent':str(max(Decimal(abs(k))/n*100 for k in offsets)),'precision_exception':False}

fields=read(BASE/'fields.json')['art'];config=read(BASE/'art.input.json');script_hash=sha(Path(__file__));rows=[];originals=[]
for identity in config['identities']:
    folder=BASE/'entities'/identity['id'];raw=read(folder/'original.raw.json');saved=read(folder/'03_material_input.execution_record.json')
    assert read(folder/'original.input.json')['previous_same_type_originals']==originals
    assert sha(folder/'original.raw.json')==saved['original_sha256']
    materials=read(folder/'alternatives.material.raw.json')
    save_new(folder/'05_rule_inputs.execution_record.json',{'date':datetime.now().astimezone().isoformat(),'actor':'Codex','step':'rule_inputs_saved_before_generation','script_sha256':script_hash,'original':raw,'original_sha256':sha(folder/'original.raw.json'),'material_sha256':sha(folder/'alternatives.material.raw.json'),'creator_candidates':identity['creator_candidates'],'year_offsets':[-2,-1,1,2],'numeric_percent':5,'numeric_precision':'整数厘米，两低两高','row_order_seed':f"42:{raw['id']}",'fixed_type_rendering':'description保留，同时复制为标量作品类型以显示在两张表；不改类型、不作冲突属性。'})
    entity={k:v for k,v in raw.items() if k not in fields};entity['作品类型']=raw['description']
    entity['创作者']=identity['creator_candidates'];assert entity['创作者'][0]==raw['创作者']
    year=int(raw['创作年份'].removesuffix('年'));assert year+2<=2026
    entity['创作年份']=[raw['创作年份'],*[f'{year+k}年' for k in [-2,-1,1,2]]]
    entity['材料']=[raw['材料'],*materials];steps=[]
    for field in ['高度','宽度']:
        entity[field],detail=dimensions(raw[field]);steps.append({'field':field,**detail})
    entity['row_order']=make_row_order(entity)
    assert all(len(entity[f])==len(set(entity[f]))==5 and entity[f][0]==raw[f] for f in fields)
    assert sha(folder/'original.raw.json')==saved['original_sha256']
    save_new(folder/'entity.pending_review.json',entity)
    save_new(folder/'06_assembly.execution_record.json',{'date':datetime.now().astimezone().isoformat(),'actor':'Codex','script_sha256':script_hash,'steps':steps,'creator_rule':'预分配五名，首名原值，后四名备选','year_offsets':[-2,-1,1,2],'fixed_type':raw['description'],'derived_field':'作品类型由description复制，用于两表显示','checks':{'five_distinct':True,'raw_originals_unchanged':True,'type_unchanged':True,'all_attributes_original_values_unchanged':True},'user_review':'候选待审','output':'entity.pending_review.json'})
    rows.append(entity);originals.append(raw)
validation=check(rows,require_row_order=True,per_type={'art':10});assert not validation['errors'],validation
records=build_records(rows,(1,2,3,4));assert len(records)==400
for i in range(0,len(records),2):
    a,b=records[i:i+2];assert (a['value_a'],a['value_b'])==(b['value_b'],b['value_a'])
    assert a['field']!='作品类型' and b['field']!='作品类型'
for entity in rows:
    for field in fields:
        a=create_entity_table(entity,field,entity[field][0])
        for alt in entity[field][1:]:
            b=create_entity_table(entity,field,alt);assert [k for k in a if a[k]!=b[k]]==[field]
            assert a['作品类型']==b['作品类型']==entity['description']
creators=[v for e in rows for v in e['创作者']];assert len(set(creators))==50
buildings=[json.loads(s) for s in (BASE/'building.entities.pending_review.jsonl').read_text().splitlines()]
assert not set(creators)&{v for e in buildings for v in e['设计师']}
for filename,data in [('art.entities.pending_review.jsonl',rows),('art.originals.pending_review.jsonl',originals),('art.baseline_prompt_preview.jsonl',records)]:
    with (BASE/filename).open('x') as f:f.write(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in data))
save_new(BASE/'20_art_complete.execution_record.json',{'date':datetime.now().astimezone().isoformat(),'actor':'Codex','script_sha256':script_hash,'validation':validation,'data_sha256':sha(BASE/'art.entities.pending_review.jsonl'),'precision_exceptions':[],'checks':{'prior_inputs_match_raw_outputs':True,'raw_originals_unchanged':True,'fixed_type_displayed_in_both_tables':True,'type_not_tested_as_conflict':True,'only_one_attribute_differs':True,'both_orders_reverse_values':True,'100_building_and_art_names_unique':True,'400_prompts_previewed':True},'generation_boundary':'原值和材料备选由当前会话撰写，模型版本参数不可见；创作者按已准备名单，年份尺寸由脚本生成。','model_inference_run':False,'user_review':'候选待审'})
print(json.dumps({'entities':10,'validation':validation,'type_fixed_and_visible':True,'precision_exceptions':0},ensure_ascii=False))
