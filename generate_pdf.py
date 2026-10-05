from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    Flowable, Image, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table,
    TableStyle, KeepTogether,
)


ROOT = Path(__file__).resolve().parent
OUT = ROOT.parent / "output" / "pdf" / "SystemFixAI-frontend-design.pdf"
LOGO = ROOT / "assets" / "systemfixai-logo.png"
BLUE = colors.HexColor("#0A5CFF")
INK = colors.HexColor("#0A0C10")
SECONDARY = colors.HexColor("#4B5563")
MUTED = colors.HexColor("#8993A2")
LINE = colors.HexColor("#E5E8ED")
PANEL = colors.HexColor("#F7F8FA")
RED = colors.HexColor("#E5484D")


styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="Eyebrow", fontName="Helvetica", fontSize=8, leading=11, textColor=BLUE, spaceAfter=8, tracking=1.3))
styles.add(ParagraphStyle(name="HeroTitle", fontName="Helvetica-Bold", fontSize=38, leading=40, textColor=INK, spaceAfter=12))
styles.add(ParagraphStyle(name="H2x", fontName="Helvetica-Bold", fontSize=27, leading=30, textColor=INK, spaceAfter=10))
styles.add(ParagraphStyle(name="H3x", fontName="Helvetica-Bold", fontSize=13, leading=16, textColor=INK, spaceAfter=5))
styles.add(ParagraphStyle(name="Bodyx", fontName="Helvetica", fontSize=10, leading=15, textColor=SECONDARY, spaceAfter=5))
styles.add(ParagraphStyle(name="Smallx", fontName="Helvetica", fontSize=8, leading=11, textColor=SECONDARY))
styles.add(ParagraphStyle(name="Microx", fontName="Helvetica", fontSize=7, leading=9, textColor=MUTED, tracking=1))
styles.add(ParagraphStyle(name="Metricx", fontName="Helvetica-Bold", fontSize=29, leading=32, textColor=INK))
styles.add(ParagraphStyle(name="WhiteH", fontName="Helvetica-Bold", fontSize=27, leading=30, textColor=colors.white, spaceAfter=8))
styles.add(ParagraphStyle(name="WhiteB", fontName="Helvetica", fontSize=10, leading=15, textColor=colors.HexColor("#B7C0CD")))
styles.add(ParagraphStyle(name="Quote", fontName="Helvetica", fontSize=20, leading=26, textColor=INK))


class CircuitGraphic(Flowable):
    def __init__(self, width=450, height=218, messy=False):
        super().__init__()
        self.width, self.height, self.messy = width, height, messy

    def draw(self):
        c = self.canv
        w, h = self.width, self.height
        node_color = RED if self.messy else BLUE
        c.setLineWidth(1)
        c.setStrokeColor(colors.HexColor("#D5DBE4"))
        traces = [
            [(0, h*.76), (w*.25, h*.76), (w*.38, h*.59), (w*.5, h*.59)],
            [(0, h*.23), (w*.27, h*.23), (w*.39, h*.42), (w*.5, h*.42)],
            [(w, h*.75), (w*.75, h*.75), (w*.62, h*.59), (w*.5, h*.59)],
            [(w, h*.25), (w*.75, h*.25), (w*.62, h*.42), (w*.5, h*.42)],
            [(w*.18, h), (w*.18, h*.78), (w*.31, h*.62)],
            [(w*.82, h), (w*.82, h*.78), (w*.69, h*.62)],
        ]
        for pts in traces:
            p = c.beginPath()
            p.moveTo(*pts[0])
            for pt in pts[1:]:
                p.lineTo(*pt)
            c.drawPath(p)
        if self.messy:
            c.setStrokeColor(colors.HexColor("#E9B9BC"))
            c.setDash(2, 4)
            for x, y, dx, dy in [(w*.22,h*.29,w*.42,h*.67),(w*.14,h*.77,w*.32,h*.33),(w*.84,h*.28,w*.63,h*.68)]:
                c.line(x,y,dx,dy)
            c.setDash()
        cx, cy = w/2, h/2
        c.setFillColor(colors.white)
        c.setStrokeColor(node_color)
        c.setLineWidth(1.3)
        c.circle(cx, cy, 35, fill=1, stroke=1)
        c.setStrokeColor(node_color)
        c.setLineWidth(1.7)
        p = c.beginPath()
        p.moveTo(cx-18,cy); p.lineTo(cx-8,cy); p.lineTo(cx-2,cy+10); p.lineTo(cx+7,cy-10); p.lineTo(cx+13,cy); p.lineTo(cx+20,cy)
        c.drawPath(p)
        for x, y in [(0,h*.76),(0,h*.23),(w,h*.75),(w,h*.25),(w*.18,h),(w*.82,h)]:
            c.setFillColor(colors.white); c.setStrokeColor(node_color); c.circle(x,y,3.2,fill=1,stroke=1)


