"""Kirim pesan gelombang; tunggu balasan bot lewat updates-g2.jsonl (tanpa sqlite agent)."""
import json
import os
import sys
import time
import datetime

from tg import call

UPDATES = "updates-g2.jsonl"
SENT = "sent-g11b-pilot.jsonl"


def bot_texts_for_topic(topic: int) -> list[str]:
    texts = []
    if not os.path.exists(UPDATES):
        return texts
    for line in open(UPDATES):
        line = line.strip()
        if not line:
            continue
        try:
            u = json.loads(line)
        except json.JSONDecodeError:
            continue
        m = u.get("message") or u.get("edited_message") or {}
        if m.get("message_thread_id") != topic:
            continue
        if not m.get("from", {}).get("username", "").startswith("KTclaude"):
            continue
        tx = (m.get("text") or m.get("caption") or "").strip()
        if tx and not tx.startswith("Working"):
            texts.append(tx)
    return texts


def wait_reply(topic: int, min_len: int = 200, timeout: int = 420) -> str:
    end = time.time() + timeout
    time.sleep(25)
    while time.time() < end:
        texts = bot_texts_for_topic(topic)
        joined = "\n\n".join(texts)
        if len(joined) >= min_len:
            return joined
        time.sleep(12)
    return "\n\n".join(bot_texts_for_topic(topic))


def main():
    f, idx = sys.argv[1], [int(x) for x in sys.argv[2:]]
    msgs = json.load(open(f))
    log = open(SENT, "a")
    for n, i in enumerate(idx):
        m = msgs[i]
        topic = m["topic"]
        existing = "\n\n".join(bot_texts_for_topic(topic))
        if len(existing) >= 200:
            print("skip", topic, "already", len(existing), flush=True)
            continue
        if n:
            time.sleep(25)
        r = call(
            "sendMessage",
            chat_id=-1004407409583,
            message_thread_id=topic,
            text=m["text"],
        )
        rec = {
            "skill": m["skill"],
            "sisi": m["sisi"],
            "topic": topic,
            "ok": r.get("ok"),
            "desc": r.get("description"),
            "message_id": r.get("result", {}).get("message_id"),
            "time": datetime.datetime.now().astimezone().isoformat(timespec="seconds"),
        }
        body = wait_reply(topic)
        rec["reply_len"] = len(body)
        rec["hasil"] = "ok" if len(body) >= 200 else "timeout"
        print(rec, flush=True)
        log.write(json.dumps(rec) + "\n")
        log.flush()
        time.sleep(5)


if __name__ == "__main__":
    main()
