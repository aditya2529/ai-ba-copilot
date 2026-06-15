require('module').globalPaths.push('C:/Users/adity/AppData/Roaming/npm/node_modules');
const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, Header, Footer,
  AlignmentType, HeadingLevel, BorderStyle, WidthType, ShadingType, LevelFormat, PageNumber } = require('docx');
const fs = require('fs');

const BLUE="1F4E79", MID="2E75B6", GRAY="595959", LIME="1E8449", CORAL="922B21";
const border={style:BorderStyle.SINGLE,size:1,color:"CCCCCC"};
const borders={top:border,bottom:border,left:border,right:border};

function h1(t){return new Paragraph({heading:HeadingLevel.HEADING_1,spacing:{before:360,after:120},children:[new TextRun({text:t,bold:true,size:34,color:BLUE,font:"Arial"})]});}
function h2(t){return new Paragraph({heading:HeadingLevel.HEADING_2,spacing:{before:260,after:80},children:[new TextRun({text:t,bold:true,size:27,color:MID,font:"Arial"})]});}
function h3(t){return new Paragraph({heading:HeadingLevel.HEADING_3,spacing:{before:180,after:60},children:[new TextRun({text:t,bold:true,size:23,color:GRAY,font:"Arial"})]});}
function body(t,o={}){return new Paragraph({spacing:{before:60,after:60},children:[new TextRun({text:t,size:22,font:"Arial",...o})]});}
function bullet(t,bold=false){return new Paragraph({numbering:{reference:"b",level:0},spacing:{before:40,after:40},children:[new TextRun({text:t,size:22,font:"Arial",bold})]});}
function spacer(){return new Paragraph({children:[new TextRun("")],spacing:{before:60,after:60}});}
function divider(){return new Paragraph({border:{bottom:{style:BorderStyle.SINGLE,size:6,color:MID,space:1}},spacing:{before:160,after:160},children:[new TextRun("")]});}
function callout(t){return new Table({width:{size:9360,type:WidthType.DXA},columnWidths:[9360],rows:[new TableRow({children:[new TableCell({borders,width:{size:9360,type:WidthType.DXA},shading:{fill:"E8F4FD",type:ShadingType.CLEAR},margins:{top:120,bottom:120,left:200,right:200},children:[new Paragraph({children:[new TextRun({text:t,size:22,font:"Arial",italics:true,color:BLUE})]})]})]})]});}
function qaHeader(){return new TableRow({children:[
  new TableCell({borders,width:{size:3500,type:WidthType.DXA},shading:{fill:"1F4E79",type:ShadingType.CLEAR},margins:{top:80,bottom:80,left:120,right:120},children:[new Paragraph({children:[new TextRun({text:"Question",bold:true,size:22,color:"FFFFFF",font:"Arial"})]})]}),
  new TableCell({borders,width:{size:5860,type:WidthType.DXA},shading:{fill:"1F4E79",type:ShadingType.CLEAR},margins:{top:80,bottom:80,left:120,right:120},children:[new Paragraph({children:[new TextRun({text:"Your Answer",bold:true,size:22,color:"FFFFFF",font:"Arial"})]})]}),
]});}
function qa(q,a,shade,qColor){return new TableRow({children:[
  new TableCell({borders,width:{size:3500,type:WidthType.DXA},shading:{fill:shade?"D6E4F0":"EBF5FB",type:ShadingType.CLEAR},margins:{top:80,bottom:80,left:120,right:120},children:[new Paragraph({children:[new TextRun({text:q,size:20,bold:true,color:qColor||BLUE,font:"Arial"})]})]}),
  new TableCell({borders,width:{size:5860,type:WidthType.DXA},shading:{fill:shade?"FAFAFA":"FFFFFF",type:ShadingType.CLEAR},margins:{top:80,bottom:80,left:120,right:120},children:[new Paragraph({children:[new TextRun({text:a,size:20,font:"Arial"})]})]}),
]});}
function qaTable(rows){return new Table({width:{size:9360,type:WidthType.DXA},columnWidths:[3500,5860],rows});}

