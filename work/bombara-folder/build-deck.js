const pptxgen = require('pptxgenjs');
const pres = new pptxgen();
pres.layout = 'LAYOUT_16x9';           // 10 x 5.625 in
pres.title  = 'Bambora Creator Partnership Strategy';

// ---- Bambora palette (sampled from bamboraco.com) ----
const INK='2E2A39', DEEP='343D52', PANEL='3E4860', BLUE='B7CCDF', BLUE_DK='4E6B88',
      TINT='EEF3F8', WHITE='FFFFFF', SOFT='5A5566', GREY='7A7684', GREY_LT='C9CDD8',
      HAIR='E4E7EC', LINE_DK='4A4657';
const H='Arial', B='Calibri';
const M=0.7, COL=[0.7,3.65,6.6], CW=2.7;

const fs=require('fs');
// Slide 3 upgrades itself to a half-bleed photo layout as soon as this file exists.
const HAUS_IMG=[require('path').join(require('os').homedir(),'Bombara','assets')+'/haus-team.jpg',
                require('path').join(require('os').homedir(),'Bombara','assets')+'/haus-team.jpeg',
                require('path').join(require('os').homedir(),'Bombara','assets')+'/haus-team.png'].find(f=>fs.existsSync(f));
// stat + label rows, used by the photo layouts on slides 3 and 5
function statRows(s,items){
  items.forEach((it,i)=>{
    const y=2.5+i*0.78;
    s.addText(it[0],{x:M,y,w:1.66,h:0.5,isTextBox:true,margin:0,valign:'middle',
      fontFace:H,fontSize:19,bold:true,color:BLUE_DK});
    s.addText(it[1],{x:2.44,y,w:2.6,h:0.5,isTextBox:true,margin:0,valign:'middle',
      fontFace:B,fontSize:12,color:SOFT,lineSpacing:15});
  });
}
const pick=(...n)=>n.map(f=>require('path').join(require('os').homedir(),'Bombara','assets')+'/'+f).find(f=>fs.existsSync(f));
const HS_IMGS=[pick('histrips-1.jpg','histrips-1.jpeg','histrips-1.png'),
               pick('histrips-2.jpg','histrips-2.jpeg','histrips-2.png')].filter(Boolean);
const UGC_IMG=pick('ugc-page.jpg','ugc-page.jpeg','ugc-page.png');
const TRYBE_IMG=pick('trybe-top-creators.jpg','trybe-top-creators.jpeg','trybe-top-creators.png');
const CHART='2F6C9E';
const S=pres.ShapeType;
const dot=(s,x,y,d,c)=>s.addShape(S.ellipse,{x,y,w:d,h:d,fill:{color:c},line:{width:0}});

function kicker(s,text,dark){
  dot(s,M,0.63,0.1,dark?BLUE:BLUE_DK);
  s.addText(text,{x:M+0.22,y:0.53,w:6,h:0.3,isTextBox:true,margin:0,valign:'middle',
    fontFace:B,fontSize:10.5,bold:true,charSpacing:2.2,color:dark?BLUE:BLUE_DK});
}
function title(s,text,dark,size=36,y=1.02,w=8.6){
  const h=text.split('\n').length*size*1.16/72+0.08;   // box hugs the text
  s.addText(text,{x:M,y,w,h,isTextBox:true,margin:0,valign:'top',
    fontFace:H,fontSize:size,bold:true,color:dark?WHITE:INK,lineSpacing:size*1.16});
  return y+h;                                           // baseline for the subtitle
}
function sub(s,text,dark,y=1.72,w=8.6){
  s.addText(text,{x:M,y,w,h:0.34,isTextBox:true,margin:0,valign:'top',
    fontFace:B,fontSize:15,color:dark?GREY_LT:GREY});
}
// three tinted stat cards
function cards(s,items){
  items.forEach((it,i)=>{
    s.addShape(S.roundRect,{x:COL[i],y:2.5,w:CW,h:2.25,rectRadius:0.09,
      fill:{color:TINT},line:{width:0}});
    s.addText(it[0],{x:COL[i]+0.26,y:2.78,w:CW-0.5,h:0.6,isTextBox:true,margin:0,valign:'middle',
      fontFace:H,fontSize:it[0].length>6?24:30,bold:true,color:BLUE_DK});
    s.addText(it[1],{x:COL[i]+0.26,y:3.45,w:CW-0.5,h:1.1,isTextBox:true,margin:0,valign:'top',
      fontFace:B,fontSize:12.5,color:SOFT,lineSpacing:17});
  });
}

