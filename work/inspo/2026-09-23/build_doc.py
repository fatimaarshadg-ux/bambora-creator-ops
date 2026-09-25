import html,os
E=html.escape
det={l.split('\t')[0]:l.rstrip('\n').split('\t') for l in open('details.tsv')}
ids=dict(l.split() for l in open('driveids.txt'))
why=dict(l.rstrip('\n').split('|',1) for l in open('why.txt'))
star={'F11','F43','F42','F31','F67','F30','F54','F19','F88','F95','F84','T29','T32','T28','F89','T23','F14','F37'}
seen=[]
o=['<html><body>','<h1>Inspo links, Week of 2026-09-23</h1>',
'<p>Folder: <a href="https://drive.google.com/drive/folders/1s3Sfr56gxT-vNfFDyAc07ByDz5XZ6uOM">Bambora Inspo / Week of 2026-09-23</a>. First run, so Atria followed brands use lifetime top ads and Atria trending uses the last 14 days. Every item shows real people. ⭐ = also saved to the Atria board "Bambora Creator Inspo" (my picks, not yours). Tell me which ones you like and I will learn your taste from it.</p>']
def sec(t): o.append(f'<h2>{E(t)}</h2><ol>')
sec('Atria: top ads from followed brands (F) and trending (T), downloaded to Drive')
for l in open('order.txt'):
    nn,c,b,h=l.rstrip('\n').split('|')
    d=det[c]; nid=d[4]
    rank=d[6]; days=d[5]
    src='Followed brand, lifetime top ad' if c[0]=='F' else 'Atria trending, last 14 days'
    meta=f'https://www.facebook.com/ads/library/?id={nid}'
    s='⭐ ' if c in star else ''
    o.append(f'<li>{s}<b>{E(nn)} {E(d[2])}</b>: "{E(h)}". {src}; impression rank {E(rank or "n/a")} in its brand; running {E(days)} days. '
             f'<a href="https://drive.google.com/file/d/{ids[nn]}/view">Drive video</a> | <a href="{meta}">Meta Ad Library</a>. <i>{E(why[nn])}</i></li>')
    seen.append(d[1]); seen.append(meta)
o.append('</ol>')
sec('YouTube Shorts (links)')
for l in open('ytpicks.txt'):
    vid,ch,v,t,w=l.rstrip('\n').split('|')
    u=f'https://www.youtube.com/shorts/{vid}'
    o.append(f'<li><b>{E(ch)}</b>: "{E(t)}", {E(v)} views. <a href="{u}">{u}</a>. <i>{E(w)}</i></li>'); seen.append(u)
o.append('</ol>')
def rows(f,minv):
    if not os.path.exists(f): return []
    r=[l.rstrip('\n').split('\t') for l in open(f) if l.strip()]
    r=[x for x in r if len(x)>=5 and x[0].isdigit() and int(x[0])>=minv]
    seen_u=set(); out=[]
    for x in sorted(r,key=lambda x:-int(x[0])):
        if x[4] in seen_u: continue
        seen_u.add(x[4]); out.append(x)
    return out
def fmt(n):
    n=int(n); return f'{n/1e6:.1f}M' if n>=1e6 else f'{n/1e3:.0f}K'
sec('TikTok Shop (affiliate style: mom films the product and it sells)')
for x in rows('ttshop.tsv',20000):
    o.append(f'<li><b>@{E(x[3])}</b>: {fmt(x[0])} views, {fmt(x[1])} likes. <a href="{x[4]}">{x[4]}</a>. "{E(x[5][:100])}"</li>'); seen.append(x[4])
o.append('</ol>')
sec('TikTok (popular mom videos)')
for x in rows('tt.tsv',70000):
    o.append(f'<li><b>@{E(x[3])}</b>: {fmt(x[0])} views, {fmt(x[1])} likes. <a href="{x[4]}">{x[4]}</a>. "{E(x[5][:100])}"</li>'); seen.append(x[4])
o.append('</ol>')
sec('Instagram Reels (likes, since IG hides views)')
for x in rows('ig.tsv',30000):
    o.append(f'<li><b>{E(x[3])}</b>: {fmt(x[0])} likes, {E(x[1])} comments. <a href="{x[4]}">{x[4]}</a>. "{E(x[5][:100])}"</li>'); seen.append(x[4])
o.append('</ol>')
o.append('<h2>What stood out</h2><ul>'
'<li>Grandparent carrier ads (Nivaro, Lullahug) are top performers. A grandma or grandpa creator angle is open for Bambora.</li>'
'<li>Comment reply videos (Root\'d, EllaOla) and podcast style "rate it out of 10" (Cosmetic Times, Spotminders) are easy formats for creators to copy.</li>'
'<li>Storytime car selfies ("I ran into my ex\'s new wife at Target") hold attention before the product shows up.</li>'
'<li>Babywearing tutorials on YouTube have 70M+ views. A "how to put on the Bambora sling in 20 seconds" video is worth briefing.</li>'
'<li>Routine vlogs with a paid partner (Sunkissed Mama x Chomps) show how to fit a sling into a day in the life.</li></ul>')
o.append('</body></html>')
open('doc.html','w').write('\n'.join(o))
open('seen_add.txt','w').write('\n'.join(seen)+'\n')
t='\n'.join(o)
for bad in ['\u2014','\u2013',' \x2d ']:
    if bad in t: print('DASH FOUND',repr(bad), t[t.index(bad)-60:t.index(bad)+20])
print(len(seen),'items')
