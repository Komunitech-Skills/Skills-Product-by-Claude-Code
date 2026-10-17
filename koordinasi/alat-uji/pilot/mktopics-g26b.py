"""Buat topik forum G26b (uji ulang 1 skill × TANPA/DENGAN) untuk bot uji KEDUA @KTclaude2bot.
Topik dibuat oleh bot PENGUJI (env tester_bot_token, lewat tg.call). Token tidak pernah dicetak.
Pakai: python3 mktopics-g26b.py buat-invoice   -> topik-g26b.json di folder ini."""
import json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tg import call

C = -1004407409583
V = "1.0.8"  # versi skill yang diuji ulang (masuk nama topik)
sk = sys.argv[1:]
assert len(sk) == 1, "G26b: tepat 1 skill (uji ulang buat-invoice)"
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "topik-g26b.json")
m = json.load(open(out)) if os.path.exists(out) else {}
for n in sk:
    for sisi, lab in (("sebelum", "TANPA skill"), ("sesudah", "DENGAN skill")):
        k = f"{n}|{sisi}"
        if k in m:
            continue  # idempoten: jangan buat topik dobel
        d = {}
        for _ in range(4):
            d = call("createForumTopic", chat_id=C, name=f"G26 {n} {V} — {lab}")
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
