"""仅简化保修取值，验证月数与其他数据未变；新版另存，说明和Obsidian同步。"""
import copy,hashlib,json,re,sys
from datetime import datetime
from pathlib import Path
ROOT=Path(__file__).resolve().parent;BASE=ROOT.parent;PILOT=BASE.parents[1];REPO=PILOT.parent
sys.path.insert(0,str(PILOT))
from data_review.validate_entity_batch import check
from prompt_zh import create_entity_table
from run_baseline import build_records

def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,r):
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('x') as f:json.dump(r,f,ensure_ascii=False,indent=2);f.write('\n')
def lines(p):return [json.loads(s) for s in p.read_text().splitlines() if s]
def write_jsonl(p,rows):
    with p.open('x') as f:f.write(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows))
backups=[]
def update(p,text):
    if p.exists():
        b=ROOT/'backups'/p.relative_to(REPO);b.parent.mkdir(parents=True,exist_ok=True)
        with b.open('xb') as f:f.write(p.read_bytes())
        backups.append(str(b.relative_to(ROOT)))
    p.write_text(text)
request=read(ROOT/'00_input.execution_record.json');source=BASE/request['input'];assert sha(source)==request['input_sha256']
old=lines(source);new=copy.deepcopy(old);changes=[]
for before,row in zip(old,new):
    vals=[]
    for idx,v in enumerate(before['保修期']):
        m=re.fullmatch(r'整机保修(\d+)个月',v);assert m
        value=m[1]+'个月';vals.append(value);changes.append({'id':row['id'],'field':'保修期','value_index':idx,'before':v,'after':value,'reason':'用户要求简化措辞；月数不变。'})
    row['保修期']=vals
    assert [k for k in before if row[k]!=before[k]]==['保修期']
    assert [int(re.search(r'\d+',v)[0]) for v in before['保修期']]==[int(re.search(r'\d+',v)[0]) for v in vals]
assert len(changes)==50
validation=check(new,require_row_order=True,per_type={'product':10});assert not validation['errors'],validation
records=build_records(new,(1,2,3,4));assert len(records)==400
for i in range(0,len(records),2):
    a,b=records[i:i+2];assert (a['value_a'],a['value_b'])==(b['value_b'],b['value_a'])
for row in new:
    for field in ['制造商','发布日期','价格','重量','保修期']:
        a=create_entity_table(row,field,row[field][0])
        for alt in row[field][1:]:
            b=create_entity_table(row,field,alt);assert [k for k in a if a[k]!=b[k]]==[field]
write_jsonl(ROOT/'product.entities.pending_review.jsonl',new)
write_jsonl(ROOT/'product.baseline_prompt_preview.jsonl',records)
save(ROOT/'changes.json',changes)
manifest=read(BASE/'CURRENT_DATA.json');manifest['components']['product'].update(path=str((ROOT/'product.entities.pending_review.jsonl').relative_to(BASE)),sha256=sha(ROOT/'product.entities.pending_review.jsonl'),user_review='用户确认保修措辞简化；月数及两项3个月备选合理性未确认')
combined=[]
for c in manifest['components'].values():
    p=BASE/c['path'];assert sha(p)==c['sha256'];combined.extend(lines(p))
