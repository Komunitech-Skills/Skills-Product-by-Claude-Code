import sys, random, math
from datetime import date, timedelta
import os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "scripts"))
import peringatan_dini as P
def pois(r, lam):
    L=math.exp(-lam);k=0;p=1
    while True:
        p*=r.random()
        if p<L: return k
        k+=1
cols=["output_pcs","reject_pcs","penjualan_rp","keluhan","telat_kirim","absen"]
tot=0; cnt={1:0,2:0,3:0}; per={c:{1:0,2:0,3:0} for c in cols+["persen_reject"]}; sebab={}
for seed in range(300):
    r=random.Random(seed)
    rows=[["tanggal"]+cols]
    for i in range(45):
        t=date(2026,8,1)+timedelta(days=i)
        rows.append([t.isoformat(), str(round(r.gauss(2000,60))), str(pois(r,30)), str(round(r.gauss(9e6,4e5))),
                     str(pois(r,0.7)), str(pois(r,2)), str(pois(r,1.2))])
    a=P.buat_parser().parse_args(["x","--tanggal",(date(2026,8,1)+timedelta(days=44)).isoformat()])
    for d in range(30,45):
        a.tanggal=(date(2026,8,1)+timedelta(days=d)).isoformat()
        h=P.analisis(rows,a); tot+=1
        mx=max(m["level"] for m in h["metrik"])
        if mx: cnt[mx]+=1
        for m in h["metrik"]:
            if m["level"]:
                per[m["kolom"]][m["level"]]+=1
                for lv,tx in m["alasan"]:
                    if lv==m["level"]:
                        key=(m["kolom"],lv,"sigma3" if "3σ" in tx else "sigma2" if "2σ" in tx else "sisi" if "pola" in tx else "hari_sama" if "rata-rata hari" in tx else "target" if "target" in tx else "run" if "berturut" in tx else tx[:20]); sebab[key]=sebab.get(key,0)+1
print("hari laporan",tot)
for l in (3,2,1): print("hari dg level max",l, cnt[l], f"{cnt[l]/tot:.1%}")
for c,v in per.items(): print(c, {k:f"{x/tot:.1%}" for k,x in v.items()})
for k,v in sorted(sebab.items(), key=lambda x:-x[1])[:25]: print(k,v)