/* ---------------- 1. Title ---------------- */
let s=pres.addSlide(); s.background={color:INK};
s.addShape(S.ellipse,{x:6.95,y:0.55,w:4.3,h:4.3,fill:{color:WHITE,transparency:100},
  line:{color:LINE_DK,width:1}});
dot(s,M,1.62,0.11,BLUE);
s.addText('INTERNAL · CREATOR STRATEGY',{x:M+0.24,y:1.52,w:6,h:0.3,isTextBox:true,margin:0,
  valign:'middle',fontFace:B,fontSize:11,bold:true,charSpacing:2.4,color:BLUE});
s.addText("Bambora's Creator\nPartnership Strategy",{x:M,y:2.0,w:7.4,h:1.9,isTextBox:true,margin:0,
  valign:'top',fontFace:H,fontSize:40,bold:true,color:WHITE,lineSpacing:48});
s.addText('September 2026',{x:M,y:4.62,w:4,h:0.3,isTextBox:true,margin:0,
  fontFace:B,fontSize:11,color:GREY});
s.addNotes('Framing: this is our creator partnership strategy for the next two months.');

/* ---------------- 2. Premise ---------------- */
s=pres.addSlide(); s.background={color:INK};
kicker(s,'THE PREMISE',true);
s.addShape(S.ellipse,{x:6.5,y:1.5,w:2.4,h:2.4,fill:{color:WHITE,transparency:100},line:{color:LINE_DK,width:1}});
s.addShape(S.ellipse,{x:7.6,y:1.5,w:2.4,h:2.4,fill:{color:WHITE,transparency:100},line:{color:BLUE,width:1}});
s.addText('Every brand follows a\ndifferent playbook.',{x:M,y:2.0,w:5.5,h:1.7,isTextBox:true,margin:0,
  valign:'top',fontFace:H,fontSize:34,bold:true,color:WHITE,lineSpacing:42});
s.addNotes('No universal right answer. Two examples that sit at opposite extremes.');

/* ---------------- 3. Haus ---------------- */
s=pres.addSlide();
kicker(s,'PLAYBOOK ONE',false);
if(HAUS_IMG){
  s.addImage({path:HAUS_IMG,x:5.5,y:1.5,w:3.8,h:2.85,sizing:{type:'cover',w:3.8,h:2.85},
    shadow:{type:'outer',color:'2E2A39',blur:14,offset:3,angle:90,opacity:0.20}});
  s.addText('HAUS — gohaus.com',{x:5.5,y:4.46,w:3.8,h:0.28,isTextBox:true,margin:0,
    align:'center',fontFace:B,fontSize:10.5,color:GREY});
  sub(s,'A very high barrier to entry.',false,title(s,'Haus',false,40,1.02,4.5)+0.06,4.5);
  statRows(s,[['15%','of ad spend — the commission he puts on the table.'],
              ['$2,000','retainer for every creator who made it into his Discord.'],
              ['6 months','of zero revenue, spent training instead of selling.']]);
} else {
  sub(s,'A very high barrier to entry.',false,title(s,'Haus',false,40)+0.06);
  cards(s,[
   ['15%','of ad spend — the commission he puts on the table for creators.'],
   ['$2,000','retainer paid to every single creator who made it into his Discord.'],
   ['6 months','of zero revenue, spent training creators instead of selling.']
  ]);
}
s.addNotes('High barrier, heavy upfront investment, revenue deliberately deferred.');

/* ---------------- 4. Haus philosophy ---------------- */
s=pres.addSlide(); s.background={color:DEEP};
kicker(s,'THE PHILOSOPHY',true);
s.addText("You don't hire a\ngood creator.\nYou train a\ngood creator.",{x:M,y:1.35,w:4.3,h:2.5,
  isTextBox:true,margin:0,valign:'top',fontFace:H,fontSize:25,bold:true,color:WHITE,lineSpacing:33});
