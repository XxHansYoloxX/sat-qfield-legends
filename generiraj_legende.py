# -*- coding: utf-8 -*-
"""Generira tri legendne slike za QField teren. Arial font (Windows)."""
from PIL import Image, ImageDraw, ImageFont

FONT = r"C:\Windows\Fonts\arial.ttf"
FONTB = r"C:\Windows\Fonts\arialbd.ttf"

RAINBOW = [(179,0,0),(242,89,0),(255,191,0),(191,230,0),
           (0,191,77),(0,166,230),(0,51,217),(51,0,115)]

def lerp(c1,c2,t): return tuple(int(c1[i]+(c2[i]-c1[i])*t) for i in range(3))
def grad(stops,t):
    if t<=0: return stops[0]
    if t>=1: return stops[-1]
    n=len(stops)-1; pos=t*n; i=int(pos); return lerp(stops[i],stops[i+1],pos-i)

def bar(draw,x,y,w,h,stops,lf,rt,fs):
    for px in range(w):
        draw.line([(x+px,y),(x+px,y+h)],fill=grad(stops,px/(w-1)))
    draw.rectangle([x,y,x+w,y+h],outline=(80,80,80),width=1)
    draw.text((x,y+h+4),lf,fill=(40,40,40),font=fs)
    rb=draw.textbbox((0,0),rt,font=fs); draw.text((x+w-(rb[2]-rb[0]),y+h+4),rt,fill=(40,40,40),font=fs)

def wrap(t,f,mw,d):
    words=t.split(); lines=[]; cur=""
    for wd in words:
        test=(cur+" "+wd).strip()
        if d.textbbox((0,0),test,font=f)[2]<=mw: cur=test
        else:
            if cur: lines.append(cur)
            cur=wd
    if cur: lines.append(cur)
    return lines

def make(fn,naslov,smer,sp,sl,sr,idx):
    W=1000
    ft=ImageFont.truetype(FONTB,40); fsm=ImageFont.truetype(FONTB,24)
    fn_=ImageFont.truetype(FONTB,28); fk=ImageFont.truetype(FONTB,21)
    fd=ImageFont.truetype(FONT,20); fb=ImageFont.truetype(FONT,19)
    PAD=40; bw=W-2*PAD; bh=34
    tmp=Image.new("RGB",(W,10)); d=ImageDraw.Draw(tmp)
    y=PAD+50+14+30+bh+22+10
    sl_=wrap(smer,fsm,bw,d); y+=len(sl_)*30+20
    for (im,pal,lf,rt,kr,dl) in idx:
        y+=38+bh+26+6
        y+=len(wrap("\u25ba "+kr,fk,bw,d))*27+4
        y+=len(wrap(dl,fd,bw,d))*26+26
    H=y+PAD
    img=Image.new("RGB",(W,H),(255,255,255)); draw=ImageDraw.Draw(img)
    yy=PAD
    draw.text((PAD,yy),naslov,fill=(20,20,20),font=ft); yy+=64
    draw.line([(PAD,yy),(W-PAD,yy)],fill=(200,200,200),width=2); yy+=16
    draw.text((PAD,yy),"Smer barv za ta sklop:",fill=(20,20,20),font=fsm); yy+=34
    bar(draw,PAD,yy,bw,bh,sp,sl,sr,fb); yy+=bh+24
    for ln in wrap(smer,fsm,bw,draw): draw.text((PAD,yy),ln,fill=(60,60,60),font=fsm); yy+=30
    yy+=22
    for (im,pal,lf,rt,kr,dl) in idx:
        draw.text((PAD,yy),im,fill=(15,15,15),font=fn_); yy+=38
        bar(draw,PAD,yy,bw,bh,pal,lf,rt,fb); yy+=bh+26
        for ln in wrap("\u25ba "+kr,fk,bw,draw): draw.text((PAD,yy),ln,fill=(0,90,40),font=fk); yy+=27
        yy+=4
        for ln in wrap(dl,fd,bw,draw): draw.text((PAD,yy),ln,fill=(70,70,70),font=fd); yy+=26
        yy+=26
    img.save(fn,"PNG"); print("  ",fn)

VEG=RAINBOW; VODA=RAINBOW; INV=list(reversed(RAINBOW))
import os
os.chdir(r"C:\Users\nikok\sat-qfield-legends")
print("Generiram:")