def para(text, style="Bodyx"):
    return Paragraph(text, styles[style])


def card(title, copy, number=None, width=2.35*inch):
    top = para((f'<font color="#0A5CFF">{number} / </font>' if number else "") + title, "H3x")
    body = para(copy, "Smallx")
    t = Table([[top], [body]], colWidths=[width])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0),(-1,-1), colors.white),
        ("BOX", (0,0),(-1,-1), .6, LINE),
        ("LEFTPADDING", (0,0),(-1,-1), 12), ("RIGHTPADDING",(0,0),(-1,-1),12),
        ("TOPPADDING",(0,0),(-1,0),11), ("BOTTOMPADDING",(0,0),(-1,0),4),
        ("TOPPADDING",(0,1),(-1,1),0), ("BOTTOMPADDING",(0,1),(-1,1),12),
        ("VALIGN",(0,0),(-1,-1),"TOP"),
    ]))
    return t


def page_chrome(canvas, doc):
    canvas.saveState()
    width, height = letter
    canvas.setStrokeColor(LINE)
    canvas.setLineWidth(.6)
    canvas.line(doc.leftMargin, height-0.57*inch, width-doc.rightMargin, height-0.57*inch)
    canvas.drawImage(str(LOGO), doc.leftMargin, height-0.53*inch, width=1.12*inch, height=.42*inch, preserveAspectRatio=True, anchor="sw", mask="auto")
    canvas.setFont("Helvetica", 7)
    canvas.setFillColor(MUTED)
    canvas.drawRightString(width-doc.rightMargin, height-.39*inch, "FRONTEND DESIGN PREVIEW  /  OCT 2026")
    canvas.setStrokeColor(LINE)
    canvas.line(doc.leftMargin, .48*inch, width-doc.rightMargin, .48*inch)
    canvas.setFont("Helvetica", 7)
    canvas.setFillColor(MUTED)
    canvas.drawString(doc.leftMargin, .31*inch, "SYSTEMFIXAI  ·  SAMPLE CONTENT FOR DESIGN REVIEW")
    canvas.drawRightString(width-doc.rightMargin, .31*inch, f"{doc.page:02d}")
    canvas.restoreState()


doc = SimpleDocTemplate(str(OUT), pagesize=letter, rightMargin=.65*inch, leftMargin=.65*inch, topMargin=.75*inch, bottomMargin=.68*inch, title="SystemFixAI Frontend Design Preview", author="SystemFixAI")
story = []

# Page 1: signature hero and problem story
story += [Spacer(1, .12*inch), para("AI AUTOMATION AGENCY  /  SYSTEMS THAT RUN", "Eyebrow")]
brand = Image(str(LOGO), width=2.1*inch, height=1.05*inch, kind="proportional")
brand.hAlign = "LEFT"
story += [brand, para("We fix broken systems<br/><font color='#0A5CFF'>with AI.</font>", "HeroTitle"), para("SystemFixAI finds the manual, slow, error-prone work in your operations and replaces it with automations that run around the clock.", "Bodyx")]
story += [Spacer(1, 5), CircuitGraphic(width=7.05*inch, height=2.55*inch), Spacer(1, 6)]
story += [para("THE SYSTEM GAP", "Eyebrow"), para("Your business runs on duct tape.", "H2x"), para("Copy-pasting between tools. Leads that go cold in inboxes. Reports built by hand, every week.", "Bodyx")]
ba = Table([[CircuitGraphic(width=3.36*inch,height=1.48*inch,messy=True), CircuitGraphic(width=3.36*inch,height=1.48*inch)]], colWidths=[3.45*inch,3.45*inch])
ba.setStyle(TableStyle([("BACKGROUND",(0,0),(0,0),PANEL),("BACKGROUND",(1,0),(1,0),colors.white),("BOX",(0,0),(-1,-1),.6,LINE),("INNERGRID",(0,0),(-1,-1),.6,LINE),("LEFTPADDING",(0,0),(-1,-1),8),("RIGHTPADDING",(0,0),(-1,-1),8),("TOPPADDING",(0,0),(-1,-1),8),("BOTTOMPADDING",(0,0),(-1,-1),8)]))
story += [ba, Spacer(1, 8), para("BEFORE / DISCONNECTED                                      AFTER / CONNECTED", "Microx"), PageBreak()]

