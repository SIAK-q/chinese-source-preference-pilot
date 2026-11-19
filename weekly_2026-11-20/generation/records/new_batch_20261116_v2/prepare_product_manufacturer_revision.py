"""发现已知品牌用字后，仅为PRODUCT-05制造商备选1保存修改prompt。"""
import hashlib,json
from datetime import datetime
from prepare_person import BASE,read,save_new
folder=BASE/'entities/PRODUCT-05';original=read(folder/'original.raw.json');values=read(folder/'alternatives.manufacturer.raw.json')
current={**original,'制造商':[original['制造商'],*values]}
feedback='Codex助手检查：制造商备选1“顺丰电器有限公司”使用了已知品牌“顺丰”。只将该备选改为“顺益电器有限公司”；其他值保持原样。其他属性四备选尚未组装，本次只处理现有制造商五值，不声称用户作了此决定。'
prompt=(BASE/'templates/product.revision.txt').read_text().replace('{{current_table_json}}',json.dumps(current,ensure_ascii=False,indent=2)).replace('{{specific_feedback_and_requested_changes}}',feedback)
with (folder/'manufacturer.revision.prompt.txt').open('x') as f:f.write(prompt)
save_new(folder/'04b_manufacturer_revision_input.execution_record.json',{'date':datetime.now().astimezone().isoformat(),'actor':'Codex','assistant_flag':feedback,'user_decision':'未作此具体决定；助手按避免已知品牌的既定要求修订。','prompt_sha256':hashlib.sha256(prompt.encode()).hexdigest(),'before':values,'raw_preserved':True})
print(prompt)
