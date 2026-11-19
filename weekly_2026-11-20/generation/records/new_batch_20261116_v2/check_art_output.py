"""艺术原值格式与固定背景检查，不冒称作品材料相容性已获人工确认。"""
import sys,re,hashlib
from datetime import datetime
from prepare_person import BASE,read,save_new
folder=BASE/'entities'/sys.argv[1];raw=read(folder/'original.raw.json');inp=read(folder/'original.input.json');saved=read(folder/'01_input.execution_record.json')
fields=read(BASE/'fields.json')['art']
checks={'expected_fields':set(raw)=={'id','name','entity_class','description',*fields},'identity_matches':all(raw[k]==inp[k] for k in ['id','name','entity_class']),'fixed_type':raw['description']==inp['fixed_art_type'],'fixed_creator':raw['创作者']==inp['fixed_creator'],'year_valid':bool(re.fullmatch(r'\d{4}年',raw['创作年份'])) and int(raw['创作年份'][:-1])<=2026,'positive_cm_dimensions':all(re.fullmatch(r'[1-9]\d*厘米',raw[f]) for f in ['高度','宽度']),'prompt_unchanged':hashlib.sha256((folder/'original.prompt.txt').read_bytes()).hexdigest()==saved['prompt_sha256']}
assert all(checks.values()),checks
save_new(folder/'02_output.execution_record.json',{'date':datetime.now().astimezone().isoformat(),'actor':'Codex','model':saved['model'],'sampling_parameters':'不可见','raw_output':'original.raw.json','raw_sha256':hashlib.sha256((folder/'original.raw.json').read_bytes()).hexdigest(),'checks':checks,'assistant_review':'生成时同时考虑固定作品类型、材料和作品本体尺寸；不冒称艺术专业或用户审核。','user_review':'未审核','edits':[]})
print(raw['id'],'原值检查通过')
