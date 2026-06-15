require('module').globalPaths.push('C:/Users/adity/AppData/Roaming/npm/node_modules');
const PptxGenJS = require('pptxgenjs');
const pptx = new PptxGenJS();
pptx.layout = 'LAYOUT_WIDE';

// Palette
const NAVY="0B1F3A", DEEP="12345D", BLUE="2E75B6", SKY="7FB3D5", PALE="D6EAF8",
      WHITE="FFFFFF", SOFT="F4F8FB", GRAY="566573", LIME="27AE60", CORAL="E74C3C", GOLD="F39C12", PURPLE="7D3C98";

const TOTAL = 12;
function dots(s, idx){ const cx=12.6, cy=7.15; for(let i=0;i<TOTAL;i++){ s.addShape(pptx.ShapeType.ellipse,{x:cx-(TOTAL-1-i)*0.16,y:cy,w:0.09,h:0.09,fill:{color:i===idx?WHITE:"3B5A7A"},line:{color:i===idx?WHITE:"3B5A7A"}});}}
function eyebrow(s,t){ s.addText(t,{x:0.9,y:0.6,w:12,h:0.4,fontSize:13,bold:true,color:BLUE,fontFace:"Calibri",charSpacing:4});}
function base(s,idx){ s.background={color:SOFT}; dots(s,idx);}
function baseDark(s,idx){ s.background={color:NAVY}; dots(s,idx);}

