"""整理实际剩余标记；建议与用户决定分开，不改候选。"""
import hashlib,json,re
from datetime import datetime
from pathlib import Path
ROOT=Path(__file__).resolve().parent;BASE=ROOT.parent;PILOT=BASE.parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def save(p,r):
 with p.open('x') as f:json.dump(r,f,ensure_ascii=False,indent=2);f.write('\n')
manifest=read(BASE/'CURRENT_DATA.json');input_paths=[BASE/manifest['components'][k]['path'] for k in ['event','product']];hashes={str(p.relative_to(BASE)):sha(p) for p in input_paths}
save(ROOT/'00_input.execution_record.json',{'date':datetime.now().astimezone().isoformat(),'actor':'Codex','step':'closeout_inputs_saved_before_classification','input_hashes':hashes,'script_sha256':sha(Path(__file__)),'user_context':'用户OK，同意继续收口具体数据待定项；未据此声称两项3个月保修已逐值认可。'})
events=[json.loads(s) for s in input_paths[0].read_text().splitlines()];flags=[]
for row in events:
 city=row['主办方'][0].split('市')[0];assert city in row['name']
 assert all(v.startswith(city+'市') for v in row['主办方'])
 for v in row['主办方']:
  shared=sorted({row['name'][i:i+2] for i in range(len(row['name'])-1) if re.fullmatch(r'[一-龿]{2}',row['name'][i:i+2]) and row['name'][i:i+2] in v})
  extra=[s for s in shared if s!=city]
  flags.append({'id':row['id'],'value':v,'shared_city':city,'additional_shared_terms':extra,'assistant_disposition':'城市五值共同；主题词重合只保留提醒，不自动判错或证明等可信。','user_decision':'本次未新增逐值决定'})
products=[json.loads(s) for s in input_paths[1].read_text().splitlines()];warranties=[r for r in products if r['id'] in ['PRODUCT-04','PRODUCT-09']]
assert all(r['保修期']==['12个月','3个月','6个月','18个月','24个月'] for r in warranties)
city_only=sum(not r['additional_shared_terms'] for r in flags);assert city_only==32 and len(flags)-city_only==18
save(ROOT/'01_findings.json',{'date':datetime.now().astimezone().isoformat(),'actor':'Codex','event_flags':flags,'counts':{'city_only':32,'city_plus_theme':18},'warranty_rows':warranties,'assistant_recommendation':'暂保留当前候选；3个月来自已审档位，偏短是助手主观标记，不足以要求改原值或改规则。','user_decision':'两项3个月是否保留待用户明确答复；未改数据。','data_changed':False,'model_inference_run':False})
text='# 本批候选：剩余标记\n\n- **结论**：目前没有新增的格式或范围错误；建议保留当前候选，不因助手提醒自动改数据。\n- **活动50条**：32条只共享地名，18条还共享主题词；每个活动的五个主办方都在同城，地名相同不能区分五值。主题词提醒保留，不等于已验证等可信。\n- **保修两条**：“3个月”来自已定档位，符合脚本规则；“偏短”是助手判断，没有足够依据判错。建议保留，等用户确认。\n\n| 产品 | 原值 | 四个备选 |\n|---|---|---|\n'
for r in warranties:text+='| '+r['name']+' | '+r['保修期'][0]+' | '+'、'.join(r['保修期'][1:])+' |\n'
text+='\n- **本次没有修改**：月数、实体数据及当前版本指针保持原样。\n- **下一步**：确定这两项保修是否保留，再冻结运行版本、准备完整新数据baseline。\n- **记录**：closeout_review_20261118/保存输入哈希、分类脚本和逐条标记；提醒与用户决定分开。\n'
source=ROOT/'REVIEW.md';mirror=PILOT/'notes/02 数据/合成数据/本批候选剩余标记.md'
for p in [source,mirror]:
 with p.open('x') as f:f.write(text)
assert source.read_bytes()==mirror.read_bytes()
p=PILOT/'HANDOFF.md'
with (ROOT/'HANDOFF.before.md').open('x') as f:f.write(p.read_text())
entry='- **2026-11-18 收口标记分类，未改数据**：活动50条文字重合中32条仅地名，18条含主题词；地名五值共有，不按50个错误处理。两项3个月保修符合已定档位，“偏短”只是助手判断，建议保留但未写成用户已确认。\n- **交付和下一步**：closeout_review_20261118/REVIEW.md与Obsidian《本批候选剩余标记》一致；输入哈希和逐条分类留档。待用户决定两项3个月是否保留，再冻结运行版本、准备完整baseline；本步未推理。\n\n'
p.write_text(p.read_text().replace('# HANDOFF\n\n','# HANDOFF\n\n'+entry,1))
assert all(sha(BASE/p)==h for p,h in hashes.items())
save(ROOT/'02_complete.execution_record.json',{'date':datetime.now().astimezone().isoformat(),'actor':'Codex','script_sha256':sha(Path(__file__)),'document_sha256':sha(source),'mirror_equal':True,'source_data_unchanged':True,'counts':{'city_only':32,'city_plus_theme':18,'warranty_rows':2},'model':'无模型调用；脚本分类','model_inference_run':False})
print(json.dumps({'city_only':32,'city_plus_theme':18,'warranty_rows':2,'mirror_equal':True,'data_changed':False},ensure_ascii=False))