combined_validation=check(combined,require_row_order=True,per_type={c:10 for c in manifest['components']});assert not combined_validation['errors']
assert len(build_records(combined,(1,2,3,4)))==2720
write_jsonl(ROOT/'entities.generated60.pending_review.jsonl',combined)
manifest.update(updated=datetime.now().astimezone().isoformat(),combined_partial_data={'path':str((ROOT/'entities.generated60.pending_review.jsonl').relative_to(BASE)),'sha256':sha(ROOT/'entities.generated60.pending_review.jsonl'),'not_final':True})
update(BASE/'CURRENT_DATA.json',json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
text=(BASE/'REVIEW_product.md').read_text();text=re.sub(r'整机保修(\d+)个月',r'\1个月',text).replace('保修只改整机月数','保修只改月数').replace('按固定档位带出“3个月”','按固定档位带出“3个月”')
text=text.replace('# 新批次产品备选\n\n','# 新批次产品备选\n\n- **2026-11-18措辞更新**：保修期统一写“12个月”这类值；只删固定前缀，50个值的月数均未变。\n',1)
with (ROOT/'REVIEW_product.md').open('x') as f:f.write(text)
mirror=PILOT/'notes/02 数据/合成数据/新批次产品备选.md'
update(BASE/'REVIEW_product.md',text);update(mirror,text);assert mirror.read_bytes()==(BASE/'REVIEW_product.md').read_bytes()
prompt_doc='# 产品生成与修改prompt\n\n- **当前版本**：2026-11-18按用户要求简化保修措辞；取值写“24个月”，不额外定义“均指整机保修”。\n- **规则**：只改变保修月数，不添加配件或其他条件；其他规则和档位保持原样。\n- **留档**：新版模板在new_batch_20261116_v2/product_warranty_wording_20261118/templates；旧实际输入及冻结模板保留，不追改历史。\n- **执行边界**：新版模板供后续使用；本次已生成数据只做格式转换，没有按新版prompt重生成。\n'
for stage,title in [('original','生成原值'),('alternatives','生成四备选'),('revision','按反馈修改')]:
    prompt_doc+=f'\n<details>\n<summary>{title}：当前prompt原文</summary>\n\n```text\n'+(ROOT/f'templates/product.{stage}.txt').read_text().rstrip()+'\n```\n\n</details>\n'
for p in [PILOT/'data_generation/product_plan/PRODUCT_PROMPTS_DRAFT.md',PILOT/'notes/02 数据/合成数据/产品生成与修改prompt.md']:
    update(p,prompt_doc)
assert (PILOT/'data_generation/product_plan/PRODUCT_PROMPTS_DRAFT.md').read_bytes()==(PILOT/'notes/02 数据/合成数据/产品生成与修改prompt.md').read_bytes()
save(PILOT/'data_generation/product_plan/CURRENT_PROMPTS.json',{'updated':'2026-11-18','templates':{stage:str((ROOT/f'templates/product.{stage}.txt').relative_to(PILOT)) for stage in ['original','alternatives','revision']},'previous_frozen_templates':'data_generation/new_batch_20261116_v2/templates','decision_record':str((ROOT/'00_input.execution_record.json').relative_to(PILOT))})
p=PILOT/'ENTITY_GENERATION_PROTOCOL_DRAFT.md';s=p.read_text().replace('updated: 2026-11-16','updated: 2026-11-18').replace('status: 当前生成规程；70实体候选已生成，未定稿','status: 当前生成规程；新批次60实体候选已生成，未定稿').replace('- **保修期**：一次只改一个条件，选相邻常用档位；产品整机月数按已审产品prompt执行。','- **保修期**：取值写“N个月”；只改变保修月数，不添加配件或其他条件，档位按当前产品prompt执行。')
update(p,s);protocol_mirror=PILOT/'notes/02 数据/合成数据/实体生成规程（给老师草稿）.md';update(protocol_mirror,s);assert p.read_bytes()==protocol_mirror.read_bytes()
p=BASE/'README.md';s=p.read_text().replace('entities.generated60.pending_review.jsonl仅为部分候选','product_warranty_wording_20261118/entities.generated60.pending_review.jsonl仅为部分候选').replace('两项3个月保修','两项3个月保修')
s+='- **保修措辞（11-18）**：按用户要求改为“N个月”，当前产品组件在product_warranty_wording_20261118；月数未变，新模板入口为product_plan/CURRENT_PROMPTS.json，旧prompt保留。\n';update(p,s)
p=PILOT/'data_generation/product_plan/README.md';s=p.read_text();first,rest=s.split('\n',1);update(p,first+'\n\n- **11-18当前模板**：见CURRENT_PROMPTS.json及PRODUCT_PROMPTS_DRAFT.md；保修只写“N个月”，旧原文及预览文件保留为历史。\n'+rest)
block='- **2026-11-18 用户确认保修措辞简化，已执行**：10产品50个保修取值从“整机保修N个月”改为“N个月”，月数、档位、其他字段和行序不变；新版另存data_generation/new_batch_20261116_v2/product_warranty_wording_20261118，原始raw及旧prompt均保留。\n- **当前入口与检查**：CURRENT_DATA.json切换新版产品与60实体合并候选；产品400题、全60实体2720题预览检查通过，未推理。产品查看页、当前产品prompt及实体规程已同步Obsidian并逐字核对；新版模板仅供后续，不冒称本批按新版重新生成。\n- **下一步**：艺术10个仍未生成；两项3个月保修月数仍为待看，不把措辞确认写成数值合理性认可。记录见该修订目录00/01及changes.json。\n\n'
p=PILOT/'HANDOFF.md';update(p,p.read_text().replace('# HANDOFF\n\n','# HANDOFF\n\n'+block,1))
p=REPO/'HANDOFF.md';update(p,p.read_text().replace('更新日期**：2026-11-17','更新日期**：2026-11-18'))
coord='## 保修措辞更新（2026-11-18；Codex同步）\n\n- **已执行**：产品保修值统一“N个月”，50个值月数不变；用户仅确认措辞，未确认两项3个月的合理性。\n- **当前数据**：CURRENT_DATA.json指向product_warranty_wording_20261118新版产品及60实体合并候选；旧raw、模板、数据保留。\n- **下一步**：艺术10个；完整新数据baseline未跑。产品prompt和规程已同步Obsidian。\n\n'
for name in ['codex.md','claude.md']:
    p=PILOT/'coordination'/name;first,rest=p.read_text().split('\n',1);update(p,first+'\n\n'+coord+rest.lstrip('\n'))
assert sha(source)==request['input_sha256']
for stage,item in request['templates'].items():assert sha(BASE/item['source'])==item['source_sha256']
save(ROOT/'01_complete.execution_record.json',{'date':datetime.now().astimezone().isoformat(),'actor':'Codex','script_sha256':sha(Path(__file__)),'changes_count':len(changes),'changes':'changes.json','validation':validation,'combined_validation':combined_validation,'checks':{'only_warranty_strings_changed':True,'all_month_numbers_unchanged':True,'all_other_fields_and_row_order_unchanged':True,'old_data_and_frozen_prompts_unchanged':True,'product_400_prompt_checks':True,'combined_2720_prompt_preview':True,'three_doc_mirrors_equal':True},'backups':backups,'output_sha256':sha(ROOT/'product.entities.pending_review.jsonl'),'model_inference_run':False,'model':'无模型调用；Python脚本转换','unresolved':'PRODUCT-04、PRODUCT-09的3个月保修相容性仍待看。'})
with (ROOT/'README.md').open('x') as f:f.write('# 保修措辞简化\n\n- **决定**：用户11-18同意直接写“N个月”。\n- **修改**：10产品50个值只删“整机保修”，所有月数与其他字段未变。\n- **模板**：新版另存templates；旧实际prompt、raw和数据保留。\n- **检查**：产品400题、全60实体2720题预览通过；未跑模型。\n- **记录**：输入见00_input，逐值对照见changes.json，检查与备份见01_complete。\n- **待看**：两项3个月保修月数未改，不能把措辞确认当成数值审核。\n')
print(json.dumps({'values_changed':len(changes),'months_unchanged':True,'entities':len(combined),'mirrors_equal':True,'errors':validation['errors']},ensure_ascii=False))
