# Verifikasi independen (penguji), Decimal, tanpa memakai kode skill
from decimal import Decimal as D, ROUND_FLOOR, ROUND_HALF_UP, ROUND_CEILING
def r0(x): return D(x).quantize(D(1), rounding=ROUND_HALF_UP)
def fl(x): return D(x).to_integral_value(rounding=ROUND_FLOOR)
def ppn(dpp): return fl(D(dpp)*D(11)/D(100))
def ppn12(dpp): return fl(D(dpp)*D(12)/D(100)*D(11)/D(12))
def split_incl(g):
    g=D(g); best=None
    for d in range(int(g*100/111)-5, int(g*100/111)+6):
        if d+ppn(d)<=g: best=d
    return D(best), ppn(best), g-best-ppn(best)
def pct(a,b): return (D(a)*100/D(b)).quantize(D('0.1'), rounding=ROUND_HALF_UP)
def score(costs, leads, tenggat, terms, kual, qb, qn, w):
    mn=min(costs.values()); ml=min(leads.values()); out={}
    for k in costs:
        sb=D(100)*mn/costs[k]
        sl=D(0) if (tenggat is not None and leads[k]>tenggat) else D(100)*(ml+1)/(leads[k]+1)
        dp,tempo=terms[k]; hb=-dp/D(100)*leads[k]+(1-dp/D(100))*tempo
        st=max(D(0),min(D(100),D(50)+hb*D(50)/D(30)))
        sk=kual.get(k,D(3))*20; sm=D(100)*qn/qb[k]
        tot=(w[0]*sb+w[1]*sl+w[2]*st+w[3]*sk+w[4]*sm)/sum(w)
        out[k]=[round(float(x),2) for x in (sb,sl,st,sk,sm,tot)]
    return out
print("== S1 tepung 600 kg, tenggat 5")
A=r0(D(118000)*60); Ad=r0(A*D('0.05')); At=A-Ad+100000
print("Sentosa subtotal",A,"diskon",Ad,"total",At,"per kg",(At/600).quantize(D('0.01')))
Bs=D(11200)*600+150000; Bp=ppn(Bs); Bt=Bs+Bp; Bp_noong=ppn(D(11200)*600)
print("Mitra DPP",Bs,"PPN",Bp,"(12x11/12:",ppn12(Bs),") total",Bt,"per kg",(Bt/600).quantize(D('0.01')),"| bila ongkir tak kena PPN: PPN",Bp_noong,"total",D(11200)*600+Bp_noong+150000)
Ct=D(11900)*600; print("Berkah total",Ct)
print("selisih Mitra",Bt-At,pct(Bt-At,At),"% | Berkah",Ct-At,pct(Ct-At,At),"%")
print("potensi PPN Sentosa",ppn(At))
c={'S':At,'M':Bt,'B':Ct}; l={'S':D(3),'M':D(4),'B':D(7)}; t={'S':(D(0),D(0)),'M':(D(0),D(30)),'B':(D(100),D(0))}
print(score(c,l,D(5),t,{},{'S':D(600),'M':D(600),'B':D(600)},D(600),[D(40),D(20),D(15),D(15),D(10)]))
# 2x
A2=r0(D(118000)*120); A2t=A2-r0(A2*D('0.05'))+100000; B2=D(11200)*1200+150000; B2t=B2+ppn(B2); C2=D(11900)*1200
print("2x:",A2t,B2t,C2, "per kg", (A2t/1200).quantize(D('0.01')),(B2t/1200).quantize(D('0.01')))
# bagi 70/30
a=D(118000)*42+100000; b=D(11200)*300+150000; b=b+ppn(b); print("bagi 70/30:",a,b,a+b,"tambahan",a+b-At,pct(a+b-At,At))
# Sentosa bila 'di atas 50 dus' dibaca >=50 sama saja utk 60 dus
print("== S2 box kue 1000 pcs, tenggat 7")
m_g=D(2100)*1000+120000; d,p,s=split_incl(m_g); print("Mandiri gross",m_g,"DPP",d,"PPN",p,"sisa",s)
k_t=D(135000)/50*1000+D(15000)*20; print("Kilat",k_t)
kj=D(2400)*1000; print("Karton Jaya",kj,"(+biaya ambil)")
pn=D(2300)*1000; pnp=ppn(pn); print("Pack Nusantara",pn,"PPN",pnp,"total",pn+pnp)
c={'Mandiri':m_g,'Kilat':k_t,'Karton':kj,'Pack':pn+pnp}; l={'Mandiri':D(10),'Kilat':D(1),'Karton':D(7),'Pack':D(7)}
t={'Mandiri':(D(50),D(0)),'Kilat':(D(0),D(0)),'Karton':(D(0),D(14)),'Pack':(D(0),D(30))}
k={'Mandiri':D(4),'Pack':D(4)}; qb={x:D(1000) for x in c}
for nm,w in (("default",[40,20,15,15,10]),("acara/cepat ref",[30,40,10,15,5])):
    print(nm,score(c,l,D(7),t,k,qb,D(1000),[D(x) for x in w]))
for x in c: print(x,"selisih",c[x]-min(c.values()),pct(c[x]-min(c.values()),min(c.values())),"per pcs",(c[x]/1000).quantize(D('0.01')))
