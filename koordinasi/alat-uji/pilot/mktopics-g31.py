"""G31: uji formal kasir-lokal 1.1.13 + absensi-lokal 1.0.11 di bot uji kedua (streaming.mode off), database bersih.
4 topik BARU (skill x TANPA/DENGAN). Pesan: scratchpad/g28/msgs-g28-asli.json (pesan pembuka kasir & absensi; msgs-g28.json di repo tidak memuat absensi) + msgs-g28-lanjutan.json (4 'ya', di luar kuota 10). Berkas msgs-g31.json dibangun ulang dengan sumber ini.
Urutan msgs-g31.json: [kasir TANPA, kasir TANPA ya, kasir DENGAN, kasir DENGAN ya, absensi TANPA, absensi TANPA ya, absensi DENGAN, absensi DENGAN ya]."""
import json, os, sys, time
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from tg import call
C = -1004407409583
V = {"kasir-lokal": "1.1.13", "absensi-lokal": "1.0.11"}
out = os.path.join(HERE, "topik-g31.json")
m = json.load(open(out)) if os.path.exists(out) else {}
for n in V:
    for sisi, lab in (("sebelum", "TANPA skill"), ("sesudah", "DENGAN skill")):
        k = f"{n}|{sisi}"
        if m.get(k): continue
        d = call("createForumTopic", chat_id=C, name=f"G31 {n} {V[n]} — {lab}")
        assert d.get("ok"), d
        m[k] = d["result"]["message_thread_id"]; json.dump(m, open(out, "w"), indent=1); time.sleep(1.5)
g = json.load(open(os.path.join(HERE, "msgs-g28.json"), encoding="utf-8"))
l = json.load(open(os.path.join(HERE, "msgs-g28-lanjutan.json"), encoding="utf-8"))
def pick(src, skill, sisi): return [dict(x) for x in src if x["skill"] == skill and x["sisi"] == sisi]
msgs = []
for n in V:
    for sisi in ("sebelum", "sesudah"):
        for x in pick(g, n, sisi) + pick(l, n, sisi):
            x["topic"] = m[f"{n}|{sisi}"]; x["gel"] = "G31"; x["versi"] = V[n]
            x["catatan"] = f"G31 formal {n} {V[n]} ({'TANPA' if sisi=='sebelum' else 'DENGAN'}), streaming.mode off, DB bersih"
            msgs.append(x)
json.dump(msgs, open(os.path.join(HERE, "msgs-g31.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(m); print([(i, x["skill"], x["sisi"], x.get("balas")) for i, x in enumerate(msgs)])
