import os,re,glob
D=os.path.dirname(os.path.abspath(__file__))+'/tt'
spam=re.compile(r'(follow|f4f|check my|dm me|promo|link in bio|http)',re.I)
for f in sorted(glob.glob(D+'/*.txt')):
    h=os.path.basename(f)[:-4]; txt=open(f).read()
    if 'NO VIDEOS' in txt or not txt.strip(): print(f'{h:28} NO DATA {txt[:80]!r}'); continue
    vids=txt.split('\n## ')[1:]; per=[]
    for v in vids:
        m=re.search(r'views=(\S+) likes=(\S+) comments=(\S+)',v)
        real=0
        for line in v.split('\n')[1:]:
            mm=re.match(r'\s+- (\S+): (.*)',line)
            if not mm: continue
            u,t=mm.groups()
            if u==h or spam.search(t): continue
            if len(re.findall(r'[A-Za-z]{2,}',t))>=2: real+=1
        per.append(f"{m.group(1)}v/{m.group(3)}c/{real}r" if m else '?')
    avg=sum(int(p.split('/')[2][:-1]) for p in per if p!='?')/max(len(per),1)
    print(f'{h:28} avgReal={avg:.1f}  '+'  '.join(per))
