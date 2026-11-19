"""将既有生成记录整理成简短过程页，嵌入真实样例；不改数据、不重生成。"""
import hashlib,json
from datetime import datetime
from pathlib import Path
BASE=Path(__file__).resolve().parent;PILOT=BASE.parents[1]
RECORD=BASE/'process_review_20261118';RECORD.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,r):
    with p.open('x') as f:json.dump(r,f,ensure_ascii=False,indent=2);f.write('\n')
def read(p):return json.loads(p.read_text())
manifest_before=sha(BASE/'CURRENT_DATA.json');data_before=sha(BASE/'entities.generated70.pending_review.jsonl')
save(RECORD/'00_input.execution_record.json',{'date':datetime.now().astimezone().isoformat(),'actor':'Codex','user_request':'我看看过程。','previous_user_preference':'那我觉得wfw有什么我保存对应的就差不多','purpose':'展示已有过程与真实输入输出，不追加重新生成要求。','input_manifest_sha256':manifest_before,'input_data_sha256':data_before,'script':str(Path(__file__).relative_to(BASE)),'script_sha256':sha(Path(__file__))})
sources={}
def block(relative,language='json'):
    p=BASE/relative;sources[relative]=sha(p)
    return '```'+language+'\n'+p.read_text().rstrip()+'\n```\n'
folder='entities/ART-01/'
entity=read(BASE/folder/'entity.pending_review.json')
text='# 本批数据的生成过程\n\n- **当前**：新批次七类各10，共70个候选；每项原值＋四备选，未定稿，完整baseline未跑。\n- **本页怎么读**：先看步骤，再展开《双陵晨光图》的真实prompt、输出和脚本处理；下面用的是已经保存的记录。\n- **生成方式**：Codex在当前会话读已存任务prompt后撰写输出；任务prompt不是完整聊天上下文，具体模型版本与参数不可见。\n\n'
text+='- **1．定规则**：确定七类、39种属性、姓名地名池及备选规则。艺术类型沿用准备设定；创作者姓名先分配，不让模型另起姓名。\n- **2．写模板**：Codex按规程编写各类原值模板；产品使用已审模板，其他模板不记为用户逐句审核通过。11-16保存冻结记录。\n- **3．填实际输入**：逐实体填名称、固定背景、候选名单和此前同类原值；先存input和prompt，再生成该实体原值。\n- **4．生成原值**：当前会话生成完整表；固定提供的姓名、性别或作品类型沿用输入，其余内容同时考虑整表搭配。保存raw后再处理下个实体。\n- **5．补四备选**：文本内容带完整原表生成；名单、日期、数值等由脚本按规则补齐。每项实验只替换一个属性。\n- **6．检查**：检查五值互异、单位、范围、行序、单属性差异和双表顺序；格式检查不算用户审核，也不证明等可信。\n- **7．处理修改**：另存新版及修改前后、原因、谁作决定。机构规模、活动删“周”、制造商及保修措辞修改均保留旧版。\n- **8．交付**：说明与Obsidian同步后按类给用户看；CURRENT_DATA.json指向当前各组件及70个合并候选。\n\n'
text+='| 内容 | 实际怎样得到 |\n|---|---|\n| 各类原值 | 当前会话按保存的任务prompt生成，固定名单与背景沿用输入 |\n| 人物职业＋学历、身高＋体重备选 | 两组成对生成；实验仍只改一个属性 |\n| 行业、建筑/艺术材料、活动主办方、产品制造商备选 | 读完整原表后，当前会话撰写四个备选 |\n| 创作者、设计师及城市等 | 从已准备名单按保存的规则分配或抽取 |\n| 日期、数值、保修月数等 | 脚本按已定区间、幅度或档位生成 |\n\n'
text+='<details>\n<summary>真实样例①：生成前保存的原值prompt（原文）</summary>\n\n'+block(folder+'original.prompt.txt','text')+'\n</details>\n\n'
text+='<details>\n<summary>真实样例②：当前会话随后写出的原始输出（原文）</summary>\n\n'+block(folder+'original.raw.json')+'\n</details>\n\n'
text+='<details>\n<summary>真实样例③：材料备选的实际prompt和原始输出</summary>\n\n'+block(folder+'alternatives.material.prompt.txt','text')+'\n'+block(folder+'alternatives.material.raw.json')+'\n</details>\n\n'
text+='- **样例中脚本补的部分**：创作者用预分配五人；年份取−2、−1、+1、+2年；85厘米高度取81、83、87、89厘米；115厘米宽度取110、112、118、120厘米。\n- **固定背景处理**：把description中的“架上绘画”复制成可显示的“作品类型”行；不作为冲突属性。\n\n'
text+='| 属性 | 原值 | 备选1 | 备选2 | 备选3 | 备选4 |\n|---|---|---|---|---|---|\n'
for field in ['创作者','创作年份','高度','宽度','材料']:text+='| '+field+' | '+' | '.join(entity[field])+' |\n'
text+='\n<details>\n<summary>真实样例④：脚本执行前的输入与执行后记录（原文）</summary>\n\n'+block(folder+'05_rule_inputs.execution_record.json')+'\n'+block(folder+'06_assembly.execution_record.json')+'\n</details>\n\n'
text+='<details>\n<summary>真实修改样例：保修措辞的决定与前后对照</summary>\n\n- **用户要求**：保修值直接写“N个月”；prompt不额外定义“均指整机保修”。\n- **实际修改**：50个值删除固定前缀，月数不变；这不是重生成。\n\n'+block('product_warranty_wording_20261118/00_input.execution_record.json')+'\n'
changes=read(BASE/'product_warranty_wording_20261118/changes.json');sources['product_warranty_wording_20261118/changes.json']=sha(BASE/'product_warranty_wording_20261118/changes.json')
text+='| 产品 | 位置 | 修改前 | 修改后 |\n|---|---|---|---|\n'
for c in changes[:5]:text+='| '+c['id']+' | '+('原值' if c['value_index']==0 else '备选'+str(c['value_index']))+' | '+c['before']+' | '+c['after']+' |\n'
text+='\n</details>\n\n'
text+='- **全批记录位置**：`pilot/data_generation/new_batch_20261116_v2/`；各实体过程在`entities/实体ID/`，当前版本以`CURRENT_DATA.json`为准。\n- **这次只展示过程**：没有改实体数据，没有重新调用模型，也没有跑baseline。\n'
source=BASE/'GENERATION_PROCESS_REVIEW.md';mirror=PILOT/'notes/02 数据/合成数据/本批数据的生成过程.md'
for p in [source,mirror]:
    with p.open('x') as f:f.write(text)
