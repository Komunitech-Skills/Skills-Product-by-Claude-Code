"""Buat topik forum G20 (5 skill × TANPA/DENGAN). Bot pertama @KTclaude1_bot."""
import json
import os
import subprocess
import time

tok = os.environ["bot_token"]
C = "-1004407409583"
sk = [
    "balas-chat-cs",
    "foto-produk-brief",
    "sop-writer",
    "laporan-insiden-usaha",
    "surat-resmi",
]
m = {}
for n in sk:
    for sisi, lab in (("sebelum", "TANPA skill"), ("sesudah", "DENGAN skill")):
        for _ in range(4):
            r = subprocess.run(
                [
                    "curl",
                    "-s",
                    "-X",
                    "POST",
                    f"https://api.telegram.org/bot{tok}/createForumTopic",
                    "--data-urlencode",
                    f"chat_id={C}",
                    "--data-urlencode",
                    f"name=G20 {n} — {lab}",
                ],
                capture_output=True,
                text=True,
            )
            if r.stdout.strip():
                break
            time.sleep(3)
        d = json.loads(r.stdout) if r.stdout.strip() else {}
        if d.get("ok"):
            m[f"{n}|{sisi}"] = d["result"]["message_thread_id"]
        else:
            print("FAIL", n, sisi, d.get("description"))
        time.sleep(1.5)
out = os.path.join(os.path.dirname(__file__), "topik-g20.json")
json.dump(m, open(out, "w"), indent=1)
print(m)
