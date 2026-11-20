"""校验实际输出的题数、BF16、数据SHA、固定模型版本及逐题概率。"""
import hashlib,json,math,sys
from pathlib import Path
from model_compat import PINNED

def validate(path,expected_sha,expected_model,count):
    d=json.loads(path.read_text());results=d['results']
    assert count in (16,3040)
    assert d['data_sha256']==expected_sha and d['model']==expected_model
    assert d['n_records']==len(results)==count
    assert d['dtype'] in ('torch.bfloat16','bfloat16'), '实际精度不是BF16'
    assert d['revision_requested']==PINNED[expected_model]
    assert d['revision_loaded']==PINNED[expected_model], '实际模型版本与固定版本不符'
    assert d['alts']==[1,2,3,4] and d['limit']==(16 if count==16 else 0)
    assert all(math.isfinite(r['prob_a']) and math.isfinite(r['prob_b']) and 0<=r['prob_a']<=1 and 0<=r['prob_b']<=1 and abs(r['prob_a']+r['prob_b']-1)<1e-4 for r in results)
    prompts=path.parent/d['prompts_file']
    assert len(prompts.read_text().splitlines())==count
    assert hashlib.sha256(prompts.read_bytes()).hexdigest()==d['prompts_sha256']
    print(f'{count}题输出校验通过：BF16、数据SHA、固定模型版本及概率有效。')

if __name__=='__main__':validate(Path(sys.argv[1]),sys.argv[2],sys.argv[3],int(sys.argv[4]))
