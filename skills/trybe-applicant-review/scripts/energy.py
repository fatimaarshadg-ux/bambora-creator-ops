import json, os, wave, numpy as np
S=os.path.dirname(os.path.abspath(__file__))
out={}
for l in open(S+'/yap.jsonl'):
    r=json.loads(l); w=f"{S}/vid/{r['key']}.wav"
    if r.get('err') or not r.get('words') or not os.path.exists(w): continue
    wf=wave.open(w); x=np.frombuffer(wf.readframes(wf.getnframes()),dtype=np.int16).astype(float)/32768
    fr=400; n=len(x)//fr; e=np.array([np.sqrt(np.mean(x[i*fr:(i+1)*fr]**2))+1e-6 for i in range(n)])
    db=20*np.log10(e); voiced=db>np.percentile(db,40)
    # pitch via autocorrelation on voiced 40ms frames
    pit=[]
    for i in np.where(voiced)[0][::3]:
        seg=x[i*fr:(i+1)*fr]*np.hanning(fr); ac=np.correlate(seg,seg,'full')[fr-1:]
        lo,hi=16000//400,16000//80; k=lo+np.argmax(ac[lo:hi])
        if ac[k]>0.3*ac[0]: pit.append(16000/k)
    wps=r['words']/max(r['speech'],1)
    out.setdefault(r['name'],[]).append(dict(wps=round(wps,2),loud_sd=round(float(np.std(db[voiced])),1),pitch_sd=round(float(np.std(pit)) if len(pit)>5 else 0,0),speech=r['speech']))
for k,v in out.items():
    print(k[:22].ljust(22), ' | '.join(f"wps {a['wps']} loud {a['loud_sd']} pitch {a['pitch_sd']:.0f} sp {a['speech']}" for a in v))
