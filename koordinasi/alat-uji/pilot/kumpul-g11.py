import json
t=json.load(open('topik-g11.json')); inv={v:k for k,v in t.items()}
sent={}
for l in open('sent-g2.jsonl'):
    r=json.loads(l)
    if r['topic'] in inv: sent[r['topic']]=r
msgs={}
for l in open('updates-g2.jsonl'):
    u=json.loads(l); x=u.get('message') or u.get('edited_message') or {}
    th=x.get('message_thread_id')
    if th not in inv: continue
    if not x.get('from',{}).get('username','').startswith('KTclaude'): continue
    tx=x.get('text') or x.get('caption') or ''
    if 'document' in x: tx+=f"\n[LAMPIRAN: {x['document'].get('file_name')}]"
    msgs.setdefault(th,{})[x['message_id']]=tx
out=[]
for k,th in t.items():
    sk,s=k.split('|'); sisi='TANPA' if s=='sebelum' else 'DENGAN'
    out.append(f"=== {sk} | {sisi} | topik {th} ===")
    ms=[v for mid,v in sorted(msgs.get(th,{}).items()) if v.strip() and not v.strip().startswith('Working')]
    out.append("\n\n[--- pesan Telegram berikutnya ---]\n\n".join(ms) if ms else "TIMEOUT / tidak ada balasan")
    out.append("")
open('jawaban-g11-tg.txt','w').write("\n".join(out))
for th in inv: print(th, inv[th], len(msgs.get(th,{})), sum(len(v) for v in msgs.get(th,{}).values()))