# Page 2: services
story += [Spacer(1, .15*inch), para("FOUR SYSTEMS / ONE AUTOMATION PARTNER", "Eyebrow"), para("From first message to back office.", "H2x"), para("Connect conversations, sales, content, and operations. Let automation carry the handoff from one step to the next.", "Bodyx"), Spacer(1, 13)]
service_data = [
    ("Customer conversations", "Email automation<br/>AI voice agent integration<br/>WhatsApp automation<br/>Instagram/Facebook DMs and comments<br/>Support chatbots"),
    ("Sales & bookings", "Lead generation and outreach<br/>Sales-to-CRM handoffs<br/>CRM automation<br/>Booking and reminders"),
    ("AI content engine", "AI content creation<br/>Content review and approval<br/>Repurpose content across channels"),
    ("Business operations", "Finance and accounting<br/>Invoice processing and payment reminders<br/>Reconciliation<br/>Legal and compliance<br/>Procurement and inventory"),
]
cards = [card(t,d,f"{i:02d}",width=3.3*inch) for i,(t,d) in enumerate(service_data,1)]
grid = Table([[cards[0],cards[1]],[cards[2],cards[3]]],colWidths=[3.55*inch]*2,rowHeights=[1.55*inch,1.55*inch])
grid.setStyle(TableStyle([("VALIGN",(0,0),(-1,-1),"TOP"),("LEFTPADDING",(0,0),(-1,-1),0),("RIGHTPADDING",(0,0),(-1,-1),7),("TOPPADDING",(0,0),(-1,-1),0),("BOTTOMPADDING",(0,0),(-1,-1),9)]))
story += [grid, Spacer(1, 15), para("YOUR CURRENT TOOLKIT", "Eyebrow"), para("Works with the tools you already use.", "H2x"), para("No rip-and-replace project. Connect the systems your team relies on today.", "Bodyx"), Spacer(1, 12)]
tools = ["Slack", "HubSpot", "Salesforce", "Notion", "Google Workspace", "Stripe", "Airtable", "n8n", "Make", "Zapier", "OpenAI", "Anthropic"]
tool_table = Table([[para(t,"H3x") for t in tools[i:i+4]] for i in range(0,12,4)],colWidths=[1.78*inch]*4,rowHeights=[.65*inch]*3)
tool_table.setStyle(TableStyle([("BOX",(0,0),(-1,-1),.5,LINE),("INNERGRID",(0,0),(-1,-1),.5,LINE),("BACKGROUND",(0,0),(-1,-1),PANEL),("ALIGN",(0,0),(-1,-1),"CENTER"),("VALIGN",(0,0),(-1,-1),"MIDDLE"),("LEFTPADDING",(0,0),(-1,-1),5),("RIGHTPADDING",(0,0),(-1,-1),5)]))
story += [tool_table, PageBreak()]

# Page 3: process and outcomes
story += [Spacer(1,.15*inch),para("A CLEAR PATH TO LIVE","Eyebrow"),para("From audit to autopilot in weeks.","H2x"),para("A short, collaborative process with working systems and clear ownership at every step.","Bodyx"),Spacer(1,12)]
steps = [("01 / 3 DAYS","Audit","Map the process, tools, and places work gets stuck.","PROCESS MAP"),("02 / 1 WEEK","Design","Agree on a scoped plan, safeguards, and success measure.",""),("03 / 2 WEEKS","Build","Connect the systems and test with your real workflow.","LIVE AUTOMATION"),("04 / 3 DAYS","Deploy","Launch with a clear handover and team walkthrough.",""),("05 / ONGOING","Optimize","Review performance and improve as the operation changes.","MONTHLY REPORT")]
step_data=[]
for n,t,d,chip in steps:
    step_data.append([para(n,"Eyebrow"),para(t,"H3x"),para(d,"Smallx"),para(f'<font color="#0A5CFF">{chip}</font>' if chip else "&nbsp;","Microx")])
