"""按用户决定仅删人物籍贯及对应行序，另存70实体定稿v2，旧版不动。"""
import copy,hashlib,json,sys
from datetime import datetime
from pathlib import Path
ROOT=Path(__file__).resolve().parent;PILOT=ROOT.parents[1];REPO=PILOT.parent;BASE=PILOT/'data_generation/new_batch_20261116_v2'
sys.path.insert(0,str(PILOT))
from data_review.validate_entity_batch import check,FIELDS
from run_baseline import build_records

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def save(p,r):
 p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('x') as f:json.dump(r,f,ensure_ascii=False,indent=2);f.write('\n')
backups=[]
def update(p,s):
 b=ROOT/'backups'/p.relative_to(REPO);b.parent.mkdir(parents=True,exist_ok=True)
 with b.open('xb') as f:f.write(p.read_bytes())
 backups.append(str(b.relative_to(ROOT)));p.write_text(s)
manifest=read(BASE/'CURRENT_DATA.json');source=PILOT/manifest['final_release']['path'];source_sha=sha(source)
assert manifest['final_release']['version']=='final70_20261118_v1' and source_sha==manifest['final_release']['sha256']
quote='人物删去"籍贯"一列，其他属性不重新生成。理由：籍贯和出生地、现居城市一样都是地名题，内容重复；老师 11-09 在 21:19–21:30 只建议了出生地和现居城市。删完人物剩 8 项，每个模型 3040 题。改前版本保留，改动写进记录。然后 70 个实体定稿，给出定稿文件和 SHA256。'
reason='籍贯和出生地、现居城市一样都是地名题，内容重复；老师11-09在21:19–21:30只建议了出生地和现居城市。'
now=datetime.now().astimezone().isoformat()
save(ROOT/'00_input.execution_record.json',{'date':now,'actor':'Codex','step':'删除前保存实际输入与用户决定','user_message_verbatim':quote,'reason_provided_by_user':reason,'source':str(source.relative_to(PILOT)),'source_sha256':source_sha,'source_manifest_sha256':sha(BASE/'CURRENT_DATA.json'),'script_sha256':sha(Path(__file__)),'method':'删除人物籍贯数组及row_order中该字段；其余属性值、顺序和实体不改，不调用模型。'})
before=[json.loads(s) for s in source.read_text().splitlines() if s];after=copy.deepcopy(before);changes=[]
for old,row in zip(before,after):
 if row['entity_class']=='person':
  removed=row.pop('籍贯');old_order=row['row_order'][:];row['row_order']=[k for k in old_order if k!='籍贯']
  changes.append({'id':row['id'],'name':row['name'],'removed_field':'籍贯','removed_values':removed,'row_order_before':old_order,'row_order_after':row['row_order'],'other_values_changed':False,'actor':'Codex执行用户决定','reason':reason})
  assert len([k for k,v in row.items() if isinstance(v,list) and k!='row_order'])==8
  expected=copy.deepcopy(old);expected.pop('籍贯');expected['row_order']=[k for k in old['row_order'] if k!='籍贯'];assert row==expected
 else:assert row==old
assert len(changes)==10 and len(after)==70 and not any('籍贯' in r or '籍贯' in r['row_order'] for r in after)
schema=copy.deepcopy(FIELDS);schema['person']=[f for f in schema['person'] if f!='籍贯']
assert sum(map(len,schema.values()))==38
validation=check(after,require_row_order=True,per_type={k:10 for k in schema},fields=schema);assert not validation['errors'],validation
records=build_records(after,(1,2,3,4));old_records=build_records(before,(1,2,3,4))
assert len(records)==3040 and len(old_records)==3120 and validation['instances']==380
assert not any(r['field']=='籍贯' for r in records)
for i in range(0,len(records),2):
 a,b=records[i:i+2];assert (a['value_a'],a['value_b'])==(b['value_b'],b['value_a'])
