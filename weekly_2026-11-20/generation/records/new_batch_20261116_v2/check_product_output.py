"""检查产品原值；不做外部品牌核验，不放宽产品规则。"""
import sys,re,hashlib
from datetime import datetime
from decimal import Decimal,ROUND_FLOOR
from prepare_person import BASE,read,save_new
folder=BASE/'entities'/sys.argv[1];raw=read(folder/'original.raw.json');inp=read(folder/'original.input.json');saved=read(folder/'01_input.execution_record.json');fields=read(BASE/'fields.json')['product']
d=datetime.strptime(raw['发布日期'],'%Y年%m月%d日').date()
checks={'five_expected_fields':set(raw)=={'id','name','entity_class',*fields},'identity_matches':raw['id']==inp['id'] and raw['name']==inp['name'] and raw['entity_class']=='product','date_not_future':d.isoformat()<=inp['date'],'price_unit':bool(re.fullmatch(r'[1-9]\d*元人民币',raw['价格'])),'weight_unit':bool(re.fullmatch(r'[1-9]\d*(?:\.\d+)?(?:公斤|克)',raw['重量'])),'warranty_months_only':bool(re.fullmatch(r'整机保修(?:3|6|12|18|24|36|48|60)个月',raw['保修期'])),'manufacturer_not_model_hint':inp['name'].split()[0] not in raw['制造商'],'prompt_unchanged':hashlib.sha256((folder/'original.prompt.txt').read_bytes()).hexdigest()==saved['prompt_sha256']}
assert all(checks.values()),checks
save_new(folder/'02_output.execution_record.json',{'date':datetime.now().astimezone().isoformat(),'actor':'Codex','model':saved['model'],'sampling_parameters':'不可见','raw_output':'original.raw.json','raw_sha256':hashlib.sha256((folder/'original.raw.json').read_bytes()).hexdigest(),'checks':checks,'assistant_review':'按产品类型联合生成价格、整机净重和整机保修；公司名为候选，未外部查重。','user_review':'未审核','edits':[]})
print(raw['id'],'原值检查通过')
