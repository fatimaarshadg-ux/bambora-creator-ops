const pptxgen = require("pptxgenjs");

const INK = "1A1A1A";
const CARD_DARK = "262626";
const GRAY = "6B6B6B";
const GRAY_ON_DARK = "A8A8A8";
const TINT = "F3F4F2";
const GREEN = "2F5D50";
const GREEN_ON_DARK = "8FBFAE";
const WHITE = "FFFFFF";
const HEAD = "Arial";
const BODY = "Calibri";

const pres = new pptxgen();
pres.layout = "LAYOUT_16x9";
pres.title = "Updates & Next Steps";

function text(slide, str, opts) {
  slide.addText(str, Object.assign({ isTextBox: true, margin: 0, fontFace: BODY, valign: "top" }, opts));
}

// 1. Title
{
  const s = pres.addSlide();
  s.background = { color: INK };
  s.addShape(pres.shapes.OVAL, { x: 0.6, y: 0.6, w: 0.22, h: 0.22, fill: { color: GREEN_ON_DARK }, line: { color: GREEN_ON_DARK, width: 0 } });
  text(s, "Creative Engine", { x: 0.95, y: 0.58, w: 5, h: 0.28, fontSize: 12, color: GRAY_ON_DARK, charSpacing: 2, valign: "middle" });
  text(s, "Updates &\nNext Steps", { x: 0.6, y: 1.7, w: 8.5, h: 2.1, fontFace: HEAD, fontSize: 54, bold: true, color: WHITE });
  text(s, "Fatima  ·  September 2026", { x: 0.6, y: 4.7, w: 6, h: 0.3, fontSize: 13, color: GRAY_ON_DARK });
}

// 2. Updates: title left, numbered rows right
{
  const s = pres.addSlide();
  s.background = { color: WHITE };
  text(s, "Updates", { x: 0.6, y: 0.6, w: 3, h: 0.7, fontFace: HEAD, fontSize: 38, bold: true, color: INK });
  text(s, "What got done", { x: 0.6, y: 1.35, w: 3, h: 0.3, fontSize: 13, color: GRAY });

  const rows = [
    ["Creative engine workspace", "Built the Notion workspace for the creative engine."],
    ["Ad account audit", "Watched all of our existing ads to learn what's working, what isn't, and how our customers talk."],
    ["Team alignment", "Internal creative strategy with Isla. Creator outreach strategy with Yelly."],
    ["Trybe strategy", "New creator brief, a safety guidelines checklist, and inspo."],
    ["Miscellaneous", "Team comms, Shopify website builder skills for Liam, and automating part of Yelly's reporting."],
  ];
  const x0 = 3.9, y0 = 0.62, rowH = 0.9;
  rows.forEach((r, i) => {
    const y = y0 + i * rowH;
    text(s, "0" + (i + 1), { x: x0, y: y, w: 0.6, h: 0.35, fontFace: HEAD, fontSize: 16, bold: true, color: GREEN });
    text(s, r[0], { x: x0 + 0.7, y: y, w: 4.8, h: 0.3, fontSize: 16, bold: true, color: INK });
    text(s, r[1], { x: x0 + 0.7, y: y + 0.31, w: 4.8, h: 0.5, fontSize: 12.5, color: GRAY });
  });
}