s.addText("— Haus's founder",{x:M,y:3.95,w:4,h:0.3,isTextBox:true,margin:0,
  fontFace:B,fontSize:11,italic:true,color:GREY_LT});
const pts=[
 ['Potential over polish','He filtered for upside, not for skill that already existed.'],
 ['The retainer bought focus','Mortgage paid, bills paid — now they can concentrate on learning.'],
 ['Not everyone gets in','For a while he cast only jacked guys; testing skinny guys did not work out.']
];
pts.forEach((p,i)=>{
  const y=1.45+i*0.98;
  dot(s,5.4,y+0.09,0.1,BLUE);
  s.addText(p[0],{x:5.62,y,w:3.7,h:0.3,isTextBox:true,margin:0,valign:'top',
    fontFace:B,fontSize:14,bold:true,color:WHITE});
  s.addText(p[1],{x:5.62,y:y+0.32,w:3.7,h:0.58,isTextBox:true,margin:0,valign:'top',
    fontFace:B,fontSize:12,color:GREY_LT,lineSpacing:16});
});
s.addText('The trade: profit deferred for six months, creators paid out of his own pocket.',
  {x:M,y:4.6,w:8.6,h:0.35,isTextBox:true,margin:0,fontFace:B,fontSize:13,italic:true,color:BLUE});
s.addNotes('He is bullish that good creators are trained, not hired.');

/* ---------------- 5. Hi Strips ---------------- */
s=pres.addSlide();
kicker(s,'PLAYBOOK TWO',false);
if(HS_IMGS.length){
  HS_IMGS.slice(0,2).forEach((f,i)=>{
    const x=5.62+i*1.88;
    s.addImage({path:f,x,y:0.95,w:1.64,h:3.55,sizing:{type:'cover',w:1.64,h:3.55},
      shadow:{type:'outer',color:'2E2A39',blur:14,offset:3,angle:90,opacity:0.22}});
  });
  s.addText('Creators at any scale, posting anyway.',
    {x:5.62,y:4.62,w:3.52,h:0.28,isTextBox:true,margin:0,align:'center',
     fontFace:B,fontSize:11,italic:true,color:GREY});
  sub(s,'Say yes to everybody.',false,title(s,'Hi Strips',false,40,1.02,4.5)+0.06,4.5);
  statRows(s,[['Never','a retainer has been paid — not even to their best on TRYBE.'],
              ['5%','commission. That is the entire deal, top to bottom.'],
              ['Zero views','and they still get product. Entirely on purpose.']]);
} else {
  sub(s,'Say yes to everybody.',false,title(s,'Hi Strips',false,40)+0.06);
  cards(s,[
   ['Never','A retainer has never been paid to a creator. Not even their best ones on TRYBE.'],
   ['5%','Commission. That is the entire deal, top to bottom, for everyone.'],
   ['Zero views','Creators with no audience make videos for them. Entirely on purpose.']
  ]);
}
s.addNotes('They refuse nobody and pay nobody a retainer. It is working — they are a big brand.');

/* ---------------- 6. Why it works ---------------- */
s=pres.addSlide();
kicker(s,'WHY IT WORKS',false);
title(s,"It isn't about creator ROI.\nIt's about retail.",false,30,1.0,7.6);
const steps=[
 ['1','Product to everyone','Any creator, any scale, no filter — it all goes out.'],
 ['2','Volume creates demand','A constant stream of content makes the brand look like it is everywhere.'],
 ['3','Retail opens','Buyers watch what is trending. They walk into those rooms already known.']
];
steps.forEach((st,i)=>{
  s.addShape(S.ellipse,{x:COL[i],y:2.6,w:0.52,h:0.52,fill:{color:BLUE},line:{width:0}});
  s.addText(st[0],{x:COL[i],y:2.6,w:0.52,h:0.52,isTextBox:true,margin:0,align:'center',valign:'middle',
    fontFace:H,fontSize:15,bold:true,color:INK});
  s.addText(st[1],{x:COL[i],y:3.32,w:CW,h:0.32,isTextBox:true,margin:0,valign:'top',
    fontFace:B,fontSize:14,bold:true,color:INK});
  s.addText(st[2],{x:COL[i],y:3.68,w:CW,h:0.95,isTextBox:true,margin:0,valign:'top',
    fontFace:B,fontSize:12.5,color:SOFT,lineSpacing:17});
});
s.addText('The good ones graduate to TRYBE. Still no retainer.',
  {x:M,y:4.75,w:8.6,h:0.32,isTextBox:true,margin:0,fontFace:B,fontSize:12.5,italic:true,color:BLUE_DK});
