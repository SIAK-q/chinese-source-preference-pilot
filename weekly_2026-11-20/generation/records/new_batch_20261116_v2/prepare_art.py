"""逐作品先保存实际prompt，作品类型固定，创作者使用剩余属性姓名。"""
import hashlib,json
from datetime import datetime
from prepare_person import BASE,read,save_new
config_path=BASE/'art.input.json'
if not config_path.exists():
    pool=BASE.parents[1]/'name_generation/person/reports_extended_20261115/attribute_people.jsonl';names=[json.loads(s)['name'] for s in pool.read_text().splitlines()]
    assert len(names)==len(set(names))==100
    identities=[]
    for i in range(1,11):
        old=read(BASE.parent/'night_batch_20261116/entities'/f'ART-{i:02}'/'original.raw.json')
        identities.append({'id':old['id'],'name':old['name'],'fixed_art_type':old['作品类型'],'creator_candidates':names[50+(i-1)*5:50+i*5]})
    save_new(config_path,{'date':'2026-11-18','identities':identities,'selection':'沿用准备题名和固定作品类型；五项属性重新生成。','attribute_people_pool':str(pool),'attribute_people_sha256':hashlib.sha256(pool.read_bytes()).hexdigest(),'creator_rule':'属性姓名池后50名分为十组，每组首名作原值、另四名作备选；与建筑前50名不重叠。','type_definition':'架上绘画或人物雕塑；类型为固定背景，在组装表中显示，不作为冲突属性。','dimensions':'作品本体高度、宽度，不含画框或雕塑底座。'})
config=read(config_path);batch=read(BASE/'batch.input.json');template=BASE/'templates/art.original.txt';previous=[]
assert hashlib.sha256(template.read_bytes()).hexdigest()==read(BASE/'00_templates_frozen.execution_record.json')['template_hashes']['templates/art.original.txt']
for identity in config['identities']:
    folder=BASE/'entities'/identity['id']
    if (folder/'original.raw.json').exists():
        assert (folder/'02_output.execution_record.json').exists();previous.append(read(folder/'original.raw.json'));continue
    if (folder/'original.prompt.txt').exists():print((folder/'original.prompt.txt').read_text());break
    inp={'date':config['date'],**identity,'entity_class':'art','creator_rule':config['creator_rule'],'fixed_creator':identity['creator_candidates'][0],'type_definition':config['type_definition'],'dimensions':config['dimensions'],'previous_same_type_originals':previous,'references':[]}
    prompt=template.read_text().replace('{{entity_type_zh}}','艺术作品').replace('{{input_json}}',json.dumps(inp,ensure_ascii=False,indent=2))
    save_new(folder/'original.input.json',inp)
    with (folder/'original.prompt.txt').open('x') as f:f.write(prompt)
    save_new(folder/'01_input.execution_record.json',{'date':datetime.now().astimezone().isoformat(),'actor':'Codex','step':'art_original_prompt_saved_before_output','input':'original.input.json','prompt':'original.prompt.txt','prompt_sha256':hashlib.sha256(prompt.encode()).hexdigest(),'model':batch['model'],'sampling_parameters':'不可见','context_boundary':batch['context_boundary']})
    print(prompt);break
else:print('十作品原值均已生成。')