st=Table([step_data],colWidths=[1.42*inch]*5)
st.setStyle(TableStyle([("VALIGN",(0,0),(-1,-1),"TOP"),("LINEABOVE",(0,0),(-1,0),1,BLUE),("LEFTPADDING",(0,0),(-1,-1),7),("RIGHTPADDING",(0,0),(-1,-1),7),("TOPPADDING",(0,0),(-1,-1),14),("BOTTOMPADDING",(0,0),(-1,-1),12),("BOX",(0,0),(-1,-1),.5,LINE)]))
story += [st,Spacer(1,23),para("MEASURABLE CHANGE","Eyebrow"),para("Numbers, not promises.","H2x"),para("Representative outcomes shown in the frontend concept. Confirm client figures before publication.","Bodyx"),Spacer(1,11)]
result_cards=[]
for metric, title, desc in [("−62%","Lead response time","A routing system assigns inquiries and starts follow-up."),("14 hrs/wk","Returned to the team","Live reporting replaces manual spreadsheet work."),("3.2×","Faster ticket triage","Incoming requests reach the right specialist sooner.")]:
    inner=Table([[para(metric,"Metricx")],[para(title,"H3x")],[para(desc,"Smallx")]],colWidths=[2.23*inch])
    inner.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),colors.white),("BOX",(0,0),(-1,-1),.6,LINE),("LEFTPADDING",(0,0),(-1,-1),11),("RIGHTPADDING",(0,0),(-1,-1),11),("TOPPADDING",(0,0),(-1,0),12),("BOTTOMPADDING",(0,0),(-1,-1),8)]))
    result_cards.append(inner)
rt=Table([result_cards],colWidths=[2.32*inch]*3)
rt.setStyle(TableStyle([("VALIGN",(0,0),(-1,-1),"TOP"),("LEFTPADDING",(0,0),(-1,-1),0),("RIGHTPADDING",(0,0),(-1,-1),8)]))
story += [rt,Spacer(1,16)]
stats=Table([[para("28<br/><font size='7' color='#8993A2'>SYSTEMS FIXED</font>","H3x"),para("1,240+<br/><font size='7' color='#8993A2'>HOURS SAVED</font>","H3x"),para("6 WEEKS<br/><font size='7' color='#8993A2'>AVG. PAYBACK</font>","H3x"),para("96%<br/><font size='7' color='#8993A2'>RETENTION</font>","H3x")]],colWidths=[1.76*inch]*4)
stats.setStyle(TableStyle([("LINEABOVE",(0,0),(-1,0),.7,LINE),("LINEBELOW",(0,0),(-1,0),.7,LINE),("TOPPADDING",(0,0),(-1,-1),12),("BOTTOMPADDING",(0,0),(-1,-1),12)]))
story += [stats, PageBreak()]

# Page 4: principles, testimonial, FAQ
story += [Spacer(1,.15*inch),para("HOW WE WORK","Eyebrow"),para("Built for the people who run it.","H2x"),para("A useful automation should make the day easier for the team doing the work.","Bodyx"),Spacer(1,11)]
principles=[("Fixed-scope pricing","No surprise invoices. The outcome and scope are clear before we build."),("Human in the loop","Your team approves decisions that need a person."),("You own everything","Workflows, code, and documentation are yours to keep."),("Monitored after launch","We stay close to production and catch issues early.")]
pr=Table([[card(a,b) for a,b in principles[:2]],[card(a,b) for a,b in principles[2:]]],colWidths=[3.55*inch,3.55*inch],rowHeights=[1.2*inch,1.2*inch])
pr.setStyle(TableStyle([("VALIGN",(0,0),(-1,-1),"TOP"),("LEFTPADDING",(0,0),(-1,-1),0),("RIGHTPADDING",(0,0),(-1,-1),9),("TOPPADDING",(0,0),(-1,-1),0),("BOTTOMPADDING",(0,0),(-1,-1),9)]))
story += [pr,Spacer(1,13),para("FROM THE OPERATIONS FLOOR","Eyebrow"),para("“Our Monday used to disappear into spreadsheets. Now the numbers are ready before the team arrives.”","Quote"),Spacer(1,8),para("ALEX MORGAN  /  COO, FIELDNOTE  /  14 HOURS PER WEEK BACK","Microx"),Spacer(1,18),para("COMMON QUESTIONS","Eyebrow"),para("A few things to know.","H2x")]
faq_data=[]
for q,a in [("How much does it cost?","A free audit comes first, then a fixed-scope proposal."),("How long until something is live?","Focused automations typically launch in two to four weeks."),("Which tools do you work with?","We connect CRMs, inboxes, forms, spreadsheets, support desks, databases, and APIs."),("Who owns the automations?","You own your workflows, code, documentation, and business data.")]:
    faq_data.append([para(q,"H3x"),para(a,"Smallx")])
