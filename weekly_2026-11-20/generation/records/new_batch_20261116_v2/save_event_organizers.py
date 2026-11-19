"""保存当前会话读预存prompt后撰写的主办方原始输出，并做格式检查。"""
import hashlib
from datetime import datetime
from prepare_person import BASE,read,save_new
outputs=[
['惠明市田径协会','惠明市体育总会','惠明市体育发展中心','惠明市马拉松协会'],
['双陵市文化和旅游局','双陵市全民阅读促进会','双陵市作家协会','双陵市新华书店'],
['上泉市农业技术推广中心','上泉市农学会','上泉市农业科学院','上泉市农业产业协会'],
['白原市音乐家协会','白原市青年联合会','白原市合唱协会','白原市文化和旅游局'],
['龙泽市体育局','龙泽市体育总会','龙泽市水上运动协会','龙泽市体育发展中心'],
['乐水市文化和旅游局','乐水市非物质文化遗产保护中心','乐水市文化馆','乐水市手工艺协会'],
['通溪市文化馆','通溪市戏剧家协会','通溪市青少年活动中心','通溪市文化和旅游局'],
['清山市体育总会','清山市体育局','清山市社区体育协会','清山市全民健身协会'],
['新定市科学技术局','新定市科技馆','新定市科普志愿者协会','新定市科普教育基地联合会'],
['长源市摄影家协会','长源市文化馆','长源市文学艺术界联合会','长源市文化和旅游局']]
for i,values in enumerate(outputs,1):
    folder=BASE/'entities'/f'EVENT-{i:02}'
    raw=read(folder/'original.raw.json');saved=read(folder/'03_organizer_input.execution_record.json')
    assert hashlib.sha256((folder/'alternatives.organizer.prompt.txt').read_bytes()).hexdigest()==saved['prompt_sha256']
    assert len(set([raw['主办方'],*values]))==5
    place=raw['主办方'].split('市')[0]+'市'
    assert all(v.startswith(place) and v!=raw['name'] for v in values)
    save_new(folder/'alternatives.organizer.raw.json',values)
    save_new(folder/'04_organizer_output.execution_record.json',{'date':datetime.now().astimezone().isoformat(),'actor':'Codex','step':'organizer_alternatives_generated_in_current_conversation','raw_output':'alternatives.organizer.raw.json','raw_sha256':hashlib.sha256((folder/'alternatives.organizer.raw.json').read_bytes()).hexdigest(),'checks':{'five_distinct':True,'same_locality':True,'prompt_unchanged':True},'assistant_review':'按整表活动类型选择相关单位；非实际机构事实核验。','model':saved['model'],'parameters':'不可见','user_review':'未审核','edits':[]})
print('10组主办方备选已保存，格式检查通过。')
