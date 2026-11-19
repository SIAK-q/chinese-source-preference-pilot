"""保存当前会话读完整产品prompt后撰写的制造商四备选。"""
import hashlib
from datetime import datetime
from prepare_person import BASE,read,save_new
outputs=[
['恒嘉电器有限公司','瑞宜电器有限公司','丰成电器有限公司','顺启电器有限公司'],
['嘉益电器有限公司','宏勤电器有限公司','瑞启电器有限公司','丰宜电器有限公司'],
['恒丰电器有限公司','嘉成电器有限公司','顺嘉电器有限公司','宏启电器有限公司'],
['瑞成电器有限公司','恒启电器有限公司','嘉宜电器有限公司','丰嘉电器有限公司'],
['顺丰电器有限公司','恒益电器有限公司','瑞嘉电器有限公司','嘉勤电器有限公司'],
['瑞勤车辆有限公司','嘉宜车辆有限公司','恒启车辆有限公司','顺成车辆有限公司'],
['恒嘉电子有限公司','顺宜电子有限公司','丰启电子有限公司','瑞成电子有限公司'],
['嘉宜电子有限公司','宏成电子有限公司','顺启电子有限公司','丰勤电子有限公司'],
['嘉成电子有限公司','顺勤电子有限公司','恒宜电子有限公司','丰嘉电子有限公司'],
['恒成电子有限公司','嘉启电子有限公司','瑞勤电子有限公司','顺嘉电子有限公司']]
for i,values in enumerate(outputs,1):
    folder=BASE/'entities'/f'PRODUCT-{i:02}';raw=read(folder/'original.raw.json');inp=read(folder/'03_alternatives_input.execution_record.json')
    assert hashlib.sha256((folder/'alternatives.prompt.txt').read_bytes()).hexdigest()==inp['prompt_sha256']
    assert len(set([raw['制造商'],*values]))==5
    model=raw['name'].split()[0];assert all(model not in v for v in values)
    save_new(folder/'alternatives.manufacturer.raw.json',values)
    save_new(folder/'04_manufacturer_output.execution_record.json',{'date':datetime.now().astimezone().isoformat(),'actor':'Codex','step':'manufacturer_alternatives_authored_after_saved_full_prompt','prompt':'alternatives.prompt.txt','raw_output':'alternatives.manufacturer.raw.json','raw_sha256':hashlib.sha256((folder/'alternatives.manufacturer.raw.json').read_bytes()).hexdigest(),'model':inp['model'],'parameters':'不可见','checks':{'five_distinct_company_names':True,'model_not_in_company_names':True,'prompt_unchanged':True},'assistant_review':'按电器、电子、车辆行业取常见商业用字；未外部查重，不能保证现实无同名公司。','user_review':'未审核','edits':[]})
print('十组制造商备选已保存。')
