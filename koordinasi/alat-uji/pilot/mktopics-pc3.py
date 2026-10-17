"""Buat 1 topik forum untuk uji ulang pantau-cron-openclaw 1.0.5 (DENGAN skill, bot kedua). Bot penguji @KTpenguji_bot."""
import json, os, subprocess, sys, time
tok = os.environ["tester_bot_token"]; C = "-1004407409583"
nama = "PC3 pantau-cron-openclaw 1.0.5 — DENGAN skill (uji ulang)"
d = {}
for _ in range(4):
    r = subprocess.run(["curl","-s","-X","POST",f"https://api.telegram.org/bot{tok}/createForumTopic","--data-urlencode",f"chat_id={C}","--data-urlencode",f"name={nama}"],capture_output=True,text=True)
    if r.stdout.strip(): d = json.loads(r.stdout); break
    time.sleep(3)
if not d.get("ok"): print("FAIL", d.get("description")); sys.exit(1)
t = d["result"]["message_thread_id"]
json.dump({"pantau-cron-openclaw|sesudah": t}, open("topik-pc3.json","w"), indent=1)
m = json.load(open("msgs-pc.json"))
for x in m: x["topic"] = t
json.dump(m, open("msgs-pc3.json","w"), ensure_ascii=False, indent=1)
print("topik", t)
