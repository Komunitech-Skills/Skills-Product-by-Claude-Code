from decimal import Decimal as D, ROUND_HALF_UP, ROUND_CEILING
import json,sys,os
# Verifikasi independen uji ulang v1.0.1 (Decimal). Pakai: python3 verifikasi-uji-ulang.py 0*-uji-ulang.json 10-*-uji-ulang.json
def lvl(s): return "KRITIS" if s>=15 else "TINGGI" if s>=10 else "SEDANG" if s>=5 else "RENDAH"
for f in sys.argv[1:]:
    for r in json.load(open(f)):
        s=r["kemungkinan"]*r["dampak"]; print(os.path.basename(f)[:2], s, lvl(s), r["nama"][:40])
cases={"06":([1800000,650000,900000],3,6000000,6),"07":([2000000,7500000,800000,600000],3,12000000,12),
"08":([5000000,9000000,1500000,4000000],3,30000000,12),"kafe":([4500000,2800000*3,1700000,1200000],3,8000000,12)}
for k,(b,m,kas,c) in cases.items():
    t=sum(D(x) for x in b); T=t*m; K=max(D(0),T-kas); ci=(K/c).to_integral_value(ROUND_CEILING)
    print(k,"tetap",t,"target",T,"kurang",K,"cicil",ci,"cukup",(D(kas)/t).quantize(D("0.1"),ROUND_HALF_UP))
