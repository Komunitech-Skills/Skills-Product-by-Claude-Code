# Verifikasi independen putaran 1.0.1 (penguji), Decimal, tanpa kode skill
from decimal import Decimal as D, ROUND_FLOOR, ROUND_HALF_UP
def r0(x): return D(x).quantize(D(1), rounding=ROUND_HALF_UP)
def ppn(d): return (D(d)*11/100).to_integral_value(rounding=ROUND_FLOOR)
def split_incl(g):
    g=D(g); best=None
    for d in range(int(g*100/111)-5,int(g*100/111)+6):
        if d+ppn(d)<=g: best=d
    return D(best),ppn(best),g-best-ppn(best)
def pct(a,b): return (D(a)*100/D(b)).quantize(D('0.1'),rounding=ROUND_HALF_UP)
def skor(c,l,tg,t,k,qb,qn,w):
    mn=min(c.values()); ml=min(l.values()); o={}
    for x in c:
        sb=D(100)*mn/c[x]; sl=D(0) if (tg is not None and l[x]>tg) else D(100)*(ml+1)/(l[x]+1)
        dp,te=t[x]; hb=-dp/100*l[x]+(1-dp/100)*te; st=max(D(0),min(D(100),50+hb*D(50)/30))
        tot=(w[0]*sb+w[1]*sl+w[2]*st+w[3]*k.get(x,D(3))*20+w[4]*D(100)*qn/qb[x])/sum(w)
        o[x]=round(float(tot),2)
    return o
W0=[D(40),D(20),D(15),D(15),D(10)]
print("== S1: Sentosa bila PKP & belum PPN")
s=D(6826000); s_pkp=s+ppn(s); m=D(7625700)
print("Sentosa PKP total",s_pkp,"naik",ppn(s),"| Sentosa lebih murah dari Mitra",m-s_pkp)
print("skor:",skor({'S':s_pkp,'M':m,'B':D(7140000)},{'S':D(3),'M':D(4),'B':D(7)},D(5),{'S':(D(0),D(0)),'M':(D(0),D(30)),'B':(D(100),D(0))},{},{'S':D(600),'M':D(600),'B':D(600)},D(600),W0))
print("PPN atas ongkir Mitra", ppn(6870000)-ppn(6720000))
print("== S1V margarin 180 kg, tenggat 6")
A=D(380000)*12+D(8000)*12; d,p,sisa=split_incl(A); print("Lancar",A,"DPP",d,"PPN",p,"sisa",sisa,"per kg",(A/180).quantize(D('0.01')))
B=D(24900)*180; print("Rejeki",B,"impas ongkir",A-B,"per kg",((A-B)/180).quantize(D('0.01')))
C=D(23800)*200; C2=C+ppn(C); print("Margarindo",C2,"PPN",ppn(C),"per kg",(C2/180).quantize(D('0.01')),"modal tertahan",r0(C2/200*20))
print("selisih",A-B,pct(A-B,B),C2-B,pct(C2-B,B))
print("skor",skor({'L':A,'R':B,'M':C2},{'L':D(2),'R':D(1),'M':D(7)},D(6),{'L':(D(0),D(14)),'R':(D(0),D(0)),'M':(D(30),D(30))},{},{'L':D(180),'R':D(180),'M':D(200)},D(180),W0))
L2=D(380000)*24+D(8000)*24; print("2x: Rejeki",B*2,"Lancar",L2,"Margarindo",D(23800)*360+ppn(D(23800)*360))
bag=D(24900)*126+D(385000)*10+D(80000); print("bagi 70/30",bag,"lebih mahal",bag-B,pct(bag-B,B))
print("== S3 gula per 1 kg / 10 kg (tanpa PPN, bahan pokok)")
for q in (1,10,50): print(q,"kg: Makmur",15500*q,"Sinar",16200*q,"impas ongkir",700*q)
print("== S4 kertas: Sinar",52000*50+75000,"Abadi",54500*50, "Sinar lebih murah", 54500*50-(52000*50+75000))
print("skor",skor({'S':D(2675000),'A':D(2725000)},{'S':D(2),'A':D(1)},None,{'S':(D(0),D(14)),'A':(D(0),D(0))},{},{'S':D(50),'A':D(50)},D(50),W0))
ab=D(54500)*35; sn=D(52000)*15+75000; print("bagi 70/30 Abadi 35 + Sinar 15:",ab+sn,"vs Abadi",ab+sn-D(2725000))
