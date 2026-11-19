"""先保存用户决定、实际修改输入及新版prompt；旧raw和冻结模板不动。"""
import hashlib,json
from datetime import datetime
from pathlib import Path
ROOT=Path(__file__).resolve().parent;BASE=ROOT.parent

def save(p,r):
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('x') as f:json.dump(r,f,ensure_ascii=False,indent=2);f.write('\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
manifest=json.loads((BASE/'CURRENT_DATA.json').read_text());source=BASE/manifest['components']['product']['path'];templates={}
for stage in ['original','alternatives','revision']:
    before=(BASE/f'templates/product.{stage}.txt').read_text();after=before
    if stage=='original':after=before.replace('保修期只写整机保修月数，例如“整机保修24个月”；不加入电池、配件、使用次数或服务条款。','保修期写成“24个月”这种形式，不添加配件或其他条件。')
    elif stage=='alternatives':after=before.replace('只改变整机保修月数。','只改变保修月数，不添加配件或其他条件。')
    p=ROOT/f'templates/product.{stage}.txt';p.parent.mkdir(exist_ok=True)
    with p.open('x') as f:f.write(after)
    templates[stage]={'source':str((BASE/f'templates/product.{stage}.txt').relative_to(BASE)),'source_sha256':sha(BASE/f'templates/product.{stage}.txt'),'new':str(p.relative_to(BASE)),'new_sha256':sha(p),'wording_changed':after!=before}
request={'date':datetime.now().astimezone().isoformat(),'actor':'用户决定；Codex执行','user_messages':['提问，保修期为什么一定要强调整机保修，直接写xx个月不可以。？','[prompt注明“均指整机保修”。]会否有些咬文嚼字','好的继续'],'decision':'属性保修期保留，所有取值仅写N个月；prompt只说改变保修月数，不添加配件或其他条件，不追加均指整机的定义。','scope':'仅删除10产品50个保修取值的固定前缀整机保修；月数、档位、其他字段、行序均不变。两项3个月的相容性标记仍未处理。','input':str(source.relative_to(BASE)),'input_sha256':sha(source),'templates':templates,'method':'格式转换脚本；不调用模型、不重新生成属性值。'}
save(ROOT/'00_input.execution_record.json',request)
print(json.dumps(request,ensure_ascii=False,indent=2))
