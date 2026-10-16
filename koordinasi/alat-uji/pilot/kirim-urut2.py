# Kirim pesan satu per satu; tunggu sesi topik selesai sebelum kirim berikutnya. Maks pesan = argumen.
import json, os, sys, time, datetime, subprocess, sqlite3
from tg import call

_default_db = os.path.expanduser(
    "~/komunitech-uji/openclaw-real/home/.openclaw/agents/main/agent/openclaw-agent.sqlite"
)
H = os.environ.get("OPENCLAW_AGENT_DB", _default_db)
def st(t):
    c=sqlite3.connect(f"file:{H}?mode=ro",uri=True)
    r=c.execute("select status,updated_at from session_nodes where session_key like ?",(f"%topic:{t}",)).fetchone(); c.close(); return r
def tunggu(t,lama=720,sejak_ms=0):
    # Hanya terima status yang DIPERBARUI setelah pesan dikirim (sejak_ms); status lama dari sesi
    # sebelumnya (mis. 'failed' karena router jatuh) diabaikan. Bila sampai habis waktu tidak ada
    # pembaruan sama sekali -> 'tidak-diterima' (gateway kemungkinan tidak menerima pesan).
    end=time.time()+lama; time.sleep(20); ada_baru=False
    while time.time()<end:
        r=st(t)
        if r and (r[1] or 0)>=sejak_ms:
            ada_baru=True
            if r[0] not in("running","active"): return r[0]
        time.sleep(10)
    return "masih-berjalan" if ada_baru else "tidak-diterima"
f,idx=sys.argv[1],[int(x) for x in sys.argv[2:]]
msgs=json.load(open(f)); log=open("sent-g2.jsonl","a")
for n,i in enumerate(idx):
    m=msgs[i]
    if n: time.sleep(25)
    kw=dict(chat_id=-1004407409583,message_thread_id=m["topic"],text=m["text"])
    if m.get("reply_id"): kw["reply_parameters"]={"message_id":m["reply_id"]}
    if m.get("balas"):
        rid=None
        for l in open("updates-g2.jsonl"):
            u=json.loads(l); x=u.get("message") or u.get("edited_message") or {}
            if x.get("message_thread_id")==m["topic"] and x.get("from",{}).get("username","").startswith("KTclaude") and not x.get("text","").startswith("Working"): rid=x["message_id"]
        if rid: kw["reply_parameters"]={"message_id":rid}
        else:
            # Grup memakai requireMention: tanpa balasan bot yang bisa di-reply, sebut bot secara eksplisit
            bot=os.environ.get("BOT_UJI_USERNAME","KTclaude2bot").lstrip("@")
            if "@"+bot not in kw["text"]: kw["text"]=f"@{bot} "+kw["text"]
        print("reply_to",rid,flush=True)
    t0_ms=int(time.time()*1000)-5000
    r=call("sendMessage",**kw)
    rec={"skill":m["skill"],"sisi":m["sisi"],"topic":m["topic"],"ok":r.get("ok"),"desc":r.get("description"),"message_id":r.get("result",{}).get("message_id"),"time":datetime.datetime.now().astimezone().isoformat(timespec="seconds")}
    rec["hasil"]=tunggu(m["topic"],sejak_ms=t0_ms); time.sleep(5); print(rec,flush=True); log.write(json.dumps(rec)+"\n"); log.flush()
