"""Buat topik forum G29 (3 skill x TANPA/DENGAN = 6 topik BARU) untuk bot uji KEDUA @KTclaude2bot.
Topik dibuat oleh bot PENGUJI (env tester_bot_token, lewat tg.call). Token tidak pernah dicetak.
Pakai: python3 mktopics-g29.py [skill ...]   (tanpa argumen = ketiga skill)  -> topik-g29.json di folder ini,
lalu mengisi field "topic" di msgs-g29.json (termasuk 2 lanjutan "ya" kasir) (topik TANPA dipatch skills: [] lewat
patch-topik.py topik-g29.json; gateway WAJIB restart per PID sesudahnya). Idempoten: topik yang sudah ada tidak dibuat dobel."""
import json, os, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from tg import call

C = -1004407409583
# versi skill repo yang dipasang di home bot kedua (masuk nama topik)
V = {
    "kasir-lokal": "1.1.12",
    "fider-masukan-pelanggan": "1.0.11",
    "kanboard-papan-kerja": "1.0.7",
}
sk = sys.argv[1:] or list(V)
assert 1 <= len(sk) <= 3, "maks 3 skill (gelombang G29 = 8 pesan, maks 10)"
assert all(n in V for n in sk), f"skill tidak dikenal; pilih dari {list(V)}"
out = os.path.join(HERE, "topik-g29.json")
m = json.load(open(out)) if os.path.exists(out) else {}
for n in sk:
    for sisi, lab in (("sebelum", "TANPA skill"), ("sesudah", "DENGAN skill")):
        k = f"{n}|{sisi}"
        if m.get(k):
            continue  # idempoten: jangan buat topik dobel
        d = {}
        for _ in range(4):
            d = call("createForumTopic", chat_id=C, name=f"G29 {n} {V[n]} — {lab}")
            if d.get("ok") or d.get("http") == 400:
                break
            time.sleep(3)
        if d.get("ok"):
            m[k] = d["result"]["message_thread_id"]
            json.dump(m, open(out, "w"), indent=1)
        else:
            print("FAIL", k, d.get("description"))
        time.sleep(1.5)
# isi field topic di berkas pesan (kirim-urut2.py membaca m["topic"])
for nama in ("msgs-g29.json",):
    p = os.path.join(HERE, nama)
    msgs = json.load(open(p, encoding="utf-8"))
    for x in msgs:
        t = m.get(f"{x['skill']}|{x['sisi']}")
        if t:
            x["topic"] = t
    json.dump(msgs, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(m)