// 1 COVER
{ const s=pptx.addSlide(); s.background={color:NAVY};
  s.addShape(pptx.ShapeType.rect,{x:0,y:0,w:0.25,h:'100%',fill:{color:BLUE},line:{color:BLUE}});
  s.addText("AI BA",{x:0.9,y:1.3,w:11,h:1.4,fontSize:96,bold:true,color:WHITE,fontFace:"Calibri"});
  s.addText("Copilot",{x:0.9,y:2.6,w:11,h:1.4,fontSize:96,bold:true,color:BLUE,fontFace:"Calibri"});
  s.addShape(pptx.ShapeType.rect,{x:0.95,y:4.25,w:0.6,h:0.06,fill:{color:BLUE},line:{color:BLUE}});
  s.addText("Meeting notes in. Jira stories out — in your team's voice.",{x:0.9,y:4.45,w:12,h:0.6,fontSize:23,color:SKY,fontFace:"Calibri"});
  s.addText("Internal Demo  ·  18 June",{x:0.9,y:6.9,w:8,h:0.4,fontSize:12,color:"7FB3D5",fontFace:"Calibri"});
}
// 2 PROBLEM
{ const s=pptx.addSlide(); base(s,1); eyebrow(s,"THE PROBLEM");
  s.addText("2 hours",{x:0.9,y:1.4,w:11,h:2.4,fontSize:170,bold:true,color:NAVY,fontFace:"Calibri"});
  s.addText("To turn one meeting into Jira-ready stories.",{x:0.9,y:4.3,w:12,h:0.7,fontSize:30,color:NAVY,fontFace:"Calibri"});
  s.addText("Multiplied across every BA. Every sprint. Every team.",{x:0.9,y:5.1,w:12,h:0.5,fontSize:18,color:GRAY,fontFace:"Calibri",italic:true});
}
// 3 ANSWER
{ const s=pptx.addSlide(); base(s,2); eyebrow(s,"THE ANSWER");
  s.addText("30 seconds.",{x:0.9,y:1.4,w:11,h:2.4,fontSize:170,bold:true,color:BLUE,fontFace:"Calibri"});
  s.addText("Same notes. Same quality. One click.",{x:0.9,y:4.3,w:12,h:0.7,fontSize:30,color:NAVY,fontFace:"Calibri"});
  s.addText("Paste → generate → push to Jira. Done.",{x:0.9,y:5.1,w:12,h:0.5,fontSize:18,color:GRAY,fontFace:"Calibri",italic:true});
}
// 4 LIVE DEMO splash
{ const s=pptx.addSlide(); baseDark(s,3);
  s.addShape(pptx.ShapeType.ellipse,{x:5.16,y:1.7,w:3,h:3,fill:{color:BLUE},line:{color:BLUE}});
  s.addText("▶",{x:5.16,y:1.7,w:3,h:3,fontSize:80,bold:true,color:WHITE,align:'center',fontFace:"Calibri"});
  s.addText("Live Demo",{x:0.5,y:4.9,w:12.3,h:0.9,fontSize:54,bold:true,color:WHITE,align:'center',fontFace:"Calibri"});
  s.addText("ai-ba-copilot.streamlit.app",{x:0.5,y:5.85,w:12.3,h:0.5,fontSize:18,color:SKY,align:'center',fontFace:"Calibri",italic:true});
}
// 5 WHAT YOU SAW
{ const s=pptx.addSlide(); base(s,4); eyebrow(s,"WHAT YOU JUST SAW");
  s.addText("One click. Six things happened.",{x:0.9,y:1.05,w:12,h:0.7,fontSize:28,bold:true,color:NAVY,fontFace:"Calibri"});
  const steps=[["1","Notes cleaned & scored"],["2","Two user stories written"],["3","Stories self-validated"],["4","Risks & dependencies flagged"],["5","Six test cases generated"],["6","Story points estimated"]];
  steps.forEach((st,i)=>{ const col=i%2,row=Math.floor(i/2),x=0.9+col*6.1,y=2.2+row*1.4;
    s.addShape(pptx.ShapeType.ellipse,{x,y,w:0.8,h:0.8,fill:{color:BLUE},line:{color:BLUE}});
    s.addText(st[0],{x,y,w:0.8,h:0.8,fontSize:26,bold:true,color:WHITE,align:'center',fontFace:"Calibri"});
    s.addText(st[1],{x:x+1,y:y+0.12,w:4.8,h:0.6,fontSize:17,color:NAVY,fontFace:"Calibri"});});
  s.addText("…then pushed straight to Jira →",{x:0.9,y:6.5,w:12,h:0.4,fontSize:15,color:GRAY,italic:true,fontFace:"Calibri"});
}
// 6 RAG — hero
{ const s=pptx.addSlide(); base(s,5); eyebrow(s,"UPGRADE 1 — RAG");
  s.addText("It writes like YOUR team.",{x:0.9,y:1.05,w:12,h:0.7,fontSize:30,bold:true,color:NAVY,fontFace:"Calibri"});
  s.addText("Fed 52 of our real Jira stories. It learns our language before writing.",{x:0.9,y:1.75,w:12,h:0.5,fontSize:16,color:GRAY,fontFace:"Calibri"});
  // before
  s.addShape(pptx.ShapeType.rect,{x:0.9,y:2.5,w:5.9,h:3.9,fill:{color:"FDECEA"},line:{color:CORAL,size:1},rectRadius:0.12});
  s.addText("❌  Generic AI",{x:1.1,y:2.7,w:5.5,h:0.5,fontSize:18,bold:true,color:"922B21",fontFace:"Calibri"});
  s.addText('Role guessed as:',{x:1.1,y:3.4,w:5.5,h:0.4,fontSize:14,color:GRAY,fontFace:"Calibri"});
  s.addText('"customer support representative"',{x:1.1,y:3.85,w:5.5,h:0.8,fontSize:18,bold:true,color:"922B21",fontFace:"Calibri",italic:true});
  s.addText("Wrong for a payment feature.",{x:1.1,y:5.5,w:5.5,h:0.5,fontSize:14,color:GRAY,fontFace:"Calibri"});
  // after
  s.addShape(pptx.ShapeType.rect,{x:7.1,y:2.5,w:5.9,h:3.9,fill:{color:"EAFAF1"},line:{color:LIME,size:1},rectRadius:0.12});
  s.addText("✅  With RAG",{x:7.3,y:2.7,w:5.5,h:0.5,fontSize:18,bold:true,color:"1E8449",fontFace:"Calibri"});
  s.addText('Role corrected to:',{x:7.3,y:3.4,w:5.5,h:0.4,fontSize:14,color:GRAY,fontFace:"Calibri"});
  s.addText('"registered customer"',{x:7.3,y:3.85,w:5.5,h:0.8,fontSize:18,bold:true,color:"1E8449",fontFace:"Calibri",italic:true});
  s.addText("Our actual convention + our checkout terms.",{x:7.3,y:5.5,w:5.5,h:0.5,fontSize:14,color:GRAY,fontFace:"Calibri"});
}
// 7 MCP — infrastructure
{ const s=pptx.addSlide(); base(s,6); eyebrow(s,"UPGRADE 2 — MCP SERVER");
  s.addText("From a tool → to infrastructure.",{x:0.9,y:1.05,w:12,h:0.7,fontSize:30,bold:true,color:NAVY,fontFace:"Calibri"});
  s.addText("Wrapped the whole engine so ANY AI agent can call it — autonomously.",{x:0.9,y:1.75,w:12,h:0.5,fontSize:16,color:GRAY,fontFace:"Calibri"});
  const boxes=[["🧠","AI Agents","The brain — decide what to build"],["🔌","MCP","The bridge — standard protocol"],["🛠️","BA Copilot","The hands — generate & push to Jira"]];
  boxes.forEach((b,i)=>{ const x=0.9+i*4.15;
    s.addShape(pptx.ShapeType.rect,{x,y:2.7,w:3.85,h:3.4,fill:{color:WHITE},line:{color:PALE,size:1},rectRadius:0.12});
    s.addText(b[0],{x,y:3.0,w:3.85,h:1,fontSize:48,align:'center'});
    s.addText(b[1],{x,y:4.15,w:3.85,h:0.5,fontSize:20,bold:true,color:BLUE,align:'center',fontFace:"Calibri"});
    s.addText(b[2],{x:x+0.2,y:4.75,w:3.45,h:1,fontSize:13,color:GRAY,align:'center',fontFace:"Calibri"});
    if(i<2) s.addText("→",{x:x+3.65,y:4.0,w:0.6,h:0.8,fontSize:30,bold:true,color:SKY,align:'center'});});
  s.addText("No human clicking buttons. It plugs into a wider AI ecosystem.",{x:0.9,y:6.4,w:12,h:0.4,fontSize:14,color:GRAY,italic:true,fontFace:"Calibri"});
}
// 8 IMPACT
{ const s=pptx.addSlide(); base(s,7); eyebrow(s,"THE IMPACT");
  s.addText("If each BA writes 10 stories a sprint…",{x:0.9,y:1.05,w:12,h:0.7,fontSize:24,color:NAVY,fontFace:"Calibri"});
  const stats=[{n:"240×",l:"Faster",c:BLUE},{n:"20h",l:"Saved / BA / sprint",c:LIME},{n:"100%",l:"Your team's voice",c:GOLD}];
  stats.forEach((st,i)=>{ const x=0.9+i*4.15;
    s.addShape(pptx.ShapeType.rect,{x,y:2.4,w:3.85,h:3.6,fill:{color:WHITE},line:{color:PALE,size:1},rectRadius:0.15});
    s.addShape(pptx.ShapeType.rect,{x,y:2.4,w:3.85,h:0.15,fill:{color:st.c},line:{color:st.c}});
    s.addText(st.n,{x,y:2.9,w:3.85,h:1.9,fontSize:84,bold:true,color:st.c,align:'center',fontFace:"Calibri"});
    s.addText(st.l,{x,y:4.9,w:3.85,h:0.6,fontSize:16,color:GRAY,align:'center',fontFace:"Calibri"});});
  s.addText("A full day, per BA, every two weeks — in stories that don't need rewriting.",{x:0.9,y:6.3,w:12,h:0.6,fontSize:17,color:NAVY,italic:true,fontFace:"Calibri"});
}
// 9 WHY DIFFERENT
{ const s=pptx.addSlide(); base(s,8); eyebrow(s,"WHY IT'S DIFFERENT");
  s.addText("This isn't ChatGPT with a Jira button.",{x:0.9,y:1.05,w:12,h:0.7,fontSize:28,bold:true,color:NAVY,fontFace:"Calibri"});
  const y=2.3;
  s.addShape(pptx.ShapeType.rect,{x:0.9,y,w:5.9,h:4.3,fill:{color:WHITE},line:{color:PALE},rectRadius:0.12});
  s.addText("Generic AI",{x:1.1,y:y+0.2,w:5.5,h:0.5,fontSize:18,bold:true,color:CORAL,fontFace:"Calibri"});
  ["• One draft, no quality enforcement","• You split & format manually","• Generic, not your terminology","• You create Jira tickets by hand","• No risks, tests, or estimates"].forEach((t,i)=>s.addText(t,{x:1.1,y:y+0.85+i*0.62,w:5.6,h:0.55,fontSize:14,color:GRAY,fontFace:"Calibri"}));
  s.addShape(pptx.ShapeType.rect,{x:7.1,y,w:5.9,h:4.3,fill:{color:NAVY},line:{color:NAVY},rectRadius:0.12});
  s.addText("AI BA Copilot",{x:7.3,y:y+0.2,w:5.5,h:0.5,fontSize:18,bold:true,color:SKY,fontFace:"Calibri"});
  ["✓ Hardened prompts + quality rules","✓ Always 2 clean, separate stories","✓ RAG = your team's voice","✓ One-click Jira push","✓ Risks, tests, points — included","✓ Callable by any AI agent (MCP)"].forEach((t,i)=>s.addText(t,{x:7.3,y:y+0.85+i*0.55,w:5.6,h:0.5,fontSize:14,color:WHITE,fontFace:"Calibri"}));
}
// 10 HOW IT WORKS (pipeline)
{ const s=pptx.addSlide(); base(s,9); eyebrow(s,"UNDER THE HOOD");
  s.addText("How RAG makes it yours.",{x:0.9,y:1.05,w:12,h:0.7,fontSize:28,bold:true,color:NAVY,fontFace:"Calibri"});
  const flow=[["📥","Your past\nJira stories"],["🧠","Stored as\nsearchable memory"],["🔍","New notes find\nsimilar past stories"],["✍️","AI writes using\nyour patterns"]];
  flow.forEach((f,i)=>{ const x=0.9+i*3.1;
    s.addShape(pptx.ShapeType.rect,{x,y:2.8,w:2.7,h:2.6,fill:{color:WHITE},line:{color:PALE,size:1},rectRadius:0.12});
    s.addText(f[0],{x,y:3.05,w:2.7,h:0.9,fontSize:40,align:'center'});
    s.addText(f[1],{x:x+0.15,y:4.0,w:2.4,h:1.2,fontSize:13,color:NAVY,align:'center',fontFace:"Calibri",lineSpacingMultiple:1.2});
    if(i<3) s.addText("→",{x:x+2.55,y:3.7,w:0.6,h:0.8,fontSize:28,bold:true,color:SKY,align:'center'});});
  s.addText("Free, local embeddings — no extra cost, no data leaves the stack.",{x:0.9,y:6.0,w:12,h:0.4,fontSize:14,color:GRAY,italic:true,fontFace:"Calibri"});
}
// 11 ROADMAP
{ const s=pptx.addSlide(); base(s,10); eyebrow(s,"WHAT'S NEXT");
  s.addText("Where we're heading.",{x:0.9,y:1.05,w:12,h:0.7,fontSize:28,bold:true,color:NAVY,fontFace:"Calibri"});
  s.addShape(pptx.ShapeType.rect,{x:1.4,y:4.0,w:10.6,h:0.06,fill:{color:BLUE},line:{color:BLUE}});
  const ms=[{x:1.4,l:"Shipped",t:"App · RAG · MCP",c:LIME,d:"Live on cloud\nPushes to Jira"},{x:5.2,l:"Now",t:"Token Efficiency",c:BLUE,d:"~45% fewer LLM calls\nsame quality"},{x:9.0,l:"Next",t:"Agent Platform",c:GOLD,d:"Plug into our wider\nAI agent ecosystem"}];
  ms.forEach((m,i)=>{ s.addShape(pptx.ShapeType.ellipse,{x:m.x-0.18,y:3.85,w:0.36,h:0.36,fill:{color:m.c},line:{color:m.c}});
    s.addText(m.l,{x:m.x-1.5,y:2.7,w:3,h:0.4,fontSize:13,bold:true,color:m.c,align:'center',fontFace:"Calibri",charSpacing:2});
    s.addText(m.t,{x:m.x-1.5,y:3.1,w:3,h:0.5,fontSize:17,bold:true,color:NAVY,align:'center',fontFace:"Calibri"});
    s.addText(m.d,{x:m.x-1.5,y:4.4,w:3,h:1.4,fontSize:13,color:GRAY,align:'center',fontFace:"Calibri",lineSpacingMultiple:1.3});});
}
// 12 CLOSE
{ const s=pptx.addSlide(); baseDark(s,11);
  s.addText("Your turn.",{x:0.9,y:2.1,w:12,h:1.6,fontSize:100,bold:true,color:WHITE,fontFace:"Calibri"});
  s.addShape(pptx.ShapeType.rect,{x:0.95,y:3.8,w:0.6,h:0.06,fill:{color:BLUE},line:{color:BLUE}});
  s.addText("What would make this useful for YOUR work?",{x:0.9,y:4.05,w:12,h:0.7,fontSize:25,color:SKY,fontFace:"Calibri"});
  s.addText("ai-ba-copilot.streamlit.app",{x:0.9,y:6.6,w:8,h:0.4,fontSize:14,color:"7FB3D5",italic:true,fontFace:"Calibri"});
}

pptx.writeFile({fileName:"D:/Projects/ai-ba-copilot/AI_BA_Copilot_Demo_Slides.pptx"}).then(()=>console.log("Slides done."));
