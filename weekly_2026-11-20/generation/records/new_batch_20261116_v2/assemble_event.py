"""按已定规则生成活动数值/日期备选，保留原始输出及名称修订。"""
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
    m=re.fullmatch(r'(\d+(?:\.\d+)?)(.+)',value);num,unit=Decimal(m[1]),m[2]
    precision=max(0,-num.as_tuple().exponent);step=Decimal(1).scaleb(-precision)
    n=int((num*Decimal('.05')/step).to_integral_value(rounding=ROUND_FLOOR));exception=n<2;n=max(2,n)
    offsets=[-n,-math.ceil(n/2),math.ceil(n/2),n];nums=[num+step*k for k in offsets]
    assert min(nums)>0
    return [value,*[f'{v:.{precision}f}{unit}' for v in nums]],{'step':str(step),'offsets_in_steps':offsets,'precision_exception':exception,'actual_maximum_percent':str(max(abs(v-num)/num*100 for v in nums))}
def fmt_date(d):return f'{d.year}年{d.month}月{d.day}日'
def dates(value,seed):
    orig=datetime.strptime(value,'%Y年%m月%d日').date();rng=random.Random(seed);vals=[];offsets=[]
    for low,high in [(-52,-48),(-4,-1),(1,4),(48,52)]:
        choices=[w for w in range(low,high+1) if min((orig.month-(orig+timedelta(weeks=w)).month)%12,((orig+timedelta(weeks=w)).month-orig.month)%12)<=1 and (orig+timedelta(weeks=w)).isoformat()<='2026-11-17']
        w=rng.choice(choices);offsets.append(w);vals.append(orig+timedelta(weeks=w))
    assert all(d.weekday()==orig.weekday() for d in vals)
    return [value,*map(fmt_date,vals)],offsets

def duration(value):
    if value.endswith('天'):
        n=int(value[:-1]);assert n-2>=1
        return [value,*[f'{n+k}天' for k in [-2,-1,1,2]]],{'rule':'天数按小计数±1、±2，不适用一般数值±5%。'}
    n=int(value.removesuffix('小时'))*60
    vals,detail=numeric(f'{n}分钟')
    def fmt(s):
        minutes=int(s.removesuffix('分钟'));h,m=divmod(minutes,60)
        return (f'{h}小时' if h else '')+(f'{m}分钟' if m else '')
    return [value,*[fmt(s) for s in vals[1:]]],{'rule':'小时先换算分钟，再用一般数值±5%。',**detail}

fields=read(BASE/'fields.json')['event'];rows=[];originals=[];exceptions=[];script_hash=sha(Path(__file__))
name_edits=[{'id':'EVENT-09','before':'新定科普活动周','after':'新定科普活动','actor':'Codex','reason':'周直接提示持续时间；删除提示词以符合实体名不得泄漏答案的约束。','user_decision':'助手实施的名称修订，用户尚未审核。'}]
save_new(BASE/'15_event_name_revision.json',{'date':datetime.now().astimezone().isoformat(),'changes':name_edits,'raw_outputs_preserved':True})
for i in range(1,11):
    folder=BASE/'entities'/f'EVENT-{i:02}';raw=read(folder/'original.raw.json')
    assert read(folder/'original.input.json')['previous_same_type_originals']==originals
    original_sha=sha(folder/'original.raw.json');organizers=read(folder/'alternatives.organizer.raw.json')
    seed=f"42:{raw['id']}:举办日期"
    save_new(folder/'05_rule_inputs.execution_record.json',{'date':datetime.now().astimezone().isoformat(),'actor':'Codex','script_sha256':script_hash,'original':raw,'original_sha256':original_sha,'organizer_raw_sha256':sha(folder/'alternatives.organizer.raw.json'),'date_seed':seed,'date_weeks_windows':[[-52,-48],[-4,-1],[1,4],[48,52]],'date_filter':'同星期；循环月差不超过1；不晚于2026-11-17。','numeric_rule':'约±5%，精度不足取相邻两档并记录。','duration_rule':'天数±1、±2；小时换算分钟后一般数值规则。','row_order_seed':f"42:{raw['id']}",'name_revision':name_edits if i==9 else []})
    entity={k:v for k,v in raw.items() if k not in fields}
    if i==9:entity['name']='新定科普活动'
    entity['主办方']=[raw['主办方'],*organizers]
    entity['举办日期'],weeks=dates(raw['举办日期'],seed)
    entity['持续时间'],duration_detail=duration(raw['持续时间'])
    steps=[{'field':'举办日期','selected_week_offsets':weeks},{'field':'持续时间',**duration_detail}]
    for field in ['参与人数','预算']:
        entity[field],detail=numeric(raw[field]);steps.append({'field':field,**detail})
        if detail['precision_exception']:exceptions.append({'id':raw['id'],'field':field,'values':entity[field],**detail})
    entity['row_order']=make_row_order(entity)
    assert all(len(entity[f])==len(set(entity[f]))==5 and entity[f][0]==raw[f] for f in fields)
    assert sha(folder/'original.raw.json')==original_sha
    save_new(folder/'entity.pending_review.json',entity)
    save_new(folder/'06_assembly.execution_record.json',{'date':datetime.now().astimezone().isoformat(),'actor':'Codex','script_sha256':script_hash,'steps':steps,'name_revision':name_edits if i==9 else [],'checks':{'five_distinct':True,'raw_originals_unchanged':True,'attribute_originals_unchanged':True},'user_review':'候选待审','output':'entity.pending_review.json'})
    rows.append(entity);originals.append(raw)
validation=check(rows,require_row_order=True,per_type={'event':10});assert not validation['errors'],validation
records=build_records(rows,(1,2,3,4));assert len(records)==400
for i in range(0,len(records),2):
    a,b=records[i:i+2];assert (a['value_a'],a['value_b'])==(b['value_b'],b['value_a'])
for entity in rows:
    for field in fields:
        a=create_entity_table(entity,field,entity[field][0])
        for alt in entity[field][1:]:
            b=create_entity_table(entity,field,alt);assert [k for k in a if a[k]!=b[k]]==[field]
for filename,data in [('event.entities.pending_review.jsonl',rows),('event.originals.raw.jsonl',originals),('event.baseline_prompt_preview.jsonl',records)]:
    with (BASE/filename).open('x') as f:f.write(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in data))
save_new(BASE/'16_event_complete.execution_record.json',{'date':datetime.now().astimezone().isoformat(),'actor':'Codex','script_sha256':script_hash,'validation':validation,'precision_exceptions':exceptions,'name_revision':name_edits,'checks':{'prior_inputs_match_raw_outputs':True,'raw_originals_unchanged':True,'single_field_differs':True,'both_orders_reverse_values':True,'400_prompts_previewed':True},'data_sha256':sha(BASE/'event.entities.pending_review.jsonl'),'generation_boundary':'原值及主办方备选由当前会话生成；模型版本/参数不可见；日期数值由脚本规则生成。','model_inference_run':False,'user_review':'候选待审'})
print(json.dumps({'entities':10,'validation':validation,'exceptions':exceptions,'name_edits':name_edits},ensure_ascii=False))
