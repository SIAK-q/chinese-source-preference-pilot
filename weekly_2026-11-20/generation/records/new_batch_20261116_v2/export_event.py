"""导出活动查看页并同步Obsidian，更新50实体部分候选清单。"""
import hashlib,json,sys
from datetime import datetime
from pathlib import Path
from prepare_person import BASE,read,save_new
sys.path.insert(0,str(BASE.parents[1]))
from data_review.validate_entity_batch import check
from run_baseline import build_records

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def loadlines(p):return [json.loads(s) for s in p.read_text().splitlines() if s]
def backup(p):
    dest=BASE/'event_export_backups_20261117'/p.relative_to(BASE.parents[2]);dest.parent.mkdir(parents=True,exist_ok=True)
    with dest.open('xb') as f:f.write(p.read_bytes())
    return str(dest.relative_to(BASE))
fields=read(BASE/'fields.json')['event'];rows=loadlines(BASE/'event.entities.pending_review.jsonl')
text='# 新批次活动备选\n\n- **已生成**：10个活动、50属性项，每项原值＋四备选；候选待审。\n- **口径**：持续时间指整场活动；比赛记参赛人数，开放展览和节庆记累计人次。\n- **检查**：格式、日期、五值互异及400题组题预览通过，未跑模型。\n- **名称修订**：“新定科普活动周”改为“新定科普活动”，删除会提示时长的“周”；原名和理由留档，用户尚未审。\n- **待看**：主办方均与活动同城，部分还共享主题词；脚本50条文字重合标记保留，不能据此声称名称提示已排除。\n- **精度例外**：运动会预算16万元，备选14、15、17、18万元，最大差12.5%；按既定整数精度规则留档。\n\n'
text+='| 活动 | '+' | '.join(fields)+' |\n|---|'+'---|'*len(fields)+'\n'
for row in rows:text+='| '+row['name']+' | '+' | '.join(row[f][0] for f in fields)+' |\n'
for row in rows:
    text+=f"\n<details>\n<summary>{row['name']}：四备选</summary>\n\n| 属性 | 原值 | 备选1 | 备选2 | 备选3 | 备选4 |\n|---|---|---|---|---|---|\n"
    for f in fields:text+='| '+f+' | '+' | '.join(row[f])+' |\n'
    text+='\n</details>\n'
text+='\n- **留痕**：逐活动prompt、raw和规则记录在entities/EVENT-*；名称修改见15_event_name_revision.json，检查汇总见16_event_complete.execution_record.json。\n- **边界**：检查不代表等可信；具体生成模型版本和采样参数不可见。\n'
source=BASE/'REVIEW_event.md';mirror=BASE.parents[1]/'notes/02 数据/合成数据/新批次活动备选.md'
for p in [source,mirror]:
    with p.open('x') as f:f.write(text)
assert source.read_bytes()==mirror.read_bytes()
manifest=read(BASE/'CURRENT_DATA.json');backups=[backup(BASE/'CURRENT_DATA.json')]
manifest['components']['event']={'path':'event.entities.pending_review.jsonl','sha256':sha(BASE/'event.entities.pending_review.jsonl'),'count':10,'user_review':'候选待审；名称修订及主办方文字重合已标记'}
combined=[]
for c in manifest['components'].values():
    p=BASE/c['path'];assert sha(p)==c['sha256'];combined.extend(loadlines(p))
validation=check(combined,require_row_order=True,per_type={c:10 for c in manifest['components']});assert not validation['errors'],validation
records=build_records(combined,(1,2,3,4));assert len(records)==2320
p=BASE/'entities.generated50.pending_review.jsonl'
with p.open('x') as f:f.write(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in combined))
manifest.update(updated=datetime.now().astimezone().isoformat(),generated_entities=50,not_yet_generated=['product','art'],combined_partial_data={'path':p.name,'sha256':sha(p),'not_final':True})
(BASE/'CURRENT_DATA.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
p=BASE/'README.md';backups.append(backup(p));s=p.read_text().replace('地点及建筑各10个原值及四备选已生成；其余三类尚未生成。','地点、建筑及活动各10个原值及四备选已生成；产品与艺术尚未生成。').replace('列出40个实体','列出50个实体').replace('entities.generated40.pending_review.jsonl仅为部分候选','entities.generated50.pending_review.jsonl仅为部分候选').replace('用户看建筑表；随后活动类。','用户看活动表；随后产品类，使用已审产品prompt。')
s+='- **活动**：[当前活动表](REVIEW_event.md)已同步Obsidian；名称删“周”、预算精度例外及主办方文字重合标记均留档，候选待审。\n';p.write_text(s)
block='- **2026-11-17 活动10实体含四备选已生成，当前50/70**：逐活动先存原值prompt，主办方带整表先存prompt后生成；日期、时长、人数、预算由规则脚本生成。50属性项400题组题预览通过，未推理。\n- **修订及标记**：助手将“新定科普活动周”删“周”，避免直接提示时长；raw原名未覆盖，修改见15记录。运动会16万元预算整数精度例外为±1/±2万元（最大12.5%）；主办方50条地名/主题词重合标记保留待看，不称名称提示已排除。\n- **交付及下一步**：REVIEW_event.md与Obsidian《新批次活动备选》一致；CURRENT_DATA.json指向50实体部分候选（290属性项、2320题），未定稿。用户本轮“OK”作继续活动指示，不扩成建筑全部备选逐项人审。随后产品、艺术共20实体；完整新数据baseline未跑。检查及导出见16_event_complete、17_event_export。\n\n'
p=BASE.parents[1]/'HANDOFF.md';backups.append(backup(p));p.write_text(p.read_text().replace('# HANDOFF\n\n','# HANDOFF\n\n'+block,1))
coord='## 最新活动交接（2026-11-17；Codex同步）\n\n- **已生成**：五类各10，共50实体含四备选；当前组件见`pilot/data_generation/new_batch_20261116_v2/CURRENT_DATA.json`。\n- **活动**：400题组题预览通过，未推理；名称删“周”、预算精度例外、主办方文字重合标记留档；Obsidian《新批次活动备选》已同步，候选待审。\n- **下一步**：产品类使用已审prompt；产品、艺术共20实体未生成，完整新数据baseline未跑。\n- **分工**：Codex继续数据；Claude20实体夜间流程测试已完成，不与完整新数据baseline混淆。\n\n'
for name in ['codex.md','claude.md']:
    p=BASE.parents[1]/'coordination'/name;backups.append(backup(p));first,rest=p.read_text().split('\n',1);p.write_text(first+'\n\n'+coord+rest.lstrip('\n'))
save_new(BASE/'17_event_export.execution_record.json',{'date':datetime.now().astimezone().isoformat(),'actor':'Codex','script_sha256':sha(Path(__file__)),'review_sha256':sha(source),'source':str(source),'mirror':str(mirror),'mirror_equal':source.read_bytes()==mirror.read_bytes(),'backups':backups,'validation':validation,'combined_prompts_previewed':len(records),'model_inference_run':False,'user_feedback':{'verbatim':'OK','interpretation':'继续活动类；未记建筑所有备选已逐项人工审核。'}})
print(json.dumps({'entities':len(combined),'attributes':validation['instances'],'prompts_previewed':len(records),'errors':validation['errors'],'review_flags':len(validation['review']),'mirror_equal':True},ensure_ascii=False))
