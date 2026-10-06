from decimal import Decimal, ROUND_HALF_UP
import re
def r(x): return int(Decimal(x).quantize(Decimal(1),rounding=ROUND_HALF_UP))
def order(items, disc_pct=0, ongkir=0, paid=0):
    sub=sum(q*p for q,p in items); d=r(Decimal(sub)*Decimal(str(disc_pct))/100); s=sub-d; t=s+ongkir
    return dict(lines=[q*p for q,p in items], prices=[p for q,p in items], sub=sub, disc=d, after=s, ong=ongkir, tot=t, paid=paid, sisa=t-paid)
S={}
# scenario 1
o1=[order([(2,45000),(1,45000),(3,10000)],0,12000), order([(1,129000),(2,15000)],0,10000),
    order([(2,35000),(1,35000)],0,22000), order([(1,35000)],0,12000), order([(5,10000),(3,15000)],0,0),
    order([(2,129000)],0,22000,280000)]
full=[o1[i] for i in (0,1,2,4,5)]
agg1=dict(omzet=sum(o['after'] for o in full), ong=sum(o['ong'] for o in full), tag=sum(o['tot'] for o in full),
  belum=o1[0]['tot']+o1[2]['tot']+o1[4]['tot'], omzet_incl_fitri=sum(o['after'] for o in o1), tag_incl=sum(o['tot'] for o in o1))
S[1]=(o1,agg1)
o2=[order([(3,95000),(2,105000)],10,18000,200000), order([(4,85000),(1,95000)],12.5,25000,150000), order([(3,105000)],5,15000,314250)]
agg2=dict(omzet=sum(o['after'] for o in o2), ong=sum(o['ong'] for o in o2), tag=sum(o['tot'] for o in o2), belum=o2[0]['sisa']+o2[1]['sisa'])
S[2]=(o2,agg2)
o4=[order([(2,75000),(1,75000)],0,10000), order([(1,165000)],0,20000), order([(3,75000),(1,165000)],0,10000)]
agg4=dict(omzet=sum(o['after'] for o in o4), ong=sum(o['ong'] for o in o4), tag=sum(o['tot'] for o in o4), belum=sum(o['tot'] for o in o4))
S[4]=(o4,agg4)
for k,(os,ag) in S.items():
    allowed=set(ag.values())
    for o in os:
        for v in o['lines']+o['prices']+[o['sub'],o['disc'],o['after'],o['ong'],o['tot'],o['paid'],o['sisa']]: allowed.add(v)
    print('SKEN',k,[(o['sub'],o['disc'],o['tot'],o['sisa']) for o in os],ag)
    for side in ('s','b')+(('st','bt') if k==1 else ()):
        f={'s':f'out-s{k}.txt','b':f'out-b{k}.txt','st':'out-s1t.txt','bt':'out-b1t.txt'}[side]
        t=open(f).read()
        nums=[int(x.replace('.','')) for x in re.findall(r'(?<![\d.])(\d{1,3}(?:\.\d{3})+)(?![\d.])',t)]
        nums+= [int(x)*1000 for x in re.findall(r'(\d+)\s?rb\b',t)]
        nums+= [int(x) for x in re.findall(r'(?<![\d.,])(\d{4,7})(?![\d.,])',t) if 1000<=int(x)<=2000000]
        bad=sorted(set(n for n in nums if n not in allowed and n>=1000))
        print(' ',f,'angka di luar hitungan:',bad)
