import json,math,sys
def lvl(s): return "KRITIS" if s>=15 else "TINGGI" if s>=10 else "SEDANG" if s>=5 else "RENDAH"
for f in ["01-kafe-bekasi","02-bengkel-makassar","03-toko-online-jogja","05-warung-pasar"]:
    for r in json.load(open(sys.argv[1]+"/"+f+".json")): s=r["kemungkinan"]*r["dampak"]; print(f, r["nama"][:30], s, lvl(s))
for b,m,k in [((4500000,8400000,1700000,1200000),3,8000000),((7000000,900000,650000,500000),3,20000000),((0,2500000,600000,1000000),6,15000000)]:
    t=sum(b);T=t*m;K=max(0,T-k);print(t,T,K,round(k/t,2),"cicil12=",math.ceil(K/12),"cicil6=",math.ceil(K/6),"cicil3=",math.ceil(K/3))
