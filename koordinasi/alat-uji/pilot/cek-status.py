import sqlite3,sys
H="/tmp/claude-0/-home-user-Skills/d777d314-a309-56aa-81f9-6ad58561dd1c/scratchpad/openclaw-real/home/.openclaw/agents/main/agent/openclaw-agent.sqlite"
c=sqlite3.connect(f"file:{H}?mode=ro",uri=True)
ids=sys.argv[1:]
r={t:c.execute("select status from session_nodes where session_key like ?",(f"%topic:{t}",)).fetchone() for t in ids}
print(r); sys.exit(0 if all(v and v[0] not in ("running","active") for v in r.values()) else 1)