s.addNotes('From the masterclass: being everywhere is what opened the retail doors.');

/* ---------------- 7. Side by side ---------------- */
s=pres.addSlide();
kicker(s,'SIDE BY SIDE',false);
sub(s,'It depends on where we are in our journey.',false,title(s,'Neither one is wrong.',false,34)+0.06);
s.addText('HAUS',{x:3.0,y:2.22,w:3.0,h:0.28,isTextBox:true,margin:0,
  fontFace:B,fontSize:11.5,bold:true,charSpacing:1.8,color:BLUE_DK});
s.addText('HI STRIPS',{x:6.3,y:2.22,w:3.0,h:0.28,isTextBox:true,margin:0,
  fontFace:B,fontSize:11.5,bold:true,charSpacing:1.8,color:BLUE_DK});
const rows=[
 ['Barrier to entry','Very high','None'],
 ['Retainer','$2,000 per creator','Never, at any level'],
 ['Commission','15% of ad spend','5%'],
 ['Time to revenue','Six months of nothing','Immediate reach'],
 ['The endgame','A trained, elite bench','Retail distribution']
];
rows.forEach((r,i)=>{
  const y=2.68+i*0.47;
  s.addShape(S.line,{x:M,y:y-0.08,w:8.6,h:0,line:{color:HAIR,width:1}});
  s.addText(r[0],{x:M,y,w:2.2,h:0.34,isTextBox:true,margin:0,valign:'middle',
    fontFace:B,fontSize:11.5,color:GREY});
  s.addText(r[1],{x:3.0,y,w:3.1,h:0.34,isTextBox:true,margin:0,valign:'middle',
    fontFace:B,fontSize:12.5,color:INK});
  s.addText(r[2],{x:6.3,y,w:3.0,h:0.34,isTextBox:true,margin:0,valign:'middle',
    fontFace:B,fontSize:12.5,color:INK});
});
s.addNotes('There is no right or wrong strategy — only the one that fits the stage we are at.');

/* ---------------- 8. Our playbook ---------------- */
s=pres.addSlide(); s.background={color:INK};
kicker(s,'OUR PLAYBOOK',true);
sub(s,'Earning from day one, and still investing in our creators.',true,title(s,'We sit in between.',true,36)+0.06);
s.addShape(S.line,{x:1.0,y:2.95,w:8.0,h:0,line:{color:LINE_DK,width:1.5}});
dot(s,0.94,2.89,0.12,GREY);
dot(s,8.94,2.89,0.12,GREY);
dot(s,4.85,2.8,0.3,BLUE);
s.addText('BAMBORA',{x:3.5,y:2.38,w:3.0,h:0.3,isTextBox:true,margin:0,align:'center',
  fontFace:B,fontSize:12.5,bold:true,charSpacing:1.6,color:BLUE});
s.addText('HI STRIPS',{x:M,y:3.12,w:2.2,h:0.26,isTextBox:true,margin:0,
  fontFace:B,fontSize:11,bold:true,charSpacing:1.2,color:WHITE});
s.addText('No barrier',{x:M,y:3.36,w:2.2,h:0.26,isTextBox:true,margin:0,
  fontFace:B,fontSize:10.5,color:GREY});
s.addText('HAUS',{x:7.1,y:3.12,w:2.2,h:0.26,isTextBox:true,margin:0,align:'right',
  fontFace:B,fontSize:11,bold:true,charSpacing:1.2,color:WHITE});
s.addText('Very high barrier',{x:7.1,y:3.36,w:2.2,h:0.26,isTextBox:true,margin:0,align:'right',
  fontFace:B,fontSize:10.5,color:GREY});
