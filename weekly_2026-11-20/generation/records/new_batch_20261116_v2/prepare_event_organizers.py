"""保存带完整原表的主办方备选prompt后供当前会话生成。"""
import hashlib,json
from datetime import datetime
from prepare_person import BASE,read,save_new
p=BASE/'templates/event.alternatives.txt'
assert hashlib.sha256(p.read_bytes()).hexdigest()==read(BASE/'00_templates_frozen.execution_record.json')['template_hashes']['templates/event.alternatives.txt']
for i in range(1,11):
    folder=BASE/'entities'/f'EVENT-{i:02}'
    raw=read(folder/'original.raw.json')
    requirement='主办方须为该活动所在地名＋适合该活动的单位全名；不要使用活动题名充当单位。保留原地名，每项为一个单位，不添加联合主办关系；四项职能应与活动类型相配。'
    prompt=p.read_text().replace('{{original_table_json}}',json.dumps(raw,ensure_ascii=False,indent=2)).replace('{{target_field}}','主办方').replace('{{field_requirements}}',requirement)
    with (folder/'alternatives.organizer.prompt.txt').open('x') as f:f.write(prompt)
    save_new(folder/'03_organizer_input.execution_record.json',{'date':datetime.now().astimezone().isoformat(),'actor':'Codex','step':'organizer_prompt_saved_before_output','original_sha256':hashlib.sha256((folder/'original.raw.json').read_bytes()).hexdigest(),'prompt_sha256':hashlib.sha256(prompt.encode()).hexdigest(),'model':'Codex；具体型号/版本不可见','parameters':'不可见','context':'当前会话逐项撰写，非隔离API调用'})
    print(raw['id']+'\n'+prompt)
