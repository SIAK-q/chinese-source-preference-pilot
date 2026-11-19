"""先保存完整已审备选prompt和规则执行输入；制造商由当前会话撰写，日期数值由脚本生成。"""
import hashlib,json
from datetime import datetime
from prepare_person import BASE,read,save_new
p=BASE/'templates/product.alternatives.txt'
assert hashlib.sha256(p.read_bytes()).hexdigest()==read(BASE/'00_templates_frozen.execution_record.json')['template_hashes']['templates/product.alternatives.txt']
for i in range(1,11):
    folder=BASE/'entities'/f'PRODUCT-{i:02}';raw=read(folder/'original.raw.json')
    prompt=p.read_text().replace('{{original_table_json}}',json.dumps(raw,ensure_ascii=False,indent=2))
    with (folder/'alternatives.prompt.txt').open('x') as f:f.write(prompt)
    save_new(folder/'03_alternatives_input.execution_record.json',{'date':datetime.now().astimezone().isoformat(),'actor':'Codex','step':'full_product_alternatives_prompt_saved_before_output','original_sha256':hashlib.sha256((folder/'original.raw.json').read_bytes()).hexdigest(),'prompt_sha256':hashlib.sha256(prompt.encode()).hexdigest(),'model':'Codex；具体型号/版本不可见','parameters':'不可见','method':'制造商四备选在当前会话生成并保存raw；日期/价格/重量/保修按同一已审prompt的明确规则由另存脚本生成。完整组装输出不冒称纯模型raw。','date_seed':f"42:{raw['id']}:发布日期",'date_windows_days':[[-365,-183],[-182,-30],[30,182],[183,365]],'numeric_percent':5,'numeric_precision_exception_allowed':False,'warranty_slots':[3,6,12,18,24,36,48,60]})
    print(raw['id']+'\n'+prompt)