const prin=[
 ['Revenue from day one','Not six months from now.'],
 ['We invest in our creators','Unlike Hi Strips, we put something in.'],
 ['A filter, not a wall','The bar is not high. It is not low either.']
];
prin.forEach((p,i)=>{
  s.addText(p[0],{x:COL[i],y:3.98,w:CW,h:0.3,isTextBox:true,margin:0,valign:'top',
    fontFace:B,fontSize:13.5,bold:true,color:WHITE});
  s.addText(p[1],{x:COL[i],y:4.32,w:CW,h:0.55,isTextBox:true,margin:0,valign:'top',
    fontFace:B,fontSize:11.5,color:GREY_LT,lineSpacing:15});
});
s.addNotes('Not Haus, not Hi Strips. The middle, for at least the next two months.');

/* ---------------- 9. The plan ---------------- */
s=pres.addSlide();
kicker(s,'THE CREATORS WE HAVE',false);
title(s,'Where we start.',false,34);
const plan=[
 ['01','Keep the top 10','Our ten best creators of all time stay on exactly the rate they are on today: 12%.'],
 ['02','Let the rest go','Nobody holds that level of quality for a 5% commission. That is human psychology.'],
 ['03','No retainers on top','At 12% commission, adding a retainer makes a creator unprofitable for us.'],
 ['04','Train deeper','Fewer creators, far more specific direction from me on every brief.']
];
plan.forEach((p,i)=>{
  const y=2.05+i*0.73;
  s.addShape(S.ellipse,{x:M,y:y+0.01,w:0.44,h:0.44,fill:{color:TINT},line:{width:0}});
  s.addText(p[0],{x:M,y:y+0.01,w:0.44,h:0.44,isTextBox:true,margin:0,align:'center',valign:'middle',
    fontFace:B,fontSize:12,bold:true,color:BLUE_DK});
  s.addText(p[1],{x:1.32,y,w:7.9,h:0.3,isTextBox:true,margin:0,valign:'top',
    fontFace:B,fontSize:14,bold:true,color:INK});
  s.addText(p[2],{x:1.32,y:y+0.3,w:7.9,h:0.32,isTextBox:true,margin:0,valign:'top',
    fontFace:B,fontSize:12.5,color:SOFT});
});
s.addNotes('Goal: make money from the very beginning rather than waiting six months.');

/* ---------------- 9b. The top 10, from TRYBE ---------------- */
if(TRYBE_IMG){
  s=pres.addSlide();
  kicker(s,'THE TOP 10',false);
  title(s,'The ten we keep.',false,30,0.95);
  s.addImage({path:TRYBE_IMG,x:2.0,y:1.62,w:6.0,h:3.48,
    shadow:{type:'outer',color:'2E2A39',blur:16,offset:3,angle:90,opacity:0.20}});
  s.addNotes('Creative Performance grouped by creator, ranked on TRYBE sales. '+
             'These are the ten that stay on 12%.');
}

/* ---------------- 10b. Where the sales come from ---------------- */
if(TRYBE_IMG){
  s=pres.addSlide();
  kicker(s,'CONCENTRATION',false);
  sub(s,'TRYBE sales, all time. Within the top nine, two creators are 65% of the total.',
      false,title(s,'Two creators are most of it.',false,32)+0.06);
  // single series -> single hue, no legend; the title names the measure
  const rows=[['Kia Layton',24.5],['Cambria Reau',17.7],['Jennifer Thomas',4.43],
              ['Tayler Raza',4.06],['Mary Saggau',3.64],['Sophia Lease',3.20],
              ['Cloe Peluola',2.63],['Myrka Bustillo',2.45],['Ciara Burnett',2.38]].reverse();
  s.addChart(pres.ChartType.bar,[{name:'TRYBE sales ($K)',
      labels:rows.map(r=>r[0]), values:rows.map(r=>r[1])}],
    {x:0.62,y:2.32,w:8.76,h:2.82,
     barDir:'bar', barGapWidthPct:45, chartColors:[CHART],
     showLegend:false, showTitle:false,
     showValue:true, dataLabelPosition:'outEnd', dataLabelFormatCode:'"$"0.0,,"K"',
     dataLabelColor:SOFT, dataLabelFontFace:B, dataLabelFontSize:10,
     catAxisLabelColor:INK, catAxisLabelFontFace:B, catAxisLabelFontSize:11,
     catAxisLineShow:false, catGridLine:{style:'none'},
     valAxisHidden:true, valAxisLineShow:false, valGridLine:{style:'none'},
     valAxisMaxVal:28});
  s.addNotes('Only the top nine are shown, out of 194 creators. '+
             'Kia Layton and Cambria Reau together are about 65% of this group.');
}

