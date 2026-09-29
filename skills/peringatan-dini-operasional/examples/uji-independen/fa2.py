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
for lam in (0.7, 3, 7, 15, 30):
    tot=0; lv={1:0,2:0,3:0}; hs={1:0,2:0}; sg3=0
    for seed in range(300):
        r=random.Random(seed*7+int(lam*10))
        rows=[["tanggal","telat_kirim"]]+[[(date(2026,8,1)+timedelta(days=i)).isoformat(), str(pois(r,lam))] for i in range(45)]
        a=P.buat_parser().parse_args(["x"])
        for d in range(30,45):
            a.tanggal=(date(2026,8,1)+timedelta(days=d)).isoformat()
            m=P.analisis(rows,a)["metrik"][0]; tot+=1
            if m["level"]: lv[m["level"]]+=1
            for l,t in m["alasan"]:
                if "rata-rata hari" in t: hs[l]+=1
                if "3σ" in t: sg3+=1
    print(f"Poisson λ={lam}: hari {tot} | merah {lv[3]/tot:.1%} oranye {lv[2]/tot:.1%} kuning {lv[1]/tot:.1%} | aturan hari-sama: oranye {hs[2]/tot:.1%} kuning {hs[1]/tot:.1%} | 3σ {sg3/tot:.2%}")
