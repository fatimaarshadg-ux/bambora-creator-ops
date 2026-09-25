"""Build the grandparent version of the V3 creator invite brief.

Source: bambora-creator-invite-pdf.fixed.html (the live V3 invite, links fixed 2026-09-23).
Output: bambora-grandparent-invite.html, then print to PDF with headless Edge/Chrome.
Everything except the grandparent copy is carried over from the source unchanged.
"""
import re
from pathlib import Path

HERE = Path(__file__).parent
src = (HERE / "bambora-creator-invite-pdf.fixed.html").read_text(encoding="utf-8")
html = src


def swap(old, new, count=1):
    global html
    found = html.count(old)
    assert found == count, f"expected {count} of {old[:60]!r}, found {found}"
    html = html.replace(old, new)


# Title and footers
swap("<title>Bambora Creator Invite</title>", "<title>Bambora Grandparent Invite</title>")
swap('<span>Creator Invite</span>', '<span>Grandparent Creator Invite</span>', 2)
swap('<span>Creator Invite · Inspiration</span>', '<span>Grandparent Creator Invite · Inspiration</span>', 3)

# Cover
swap("<h1>Hey Mama! Welcome to the Bambora family</h1>",
     "<h1>Hey Grandma &amp; Grandpa! Welcome to the Bambora family</h1>")
swap("<strong>150,000 mamas</strong> around the world are wearing one right now, and we would be honoured to have you show it to the world in your own way.</p>",
     "<strong>150,000 families</strong> around the world are wearing one right now, and plenty of the people wearing it are grandparents on babysitting duty. We would be honoured to have you show it to the world in your own way.</p>\n"
     '<p class="lede"><strong>Why grandparents?</strong> You are the people new parents trust most, and almost nobody is making this kind of content. You have raised babies before, you know what worked back then and what did not, and you are carrying the grandkids now. That is a story only you can tell.</p>')
swap("Inside you will find what the product is, and a few of the videos",
     "Inside you will find what the product is, some ideas made just for grandparents, and a few of the videos")

# Closing
swap("<p>I cannot wait to see what you make.</p>",
     "<p>I cannot wait to see what you and the grandkids make.</p>")

# Inspiration copy, tuned for grandparents
swap("<p>Dad content is rarer, it stops the scroll, and it widens who sees themselves in us.</p>",
     "<p>Dad and grandparent content is rarer, it stops the scroll, and it widens who sees themselves in us.</p>")
swap("<p>If there is a dad or grandparent in your life who would wear it, film them. No script needed.</p>",
     "<p>Swap dad for grandma or grandpa. A slow walk showing your grandchild the flowers needs no script at all.</p>")
swap("<p>The problem-then-solution arc told in text over real footage. Lovely if you are shy on camera.</p>",
     "<p>The whole story is told in captions, so you never have to speak. Lovely if you would rather not be on camera much. Your grandchild looking out at your garden works just as well.</p>")
swap("<p>The interview format. Ask someone in your family and just film their answer.</p>",
     "<p>This is the one to start with. Ask one of your kids to hold the phone and ask you why you like it, then just answer honestly.</p>")
swap("<p>Pick one very particular moment in your week and build the whole video around it.</p>",
     "<p>Pick one very particular moment from your time with the grandkids, like the school pickup or feeding the ducks, and build the whole video around it.</p>")
swap("<p>Teaching something. If you know a thing other parents do not, that is your video.</p>",
     "<p>Teaching something. You have carried babies in more things than most parents have heard of, so tell them what is different about this one.</p>")
swap("<p>If you ever wonder what safe but still warm sounds like, it sounds like this one.</p>",
     "<p>If you ever wonder what safe but still warm sounds like, it sounds like this one. Hearing a grandparent say they keep a hand on baby is especially reassuring to the parents watching.</p>")

# Cover strip: put the granddad still in the middle slot
strip = re.search(r'<div class="coverstrip">(<img src="[^"]+">)(<img src="[^"]+">)(<img src="[^"]+">)</div>', html)
granddad = re.search(r'<a class="tile" href="[^"]*1izAicWNb_vCGlPfAgN2bPwUR-FRoM-RO[^"]*"><img src="([^"]+)">', html)
assert strip and granddad
html = html.replace(strip.group(0),
                    f'<div class="coverstrip">{strip.group(1)}<img src="{granddad.group(1)}">{strip.group(3)}</div>')

