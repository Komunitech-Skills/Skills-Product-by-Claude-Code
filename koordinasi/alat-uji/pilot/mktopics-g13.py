"""Buat topik forum gelombang (N skill × TANPA/DENGAN). Jalankan hanya setelah persetujuan pemilik.
Pakai: bot_token=<token bot gateway yang dipakai> python3 mktopics-g13.py [msgs-g13.json]
Nama topik: "G13 <skill> — TANPA skill" / "— DENGAN skill". Keluaran: topik-g13.json."""
import json, os, sys, time, urllib.request, urllib.parse

tok = os.environ["bot_token"]  # token bot yang MENJALANKAN gateway (pemilik topik), tidak dicetak
C = "-1004407409583"
GEL = os.environ.get("GEL", "G13")
src = sys.argv[1] if len(sys.argv) > 1 else "msgs-g13.json"
sk = []
for m in json.load(open(src)):
    if m["skill"] not in sk:
        sk.append(m["skill"])

def tg(method, **kw):
    data = urllib.parse.urlencode(kw).encode()
    try:
        with urllib.request.urlopen(f"https://api.telegram.org/bot{tok}/{method}", data, timeout=40) as r:
            return json.load(r)
    except Exception as e:
        return {"ok": False, "description": type(e).__name__}

m = {}
for n in sk:
    for sisi, lab in (("sebelum", "TANPA skill"), ("sesudah", "DENGAN skill")):
        d = {}
        for _ in range(4):
            d = tg("createForumTopic", chat_id=C, name=f"{GEL} {n} — {lab}")
            if d.get("ok"):
                break
            time.sleep(3)
        if d.get("ok"):
            m[f"{n}|{sisi}"] = d["result"]["message_thread_id"]
        else:
            print("FAIL", n, sisi, d.get("description"))
        time.sleep(1.5)
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"topik-{GEL.lower()}.json")
json.dump(m, open(out, "w"), indent=1)
# isi field topic di msgs
msgs = json.load(open(src))
for x in msgs:
    x["topic"] = m.get(f"{x['skill']}|{x['sisi']}", x.get("topic", 0))
json.dump(msgs, open(src, "w"), ensure_ascii=False, indent=1)
print(m)
