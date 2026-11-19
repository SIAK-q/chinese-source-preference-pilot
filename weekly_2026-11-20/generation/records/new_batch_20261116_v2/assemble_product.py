"""按已审产品规则组装备选；产品精度不足立即报告，不放宽±5%。"""
import hashlib,json,math,random,re,sys
from datetime import datetime,timedelta
from decimal import Decimal,ROUND_FLOOR
from pathlib import Path
from prepare_person import BASE,read,save_new
sys.path.insert(0,str(BASE.parents[1]))
from data_review.validate_entity_batch import check
from prompt_zh import create_entity_table,make_row_order
from run_baseline import build_records

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def numeric(value):
    m=re.fullmatch(r'(\d+(?:\.\d+)?)(.+)',value);n,unit=Decimal(m[1]),m[2];precision=max(0,-n.as_tuple().exponent);step=Decimal(1).scaleb(-precision)
    max_steps=int((n*Decimal('.05')/step).to_integral_value(rounding=ROUND_FLOOR))
    if max_steps<2:raise ValueError(f'产品同精度无法在±5%得到四值，须报告等待处理：{value}')
    offsets=[-max_steps,-math.ceil(max_steps/2),math.ceil(max_steps/2),max_steps];nums=[n+step*k for k in offsets]
    assert min(nums)>0 and all(abs(x-n)/n<=Decimal('.05') for x in nums)
    return [value,*[f'{x:.{precision}f}{unit}' for x in nums]],{'unit':unit,'precision':precision,'step':str(step),'offsets_in_steps':offsets,'actual_maximum_percent':str(max(abs(x-n)/n*100 for x in nums)),'precision_exception':False}

fields=read(BASE/'fields.json')['product'];rows=[];originals=[];flags=[];script_hash=sha(Path(__file__));slots=[3,6,12,18,24,36,48,60]
for i in range(1,11):
    folder=BASE/'entities'/f'PRODUCT-{i:02}';raw=read(folder/'original.raw.json');inp=read(folder/'03_alternatives_input.execution_record.json')
    assert read(folder/'original.input.json')['previous_products']==originals
    assert sha(folder/'original.raw.json')==inp['original_sha256']
    assert sha(folder/'alternatives.prompt.txt')==inp['prompt_sha256']
    seed=inp['date_seed'];name_revision=folder/'manufacturer.revision.raw.json'
    manufacturers=read(name_revision)['data']['制造商'] if name_revision.exists() else [raw['制造商'],*read(folder/'alternatives.manufacturer.raw.json')]
    save_new(folder/'05_rule_inputs.execution_record.json',{'date':datetime.now().astimezone().isoformat(),'actor':'Codex','step':'rule_inputs_saved_before_execution','script_sha256':script_hash,'original':raw,'date_seed':seed,'date_windows_days':inp['date_windows_days'],'numeric_percent':5,'numeric_precision_exception_allowed':False,'warranty_slots':slots,'manufacturer_values':manufacturers,'manufacturer_revision':str(name_revision.name) if name_revision.exists() else None,'row_order_seed':f"42:{raw['id']}"})
    entity={k:v for k,v in raw.items() if k not in fields};entity['制造商']=manufacturers
    original_date=datetime.strptime(raw['发布日期'],'%Y年%m月%d日').date();rng=random.Random(seed)
    offsets=[rng.randint(a,b) for a,b in inp['date_windows_days']];dates=[original_date+timedelta(days=d) for d in offsets]
    assert all(d.isoformat()<='2026-11-17' for d in dates)
    entity['发布日期']=[raw['发布日期'],*[f'{d.year}年{d.month}月{d.day}日' for d in dates]]
    steps=[{'field':'发布日期','offsets_days':offsets,'seed':seed}]
    for field in ['价格','重量']:
        entity[field],detail=numeric(raw[field]);steps.append({'field':field,**detail})
    months=int(re.fullmatch(r'整机保修(\d+)个月',raw['保修期'])[1]);idx=slots.index(months)
    if idx<2 or idx+2>=len(slots):raise ValueError(f"{raw['id']}保修档位不足：{months}")
    alternatives=slots[idx-2:idx]+slots[idx+1:idx+3]
    entity['保修期']=[raw['保修期'],*[f'整机保修{m}个月' for m in alternatives]]
    steps.append({'field':'保修期','rule':'固定档位取最近两低两高','month_alternatives':alternatives})
    if 3 in alternatives:flags.append({'id':raw['id'],'field':'保修期','value':'整机保修3个月','actor':'Codex','reason':'按已审档位机械得到，但对该日常产品偏短；相容性尚未确认，不记为通过。','user_decision':'待看'})
    entity['row_order']=make_row_order(entity)
    assert all(len(entity[f])==len(set(entity[f]))==5 and entity[f][0]==raw[f] for f in fields)
    assert sha(folder/'original.raw.json')==inp['original_sha256']
    save_new(folder/'entity.pending_review.json',entity)
    save_new(folder/'06_assembly.execution_record.json',{'date':datetime.now().astimezone().isoformat(),'actor':'Codex','script_sha256':script_hash,'steps':steps,'checks':{'five_distinct_values':True,'originals_unchanged':True,'prices_and_weights_within_five_percent':True,'precision_and_units_preserved':True,'dates_in_four_windows':True},'assistant_flags':[f for f in flags if f['id']==raw['id']],'user_review':'候选待审','output':'entity.pending_review.json','model_inference_run':False})
    rows.append(entity);originals.append(raw)
validation=check(rows,require_row_order=True,per_type={'product':10});assert not validation['errors'],validation
records=build_records(rows,(1,2,3,4));assert len(records)==400
for i in range(0,len(records),2):
    a,b=records[i:i+2];assert (a['value_a'],a['value_b'])==(b['value_b'],b['value_a'])
for entity in rows:
    for field in fields:
        a=create_entity_table(entity,field,entity[field][0])
        for alt in entity[field][1:]:
            b=create_entity_table(entity,field,alt);assert [k for k in a if a[k]!=b[k]]==[field]
for filename,data in [('product.entities.pending_review.jsonl',rows),('product.originals.pending_review.jsonl',originals),('product.baseline_prompt_preview.jsonl',records)]:
    with (BASE/filename).open('x') as f:f.write(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in data))
save_new(BASE/'18_product_complete.execution_record.json',{'date':datetime.now().astimezone().isoformat(),'actor':'Codex','script_sha256':script_hash,'validation':validation,'assistant_flags':flags,'precision_exceptions':[],'data_sha256':sha(BASE/'product.entities.pending_review.jsonl'),'checks':{'prior_inputs_match_raw_outputs':True,'originals_unchanged':True,'single_field_differs':True,'both_orders_reverse_values':True,'400_prompts_previewed':True},'generation_boundary':'原值及制造商备选由当前会话撰写，版本参数不可见；日期价格重量保修为脚本规则输出，完整实体不冒称纯模型raw。','manufacturer_revision':'PRODUCT-05备选1顺丰改顺益；修改prompt/raw和改前raw均保留。','model_inference_run':False,'user_review':'候选待审；两项3个月整机保修未确认合理性。'})
print(json.dumps({'entities':10,'validation':validation,'precision_exceptions':0,'assistant_flags':flags},ensure_ascii=False))