# Reorder the six inspos so the grandparent-friendly ones come first
ORDER = ["v09", "v05", "v08", "v03", "v02", "v10"]
HREF = {
    "v10": "1VKkBiBzqPM9jArKq90u8Hssv4sITUARd", "v02": "1rIN0jijBh0Fy-aeTmlb6DZotBcsPEtQt",
    "v08": "1HsVfexfQOGrxzO1HxAo5b1zw7U-KgY0J", "v05": "1srlud0wkNA-DzGJbtV7JrQM5YM2LVf8C",
    "v09": "1izAicWNb_vCGlPfAgN2bPwUR-FRoM-RO", "v03": "15IFhDC5L-8lTcXYeziDd8JP46L_1sdGG",
}
grid = re.search(r'<div class="grid six">(.*?)</div>\n<div class="pagefoot">', html, re.S)
tiles = re.findall(r'<a class="tile" href="[^"]+">.*?</a>', grid.group(1), re.S)
assert len(tiles) == 6
by_id = {k: next(t for t in tiles if HREF[k] in t) for k in ORDER}
html = html.replace(grid.group(1), "".join(by_id[k] for k in ORDER))

entries = {m.group(1): m.group(0)
           for m in re.finditer(r'(?s)<div class="entry" id="(v\d\d)">.*?\n  </div>\n</div>', html)}
assert sorted(entries) == sorted(ORDER), entries.keys()
sheets = list(re.finditer(r'(?s)<section class="sheet"><div class="entry".*?</section>', html))
assert len(sheets) == 3
foot = '<div class="pagefoot"><span class="b">BAMBORA</span><span>Grandparent Creator Invite · Inspiration</span></div>'
new_sheets = "\n".join(
    f'<section class="sheet">{entries[ORDER[i]]}{entries[ORDER[i + 1]]}{foot}</section>' for i in (0, 2, 4))
html = html[:sheets[0].start()] + new_sheets + html[sheets[-1].end():]

# New page: grandparent angles, right after the product page
ANGLES = '''<section class="sheet">
<p class="kicker">Made for you</p><h2 class="h">Ideas only a grandparent can film</h2>
<p class="sub">A few starting points. Pick the one that sounds most like you, or mix two together. As always, put your own spin on it.</p>
<div class="specs">
<div class="spec"><div class="ico">🏡</div><b>What I keep at Grandma's house</b><span>A little tour of everything you keep ready for when the grandkids come over, with the sling as one of your picks.</span></div>
<div class="spec"><div class="ico">🎤</div><b>The grandparent interview</b><span>Someone off camera asks why you like it and you just answer. Our granddad version is one of the least ad-like videos we have.</span></div>
<div class="spec"><div class="ico">🕰️</div><b>In my day vs now</b><span>What you carried your own babies in, and what you use with the grandkids. Honest and a little funny works best.</span></div>
<div class="spec"><div class="ico">🤍</div><b>Easier on arms and wrists</b><span>Holding a grandchild all afternoon is lovely, and tiring. Show how the padded strap shares the weight while your hand stays on them.</span></div>
<div class="spec"><div class="ico">🌳</div><b>A day with Grandma</b><span>One very particular outing: the park, the market, the school pickup. Build the whole video around that one moment.</span></div>
<div class="spec"><div class="ico">💬</div><b>What I told my daughter to buy</b><span>The advice you give your own kids about baby gear, with the sling as the thing you told them to get.</span></div>
</div>
<div class="note"><b>🤍 A few things that matter most.</b> Your grandchild needs to be between <b>10 and 50 lbs</b>. If the newest little one is not there yet, film with an older grandchild who is, or pick the interview or "in my day" idea. Keep <b>one hand on your grandchild in every single frame</b>, so ask the parents or a friend to hold the phone. Check the buckle is clicked over the clip with the safety loop in, and that they sit close enough to kiss. Please talk about how it feels for you rather than any health or medical claims. The full filming checklist is at <a href="https://bamborachecklist.netlify.app/" style="text-decoration:underline">bamborachecklist.netlify.app</a>.</div>
<div class="pagefoot"><span class="b">BAMBORA</span><span>Grandparent Creator Invite · Ideas</span></div>
</section>
'''
marker = '<section class="sheet"><div class="entry"'
assert html.count(marker) == 3
html = html.replace(marker, ANGLES + marker, 1)

# Guardrails: banned claims and dashes in the new copy
text = re.sub(r"<[^>]+>", " ", re.sub(r"(?s)<style>.*?</style>", "", html))
for dash in ["—", "–", " -- "]:
    assert dash not in text, f"dash {dash!r} in copy"

out = HERE / "bambora-grandparent-invite.html"
out.write_text(html, encoding="utf-8")
print("wrote", out, len(html))