fq=Table(faq_data,colWidths=[2.25*inch,4.85*inch])
fq.setStyle(TableStyle([("LINEABOVE",(0,0),(-1,0),.6,LINE),("LINEBELOW",(0,0),(-1,-1),.6,LINE),("LINEBELOW",(0,0),(-1,-2),.4,LINE),("VALIGN",(0,0),(-1,-1),"TOP"),("LEFTPADDING",(0,0),(-1,-1),7),("RIGHTPADDING",(0,0),(-1,-1),7),("TOPPADDING",(0,0),(-1,-1),8),("BOTTOMPADDING",(0,0),(-1,-1),8)]))
story += [fq, PageBreak()]

# Page 5: conversion-focused close
story += [Spacer(1,.28*inch),para("START WITH THE BOTTLENECK","Eyebrow"),para("Find out what’s broken.","H2x"),para("Free 30-minute system audit. No pitch deck.","Bodyx"),Spacer(1,14)]
cta_content=Table([[para("FREE AUDIT","Eyebrow"),para("WORK EMAIL","Microx")],[para("A focused conversation about the process, tools, and handoffs slowing your team down.","WhiteB"),para("you@company.com<br/><br/><font color='#FFFFFF'>[ Book my audit  → ]</font>","WhiteB")]],colWidths=[3.65*inch,3.35*inch],rowHeights=[.35*inch,1.0*inch])
cta_content.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),INK),("TEXTCOLOR",(0,0),(-1,-1),colors.white),("BOX",(0,0),(-1,-1),0,INK),("LEFTPADDING",(0,0),(-1,-1),17),("RIGHTPADDING",(0,0),(-1,-1),17),("TOPPADDING",(0,0),(-1,-1),12),("BOTTOMPADDING",(0,0),(-1,-1),12),("VALIGN",(0,0),(-1,-1),"MIDDLE")]))
story += [cta_content,Spacer(1,10),para("FREE  ·  30 MIN  ·  REPLY WITHIN 24H  ·  YOUR PROCESS, YOUR CALL","Microx"),Spacer(1,34)]
story += [para("A better system should feel clear.","H2x"),para("SystemFixAI finds the manual, slow, error-prone work in your operations and builds the automation to make it run smoothly.","Bodyx"),Spacer(1,18)]
closing=Table([[para("SYSTEMFIXAI","H3x"),para("SERVICES<br/><br/>AI agents<br/>Workflow automation<br/>Integrations","Smallx"),para("COMPANY<br/><br/>Work<br/>About<br/>Contact","Smallx"),para("LEGAL<br/><br/>Privacy<br/>Terms","Smallx")]],colWidths=[2.45*inch,1.55*inch,1.55*inch,1.45*inch])
closing.setStyle(TableStyle([("LINEABOVE",(0,0),(-1,-1),.6,LINE),("VALIGN",(0,0),(-1,-1),"TOP"),("LEFTPADDING",(0,0),(-1,-1),7),("RIGHTPADDING",(0,0),(-1,-1),7),("TOPPADDING",(0,0),(-1,-1),13)]))
story += [closing,Spacer(1,15),CircuitGraphic(width=7.05*inch,height=1.0*inch)]

doc.build(story,onFirstPage=page_chrome,onLaterPages=page_chrome)
print(OUT)
