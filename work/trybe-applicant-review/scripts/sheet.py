import os
from PIL import Image, ImageDraw
S=os.path.dirname(os.path.abspath(__file__)); V=S+'/vid'
rows=[]
for line in open(S+'/apps.tsv'):
    p=(line.rstrip('\n').split('\t')+['']*6)[:6]
    if p[2] in ('AT','LV','PK') or not p[5]: continue
    fr=[f'{V}/{p[0]}_{j}_{t}.jpg' for j in range(2) for t in (1,6,12)]
    rows.append((p[0]+' '+p[1],fr))
W,H=150,267; per=6
for k in range(0,len(rows),per):
    chunk=rows[k:k+per]
    img=Image.new('RGB',(160+6*W,len(chunk)*H),'white'); d=ImageDraw.Draw(img)
    for r,(name,fr) in enumerate(chunk):
        d.text((5,r*H+10),name,fill='black')
        for c,f in enumerate(fr):
            if os.path.exists(f) and os.path.getsize(f)>0:
                im=Image.open(f); im.thumbnail((W-4,H-4)); img.paste(im,(160+c*W,r*H))
    img.save(f'{S}/sheet_{k//per:02d}.jpg',quality=70)
print(len(rows))
