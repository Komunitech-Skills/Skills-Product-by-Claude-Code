# Read-only poller: only getUpdates, never sends anything.
import json, time, sys, datetime
from tg import call
end=time.time()+int(sys.argv[1]); off=None
out=open('updates-g2.jsonl','a')
while time.time()<end:
    kw={"timeout":25}
    if off: kw["offset"]=off
    r=call("getUpdates",**kw)
    for u in r.get("result",[]):
        off=u["update_id"]+1
        u["_recv"]=datetime.datetime.now().astimezone().isoformat(timespec="seconds")
        out.write(json.dumps(u,ensure_ascii=False)+"\n"); out.flush()
        m=u.get("message") or u.get("edited_message") or {}
        print(("EDIT" if "edited_message" in u else "MSG"), m.get("message_thread_id"), m.get("message_id"), len(m.get("text","")), repr(m.get("text","")[:60]), flush=True)
    if not r.get("ok"): time.sleep(5)
