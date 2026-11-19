"""导出产品候选及Obsidian镜像，保留旧文件后更新60实体清单。"""
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
    dest=BASE/'product_export_backups_20261117'/p.relative_to(BASE.parents[2]);dest.parent.mkdir(parents=True,exist_ok=True)
    with dest.open('xb') as f:f.write(p.read_bytes())
    return str(dest.relative_to(BASE))
fields=read(BASE/'fields.json')['product'];rows=loadlines(BASE/'product.entities.pending_review.jsonl')
text='# 新批次产品备选\n\n- **已生成**：10个产品、50属性项，每项原值＋四备选；候选待审。\n- **规则**：价格和净重备选均在±5%内，单位及精度不变；发布日期按四区间抽样；保修只改整机月数。\n- **检查**：格式、日期范围、五值互异及400题组题预览通过，无精度例外，未跑模型。\n- **重点看**：C10滴滤咖啡机和P10手机按固定档位带出“整机保修3个月”，助手认为偏短，尚未确认合理性。\n- **修改**：C20制造商备选1“顺丰电器有限公司”改为“顺益电器有限公司”，避开已知品牌用字；旧raw和修改prompt保留，未做外部公司查重。\n\n'
text+='| 产品 | '+' | '.join(fields)+' |\n|---|'+'---|'*len(fields)+'\n'
for row in rows:text+='| '+row['name']+' | '+' | '.join(row[f][0] for f in fields)+' |\n'
for row in rows:
    text+=f"\n<details>\n<summary>{row['name']}：四备选</summary>\n\n| 属性 | 原值 | 备选1 | 备选2 | 备选3 | 备选4 |\n|---|---|---|---|---|---|\n"
    for f in fields:text+='| '+f+' | '+' | '.join(row[f])+' |\n'
    text+='\n</details>\n'
text+='\n- **留痕**：逐产品prompt、raw和规则记录在entities/PRODUCT-*；汇总检查见18_product_complete.execution_record.json。\n- **生成方式**：原值和制造商备选由当前会话撰写，模型版本参数不可见；日期、价格、重量、保修备选由脚本生成，不把完整组装输出当作纯模型raw。\n- **审核边界**：格式和范围通过不代表全部备选等可信；本类尚未获用户审核。\n'
source=BASE/'REVIEW_product.md';mirror=BASE.parents[1]/'notes/02 数据/合成数据/新批次产品备选.md'
for p in [source,mirror]:
    with p.open('x') as f:f.write(text)
assert source.read_bytes()==mirror.read_bytes()
manifest=read(BASE/'CURRENT_DATA.json');backups=[backup(BASE/'CURRENT_DATA.json')]
manifest['components']['product']={'path':'product.entities.pending_review.jsonl','sha256':sha(BASE/'product.entities.pending_review.jsonl'),'count':10,'user_review':'候选待审；两项3个月整机保修未确认合理性'}
combined=[]
for c in manifest['components'].values():
    p=BASE/c['path'];assert sha(p)==c['sha256'];combined.extend(loadlines(p))
validation=check(combined,require_row_order=True,per_type={c:10 for c in manifest['components']});assert not validation['errors'],validation
assert len(build_records(combined,(1,2,3,4)))==2720
p=BASE/'entities.generated60.pending_review.jsonl'
with p.open('x') as f:f.write(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in combined))
manifest.update(updated=datetime.now().astimezone().isoformat(),generated_entities=60,not_yet_generated=['art'],combined_partial_data={'path':p.name,'sha256':sha(p),'not_final':True})
(BASE/'CURRENT_DATA.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
p=BASE/'README.md';backups.append(backup(p));s=p.read_text().replace('地点、建筑及活动各10个原值及四备选已生成；产品与艺术尚未生成。','地点、建筑、活动及产品各10个原值及四备选已生成；艺术尚未生成。').replace('列出50个实体','列出60个实体').replace('entities.generated50.pending_review.jsonl仅为部分候选','entities.generated60.pending_review.jsonl仅为部分候选').replace('用户看活动表；随后产品类，使用已审产品prompt。','用户看产品，尤其两项3个月保修；随后艺术类。')
s+='- **产品**：[当前产品表](REVIEW_product.md)已同步Obsidian；价格重量±5%无精度例外，两项短保修待看，制造商一项修订留痕。\n';p.write_text(s)
block='- **2026-11-17 产品10实体含四备选已生成，当前60/70**：使用已审三段产品模板，逐产品先存实际原值prompt再生成；完整备选prompt先存，制造商由当前会话撰写，日期/价格/重量/整机保修由脚本按规则生成，完整组装不冒称纯模型raw。400题预览、单位/精度/四日期区间/±5%检查通过，无精度例外，未推理。\n- **待看与修改**：C10滴滤咖啡机和P10手机按固定档位带出3个月整机保修，助手标偏短，合理性未确认。C20制造商备选1顺丰改顺益，先保存修改prompt、后生成修订raw，旧raw保留；未外部品牌查重。\n- **交付及下一步**：REVIEW_product.md与Obsidian《新批次产品备选》一致；CURRENT_DATA.json新增产品，60实体部分候选为340属性项、2720题。用户本轮OK仅作继续产品指示，不扩成活动50条标记或名称修订已获逐项审核。下一类艺术10个；完整新数据baseline未跑。检查及导出见18_product_complete、19_product_export。\n\n'
p=BASE.parents[1]/'HANDOFF.md';backups.append(backup(p));p.write_text(p.read_text().replace('# HANDOFF\n\n','# HANDOFF\n\n'+block,1))
coord='## 最新产品交接（2026-11-17；Codex同步）\n\n- **已生成**：六类各10，共60实体含四备选；当前组件见`pilot/data_generation/new_batch_20261116_v2/CURRENT_DATA.json`。\n- **产品**：400题预览通过，价格重量严格±5%无精度例外；两项3个月整机保修待看，制造商一项修订留痕。Obsidian《新批次产品备选》已同步。\n- **剩余**：艺术10个未生成；全批未定稿、完整新数据baseline未跑。\n- **分工**：Codex继续数据；Claude20实体流程测试已完成，不重复改个人信源代码。\n\n'
for name in ['codex.md','claude.md']:
    p=BASE.parents[1]/'coordination'/name;backups.append(backup(p));first,rest=p.read_text().split('\n',1);p.write_text(first+'\n\n'+coord+rest.lstrip('\n'))
save_new(BASE/'19_product_export.execution_record.json',{'date':datetime.now().astimezone().isoformat(),'actor':'Codex','script_sha256':sha(Path(__file__)),'review_sha256':sha(source),'source':str(source),'mirror':str(mirror),'mirror_equal':source.read_bytes()==mirror.read_bytes(),'backups':backups,'validation':validation,'combined_prompts_previewed':2720,'model_inference_run':False,'user_feedback':{'verbatim':'OK','interpretation':'继续产品类；未记活动全部备选/标记已人工确认。'}})
print(json.dumps({'entities':len(combined),'attributes':validation['instances'],'prompts_previewed':2720,'errors':validation['errors'],'mirror_equal':True},ensure_ascii=False))
