import json, os, wave, numpy as np
S=os.path.dirname(os.path.abspath(__file__)); T=S+'/top'
YAP=set('77a51f79 f556156c 9a6e2ff5 efe9f7f6 8ae9bb0e ef5d0847 344cc8e1 a665b0f2 3aa7d872 ca349dd0 1d722c3b 623fe23a bb6cdf87 f44d3c9b 62f623a0 9f09d43f 25f526ff 91d6c50c 5e8ebf86 97076578 f67081e8 e4431696 7304f087 6c916aab e191db96 9e66828a d75b70c3 b2544736 3dc7f374 d76f585a'.split())
def metrics(w, words, speech):
    wf=wave.open(w); x=np.frombuffer(wf.readframes(wf.getnframes()),dtype=np.int16).astype(float)/32768
    fr=400; n=len(x)//fr; e=np.array([np.sqrt(np.mean(x[i*fr:(i+1)*fr]**2))+1e-6 for i in range(n)]); db=20*np.log10(e)
    v=db>np.percentile(db,40); pit=[]
    for i in np.where(v)[0][::3]:
        seg=x[i*fr:(i+1)*fr]*np.hanning(fr); ac=np.correlate(seg,seg,'full')[fr-1:]; lo,hi=40,200; k=lo+np.argmax(ac[lo:hi])
        if ac[k]>0.3*ac[0]: pit.append(16000/k)
    first=np.argmax(db>np.percentile(db,60))*fr/16000
    return dict(wps=words/max(speech,1), loud=float(np.std(db[v])), pitch=float(np.std(pit)) if len(pit)>5 else 0, cover=speech/25, first=first)
rows=[]
for fn in ('top.jsonl','recent.jsonl'):
    for l in open(T+'/'+fn):
        r=json.loads(l)
        if r.get('key') in YAP and r.get('words') and os.path.exists(f"{T}/{r['key']}.wav"):
            rows.append(dict(creator=r['creator'],key=r['key'],**metrics(f"{T}/{r['key']}.wav",r['words'],r['speech'])))
seen=set(); rows=[r for r in rows if not (r['key'] in seen or seen.add(r['key']))]
A=lambda k:np.array([r[k] for r in rows])
print('n',len(rows))
for k in ('wps','loud','pitch','cover','first'):
    a=A(k); print(f"{k:6} p10={np.percentile(a,10):.2f} p25={np.percentile(a,25):.2f} median={np.median(a):.2f} p75={np.percentile(a,75):.2f}")
json.dump(rows,open(S+'/taste_rows.json','w'),indent=1)