// Trybe strategy A: commission tiers + the ten staying on 12%
{
  const s = pres.addSlide();
  s.background = { color: WHITE };
  text(s, "Trybe strategy", { x: 0.6, y: 0.6, w: 4, h: 0.7, fontFace: HEAD, fontSize: 34, bold: true, color: INK });
  text(s, "Who stays on which commission", { x: 0.6, y: 1.3, w: 4, h: 0.3, fontSize: 13, color: GRAY });

  const tiers = [
    ["12%", "Only 10 creators stay here: our top 10 non-sale ads creators."],
    ["5%", "Everyone else moves to the 5% program."],
    ["Out", "Creators who haven't agreed to 5% get dropped, and we move on to new creators."],
  ];
  tiers.forEach((t, i) => {
    const y = 2.05 + i * 0.95;
    text(s, t[0], { x: 0.6, y, w: 1.1, h: 0.6, fontFace: HEAD, fontSize: 26, bold: true, color: GREEN });
    text(s, t[1], { x: 1.75, y: y + 0.04, w: 2.75, h: 0.75, fontSize: 12.5, color: INK });
  });

  const top = [
    ["Cambria Reau", "$15,670", "0.96"], ["Tayler Raza", "$3,863", "0.82"], ["Mary Saggau", "$3,640", "1.02"],
    ["Sophia Lease", "$3,040", "1.10"], ["Myrka Bustillo", "$2,450", "0.98"], ["Ciara Burnett", "$2,376", "1.06"],
    ["Carissa Lyman", "$2,250", "0.72"], ["Cassie Avery Charvat", "$2,010", "1.17"], ["Tasha Clay", "$1,920", "1.20"],
    ["Lilly Clark", "$1,861", "0.81"],
  ];
  const tx = 5.0, tw = 4.4;
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: tx, y: 0.6, w: tw, h: 4.45, rectRadius: 0.08, fill: { color: TINT }, line: { color: TINT, width: 0 } });
  text(s, "The 10 staying on 12%", { x: tx + 0.25, y: 0.78, w: tw - 0.5, h: 0.3, fontSize: 14, bold: true, color: INK });
  const hdr = (t, align) => ({ text: t, options: { bold: true, color: GRAY, fontSize: 9.5, fontFace: BODY, align: align || "left" } });
  const cell = (t, align, bold) => ({ text: t, options: { color: INK, fontSize: 11, fontFace: BODY, align: align || "left", bold: !!bold } });
  const rowsT = [[hdr("#"), hdr("Creator"), hdr("Trybe sales", "right"), hdr("Sales per $1", "right")]];
  top.forEach((r, i) => rowsT.push([{ text: String(i + 1), options: { color: GREEN, bold: true, fontSize: 11, fontFace: HEAD } }, cell(r[0]), cell(r[1], "right"), cell(r[2], "right")]));
  s.addTable(rowsT, { x: tx + 0.25, y: 1.18, colW: [0.4, 1.8, 0.8, 0.9], rowH: 0.31, margin: 0, valign: "middle", border: { type: "none" } });
  text(s, "Non-sale ads, Trybe attribution only.", { x: tx + 0.25, y: 4.68, w: tw - 0.5, h: 0.25, fontSize: 10, italic: true, color: GRAY });
}

// Trybe strategy B: who goes where
{
  const s = pres.addSlide();
  s.background = { color: WHITE };
  text(s, "Who goes where", { x: 0.6, y: 0.6, w: 8, h: 0.7, fontFace: HEAD, fontSize: 34, bold: true, color: INK });
  text(s, "We work both channels, and spend the time where the leverage is", { x: 0.6, y: 1.3, w: 8.8, h: 0.3, fontSize: 13, color: GRAY });

  const cols = [
    ["Trybe", "Creators with TikTok Shop experience, plus IG creators with good yapper content."],
    ["Social Snowball", "Everyone else gets our Social Snowball link. Ties back to the strategy Histrips is following."],
  ];
  const gap = 0.25, w = (10 - 1.2 - gap) / 2, y = 1.9, h = 1.25;
  cols.forEach((c, i) => {
    const x = 0.6 + i * (w + gap);
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, rectRadius: 0.08, fill: { color: TINT }, line: { color: TINT, width: 0 } });
    text(s, c[0], { x: x + 0.25, y: y + 0.2, w: w - 0.5, h: 0.3, fontSize: 16, bold: true, color: GREEN });
    text(s, c[1], { x: x + 0.25, y: y + 0.56, w: w - 0.5, h: 0.6, fontSize: 12, color: INK });
  });

  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 0.6, y: 3.4, w: 8.8, h: 0.8, rectRadius: 0.08, fill: { color: INK }, line: { color: INK, width: 0 } });
  text(s, [
    { text: "Both get  ", options: { bold: true, color: GREEN_ON_DARK } },
    { text: "our training material and top performing angles. There's potential to train them into good retainer-based creators eventually.", options: { color: WHITE } },
  ], { x: 0.85, y: 3.4, w: 8.3, h: 0.8, fontSize: 12.5, valign: "middle" });

  text(s, [
    { text: "Efficiency rule: ", options: { bold: true, color: INK } },
    { text: "the bulk of our time goes to high GMV, high potential creators on Trybe. Everyone else gets something automated, like the weekly inspo on the inspo site.", options: { color: GRAY } },
  ], { x: 0.6, y: 4.42, w: 8.8, h: 0.6, fontSize: 12.5 });
}

