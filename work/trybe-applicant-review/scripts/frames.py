import subprocess, os, json
S=os.path.dirname(os.path.abspath(__file__)); V=S+'/vid'
for line in open(S+'/apps.tsv'):
    p=(line.rstrip('\n').split('\t')+['']*6)[:6]
    if p[2] in ('AT','LV','PK'): continue
    for j,v in enumerate(p[5].split()[:2]):
        key=f'{p[0]}_{j}'
        for t in (1,6,12):
            f=f'{V}/{key}_{t}.jpg'
            if os.path.exists(f) and os.path.getsize(f)>0: continue
            subprocess.run(['ffmpeg','-y','-loglevel','error','-ss',str(t),'-i','https://cdn.jointrybe.com/creators/'+v,'-frames:v','1','-vf','scale=240:-2,format=yuvj420p','-strict','unofficial',f],timeout=180)
print('frames done')