const doc=new Document({
  numbering:{config:[{reference:"b",levels:[{level:0,format:LevelFormat.BULLET,text:"•",alignment:AlignmentType.LEFT,style:{paragraph:{indent:{left:720,hanging:360}}}}]}]},
  styles:{default:{document:{run:{font:"Arial",size:22}}},paragraphStyles:[
    {id:"Heading1",name:"Heading 1",basedOn:"Normal",next:"Normal",quickFormat:true,run:{size:34,bold:true,font:"Arial",color:BLUE},paragraph:{spacing:{before:360,after:120},outlineLevel:0}},
    {id:"Heading2",name:"Heading 2",basedOn:"Normal",next:"Normal",quickFormat:true,run:{size:27,bold:true,font:"Arial",color:MID},paragraph:{spacing:{before:260,after:80},outlineLevel:1}},
    {id:"Heading3",name:"Heading 3",basedOn:"Normal",next:"Normal",quickFormat:true,run:{size:23,bold:true,font:"Arial",color:GRAY},paragraph:{spacing:{before:180,after:60},outlineLevel:2}},
  ]},
  sections:[{
    properties:{page:{size:{width:12240,height:15840},margin:{top:1440,right:1440,bottom:1440,left:1440}}},
    headers:{default:new Header({children:[new Paragraph({border:{bottom:{style:BorderStyle.SINGLE,size:4,color:MID,space:1}},children:[new TextRun({text:"AI BA Copilot — Demo Playbook (RAG + MCP)  ·  18 June",size:18,font:"Arial",color:GRAY,italics:true})]})]})},
    footers:{default:new Footer({children:[new Paragraph({alignment:AlignmentType.RIGHT,children:[new TextRun({text:"Page ",size:18,font:"Arial",color:GRAY}),new TextRun({children:[PageNumber.CURRENT],size:18,font:"Arial",color:GRAY}),new TextRun({text:" of ",size:18,font:"Arial",color:GRAY}),new TextRun({children:[PageNumber.TOTAL_PAGES],size:18,font:"Arial",color:GRAY})]})]})},
    children:[
      // COVER
      new Paragraph({alignment:AlignmentType.CENTER,spacing:{before:1200,after:200},children:[new TextRun({text:"🚀 AI BA Copilot",size:64,bold:true,color:BLUE,font:"Arial"})]}),
      new Paragraph({alignment:AlignmentType.CENTER,spacing:{after:100},children:[new TextRun({text:"Demo Playbook",size:38,color:MID,font:"Arial"})]}),
      new Paragraph({alignment:AlignmentType.CENTER,spacing:{after:60},children:[new TextRun({text:"Now with RAG (your team's voice) + MCP (agent-ready)",size:22,color:GRAY,italics:true,font:"Arial"})]}),
      new Paragraph({alignment:AlignmentType.CENTER,spacing:{after:1600},children:[new TextRun({text:"Internal Showcase  ·  18 June",size:20,color:GRAY,font:"Arial"})]}),
      divider(),

      // 1. WHAT
      h1("1. What This Tool Does"),
      body("AI BA Copilot turns raw meeting notes into production-ready Jira user stories — with acceptance criteria, test cases, risk analysis, and story-point estimates — then pushes them straight to your Jira board. One click, ~30 seconds."),
      spacer(),
      callout("\"How many of you have left a meeting with notes, then spent 2 hours turning them into proper Jira tickets? That's what this solves.\""),
      spacer(),
      h2("What's new since last time (the two big upgrades)"),
      h3("🧠 RAG — it now writes in YOUR team's voice"),
      body("Generic AI writes generic stories. I fed the tool 52 of our real Jira stories, and it now learns from our actual history before writing — matching our terminology, roles, and patterns."),
      h3("🔌 MCP Server — it's now infrastructure, not just an app"),
      body("The whole engine is wrapped as a Model Context Protocol server, so any AI agent can call it directly — generate, validate, assess risk, estimate, push to Jira — with no human clicking buttons."),

      divider(),

      // 2. LIVE DEMO FLOW
      h1("2. Live Demo Flow (exact click path)"),
      body("The demo runs entirely on the live cloud app — no local setup needed.", {italics:true,color:GRAY}),
      callout("Live link: https://ai-ba-copilot.streamlit.app/    ·    Golden rule: show the PAIN first, then the 30-second fix. The contrast is your wow moment."),
      spacer(),

      h2("Part A — The hook (1 min, no slides)"),
      body("Say: \"Turning meeting notes into Jira stories takes a good BA 1–2 hours. Watch this do it in 30 seconds — and sound like our team while doing it.\""),

      h2("Part B — Generic generation (3 min)"),
      bullet("Open the live link → sidebar → click 'app'"),
      bullet("Mode: Simple (One-click)"),
      bullet("Paste a real-sounding note, e.g. \"Customers keep failing card payments because of invalid card numbers. We need to validate card fields and lock accounts after repeated failed attempts.\""),
      bullet("Click '🚀 Generate Everything' → 2 stories appear in ~20s"),
      bullet("Click through the tabs: Validation, Risks, Test Cases, Estimation"),
      bullet("Say: \"Six things happened in one click — clean, generate, validate, risks, tests, points.\""),

      h2("Part C — The RAG wow moment (4 min) — THE HERO"),
      bullet("Sidebar → click 'RAG Mode'"),
      bullet("Point at Corpus Status: \"It has learned from 52 of our real Jira stories.\""),
      bullet("Mode: Simple → paste the SAME card-payment note"),
      bullet("Click 'Generate Everything (RAG-augmented)' → watch for '📚 Retrieved org context'"),
      bullet("Show the story side-by-side with Part B's output"),
      callout("THE LINE: \"Same input, same tool. Generic AI guessed the role as 'customer support representative' — wrong. The RAG version used 'registered customer' — our actual convention. It learned that from our own Jira history.\""),

      h2("Part D — Push to Jira live (2 min)"),
      bullet("On the Story tab → click '🚀 Push Clean Story to Jira'"),
      bullet("Wait for ✅ Created: SCRUM-xxx"),
      bullet("Switch to your Jira board → show the freshly created tickets"),

      h2("Part E — The MCP angle (1 min, talk-only)"),
      body("MCP runs locally (it's a background service, not a web page), so don't try to show it live. Instead say:"),
      callout("\"I also wrapped this whole engine as an MCP server — meaning any AI agent can call it on its own. The Copilot becomes the hands; AI agents become the brain. That's the difference between a tool and infrastructure.\""),

      h2("Closing question (instead of 'any questions?')"),
      body("Ask: \"What would make this useful for YOUR day-to-day work?\" — it flips the room from judging to imagining, and gets you real feedback."),

      divider(),

      // 3. TIMINGS
      h1("3. Timing & Safety Net"),
      h2("Timing"),
      bullet("Hook — 1 min"),
      bullet("Generic generation — 3 min"),
      bullet("RAG hero moment — 4 min"),
      bullet("Push to Jira — 2 min"),
      bullet("MCP angle — 1 min"),
      bullet("Q&A — 5+ min   (Total talk: ~11 min + Q&A)"),
      spacer(),
      h2("Safety net"),
      callout("If the cloud app is slow or errors live: have a screen recording of the full RAG → Jira flow ready. Say \"let me show you a recording — same inputs, same result.\" Nobody will mind."),
      h3("Pre-demo checklist (morning of)"),
      bullet("Open the live link 1 hour before — confirm it loads (first load is slow as it wakes up)"),
      bullet("RAG Mode → confirm Corpus Status shows ~59 (auto-seeds if empty)"),
      bullet("Do one test 'Push to Jira' the night before — confirm a SCRUM ticket is created"),
      bullet("Have 2–3 sample notes ready to paste (incl. the card-payment one that shows RAG best)"),
      bullet("Screen-recording backup ready"),

      divider(),

      // 4. Q&A
      h1("4. Q&A Preparation"),

      h2("🟢 Basic Questions"),
      spacer(),
      qaTable([qaHeader(),
        qa("Do I need to know Agile or Jira to use it?","No. Paste your notes, click a button. It handles all the formatting.",false),
        qa("How long does it take?","About 30 seconds end-to-end, including the Jira push.",true),
        qa("What is RAG, simply?","It means the AI reads our past Jira stories first, then writes new ones in the same style — like a new hire who studied our docs before starting.",false),
        qa("What is the MCP server?","A standard 'door' that lets other AI agents call this tool automatically, instead of a human clicking buttons.",true),
        qa("Does anyone need training?","No. If you can type meeting notes, you can use it.",false),
      ]),
      spacer(),

      h2("🟡 Skeptical Questions"),
      spacer(),
      qaTable([qaHeader(),
        qa("Is RAG output actually better, or just hype?","On in-domain inputs, yes — measurably. Same card-payment note: generic AI invented the role 'customer support representative'; RAG used our real convention 'registered customer'. It learns from our 52 actual stories.","#7D6608",false,"#7D6608"),
        qa("What if RAG has no similar past story?","It gracefully falls back to normal generation — quality stays high, it just won't add org-specific flavour. We even show which past stories it used, for transparency.",true,"#7D6608"),
        qa("What data leaves our systems?","Only the notes you paste go to the LLM. The RAG memory and embeddings run locally/free — no extra service. Worth checking against our data policy for sensitive inputs.",false,"#7D6608"),
        qa("What does RAG cost us?","Nothing extra. It uses a free local embedding model — no new API, no per-call fee.",true,"#7D6608"),
        qa("What if the AI gets it wrong?","You always review before pushing to Jira. Push is a manual, deliberate step — never automatic.",false,"#7D6608"),
      ]),
      spacer(),

      h2("🔴 Sharp / Technical Questions"),
      spacer(),
      qaTable([qaHeader(),
        qa("Isn't this just ChatGPT with a Jira button?","No. ChatGPT gives one draft, no quality enforcement, no memory of our org, and you'd still build the ticket by hand. This enforces quality, learns our voice via RAG, runs a full pipeline, and pushes to Jira — and any agent can call it via MCP.",false,CORAL),
        qa("How does RAG actually work here?","Past stories are turned into vectors and stored. New notes are matched to the closest past stories, which are injected as style reference into the prompt. Local embeddings (MiniLM), local vector store (ChromaDB).",true,CORAL),
        qa("Will this replace Business Analysts?","No. It removes the mechanical part — formatting, structuring, data entry. BAs still own stakeholder conversations, prioritisation, and judgement. It gives them time back.",false,CORAL),
        qa("What's the accuracy?","Not 100% — output needs human review, especially for domain logic. It gets you 0→80% in 30 seconds; you take it 80→100%. The win is that first 80%.",true,CORAL),
        qa("How does the MCP server integrate?","It exposes tools (generate, validate, risks, estimate, push_to_jira) over the Model Context Protocol. Any MCP-compatible agent or Claude Desktop can call them. Today it runs locally; wiring into our agent platform is the next step.",false,CORAL),
        qa("Efficiency / token cost?","Actively being optimized — we already removed a wasted LLM call, and we're targeting ~45% fewer calls with no quality loss, on a separate branch so the live version stays stable.",true,CORAL),
      ]),
      spacer(),

      h2("🎁 'On the roadmap' Questions"),
      body("For all of these, \"that's on the roadmap\" is a perfectly strong answer.",{italics:true,color:GRAY}),
      spacer(),
      qaTable([qaHeader(),
        qa("Can it push to Confluence / Azure DevOps?","Not yet — Jira first. Those are on the roadmap.",false),
        qa("Can multiple teams have separate memories?","Single shared corpus today; per-team memory is a planned feature.",true),
        qa("Can we save our own story templates?","Planned — custom prompt templates per team.",false),
        qa("Voice / meeting transcript input?","Planned — record a meeting, transcribe, generate.",true),
      ]),

      divider(),

      // 5. PITCH
      h1("5. Your One-Line Pitch"),
      spacer(),
      callout("\"I turn meeting notes into production-ready Jira stories — in our team's voice — in under a minute, and push them straight to the board. And any AI agent can now call it autonomously.\""),
      spacer(),
      h2("Pro tip"),
      body("If asked something you don't know: \"Great question — let me come back to you on that. Anyone else?\" Honesty reads as confidence, not weakness."),
    ]
  }]
});

Packer.toBuffer(doc).then(b=>{fs.writeFileSync("D:\\Projects\\ai-ba-copilot\\AI_BA_Copilot_Demo_Playbook.docx",b);console.log("Playbook done.");});
