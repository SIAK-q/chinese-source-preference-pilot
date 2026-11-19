"""检查活动原值的格式、固定身份和prompt哈希；不替代用户审核。"""
import sys,hashlib,re
from datetime import datetime
from prepare_person import BASE,read,save_new
folder=BASE/'entities'/sys.argv[1];raw=read(folder/'original.raw.json');inp=read(folder/'original.input.json');saved=read(folder/'01_input.execution_record.json')
m=re.fullmatch(r'(\d{4})年(\d{1,2})月(\d{1,2})日',raw['举办日期']);date=datetime(*map(int,m.groups())).date()
fields=read(BASE/'fields.json')['event']
checks={'five_expected_fields':set(raw)=={'id','name','entity_class',*fields},'identity_matches':all(raw[k]==inp[k] for k in ['id','name','entity_class']),'date_not_future':date.isoformat()<=inp['date'],'positive_numbers':all(re.fullmatch(r'[1-9]\d*(?:\.\d+)?'+u,raw[f]) for f,u in [('持续时间','(?:天|小时|分钟)'),('参与人数','人(?:次)?'),('预算','万元')]),'local_organizer':any(raw['主办方'].startswith(p+'市') for p in inp['entity_places']),'prompt_unchanged':hashlib.sha256((folder/'original.prompt.txt').read_bytes()).hexdigest()==saved['prompt_sha256']}
assert all(checks.values()),checks
save_new(folder/'02_output.execution_record.json',{'date':datetime.now().astimezone().isoformat(),'actor':'Codex','step':'event_original_generated_then_checked','model':saved['model'],'sampling_parameters':'不可见','raw_output':'original.raw.json','raw_output_sha256':hashlib.sha256((folder/'original.raw.json').read_bytes()).hexdigest(),'checks':checks,'assistant_review':'生成时联合考虑类型、日期、时长、参与规模、主办方和预算；未做实际活动商业核验。','user_review':'未审核','edits':[]})
print(raw['id'],'原值检查通过')