/* ---------------- 11. How we train ---------------- */
s=pres.addSlide(); s.background={color:INK};
kicker(s,'HOW WE INVEST',true);
sub(s,'The barrier is the training, not the rate.',true,title(s,'We train them.',true,36)+0.06);
[['The checklist tool',"Dos and don'ts they fill in, not a document they read. Interactive, and quick. Live Thursday."],
 ['Weekly drops','New inspiration, new hooks and fresh data. Every single week, without fail.'],
 ['My calendar, open','A Calendly link they can use to book a call with me whenever they want one.'],
 ['Real feedback','Notes, redos and explanations on every submission through the whole first month.']
].forEach((it,i)=>{
  const x=0.7+(i%2)*4.4, y=2.4+Math.floor(i/2)*1.2;
  dot(s,x,y+0.09,0.1,BLUE);
  s.addText(it[0],{x:x+0.22,y,w:4.0,h:0.3,isTextBox:true,margin:0,valign:'top',
    fontFace:B,fontSize:14,bold:true,color:WHITE});
  s.addText(it[1],{x:x+0.22,y:y+0.32,w:4.0,h:0.66,isTextBox:true,margin:0,valign:'top',
    fontFace:B,fontSize:11.5,color:GREY_LT,lineSpacing:15});
});
s.addText('Creators who think you are just a UGC manager never feel prioritised. That is not how I run it.',
  {x:M,y:4.82,w:8.6,h:0.3,isTextBox:true,margin:0,fontFace:B,fontSize:12.5,italic:true,color:BLUE});
s.addNotes('The tool is a checklist they fill in rather than a doc they read. Built by Thursday.');

/* ---------------- 12. Month one ---------------- */
s=pres.addSlide();
kicker(s,'MONTH ONE',false);
sub(s,'A new campaign: 5% of GMV, paid weekly.',false,title(s,'Who we onboard.',false,34)+0.06);
[['Cast a wide net, approve only the good','Anyone I see real potential in gets a shot at 5%.'],
 ['Portfolio over GMV','I would normally gate on a GMV threshold. Our TAM is too small for that, so I judge the videos in their portfolio instead.'],
 ['Men and women, deliberately','Not only women. The reason is on the next slide.'],
 ['The clock starts on delivery','Month one means 30 days from the product landing, not from signing. Shipping takes one to two weeks, and we keep talking to them throughout.']
].forEach((it,i)=>{
  const y=2.12+i*0.76;
  dot(s,M,y+0.09,0.1,BLUE_DK);
  s.addText(it[0],{x:M+0.22,y,w:8.4,h:0.3,isTextBox:true,margin:0,valign:'top',
    fontFace:B,fontSize:14,bold:true,color:INK});
  s.addText(it[1],{x:M+0.22,y:y+0.3,w:8.4,h:0.42,isTextBox:true,margin:0,valign:'top',
    fontFace:B,fontSize:11.5,color:SOFT,lineSpacing:14});
});
s.addNotes('Wide net, but only the good get approved. Judged on portfolio because our TAM is small.');

/* ---------------- 13. Why men too ---------------- */
s=pres.addSlide(); s.background={color:DEEP};
kicker(s,'FROM THE DATA',true);
s.addText('25%',{x:M,y:1.75,w:3.4,h:1.35,isTextBox:true,margin:0,valign:'middle',
  fontFace:H,fontSize:64,bold:true,color:BLUE});
s.addText('of buyers on the ads Isla walked me through were men.',
  {x:M,y:3.2,w:3.5,h:0.8,isTextBox:true,margin:0,valign:'top',
   fontFace:B,fontSize:13,color:WHITE,lineSpacing:18});
s.addText('Most of our customers are women. But put a man in the video and we unlock an audience we are not reaching today.',
  {x:4.9,y:1.95,w:4.4,h:1.3,isTextBox:true,margin:0,valign:'top',
   fontFace:B,fontSize:14,color:GREY_LT,lineSpacing:20});
