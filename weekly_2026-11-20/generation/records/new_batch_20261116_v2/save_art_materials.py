"""保存当前会话读取逐作品完整prompt后撰写的材料四备选。"""
import hashlib
from datetime import datetime
from prepare_person import BASE,read,save_new
outputs=[
['布面丙烯','纸本水彩','纸本水粉','纸本水墨'],
['布面油彩','布面丙烯','纸本水粉','纸本水墨'],
['布面油彩','布面丙烯','纸本水彩','纸本水粉'],
['布面油彩','纸本水彩','纸本水墨','纸本水粉'],
['布面油彩','布面丙烯','纸本水彩','纸本水墨'],
['石材','木材','玻璃钢','不锈钢'],
['铸铜','石材','木材','不锈钢'],
['铸铜','石材','木材','玻璃钢'],
['铸铜','木材','玻璃钢','不锈钢'],
['铸铜','石材','玻璃钢','不锈钢']]
for i,values in enumerate(outputs,1):
    folder=BASE/'entities'/f'ART-{i:02}';raw=read(folder/'original.raw.json');saved=read(folder/'03_material_input.execution_record.json')
    assert hashlib.sha256((folder/'alternatives.material.prompt.txt').read_bytes()).hexdigest()==saved['prompt_sha256']
    assert len(set([raw['材料'],*values]))==5
    save_new(folder/'alternatives.material.raw.json',values)
    save_new(folder/'04_material_output.execution_record.json',{'date':datetime.now().astimezone().isoformat(),'actor':'Codex','step':'art_material_alternatives_authored_after_prompt','raw_output':'alternatives.material.raw.json','raw_sha256':hashlib.sha256((folder/'alternatives.material.raw.json').read_bytes()).hexdigest(),'checks':{'five_distinct':True,'prompt_unchanged':True},'model':saved['model'],'parameters':'不可见','assistant_review':'分别考虑原表固定类型、题名、本体尺寸；五值不靠词序变化区分。未获专业或用户审核。','user_review':'未审核','edits':[]})
print('十组材料备选已保存。')
