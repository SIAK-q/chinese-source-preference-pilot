"""导出建筑查看页、Obsidian镜像及当前40实体清单，旧文件先备份。"""
import hashlib
import json
import sys
from datetime import datetime
from pathlib import Path
from prepare_person import BASE,read,save_new
sys.path.insert(0,str(BASE.parents[1]))
from data_review.validate_entity_batch import check
from run_baseline import build_records

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def lines(p): return [json.loads(s) for s in p.read_text().splitlines() if s]
def backup(p):
    dest=BASE/'building_export_backups_20261117'/p.relative_to(BASE.parents[2])
    dest.parent.mkdir(parents=True,exist_ok=True)
    with dest.open('xb') as f:f.write(p.read_bytes())
    return str(dest.relative_to(BASE))
rows=lines(BASE/'building.entities.pending_review.jsonl')
fields=read(BASE/'fields.json')['building']
text='# 新批次建筑备选\n\n- **已生成**：10栋建筑、60属性项，每项原值＋四备选；候选待审。\n- **属性**：使用“主要材料”，取值如“钢和混凝土”；高度为总高度，人数为设计容纳人数。\n- **检查**：五值互异、材料组合去重及组题检查通过；480题仅预览，未跑模型。\n- **精度例外**：9栋整数高度按已定规则用±1、±2米，最大幅度5.6%—10%；逐项记录保留。\n\n'
text+='| 建筑 | '+' | '.join(fields)+' |\n|---|'+'---|'*len(fields)+'\n'
for r in rows:text+='| '+r['name']+' | '+' | '.join(r[f][0] for f in fields)+' |\n'
for r in rows:
    text+=f"\n<details>\n<summary>{r['name']}：四备选</summary>\n\n| 属性 | 原值 | 备选1 | 备选2 | 备选3 | 备选4 |\n|---|---|---|---|---|---|\n"
    for field in fields:text+='| '+field+' | '+' | '.join(r[field])+' |\n'
    text+='\n</details>\n'
text+='\n- **留痕**：逐栋输入、prompt和raw在entities/BUILDING-*；汇总检查见13_building_complete.execution_record.json。\n- **边界**：结构检查通过不代表等可信或工程验证；用户尚未审核本类候选。\n'
source=BASE/'REVIEW_building.md'
mirror=BASE.parents[1]/'notes/02 数据/合成数据/新批次建筑备选.md'
for p in [source,mirror]:
    with p.open('x') as f:f.write(text)
assert source.read_bytes()==mirror.read_bytes()
manifest=read(BASE/'CURRENT_DATA.json')
backups=[backup(BASE/'CURRENT_DATA.json')]
manifest['components']['building']={'path':'building.entities.pending_review.jsonl','sha256':sha(BASE/'building.entities.pending_review.jsonl'),'count':10,'user_review':'候选待审'}
combined=[]
for component in manifest['components'].values():
    path=BASE/component['path']
    assert sha(path)==component['sha256']
    combined.extend(lines(path))
validation=check(combined,require_row_order=True,per_type={c:10 for c in manifest['components']})
assert not validation['errors'],validation
assert len(build_records(combined,(1,2,3,4)))==1920
combined_path=BASE/'entities.generated40.pending_review.jsonl'
with combined_path.open('x') as f:f.write(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in combined))
manifest.update(updated=datetime.now().astimezone().isoformat(),generated_entities=40,not_yet_generated=['event','product','art'],combined_partial_data={'path':combined_path.name,'sha256':sha(combined_path),'not_final':True})
(BASE/'CURRENT_DATA.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
readme=BASE/'README.md'
backups.append(backup(readme))
s=readme.read_text().replace('地点10个原值及四备选已生成；其余四类尚未生成。','地点及建筑各10个原值及四备选已生成；其余三类尚未生成。').replace('列出30个实体','列出40个实体').replace('entities.generated30.pending_review.jsonl仅为部分候选','entities.generated40.pending_review.jsonl仅为部分候选').replace('用户看地点表及机构规模修订；随后建筑类，用“主要材料”。','用户看建筑表；随后活动类。')
s+='- **建筑**：[当前建筑表](REVIEW_building.md)已同步Obsidian；使用主要材料，9处整数高度精度例外已留档。\n'
readme.write_text(s)
project=BASE.parents[1]
block='- **2026-11-17 建筑10实体含四备选已生成，当前40/70**：使用主要材料；逐栋先存prompt再生成原值与材料备选，其余按预存规则生成。480题组题检查通过；9处整数高度采用±1/±2米，最大5.6%—10%留档，原始输出未改。\n- **当前入口**：data_generation/new_batch_20261116_v2/CURRENT_DATA.json保留机构规模修订并新增建筑；entities.generated40.pending_review.jsonl为240属性项、1920题部分候选，未定稿、未推理。REVIEW_building.md与Obsidian《新批次建筑备选》逐字一致。\n- **下一步**：用户看建筑候选，随后活动类；活动、产品、艺术共30个未生成。完整新数据baseline未跑；Claude夜间20实体流程测试不替代完整baseline。记录见13_building_complete、14_building_export。\n\n'
handoff=project/'HANDOFF.md'
backups.append(backup(handoff))
s=handoff.read_text(); handoff.write_text(s.replace('# HANDOFF\n\n','# HANDOFF\n\n'+block,1))
coord='## 最新建筑交接（2026-11-17；Codex同步）\n\n- **已生成**：人物、机构、地点、建筑各10，共40实体，含四备选；当前版本见`pilot/data_generation/new_batch_20261116_v2/CURRENT_DATA.json`。\n- **建筑**：使用主要材料；480题预览检查通过，9处整数高度例外留档，Obsidian《新批次建筑备选》已同步，候选待审。\n- **剩余**：活动、产品、艺术共30个未生成；下一类活动，完整新数据baseline未跑。\n- **分工**：Codex继续数据；Claude继续已启动的20实体夜间流程测试，避免重复修改。\n\n'
for name in ['codex.md','claude.md']:
    p=project/'coordination'/name
    backups.append(backup(p))
    s=p.read_text(); first,rest=s.split('\n',1);p.write_text(first+'\n\n'+coord+rest.lstrip('\n'))
save_new(BASE/'14_building_export.execution_record.json',{'date':datetime.now().astimezone().isoformat(),'actor':'Codex','script_sha256':sha(Path(__file__)),'source':str(source.relative_to(project)),'mirror':str(mirror.relative_to(project)),'mirror_equal':source.read_bytes()==mirror.read_bytes(),'review_sha256':sha(source),'backups':backups,'validation':validation,'combined_prompts_previewed':1920,'model_inference_run':False,'user_decision':'未新增建筑审核决定；用户“好了”仅作继续工作的指示。'})
print(json.dumps({'entities':len(combined),'validation':validation,'mirror_equal':True,'mirror':str(mirror)},ensure_ascii=False))
