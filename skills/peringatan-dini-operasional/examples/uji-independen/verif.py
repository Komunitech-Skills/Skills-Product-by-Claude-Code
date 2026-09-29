#!/usr/bin/env python3
"""Verifikator independen (penguji). Dihitung dari truth JSON generator (angka asli, bukan hasil parse
script) memakai modul statistics + Decimal, lalu dibandingkan dengan JSON script.
Level dihitung ulang dari tabel aturan di references/cara-kerja-aturan.md (dibaca sebagai spesifikasi).
Pemakaian: verif.py truth.json script.json [--lead N] [--lead-kol kol=N] [--target kol=v] [--tgl YYYY-MM-DD]
"""
import json, math, statistics as st, sys
from datetime import date, timedelta
from decimal import Decimal as D, ROUND_FLOOR, getcontext
getcontext().prec = 28

NAIK = ("reject", "telat", "absen", "downtime", "retur", "keluhan", "waste")
TURUN = ("output", "penjualan", "transaksi", "pengiriman")

def arah_dari(k):
    if any(w in k for w in NAIK): return "naik"
    if any(w in k for w in TURUN): return "turun"
    return "dua"

def q4(x):
    return None if x is None else D(x).quantize(D("0.0001"))

def main():
    truth = json.load(open(sys.argv[1])); out = json.load(open(sys.argv[2]))
    opts = sys.argv[3:]
    lead_umum, lead_kol, target = 2, {}, {}
    for i, o in enumerate(opts):
        if o == "--lead": lead_umum = int(opts[i + 1])
        if o == "--lead-kol": k, v = opts[i + 1].split("="); lead_kol[k] = int(v)
        if o == "--target": k, v = opts[i + 1].split("="); target[k] = D(v)
    tgl = date.fromisoformat(out["tanggal_laporan"])
    ser = {k: sorted((date.fromisoformat(t), D(str(v))) for t, v in d.items() if date.fromisoformat(t) <= tgl)
           for k, d in truth.items()}
    # % reject
    rj = next((k for k in ser if "reject" in k), None); op = next((k for k in ser if "output" in k), None)
    if rj and op:
        o = dict(ser[op]); ser["persen_reject"] = [(t, v / o[t] * 100) for t, v in ser[rj] if o.get(t)]
    cek = beda = 0
    def banding(nama, mine, theirs):
        nonlocal cek, beda
        cek += 1
        a = q4(mine) if mine is not None else None
        b = D(theirs) if theirs is not None else None
        ok = (a is None and b is None) or (a is not None and b is not None and abs(a - b) <= D("0.0001"))
        if not ok:
            beda += 1; print("  BEDA", nama, "verif=", a, "script=", b)
    metrik = {m["kolom"]: m for m in out["metrik"]}
    for k, titik in ser.items():
        m = metrik.get(k)
        if k.startswith("stok_"):
            pk = "pakai_" + k[5:]
            pak = [v for t, v in ser[pk] if t <= tgl][-7:]
            rp = sum(pak) / len(pak)
            sisa = titik[-1][1]
            hari = (sisa / rp).quantize(D("0.1"), rounding=ROUND_FLOOR)
            L = lead_kol.get(k, lead_umum)
            lv = 3 if hari <= L else 2 if hari <= 2 * L else 1 if hari <= 3 * L else 0
            banding(k + ".rata_pakai", rp, m["rata_pakai"]); banding(k + ".sisa_hari", hari, m["sisa_hari"])
            cek += 2
            if m["perkiraan_habis"] != (tgl + timedelta(days=int(hari))).isoformat(): beda += 1; print("  BEDA habis")
            if m["level"] != lv: beda += 1; print("  BEDA level stok", k, lv, m["level"])
            print(f"  {k}: sisa {sisa} rata pakai {rp:.4f} -> {hari} hari (lead {L}) level {lv}")
            continue
        if k.startswith("pakai_") or m is None:
            continue
        v = titik[-1][1]; vals = [x for _, x in titik]
        # rata7
        banding(k + ".rata7", sum(vals[-7:]) / 7 if len(vals) >= 7 else None, m.get("rata7"))
        if len(vals) >= 14:
            banding(k + ".rata7_seb", sum(vals[-14:-7]) / 7, m.get("rata7_sebelumnya"))
        # garis dasar
        dasar = titik[:-1][-28:]
        dv = [x for _, x in dasar]
        mean = sd = None; pencilan = []
        if len(dv) >= 2:
            mean, sd = st.mean(dv), st.stdev(dv)
            if len(dv) >= 14 and sd > 0:
                bersih = [x for x in dv if abs(x - mean) / sd <= 3]
                pencilan = [t.isoformat() for t, x in dasar if abs(x - mean) / sd > 3]
                if len(bersih) < len(dv):
                    dv = bersih; mean, sd = st.mean(dv), st.stdev(dv)
        z = (v - mean) / sd if (len(dv) >= 14 and sd) else None
        if m.get("dasar", {}).get("rata") is not None:
            banding(k + ".dasar.rata", mean, m["dasar"]["rata"]); banding(k + ".dasar.sd", sd, m["dasar"]["sd"])
            if z is not None:
                banding(k + ".batas_atas_2", mean + 2 * sd, m["dasar"]["batas_atas_2"])
                banding(k + ".batas_atas_3", mean + 3 * sd, m["dasar"]["batas_atas_3"])
                banding(k + ".batas_bawah_2", max(D(0), mean - 2 * sd), m["dasar"]["batas_bawah_2"])
                banding(k + ".batas_bawah_3", max(D(0), mean - 3 * sd), m["dasar"]["batas_bawah_3"])
            if pencilan != m["dasar"]["pencilan_diabaikan"]: beda += 1; print("  BEDA pencilan", pencilan, m["dasar"]["pencilan_diabaikan"])
        banding(k + ".z", z, m.get("z"))
        # tren (x = hari kalender sejak awal jendela)
        awal = tgl - timedelta(days=6)
        jd = [(float((t - awal).days), float(x)) for t, x in titik if t >= awal]
        slope = r2 = None
        if len(jd) >= 5:
            xs, ys = zip(*jd)
            slope = st.linear_regression(xs, ys).slope
            r2 = st.correlation(xs, ys) ** 2 if len(set(ys)) > 1 else 0.0
        tr = m.get("tren")
        if slope is not None:
            cek += 2
            if abs(slope - float(tr["kemiringan_per_hari"])) > 1e-4 or abs(r2 - float(tr["r2"])) > 1e-4:
                beda += 1; print("  BEDA tren", slope, r2, tr)
        # hari sama
        peta = dict(titik)
        sama = [peta[tgl - timedelta(days=7 * w)] for w in range(1, 5) if tgl - timedelta(days=7 * w) in peta]
        hs = None
        if len(sama) >= 2:
            rs = st.mean(sama); hs = (rs, (v - rs) / rs * 100 if rs else None)
            banding(k + ".hari_sama.rata", rs, m["hari_sama"]["rata"])
            banding(k + ".hari_sama.persen", hs[1], m["hari_sama"]["selisih_persen"])
        # beruntun
        def run(a):
            c = 0
            for i in range(len(titik) - 1, 0, -1):
                (t0, x0), (t1, x1) = titik[i - 1], titik[i]
                if (t1 - t0).days > 3: break
                if (a == "naik" and x1 > x0) or (a == "turun" and x1 < x0): c += 1
                else: break
            return c
        cek += 2
        if run("naik") != m["naik_beruntun"] or run("turun") != m["turun_beruntun"]: beda += 1; print("  BEDA beruntun")
        # level ulang dari tabel aturan
        arah = "naik" if k == "persen_reject" else arah_dari(k)
        T = target.get(k, D(m["target"]) if m.get("target") else None)
        lv = 0; alasan = []
        for a in ([arah] if arah != "dua" else ["naik", "turun"]):
            sg = 1 if a == "naik" else -1
            if z is not None:
                if z * sg >= 3: lv = max(lv, 3); alasan.append("3σ")
                elif z * sg >= 2: lv = max(lv, 2); alasan.append("2σ")
                side = 0
                for x in reversed(vals):
                    if (x - mean) * sg > 0: side += 1
                    else: break
                if side >= 7: lv = max(lv, 2); alasan.append(f"sisi{side}")
            kb = run(a)
            if kb >= 5: lv = max(lv, 2); alasan.append(f"run{kb}")
            elif kb >= 3 and arah != "dua": lv = max(lv, 1); alasan.append(f"run{kb}")
            if hs and hs[1] is not None and arah != "dua" and hs[0] >= 5:
                p = hs[1] * sg
                if p >= 35: lv = max(lv, 2); alasan.append("hs35")
                elif p >= 20: lv = max(lv, 1); alasan.append("hs20")
        if T is not None and arah != "dua":
            buruk = (lambda x: x > T) if arah == "naik" else (lambda x: x < T)
            l7 = sum(1 for x in vals[-7:] if buruk(x))
            if buruk(v):
                rel = abs((v - T) / T * 100) if T else D(100)
                tl = 3 if rel >= 50 else 2 if rel >= 10 else 1
                if l7 >= 3: tl = max(tl, 2)
                lv = max(lv, tl); alasan.append(f"target{tl}")
            elif l7 >= 3:
                lv = max(lv, 1); alasan.append("target7")
            elif slope is not None and r2 >= 0.5 and ((arah == "naik" and slope > 0) or (arah == "turun" and slope < 0)):
                sh = (float(T) - float(v)) / slope
                if 0 < sh <= 7: lv = max(lv, 1); alasan.append("proyeksi")
        cek += 1
        if lv != m["level"]: beda += 1; print("  BEDA level", k, lv, m["level"], alasan)
        print(f"  {k}: v={v} z={None if z is None else round(z,2)} mean={None if mean is None else round(mean,2)} sd={None if sd is None else round(sd,3)} "
              f"slope={None if slope is None else round(slope,3)} r2={None if r2 is None else round(r2,3)} hs={None if not hs else (round(hs[0],2), None if hs[1] is None else round(hs[1],1))} level={lv} {alasan}")
    print(f"TOTAL cek={cek} beda={beda}")
    return beda

if __name__ == "__main__":
    sys.exit(1 if main() else 0)
