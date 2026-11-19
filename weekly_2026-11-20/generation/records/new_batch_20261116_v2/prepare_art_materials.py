"""带完整作品原值保存材料备选prompt，当前会话读取后撰写四备选。"""
import hashlib,json
from datetime import datetime
from prepare_person import BASE,read,save_new
p=BASE/'templates/art.alternatives.txt'
assert hashlib.sha256(p.read_bytes()).hexdigest()==read(BASE/'00_templates_frozen.execution_record.json')['template_hashes']['templates/art.alternatives.txt']
for i in range(1,11):
    folder=BASE/'entities'/f'ART-{i:02}';raw=read(folder/'original.raw.json')
    prompt=p.read_text().replace('{{original_table_json}}',json.dumps(raw,ensure_ascii=False,indent=2)).replace('{{target_field}}','材料').replace('{{field_requirements}}','作品类型固定为'+raw['description']+'；尺寸是作品本体，不含框或底座。四种材料各自替换后应仍与类型、题名和本体尺寸相容；绘画材料可包含载体与颜料，不以仅调整词序制造差异。')
    with (folder/'alternatives.material.prompt.txt').open('x') as f:f.write(prompt)
    save_new(folder/'03_material_input.execution_record.json',{'date':datetime.now().astimezone().isoformat(),'actor':'Codex','step':'material_prompt_saved_before_output','original_sha256':hashlib.sha256((folder/'original.raw.json').read_bytes()).hexdigest(),'prompt_sha256':hashlib.sha256(prompt.encode()).hexdigest(),'model':'Codex；具体型号/版本不可见','parameters':'不可见','context':'当前会话撰写，非隔离API调用'})
    print(raw['id']+'\n'+prompt)