assert source.read_bytes()==mirror.read_bytes()
missing=[];folders=sorted(p for p in (BASE/'entities').iterdir() if p.is_dir())
for folder in folders:
    for name in ['original.input.json','original.prompt.txt','01_input.execution_record.json','original.raw.json','02_output.execution_record.json','entity.pending_review.json']:
        if not (folder/name).exists():missing.append(str(folder/name))
assert len(folders)==70 and not missing
frozen=read(BASE/'00_templates_frozen.execution_record.json')
assert all(sha(BASE/path)==h for path,h in frozen['template_hashes'].items())
p=PILOT/'HANDOFF.md';backup=RECORD/'HANDOFF.before.md'
with backup.open('x') as f:f.write(p.read_text())
entry='- **2026-11-18 按用户要求展示生成过程**：data_generation/new_batch_20261116_v2/GENERATION_PROCESS_REVIEW.md与Obsidian《本批数据的生成过程》一致。短步骤＋真实ART-01的原值prompt/raw、材料prompt/raw、规则输入/执行记录及最终五值；含保修措辞修改样例。\n- **核对与边界**：70实体核心文件齐全、冻结模板哈希未变；当前70数据与manifest未改，未重生成、未跑模型。用户要求以WFW对应材料为留档参照；不把独立API和逐次完整响应记录追加为必须重生成的门槛。任务prompt不含完整聊天上下文、版本参数不可见已注明。记录见process_review_20261118。\n\n'
p.write_text(p.read_text().replace('# HANDOFF\n\n','# HANDOFF\n\n'+entry,1))
assert sha(BASE/'CURRENT_DATA.json')==manifest_before and sha(BASE/'entities.generated70.pending_review.jsonl')==data_before
save(RECORD/'01_complete.execution_record.json',{'date':datetime.now().astimezone().isoformat(),'actor':'Codex','script_sha256':sha(Path(__file__)),'source':str(source),'mirror':str(mirror),'mirror_equal':True,'document_sha256':sha(source),'embedded_source_hashes':sources,'checks':{'70_entity_core_records_present':True,'missing_core_files':missing,'frozen_templates_unchanged':True,'current_manifest_and_data_unchanged':True},'model_inference_run':False,'generated_new_entities':False})
print(json.dumps({'source':str(source),'mirror':str(mirror),'mirror_equal':True,'entities_checked':len(folders),'missing':missing,'data_unchanged':True},ensure_ascii=False))
