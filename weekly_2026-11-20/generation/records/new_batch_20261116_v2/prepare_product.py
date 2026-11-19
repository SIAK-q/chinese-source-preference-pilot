"""按已审模板逐产品先保存输入，再生成原值。"""
import hashlib,json
from datetime import datetime
from prepare_person import BASE,read,save_new
config=BASE/'product.input.json'
if not config.exists():
    plan=BASE.parent/'product_plan/plan.json'
    save_new(config,{'date':'2026-11-17','products':read(plan)['products'],'plan_sha256':hashlib.sha256(plan.read_bytes()).hexdigest(),'selection':'沿用已定十种产品/名称与ID，五项属性重新生成。'})
batch=read(BASE/'batch.input.json');previous=[];p=BASE/'templates/product.original.txt'
assert hashlib.sha256(p.read_bytes()).hexdigest()==read(BASE/'00_templates_frozen.execution_record.json')['template_hashes']['templates/product.original.txt']
for product in read(config)['products']:
    folder=BASE/'entities'/product['id']
    if (folder/'original.raw.json').exists():
        assert (folder/'02_output.execution_record.json').exists();previous.append(read(folder/'original.raw.json'));continue
    if (folder/'original.prompt.txt').exists():print((folder/'original.prompt.txt').read_text());break
    inp={'date':'2026-11-17',**product,'previous_products':previous,'references':[]}
    prompt=p.read_text()
    for k,v in {'id':product['id'],'type':product['type'],'name':product['name'],'previous_products_or_empty_list':json.dumps(previous,ensure_ascii=False),'references_or_empty_list':'[]'}.items():prompt=prompt.replace('{{'+k+'}}',v)
    assert '{{' not in prompt
    save_new(folder/'original.input.json',inp)
    with (folder/'original.prompt.txt').open('x') as f:f.write(prompt)
    save_new(folder/'01_input.execution_record.json',{'date':datetime.now().astimezone().isoformat(),'actor':'Codex','step':'product_prompt_saved_before_output','prompt_sha256':hashlib.sha256(prompt.encode()).hexdigest(),'template_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'model':batch['model'],'sampling_parameters':'不可见','context_boundary':batch['context_boundary'],'input':'original.input.json','prompt':'original.prompt.txt','authorization':'用户已授权按类集中生成后审核；模板历史等待审核措辞不改。'})
    print(prompt);break
else:print('十产品原值均已生成。')
