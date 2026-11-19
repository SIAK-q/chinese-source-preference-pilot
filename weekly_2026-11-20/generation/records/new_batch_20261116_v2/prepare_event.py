"""每次仅保存下一个活动的实际输入与prompt，等原值检查后再推进。"""
import hashlib
import json
from datetime import datetime
from prepare_person import BASE,read,save_new
config_path=BASE/'event.input.json'
if not config_path.exists():
    old=BASE.parent/'night_batch_20261116/entities'
    identities=[{k:r[k] for k in ['id','name']} for r in [read(p) for p in sorted(old.glob('EVENT-*/original.raw.json'))]]
    save_new(config_path,{'date':'2026-11-17','identities':identities,'selection':'沿用准备的活动名和ID；五项属性重新生成。','duration_definition':'整场活动持续时间；跨日活动用天，单日活动用小时或分钟。','participation_definition':'开放展览、节庆、活动周记累计参与人次；比赛按参赛人数。','coverage':'活动类型分别考虑整表，不将所有活动套为同一规模。'})
config=read(config_path);batch=read(BASE/'batch.input.json');previous=[]
template=BASE/'templates/event.original.txt'
assert hashlib.sha256(template.read_bytes()).hexdigest()==read(BASE/'00_templates_frozen.execution_record.json')['template_hashes']['templates/event.original.txt']
for identity in config['identities']:
    folder=BASE/'entities'/identity['id']
    if (folder/'original.raw.json').exists():
        assert (folder/'02_output.execution_record.json').exists()
        previous.append(read(folder/'original.raw.json'));continue
    if (folder/'original.prompt.txt').exists():print((folder/'original.prompt.txt').read_text());break
    inp={'date':config['date'],**identity,'entity_class':'event','entity_places':batch['entity_places'],'duration_definition':config['duration_definition'],'participation_definition':config['participation_definition'],'coverage':config['coverage'],'previous_same_type_originals':previous,'references':[]}
    prompt=template.read_text().replace('{{entity_type_zh}}','活动').replace('{{input_json}}',json.dumps(inp,ensure_ascii=False,indent=2))
    save_new(folder/'original.input.json',inp)
    with (folder/'original.prompt.txt').open('x') as f:f.write(prompt)
    save_new(folder/'01_input.execution_record.json',{'date':datetime.now().astimezone().isoformat(),'actor':'Codex','step':'event_prompt_saved_before_output','prompt_sha256':hashlib.sha256(prompt.encode()).hexdigest(),'model':batch['model'],'sampling_parameters':'不可见','context_boundary':batch['context_boundary'],'input':'original.input.json','prompt':'original.prompt.txt'})
    print(prompt);break
else:print('十活动原值已齐。')