s.addText('That is why the new campaign onboards both.',
  {x:4.9,y:3.4,w:4.4,h:0.4,isTextBox:true,margin:0,valign:'top',
   fontFace:B,fontSize:14,bold:true,color:WHITE});
// one measure split in two, both ends directly labelled — identity is never colour alone
s.addShape(S.roundRect,{x:4.9,y:4.24,w:4.4,h:0.34,rectRadius:0.05,
  fill:{color:'4A5570'},line:{width:0}});
s.addShape(S.roundRect,{x:4.9,y:4.24,w:1.1,h:0.34,rectRadius:0.05,
  fill:{color:BLUE},line:{width:0}});
s.addText('Men 25%',{x:4.9,y:4.66,w:1.6,h:0.26,isTextBox:true,margin:0,
  fontFace:B,fontSize:10.5,bold:true,color:BLUE});
s.addText('Women 75%',{x:7.3,y:4.66,w:2.0,h:0.26,isTextBox:true,margin:0,align:'right',
  fontFace:B,fontSize:10.5,color:GREY_LT});
s.addNotes('From the data Isla walked me through. Real room to grow the male audience.');

/* ---------------- 14. Tiers come later ---------------- */
s=pres.addSlide();
kicker(s,'TIERS',false);
sub(s,'Tiers only work if there is something to aspire to.',false,title(s,'Not yet.',false,34)+0.06);
s.addShape(S.line,{x:0.92,y:2.57,w:6.45,h:0,line:{color:HAIR,width:1.5}});
[['Onboard at 5%'],['Product ships'],['Creatives go live'],['First results']].forEach((st,i)=>{
  const x=0.7+i*2.15;
  s.addShape(S.ellipse,{x,y:2.35,w:0.44,h:0.44,fill:{color:TINT},line:{width:0}});
  s.addText(String(i+1),{x,y:2.35,w:0.44,h:0.44,isTextBox:true,margin:0,align:'center',valign:'middle',
    fontFace:B,fontSize:12,bold:true,color:BLUE_DK});
  s.addText(st[0],{x,y:2.95,w:2.0,h:0.5,isTextBox:true,margin:0,valign:'top',
    fontFace:B,fontSize:12.5,bold:true,color:INK,lineSpacing:16});
});
s.addText('Then — and only then — we introduce tiers.',
  {x:M,y:3.72,w:8.6,h:0.34,isTextBox:true,margin:0,fontFace:B,fontSize:14,bold:true,color:BLUE_DK});
s.addText('Introducing them now means giving the current TRYBE and Discord batch more incentive on an already thin margin. We cannot offer 15%, and 12% is already too much.',
  {x:M,y:4.22,w:8.6,h:0.7,isTextBox:true,margin:0,valign:'top',
   fontFace:B,fontSize:12.5,color:SOFT,lineSpacing:17});
s.addNotes('Tiers arrive once the first batch has product, creatives up, and results in.');

/* ---------------- 15. Instagram feeds TRYBE ---------------- */
s=pres.addSlide();
kicker(s,'THE PIPELINE',false);
sub(s,'Good creators should not be making videos for free.',
    false,title(s,'Instagram\nfeeds TRYBE.',false,32,1.02,5.0)+0.06,5.0);
if(UGC_IMG){
  s.addImage({path:UGC_IMG,x:5.9,y:1.45,w:3.4,h:3.0,sizing:{type:'cover',w:3.4,h:3.0},
    shadow:{type:'outer',color:'2E2A39',blur:14,offset:3,angle:90,opacity:0.20}});
  s.addText('@bamboraugc — 2,930 followers',{x:5.9,y:4.56,w:3.4,h:0.28,isTextBox:true,
    margin:0,align:'center',fontFace:B,fontSize:10.5,color:GREY});
}
[['1','They come to us','The DMs we already get, plus outreach Yelly and I refine together.'],
 ['2','We vet them','TikTok Shop experience, and a portfolio worth backing.'],
 ['3','They join TRYBE','On the 5% campaign, with the whole training stack behind them.']
].forEach((st,i)=>{
  const y=2.72+i*0.80;
  s.addShape(S.ellipse,{x:M,y,w:0.46,h:0.46,fill:{color:BLUE},line:{width:0}});
  s.addText(st[0],{x:M,y,w:0.46,h:0.46,isTextBox:true,margin:0,align:'center',valign:'middle',
    fontFace:H,fontSize:14,bold:true,color:INK});
  s.addText(st[1],{x:1.3,y:y-0.02,w:3.8,h:0.3,isTextBox:true,margin:0,valign:'top',
    fontFace:B,fontSize:14,bold:true,color:INK});
  s.addText(st[2],{x:1.3,y:y+0.28,w:3.8,h:0.46,isTextBox:true,margin:0,valign:'top',
    fontFace:B,fontSize:11.5,color:SOFT,lineSpacing:15});
});
s.addNotes('Instagram becomes the top of the funnel for TRYBE rather than a free-video channel. '+
           'I need access to the account to run this properly.');

