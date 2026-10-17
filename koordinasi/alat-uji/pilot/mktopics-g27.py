"""Buat topik forum G27 (5 skill × TANPA/DENGAN) untuk bot uji KEDUA @KTclaude2bot.
Topik dibuat oleh bot PENGUJI (env tester_bot_token, lewat tg.call). Token tidak pernah dicetak.
Pakai: python3 mktopics-g27.py skill1 skill2 ...   -> topik-g27.json di folder ini."""
import json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tg import call

C = -1004407409583
# versi skill repo yang dipasang di home bot kedua (masuk nama topik)
V = {
    "siyuan-sop": "1.0.11",
    "odoo-usaha": "1.0.5",
    "kanboard-papan-kerja": "1.0.6",
    "inventree-gudang": "1.0.6",
    "hledger-usaha": "1.0.10",
}
sk = sys.argv[1:]
assert 1 <= len(sk) <= 5, "maks 5 skill (gelombang G27 = maks 10 pesan)"
assert all(n in V for n in sk), f"skill tidak dikenal; pilih dari {list(V)}"
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "topik-g27.json")
m = json.load(open(out)) if os.path.exists(out) else {}
for n in sk:
    for sisi, lab in (("sebelum", "TANPA skill"), ("sesudah", "DENGAN skill")):
        k = f"{n}|{sisi}"
        if k in m:
            continue  # idempoten: jangan buat topik dobel
        d = {}
        for _ in range(4):
            d = call("createForumTopic", chat_id=C, name=f"G27 {n} {V[n]} — {lab}")
            if d.get("ok") or d.get("http") == 400:
                break
            time.sleep(3)
        if d.get("ok"):
            m[k] = d["result"]["message_thread_id"]
            json.dump(m, open(out, "w"), indent=1)
        else:
            print("FAIL", k, d.get("description"))
        time.sleep(1.5)
print(m)
