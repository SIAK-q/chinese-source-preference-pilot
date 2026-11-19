"""导出艺术查看页和全70候选，更新交接并同步Obsidian。"""
import hashlib,json,sys
from datetime import datetime
from pathlib import Path
from prepare_person import BASE,read,save_new
sys.path.insert(0,str(BASE.parents[1]))
from data_review.validate_entity_batch import check
from run_baseline import build_records

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def lines(p):return [json.loads(s) for s in p.read_text().splitlines() if s]
backups=[]
def update(p,text):
    if p.exists():
        b=BASE/'art_export_backups_20261118'/p.relative_to(BASE.parents[2]);b.parent.mkdir(parents=True,exist_ok=True)
        with b.open('xb') as f:f.write(p.read_bytes())
        backups.append(str(b.relative_to(BASE)))
    p.write_text(text)
rows=lines(BASE/'art.entities.pending_review.jsonl');fields=read(BASE/'fields.json')['art']
text='# 新批次艺术作品备选\n\n- **已生成**：10个作品、50属性项，每项原值＋四备选；候选待审。\n- **固定类型**：前5幅绘画、后5件人物雕塑；类型在两张表显示，不作为冲突属性。\n- **口径**：尺寸为作品本体的高度、宽度，不含画框或底座；创作者使用属性姓名池。\n- **检查**：五值互异、尺寸±5%、年份及400题组题预览通过；与建筑共100个属性姓名无重复，未跑模型。\n\n'
text+='| 作品 | 类型 | '+' | '.join(fields)+' |\n|---|---|'+'---|'*len(fields)+'\n'
for row in rows:text+='| '+row['name']+' | '+row['作品类型']+' | '+' | '.join(row[f][0] for f in fields)+' |\n'
for row in rows:
    text+=f"\n<details>\n<summary>{row['name']}：四备选</summary>\n\n| 属性 | 原值 | 备选1 | 备选2 | 备选3 | 备选4 |\n|---|---|---|---|---|---|\n"
    for f in fields:text+='| '+f+' | '+' | '.join(row[f])+' |\n'
    text+='\n</details>\n'
text+='\n- **留痕**：逐作品prompt、raw及规则记录在entities/ART-*；汇总检查见20_art_complete.execution_record.json。\n- **边界**：材料生成时考虑类型与尺寸；结构检查不代表专业审核或等可信，用户尚未审核本类。\n'
source=BASE/'REVIEW_art.md';mirror=BASE.parents[1]/'notes/02 数据/合成数据/新批次艺术备选.md'
for p in [source,mirror]:
    with p.open('x') as f:f.write(text)
assert source.read_bytes()==mirror.read_bytes()
manifest=read(BASE/'CURRENT_DATA.json');manifest['components']['art']={'path':'art.entities.pending_review.jsonl','sha256':sha(BASE/'art.entities.pending_review.jsonl'),'count':10,'user_review':'候选待审'}
combined=[]
for c in manifest['components'].values():
    p=BASE/c['path'];assert sha(p)==c['sha256'];combined.extend(lines(p))