make("legenda_1_vegetacija.png","Vegetacijski indeksi",
 "Modra = bujna, zdrava rast. Rde\u010da = slaba/redka vegetacija ali gola tla. Zelena in rumena sta vmesni stanji.",
 VEG,"nizko / slabo","visoko / bujno",
 [("NDVI \u2014 splo\u0161no zdravje rastlin",VEG,"golo / stres","bujno",
   "Modra = gosta zdrava rast, rde\u010da = golo ali pod stresom.",
   "Najpogostej\u0161i indeks za hiter pregled stanja posevkov. Poka\u017ee, kje rastline dobro rastejo (modra/zelena) in kje zaostajajo (rumena/rde\u010da). Pri zelo gosti vegetaciji se zasi\u010di - takrat raje uporabi EVI2 ali NDRE."),
  ("EVI / EVI2 \u2014 izbolj\u0161an vegetacijski indeks",VEG,"redko","gosto",
   "Modra = zelo gosta biomasa, rde\u010da = malo vegetacije.",
   "Bolj\u0161i od NDVI pri gosti vegetaciji (koruza, \u017eita pred \u017eetvijo), kjer NDVI ne razlikuje ve\u010d dobro. Uporabi v polni rastni sezoni za lo\u010devanje gosto od zelo gosto."),
  ("SAVI \u2014 indeks s korekcijo za tla",VEG,"gola tla","bujno",
   "Modra = bujna rast, rde\u010da = gola/vidna tla.",
   "Kot NDVI, a popravljen za vpliv golih tal med rastlinami. Bolj\u0161i v zgodnji sezoni ali pri redki rasti, ko se med posevki vidi zemlja (vznik, mlade rastline)."),
  ("NDRE \u2014 Red Edge (du\u0161ik/klorofil)",VEG,"pomanjkanje N","dober N",
   "Modra = veliko klorofila (dober du\u0161ik), rde\u010da = pomanjkanje.",
   "Ob\u010dutljiv na klorofil v gostih posevkih. Uporaben za oceno preskrbe z du\u0161ikom in kot opozorilo na pomanjkanje. POZOR: zanesljiv le do dolo\u010dene faze razvoja, kasneje ga zameglja koli\u010dina biomase (glej tudi vi\u0161ino sestoja)."),
  ("Klorofil (Red Edge)",VEG,"malo","veliko",
   "Modra = veliko klorofila (zdravo), rde\u010da = malo (stres/zorenje).",
   "Neposredna ocena vsebnosti klorofila v listih. Visoke vrednosti pomenijo aktivno fotosintezo in zdravo rast; nizke nakazujejo stres ali za\u010detek zorenja."),
  ("LAI \u2014 indeks listne povr\u0161ine",VEG,"gola tla","gosta kro\u0161nja",
   "Modra = gosta listna masa, rde\u010da = malo listja / gola tla.",
   "Oceni koli\u010dino listne povr\u0161ine na enoto tal (biomaso). Uporabno za oceno bujnosti sestoja in npr. \u010dasa ko\u0161nje pri krmnih rastlinah.")])

make("legenda_2_voda.png","Voda in vlaga",
 "Modra = voda ali mokra/vla\u017ena tla. Rde\u010da = suho. Pri teh slojih modra NE pomeni vegetacije, ampak vodo/vlago.",
 VODA,"suho","voda / mokro",
 [("Moisture Index (NDMI) \u2014 vla\u017enost",VODA,"su\u0161ni stres","dovolj vlage",
   "Modra = dovolj vlage, rde\u010da = su\u0161ni stres.",
   "Poka\u017ee vla\u017enost vegetacije in tal. Zelo uporaben v vro\u010dih/su\u0161nih mesecih (jun-avg) za zgodnje zaznavanje su\u0161e - rde\u010da obmo\u010dja so pod vodnim stresom \u0161e preden se vidi na NDVI."),
  ("SWIR / MNDWI \u2014 zaznava vode",VODA,"suho","voda",
   "Modra = voda, rde\u010da = suho.",
   "Bolj zanesljivo lo\u010duje vodo od mokrih tal in vegetacije kot navadni NDWI. Uporabno za zaznavanje stoje\u010de vode in mokrih obmo\u010dij na njivah."),
  ("NDWI \u2014 voda na povr\u0161ini",VODA,"suho","voda / poplava",
   "Modra = voda (mlake, poplave), rde\u010da = suho.",
   "Zazna stoje\u010do vodo na povr\u0161ini. Najbolj uporabno po obilnem de\u017eju za pregled, kje zastaja voda in se pojavljajo poplavljena obmo\u010dja na parcelah.")])

make("legenda_3_posebni.png","Posebni indeksi (obrnjena logika)",
 "POZOR: pri teh dveh je barva obrnjena po POMENU. Modra ostaja dobro/zeleno, rde\u010da pa pomeni gola tla oz. zorenje - ne slabo v obi\u010dajnem smislu.",
 INV,"vegetacija / mlado","gola tla / zrelo",
 [("BSI \u2014 indeks golih tal",INV,"vegetacija","gola / suha tla",
   "Modra = pokrita tla / vegetacija, rde\u010da = gola ali suha tla.",
   "Poka\u017ee, kje so tla gola oz. preorana (rde\u010da) in kje je vegetacijska pokrovnost (modra). Uporabno po setvi za nadzor vznika in po \u017eetvi za stanje strni\u0161\u010da."),
  ("PSRI \u2014 zorenje / senescenca",INV,"zelena rast","zorenje / zrelo",
   "Modra = zelena aktivna rast, rde\u010da = zorenje/zrelost.",
   "Poka\u017ee fazo zorenja. Ko posevek dozoreva (su\u0161i se, rumeni), gre proti rde\u010di. PRAKTI\u010cNO: ko polje na PSRI postane rde\u010de, je dozorelo - uporabno za na\u010drtovanje \u017eetve. Rumeno-oran\u017eno pomeni, da se \u017eetev pribli\u017euje.")])
print("Koncano.")
