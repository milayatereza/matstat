import re
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont as RTT
from fontTools.ttLib import TTFont as FT

MAIN="MarckScript-Regular.ttf"
FALL="/usr/share/fonts/truetype/dejavu/DejaVuSerif-Italic.ttf"
pdfmetrics.registerFont(RTT("Hand",MAIN)); pdfmetrics.registerFont(RTT("Fall",FALL))
CM=FT(MAIN).getBestCmap()
W,H=A4; LM=18*mm; RM=12*mm; ROW=9*mm; TOP=H-16*mm; BOT=14*mm
FS=15; INK=(0.10,0.15,0.45)

def fnt(ch): return "Hand" if (ord(ch) in CM and ch not in "·") else "Fall"
def runs(s):
    out=[]; 
    for ch in s:
        f=fnt(ch)
        if out and out[-1][0]==f: out[-1][1]+=ch
        else: out.append([f,ch])
    return out
def tw(s,fs=FS): return sum(pdfmetrics.stringWidth(t,f,fs*(0.86 if f=="Fall" else 1)) for f,t in runs(s))

TOK=re.compile(r"(\[\[.+?\|\|.+?\]\]|~.|@\{[^}]*\})")
def segs(s): return [t for t in TOK.split(s) if t]
def has_frac(s): return "[[" in s

def seg_w(t,fs):
    if t.startswith("[["):
        a,b=t[2:-2].split("||"); return max(lw(a,fs*.9),lw(b,fs*.9))+6
    if t.startswith("~"): return tw(t[1],fs)
    if t.startswith("@{"): return tw(t[2:-1],fs)+9
    return tw(t,fs)
def lw(s,fs): return sum(seg_w(t,fs) for t in segs(s))

def put(c,x,y,s,fs):
    for f,t in runs(s):
        sz=fs*(0.86 if f=="Fall" else 1); c.setFont(f,sz); c.drawString(x,y,t); x+=pdfmetrics.stringWidth(t,f,sz)
    return x
def draw_line(c,x,y,s,fs=FS):
    for t in segs(s):
        if t.startswith("[["):
            a,b=t[2:-2].split("||"); w=seg_w(t,fs); f2=fs*.9
            bar=y+.30*fs; c.setLineWidth(.8); c.line(x+1,bar,x+w-1,bar)
            put(c,x+(w-lw(a,f2))/2,bar+.28*fs,a,f2) if "~" not in a and "@{" not in a else draw_line(c,x+(w-lw(a,f2))/2,bar+.28*fs,a,f2)
            draw_line(c,x+(w-lw(b,f2))/2,bar-.82*fs,b,f2); x+=w
        elif t.startswith("~"):
            put(c,x,y,t[1],fs); w=tw(t[1],fs); c.setLineWidth(.8); c.line(x+w*.1,y+.62*fs,x+w*.95,y+.62*fs); x+=w
        elif t.startswith("@{"):
            inner=t[2:-1]; w=tw(inner,fs); c.setLineWidth(.8)
            p=c.beginPath(); p.moveTo(x,y+.3*fs); p.lineTo(x+2.5,y+.22*fs); p.lineTo(x+5,y-.15*fs); p.lineTo(x+8,y+.9*fs); p.lineTo(x+9+w,y+.9*fs); c.drawPath(p,stroke=1,fill=0)
            put(c,x+9,y,inner,fs); x+=w+9
        else: x=put(c,x,y,t,fs)
    return x

class Doc:
    def __init__(s,path,title=None):
        s.c=canvas.Canvas(path,pagesize=A4); s.y=TOP; s.newpage(first=True)
    def grid(s):
        c=s.c; c.setStrokeColorRGB(.78,.86,.95); c.setLineWidth(.4)
        y=TOP+ROW*0.0
        yy=TOP
        while yy>BOT-ROW: c.line(8*mm,yy,W-8*mm,yy); yy-=ROW
        x=8*mm
        while x<W-8*mm: c.line(x,BOT-ROW,x,TOP+ROW*0.0+ROW*0); x+=ROW
        c.setStrokeColorRGB(.95,.6,.6); c.setLineWidth(.8); c.line(LM-4*mm,BOT-ROW,LM-4*mm,TOP+6*mm)
        c.setFillColorRGB(*INK); c.setStrokeColorRGB(*INK)
    def newpage(s,first=False):
        if not first: s.c.showPage()
        s.grid(); s.y=TOP-ROW*0.75
    def need(s,rows):
        if s.y-(rows-1)*ROW < BOT: s.newpage()
    def line(s,text,indent=0,fs=FS,rows=None):
        r=rows or (2 if has_frac(text) else 1)
        s.need(r)
        if r==2: s.y-=ROW*0.55
        draw_line(s.c,LM+indent*mm,s.y,text,fs); s.y-=ROW*(1 if r==1 else 1.45)
    def para(s,text,indent=0,hang=0,fs=FS):
        maxw=W-LM-RM-indent*mm; words=text.split(" "); cur=""; first=True
        for w in words+[None]:
            t=(cur+" "+w).strip() if w is not None else cur
            if w is None or lw(t,fs)>maxw-(hang*mm if not first else 0):
                if cur: s.line(cur,indent+(0 if first else hang),fs); first=False
                cur=w or ""
            else: cur=t
    def gap(s,n=0.5): s.y-=ROW*n
    def head(s,text):
        s.need(2); s.line("",rows=1) if False else None
        s.c.setLineWidth(.9); s.line(text,fs=FS+2)
        s.c.line(LM,s.y+ROW*.78,LM+lw(text,FS+2),s.y+ROW*.78)
    def save(s): s.c.save()
