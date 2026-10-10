import os,sqlite3,sys
H=os.environ["SCRATCHPAD"]+"/openclaw-real/home/.openclaw/agents/main/agent/openclaw-agent.sqlite"
c=sqlite3.connect(f"file:{H}?mode=ro",uri=True)
ids=sys.argv[1:]
r={t:c.execute("select status from session_nodes where session_key like ?",(f"%topic:{t}",)).fetchone() for t in ids}
print(r); sys.exit(0 if all(v and v[0] not in ("running","active") for v in r.values()) else 1)