validation=check(combined,require_row_order=True,per_type={c:10 for c in manifest['components']});assert not validation['errors'],validation
assert len(combined)==70 and validation['instances']==390
records=build_records(combined,(1,2,3,4));assert len(records)==3120
assert all('整机保修' not in s for e in combined if e['entity_class']=='product' for s in e['保修期'])
with (BASE/'entities.generated70.pending_review.jsonl').open('x') as f:f.write(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in combined))
with (BASE/'baseline.generated70.prompt_preview.jsonl').open('x') as f:f.write(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in records))
manifest.update(updated=datetime.now().astimezone().isoformat(),status='all_candidates_generated_not_final',generated_entities=70,not_yet_generated=[],combined_partial_data={'path':'entities.generated70.pending_review.jsonl','sha256':sha(BASE/'entities.generated70.pending_review.jsonl'),'not_final':True})
update(BASE/'CURRENT_DATA.json',json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
p=BASE/'README.md';s=p.read_text();start=s.index('- **当前**：');end=s.index('\n',start)
s=s[:start]+'- **当前**：七类各10，共70实体的原值和四备选已生成；390属性项、1560冲突对、3120题／模型，候选未定稿。'+s[end:]
s=s.replace('CURRENT_DATA.json列出60个实体的当前组件；product_warranty_wording_20261118/entities.generated60.pending_review.jsonl仅为部分候选，未定稿。','CURRENT_DATA.json列出70个实体的当前组件；entities.generated70.pending_review.jsonl为完整候选，未定稿。').replace('用户看产品，尤其两项3个月保修；随后艺术类。','用户看艺术表，收口已标出的候选问题，再定稿准备完整baseline。')
s+='- **艺术**：[当前艺术表](REVIEW_art.md)已同步Obsidian；固定类型在两表显示，尺寸±5%无精度例外。\n';update(p,s)
block='- **2026-11-18 新批次70候选已全部生成，艺术10个含备选完成**：逐作品先存原值prompt和材料prompt再生成；创作者按属性姓名池后50名，年份/尺寸按规则。400题检查通过，作品类型由description复制为标量背景行，双表可见且不作冲突属性；原始输出未改。\n- **当前版本**：data_generation/new_batch_20261116_v2/CURRENT_DATA.json列七类各10组件，保留机构规模修订、保修“N个月”新版；entities.generated70.pending_review.jsonl为390属性项、1560冲突对、3120题完整候选，未定稿、未推理。全批结构/行序/姓名隔离检查通过；50条活动主办方文字重合标记仍保留。\n- **交付与下一步**：REVIEW_art.md与Obsidian《新批次艺术备选》逐字一致，产品措辞已同步。用户看艺术并收口已标候选问题，尤其两项3个月保修；不把继续生成的授权当成全部逐值人工认可。完整新数据baseline尚未跑，下一步先定稿。记录见20_art_complete、21_art_export；保修改版见product_warranty_wording_20261118。\n\n'
p=BASE.parents[1]/'HANDOFF.md';update(p,p.read_text().replace('# HANDOFF\n\n','# HANDOFF\n\n'+block,1))
coord='## 全70候选生成完成（2026-11-18；Codex同步）\n\n- **当前**：七类各10，70实体含四备选已齐；390属性项、1560冲突对、3120题／模型。\n- **版本**：CURRENT_DATA.json指向完整候选entities.generated70.pending_review.jsonl；机构规模修订和保修“N个月”均保留。\n- **检查**：全批结构/行序/姓名隔离通过；活动50条文字重合标记及两项3个月保修仍待看。\n- **下一步**：用户看Obsidian《新批次艺术备选》，收口候选问题后定稿；完整新数据baseline未跑。Codex继续数据，Claude无需重复生成。\n\n'
for name in ['codex.md','claude.md']:
    p=BASE.parents[1]/'coordination'/name;first,rest=p.read_text().split('\n',1);update(p,first+'\n\n'+coord+rest.lstrip('\n'))
p=BASE.parents[1]/'ENTITY_GENERATION_PROTOCOL_DRAFT.md';s=p.read_text().replace('新批次60实体候选已生成，未定稿','新批次70实体候选已生成，未定稿');update(p,s);update(BASE.parents[1]/'notes/02 数据/合成数据/实体生成规程（给老师草稿）.md',s)
save_new(BASE/'21_art_export.execution_record.json',{'date':datetime.now().astimezone().isoformat(),'actor':'Codex','script_sha256':sha(Path(__file__)),'review_sha256':sha(source),'mirror':str(mirror),'mirror_equal':source.read_bytes()==mirror.read_bytes(),'backups':backups,'validation':validation,'combined_data_sha256':sha(BASE/'entities.generated70.pending_review.jsonl'),'combined_prompts_previewed':3120,'checks':{'current_components_hashes_match':True,'revised_organization_component_retained':True,'simplified_warranty_values_retained':True,'all_seven_types_ten_each':True},'model_inference_run':False,'user_review':'艺术尚未审核；全批候选未定稿。'})
print(json.dumps({'entities':70,'attributes':validation['instances'],'prompts_previewed':len(records),'errors':validation['errors'],'review_flags':len(validation['review']),'mirror_equal':True,'product_component':manifest['components']['product']['path']},ensure_ascii=False))