// 3. Weekly cadence: five cards
{
  const s = pres.addSlide();
  s.background = { color: WHITE };
  text(s, "Weekly cadence", { x: 0.6, y: 0.6, w: 7, h: 0.7, fontFace: HEAD, fontSize: 38, bold: true, color: INK });
  text(s, "The loop that runs every week", { x: 0.6, y: 1.35, w: 7, h: 0.3, fontSize: 13, color: GRAY });

  const cards = [
    ["Grow the inspo site", "Add more inspo to our inspo site."],
    ["Personalize outreach", "Message each creator with the inspo relevant to them, not one size fits all."],
    ["Give feedback", "Respond to what creators delivered."],
    ["File approved work", "Upload approved files to the drive with the correct naming convention."],
    ["Sort creators", "With Yelly, keep a healthy number of Social Snowball creators in the mix."],
  ];
  const gap = 0.2, w = (10 - 1.2 - gap * 4) / 5, y = 2.0, h = 2.45;
  cards.forEach((c, i) => {
    const x = 0.6 + i * (w + gap);
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, rectRadius: 0.08, fill: { color: TINT }, line: { color: TINT, width: 0 } });
    text(s, "0" + (i + 1), { x: x + 0.18, y: y + 0.2, w: w - 0.36, h: 0.35, fontFace: HEAD, fontSize: 16, bold: true, color: GREEN });
    text(s, c[0], { x: x + 0.18, y: y + 0.68, w: w - 0.36, h: 0.55, fontSize: 14, bold: true, color: INK });
    text(s, c[1], { x: x + 0.18, y: y + 1.25, w: w - 0.36, h: 1.1, fontSize: 11.5, color: GRAY });
  });
  text(s, "05 ties back to the SC strategy of diversifying channels.", { x: 0.6, y: 4.75, w: 8.8, h: 0.3, fontSize: 12, italic: true, color: GRAY });
}

// Next steps: numbered rows left, Cassie's message right
{
  const s = pres.addSlide();
  s.background = { color: WHITE };
  text(s, "Next steps", { x: 0.6, y: 0.6, w: 4.5, h: 0.7, fontFace: HEAD, fontSize: 34, bold: true, color: INK });
  text(s, "Last week was foundations. This week:", { x: 0.6, y: 1.3, w: 4.5, h: 0.3, fontSize: 13, color: GRAY });

  const steps = [
    ["Invite more creators to Trybe", ""],
    ["More 1:1s with high potential creators", "Encouraging them to do 20 to 30 videos a month."],
    ["Help Cassie hit that volume", "She has agreed, so the bulk of my time now goes to helping her fulfil it."],
  ];
  let y = 2.0;
  steps.forEach((st, i) => {
    text(s, "0" + (i + 1), { x: 0.6, y, w: 0.6, h: 0.35, fontFace: HEAD, fontSize: 16, bold: true, color: GREEN });
    text(s, st[0], { x: 1.25, y, w: 3.5, h: 0.3, fontSize: 15, bold: true, color: INK });
    if (st[1]) text(s, st[1], { x: 1.25, y: y + 0.32, w: 3.5, h: 0.55, fontSize: 12, color: GRAY });
    y += st[1] ? 1.05 : 0.65;
  });

  // Cassie's actual Trybe DM, 635x362 crop of the screenshot
  const qx = 5.2, qw = 4.05, qh = qw * 362 / 635;
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: qx - 0.15, y: 1.2, w: qw + 0.3, h: qh + 0.75, rectRadius: 0.08, fill: { color: TINT }, line: { color: TINT, width: 0 } });
  s.addImage({ path: "cassie-crop.png", x: qx, y: 1.35, w: qw, h: qh, altText: "Screenshot of Cassie Avery Charvat's Trybe DM agreeing to post more videos" });
  text(s, "Cassie's reply on Trybe", { x: qx, y: 1.35 + qh + 0.12, w: qw, h: 0.3, fontSize: 11, bold: true, color: GRAY });
}

// 4. Open to discussion: dark, 2x2
{
  const s = pres.addSlide();
  s.background = { color: INK };
  text(s, "Open to discussion", { x: 0.6, y: 0.6, w: 8, h: 0.7, fontFace: HEAD, fontSize: 38, bold: true, color: WHITE });

  const items = [
    ["Recharm", "Connect all of our internal footage. Only 590 clips are in there today."],
    ["Influee", "Set it up for more internal b-roll. Trybe's brand guidelines don't let us use commissioned creators' footage internally without paying commission wherever it runs."],
    ["Isla's side", "Any updates from Isla."],
    ["Your comments", "Anything on the updates or the weekly cadence."],
  ];
  const gap = 0.25, w = (10 - 1.2 - gap) / 2, h = 1.55, x0 = 0.6, y0 = 1.65;
  items.forEach((it, i) => {
    const x = x0 + (i % 2) * (w + gap);
    const y = y0 + Math.floor(i / 2) * (h + gap);
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, rectRadius: 0.08, fill: { color: CARD_DARK }, line: { color: CARD_DARK, width: 0 } });
    text(s, "0" + (i + 1), { x: x + 0.25, y: y + 0.22, w: 0.5, h: 0.3, fontFace: HEAD, fontSize: 14, bold: true, color: GREEN_ON_DARK });
    text(s, it[0], { x: x + 0.8, y: y + 0.2, w: w - 1.05, h: 0.32, fontSize: 16, bold: true, color: WHITE });
    text(s, it[1], { x: x + 0.8, y: y + 0.58, w: w - 1.05, h: 0.85, fontSize: 12, color: GRAY_ON_DARK });
  });
}

pres.writeFile({ fileName: "Updates-and-Next-Steps.pptx" }).then(f => console.log("wrote", f));