remaining=[r for r in old_records if r['field']!='籍贯']
for a,b in zip(remaining,records):assert {k:v for k,v in a.items() if k!='prompt'}=={k:v for k,v in b.items() if k!='prompt'}
with (ROOT/'entities_zh.jsonl').open('x') as f:f.write(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in after))
with (ROOT/'person.entities_zh.jsonl').open('x') as f:f.write(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in after if r['entity_class']=='person'))
with (ROOT/'prompts.preview.jsonl').open('x') as f:f.write(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in records))
save(ROOT/'fields.json',schema);save(ROOT/'changes.json',changes);save(ROOT/'source_manifest.before.json',manifest)
final_sha=sha(ROOT/'entities_zh.jsonl')
with (ROOT/'SHA256SUMS').open('x') as f:f.write(final_sha+'  entities_zh.jsonl\n')
save(ROOT/'review_decisions.json',{'date':now,'decision_maker':'用户','recorded_by':'Codex','user_message_verbatim':quote,'status':'final','decisions':[{'scope':'人物籍贯','decision':'删除','reason_provided_by_user':reason},{'scope':'其他属性','decision':'不重新生成，保留现有值'},{'scope':'70实体','decision':'定稿；沿用活动主办方及3个月保修保留决定'}],'source_version':'final70_20261118_v1','source_sha256':source_sha,'final_version':'final70_20261118_v2','final_sha256':final_sha,'person_attributes':8,'attribute_instances':380,'pairs':1520,'prompts_per_model':3040})
# 当前校验规则更新为38种；旧校验源码保存在backups，旧冻结包和模板不修改。
p=PILOT/'data_review/validate_entity_batch.py';s=p.read_text();old_line='"person": ["出生日期", "职业", "学历", "身高", "体重", "婚姻状况", "现居城市", "出生地", "籍贯"],'
assert old_line in s
s=s.replace('当前确认39项','当前确认38项').replace(old_line,'"person": ["出生日期", "职业", "学历", "身高", "体重", "婚姻状况", "现居城市", "出生地"],',1);update(p,s)
manifest['status']='final';manifest['updated']=datetime.now().astimezone().isoformat()
manifest['final_release']={'path':str((ROOT/'entities_zh.jsonl').relative_to(PILOT)),'path_base':'pilot','sha256':final_sha,'version':'final70_20261118_v2','decision_record':str((ROOT/'review_decisions.json').relative_to(PILOT)),'person_attributes':8,'attribute_instances':380,'prompts_per_model':3040}
manifest['frozen_release']={'path':str((ROOT/'entities_zh.jsonl').relative_to(PILOT)),'path_base':'pilot','sha256':final_sha,'tag':'new70_20261118_v2','user_authorized':True}
manifest['components']['person']={'path':'../final70_20261118_v2/person.entities_zh.jsonl','sha256':sha(ROOT/'person.entities_zh.jsonl'),'count':10,'user_review':'用户决定删除籍贯，其他属性原样保留，人物8项，70实体定稿。'}
manifest['combined_partial_data']={'path':'../final70_20261118_v2/entities_zh.jsonl','sha256':final_sha,'not_final':False}
manifest['baseline_package_status']='旧new70_20261118_v1包为3120题；当前定稿3040题，需要新版运行包。'
update(BASE/'CURRENT_DATA.json',json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
# 当前规程与Obsidian同步；已执行prompt和旧版字段快照保留。
p=PILOT/'ENTITY_GENERATION_PROTOCOL_DRAFT.md';s=p.read_text().replace('390属性、1560冲突对、3120题／模型','380属性、1520冲突对、3040题／模型').replace('**人物9项**：出生日期、职业、学历、身高、体重、婚姻状况、现居城市、出生地、籍贯','**人物8项**：出生日期、职业、学历、身高、体重、婚姻状况、现居城市、出生地').replace('现居城市、出生地、籍贯、总部在实体地名池内取五个不同值；人物三个城市字段彼此可以相同，籍贯指祖辈居住城市。','现居城市、出生地、总部在实体地名池内取五个不同值；人物现居城市与出生地可以相同。')
s=s.replace('- **规模**：','- **人物删列（11-18用户决定）**：删除籍贯，其他值不重生成；与出生地、现居城市都是地名题，内容重复，老师11-09只建议后两项。\n- **规模**：',1)
for p in [PILOT/'ENTITY_GENERATION_PROTOCOL_DRAFT.md',PILOT/'notes/02 数据/合成数据/实体生成规程（给老师草稿）.md']:update(p,s)
# 完整表按新定稿重建，1950→1900个取值；附带行序同步删列。
def esc(v):return str(v).replace('&','&amp;').replace('|','&#124;').replace('<','&lt;').replace('>','&gt;')
md='# 新70实体定稿全表\n\n- **当前版本**：final70_20261118_v2；人物8项，70实体、380属性项、3040题／模型。\n- **本次修改**：只删人物“籍贯”；其他取值不改，活动主办方及3个月保修保留。\n- **读法**：各表列原值和四个备选；性别、作品类型写在表前。\n- **来源**：`pilot/data_generation/final70_20261118_v2/entities_zh.jsonl`；旧v1完整保留。\n\n'
expected=[]
for cls,label in {'person':'人物','organization':'机构','location':'地点','building':'建筑','event':'活动','product':'产品','art':'艺术作品'}.items():
 md+='## '+label+'\n\n'
 for r in [x for x in after if x['entity_class']==cls]:
  md+=f"### {r['name']}（{r['id']}）\n\n"
  fixed={k:v for k,v in r.items() if k not in {'id','name','entity_class','description','row_order'} and not isinstance(v,list)}
  if fixed:md+='- **固定信息**：'+'；'.join(k+'：'+esc(v) for k,v in fixed.items())+'。\n\n'
  md+='| 属性 | 原值 | 备选1 | 备选2 | 备选3 | 备选4 |\n|---|---|---|---|---|---|\n'
  for field in schema[cls]:
   cells=[esc(field),*[esc(v) for v in r[field]]];expected.append(cells);md+='| '+' | '.join(cells)+' |\n'
  md+='\n'
md+='<details>\n<summary>附带记录信息：类别、说明与实验行序</summary>\n\n| ID | 类别 | description | 行序 |\n|---|---|---|---|\n'
for r in after:md+='| '+r['id']+' | '+r['entity_class']+' | '+esc(r.get('description',''))+' | '+' → '.join(r['row_order'])+' |\n'
md+='\n</details>\n'
actual=[]
for line in md.splitlines():
 if line.startswith('| '):
  cells=[c.strip() for c in line.strip().strip('|').split('|')]
  if len(cells)==6 and cells[0]!='属性':actual.append(cells)
assert actual==expected and len(actual)==380
with (ROOT/'ENTITIES_FINAL.md').open('x') as f:f.write(md)
update(PILOT/'notes/02 数据/合成数据/新70实体定稿全表.md',md)
readme='# 新70实体定稿\n\n- **版本**：final70_20261118_v2，2026-11-18用户确认定稿。\n- **修改**：仅删10个人物的“籍贯”及行序中这一项；人物剩8项，其他取值原样保留。\n- **理由**：与出生地、现居城市都是地名题，内容重复；用户引用老师11-09（21:19–21:30）只建议出生地、现居城市。\n- **规模**：70实体、380属性项、1520冲突对、3040题／模型。\n- **文件**：`pilot/data_generation/final70_20261118_v2/entities_zh.jsonl`；旧v1完整保留。\n- **记录**：review_decisions.json存用户决定，changes.json存删前五值及行序对照，00/01存输入和检查。\n- **SHA256**：`'+final_sha+'`。\n- **运行包**：原3120题包属于旧版，当前3040题尚未打包或运行。\n'
with (ROOT/'README.md').open('x') as f:f.write(readme)
update(PILOT/'notes/02 数据/合成数据/新70实体定稿.md',readme)
# 明确旧运行入口对应旧数据，避免继续运行此前给出的3120题命令。
for p in [PILOT/'baseline_runs/new70_20261118_v1/README.md',PILOT/'notes/03 实验/新70实体baseline运行.md']:
 s=p.read_text();s=s.replace('# 新70实体：baseline运行\n\n','# 新70实体：baseline运行\n\n- **已被新版替代（11-18）**：本页命令对应删籍贯前的3120题旧包；当前定稿为3040题，请勿按本页提交。旧包与命令保留供追溯。\n',1);update(p,s)
p=BASE/'README.md';s=p.read_text();s='\n'.join(line for line in s.split('\n') if not line.startswith('- **当前**：'))
s=s.replace('# 新批次生成记录\n\n','# 新批次生成记录\n\n- **当前**：正式定稿final70_20261118_v2；已删人物籍贯，70实体、380属性项、3040题／模型。当前文件以CURRENT_DATA.json的final_release为准；下列生成记录保留历史口径。\n',1);update(p,s)
entry='- **2026-11-18 已执行删除人物籍贯并重新定稿v2**：按用户明确指令，只从10个人物删除籍贯五值和row_order中的该项；其余属性、60个非人物实体及剩余字段相对行序均未变，不重生成。理由按用户提供：地名题重复，老师11-09（21:19–21:30）仅建议出生地、现居城市。\n- **当前定稿**：data_generation/final70_20261118_v2/entities_zh.jsonl；SHA256 '+final_sha+'；人物8项、38种字段、380属性项、1520对、3040题／模型。旧final70_20261118_v1完整保留；逐人删除对照见v2/changes.json，决定见review_decisions.json，输入/检查见00/01。\n- **同步与下一步**：CURRENT_DATA.json已切新定稿，当前校验规则/规程及Obsidian定稿说明/全表同步；旧3120题baseline包已在运行页标明旧版，本次未重打包、未提交或推理。Claude来源实验后续应改接本3040题版本。\n\n'
p=PILOT/'HANDOFF.md';update(p,p.read_text().replace('# HANDOFF\n\n','# HANDOFF\n\n'+entry,1))
coord='## 删籍贯后定稿v2（2026-11-18；Codex同步）\n\n- **已执行**：人物删除籍贯及对应行序，其他属性不重新生成；70实体定稿，人物8项、3040题／模型。\n- **当前文件**：pilot/data_generation/final70_20261118_v2/entities_zh.jsonl；SHA256 `'+final_sha+'`。\n- **留痕**：同目录review_decisions.json、changes.json、00/01记录；旧v1保留。\n- **注意版本**：旧baseline包与此前来源实验检查基于3120题，后续请改接v2；本次未提交或推理。\n\n'
for name in ['codex.md','claude.md']:
 p=PILOT/'coordination'/name;first,rest=p.read_text().split('\n',1);update(p,first+'\n\n'+coord+rest.lstrip('\n'))
assert sha(source)==source_sha
assert (ROOT/'ENTITIES_FINAL.md').read_bytes()==(PILOT/'notes/02 数据/合成数据/新70实体定稿全表.md').read_bytes()
assert (ROOT/'README.md').read_bytes()==(PILOT/'notes/02 数据/合成数据/新70实体定稿.md').read_bytes()
save(ROOT/'01_complete.execution_record.json',{'date':datetime.now().astimezone().isoformat(),'actor':'Codex','script_sha256':sha(Path(__file__)),'final_file':'entities_zh.jsonl','final_sha256':final_sha,'source_sha256':source_sha,'validation':validation,'checks':{'deleted_person_columns':len(changes),'person_remaining_attributes':8,'all_other_values_unchanged':True,'all_non_person_entities_unchanged':True,'remaining_row_order_preserved':True,'old_version_unchanged':True,'all_remaining_pair_metadata_unchanged':True,'prompts_per_model':len(records),'markdown_attribute_rows':len(actual),'markdown_1900_values_match':True,'obsidian_mirrors_equal':True},'backups':backups,'model':'无模型调用；脚本删列、检查、导出','regenerated_attributes':False,'inference_run':False})
print(json.dumps({'file':str(ROOT/'entities_zh.jsonl'),'sha256':final_sha,'entities':len(after),'person_attributes':8,'attribute_instances':380,'prompts_per_model':len(records),'other_values_unchanged':True,'old_version_unchanged':True,'mirrors_equal':True},ensure_ascii=False))