/* ---------------- 16. Decisions ---------------- */
s=pres.addSlide(); s.background={color:DEEP};
kicker(s,'OPEN',true);
title(s,'Four things to decide.',true,34);
[['1','Are we on board?','5% of GMV, paid weekly, onboarding men and women. I need a yes before I build the new campaign.'],
 ['2','Jennifer','Still on TRYBE. Liam raised moving her back to a straight retainer. Tell me which way and I will have that conversation.'],
 ['3','Instagram access','I want to be hands-on with the messaging and the outreach, working alongside Yelly.'],
 ['4','The creators we move on from','We have already told them exciting things were coming. We need to agree how we land that.']
].forEach((d,i)=>{
  const x=0.7+(i%2)*4.5, y=1.85+Math.floor(i/2)*1.62;
  s.addShape(S.roundRect,{x,y,w:4.1,h:1.48,rectRadius:0.09,fill:{color:PANEL},line:{width:0}});
  s.addShape(S.ellipse,{x:x+0.28,y:y+0.24,w:0.3,h:0.3,fill:{color:BLUE},line:{width:0}});
  s.addText(d[0],{x:x+0.28,y:y+0.24,w:0.3,h:0.3,isTextBox:true,margin:0,align:'center',valign:'middle',
    fontFace:B,fontSize:11,bold:true,color:INK});
  s.addText(d[1],{x:x+0.68,y:y+0.22,w:3.2,h:0.34,isTextBox:true,margin:0,valign:'middle',
    fontFace:B,fontSize:14,bold:true,color:WHITE});
  s.addText(d[2],{x:x+0.28,y:y+0.66,w:3.55,h:0.68,isTextBox:true,margin:0,valign:'top',
    fontFace:B,fontSize:11,color:GREY_LT,lineSpacing:14});
});
s.addNotes('The sign-off I need before building the campaign, plus the three open conversations.');

pres.writeFile({fileName:''+require('os').homedir()+'/Bombara/Bambora-Creator-Partnership-Strategy.pptx'})
  .then(f=>{
    // pptxgenjs writes a third <c:axId> into <c:barChart> that no axis element declares.
    // PowerPoint can discard the chart and call the file corrupt, so strip the orphan.
    if(!f||!fs.existsSync(f)) return;
    let AdmZip; try{ AdmZip=require('adm-zip'); }catch(e){ console.log('wrote',f,'(adm-zip missing — chart axIds not repaired)'); return; }
    const zip=new AdmZip(f); let fixed=0;
    zip.getEntries().filter(e=>/^ppt\/charts\/chart\d+\.xml$/.test(e.entryName)).forEach(e=>{
      let xml=zip.readAsText(e);
      const declared=new Set([...xml.matchAll(/<c:(?:catAx|valAx|serAx)>[\s\S]*?<c:axId val="(\d+)"\/>/g)].map(m=>m[1]));
      xml=xml.replace(/<c:barChart>[\s\S]*?<\/c:barChart>/,plot=>
        plot.replace(/<c:axId val="(\d+)"\/>/g,(tag,id)=>{ if(declared.has(id))return tag; fixed++; return ''; }));
      zip.updateFile(e.entryName,Buffer.from(xml,'utf8'));
    });
    if(fixed) zip.writeZip(f);
    console.log('wrote',f, fixed?`(repaired ${fixed} orphan axId)`:'');
  });
