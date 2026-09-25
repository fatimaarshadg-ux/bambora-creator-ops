import subprocess, json, os, sys
from faster_whisper import WhisperModel
S=os.path.dirname(os.path.abspath(__file__)); V=S+'/vid'
model=WhisperModel('small', device='cpu', compute_type='int8')
out=open(S+'/yap.jsonl','a')
done={json.loads(l)['key'] for l in open(S+'/yap.jsonl')} if os.path.getsize(S+'/yap.jsonl') else set()
for line in open(S+'/apps.tsv'):
    p=(line.rstrip('\n').split('\t')+['']*6)[:6]
    idx,name,country=p[0],p[1],p[2]
    if country in ('AT','LV','PK'): continue
    vids=p[5].split() if len(p)>5 and p[5] else []
    for j,v in enumerate(vids[:3]):
        key=f'{idx}_{j}'
        if key in done: continue
        url='https://cdn.jointrybe.com/creators/'+v
        wav=f'{V}/{key}.wav'
        r={'key':key,'idx':int(idx),'name':name}
        try:
            subprocess.run(['ffmpeg','-y','-loglevel','error','-t','25','-i',url,'-vn','-ac','1','-ar','16000',wav],timeout=120,check=True)
            for t in (1,6,12):
                subprocess.run(['ffmpeg','-y','-loglevel','error','-ss',str(t),'-i',url,'-frames:v','1','-vf','scale=240:-2,format=yuvj420p','-strict','unofficial',f'{V}/{key}_{t}.jpg'],timeout=90)
            segs,info=model.transcribe(wav,beam_size=1,vad_filter=True)
            segs=list(segs)
            txt=' '.join(s.text.strip() for s in segs)
            r.update(lang=info.language,lp=round(info.language_probability,2),speech=round(sum(s.end-s.start for s in segs),1),words=len(txt.split()),text=txt[:400])
        except Exception as e:
            r['err']=str(e)[:200]
        out.write(json.dumps(r)+'\n'); out.flush()
print('DONE')
