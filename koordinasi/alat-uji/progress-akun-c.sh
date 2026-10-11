#!/usr/bin/env bash
# Hitung progress antrean Akun C dari papan-tugas + (opsional) dashboard automation-progress.
# Tanpa secret. Output satu baris (mesin) + baris TG (manusia).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
PAPAN="${ROOT}/koordinasi/papan-tugas.md"
PROGRESS_MD="${ROOT}/koordinasi/automation-progress-akun-c.md"

exec python3 - "$PAPAN" "$PROGRESS_MD" <<'PY'
import re
import sys
from pathlib import Path

papan = Path(sys.argv[1])
progress_md = Path(sys.argv[2])
text = papan.read_text(encoding="utf-8")

items: list[tuple[str, str, str]] = []  # (id, kind, status)


def classify_status(raw: str) -> str:
    s = raw.strip().lower()
    if re.search(r"\bselesai\b|\blulus\b|\[x\]", s):
        return "selesai"
    if re.search(r"\bdikerjakan\b|\bsedang\b|\bin_progress\b|\[~\]|\[~\]", s):
        return "in_progress"
    if re.search(r"\bbelum\b|\bantre\b|\[ \]|\bsiap diuji\b|\bbutuh uji\b", s):
        return "tersisa"
    # default open backlog
    return "tersisa"


def add(kind: str, item_id: str, status_col: str) -> None:
    items.append((item_id, kind, classify_status(status_col)))


# --- Tabel ## Tugas Akun C (baris | Cn | ...)
in_c_table = False
for line in text.splitlines():
    if line.startswith("## Tugas Akun C"):
        in_c_table = True
        continue
    if in_c_table:
        if line.startswith("## ") and not line.startswith("## Tugas Akun C"):
            in_c_table = False
            continue
        m = re.match(r"^\|\s*(C\d+)\s*\|", line)
        if m:
            parts = [p.strip() for p in line.strip("|").split("|")]
            if len(parts) >= 4:
                add("C", parts[0], parts[-1])

# --- ## Antrean uji Akun C (checkbox)
in_antrean = False
for line in text.splitlines():
    if line.startswith("## Antrean uji Akun C"):
        in_antrean = True
        continue
    if in_antrean:
        if line.startswith("## "):
            in_antrean = False
            continue
        m = re.match(r"^-\s*\[(x|X|~|\s)\]\s*(.+)$", line.strip())
        if m:
            mark, body = m.group(1), m.group(2).strip()
            if mark.lower() == "x":
                st = "selesai"
            elif mark == "~":
                st = "in_progress"
            else:
                st = "tersisa"
            slug = body[:48].replace("|", "/")
            items.append((f"antrean:{slug}", "antrean", st))

# --- Permintaan antar-akun — progress Akun C (checkbox)
in_perm = False
for line in text.splitlines():
    if line.startswith("## Permintaan antar-akun — progress Akun C"):
        in_perm = True
        continue
    if in_perm:
        if line.startswith("## ") and "progress Akun C" not in line:
            in_perm = False
            continue
        m = re.match(r"^-\s*\[(x|X|~|\s)\]\s*(.+)$", line.strip())
        if m:
            mark, body = m.group(1), m.group(2).strip()
            if mark.lower() == "x":
                st = "selesai"
            elif mark == "~":
                st = "in_progress"
            else:
                st = "tersisa"
            slug = body[:48].replace("|", "/")
            items.append((f"perm:{slug}", "perm", st))

# --- Override manual dari dashboard automation-progress (opsional)
if progress_md.is_file():
    pm = progress_md.read_text(encoding="utf-8")
    dash = re.search(
        r"## Dashboard antrean Akun C\s*\n(.*?)(?:\n## |\Z)",
        pm,
        re.DOTALL,
    )
    if dash:
        block = dash.group(1)
        for line in block.splitlines():
            m = re.match(
                r"^\|\s*([^|]+)\|\s*(selesai|in_progress|tersisa|open)\s*\|",
                line.strip(),
                re.I,
            )
            if m:
                item_id = m.group(1).strip()
                st = m.group(2).lower()
                if st == "open":
                    st = "tersisa"
                # replace same id or append
                replaced = False
                for i, (iid, kind, _) in enumerate(items):
                    if iid == item_id:
                        items[i] = (iid, kind, st)
                        replaced = True
                        break
                if not replaced:
                    items.append((item_id, "manual", st))

total = len(items)
selesai = sum(1 for _, _, s in items if s == "selesai")
in_progress = sum(1 for _, _, s in items if s == "in_progress")
tersisa = sum(1 for _, _, s in items if s == "tersisa")
persen = round((selesai / total) * 100) if total else 0
# Skala /100 untuk TG: "67/100" = persen selesai, bukan 67 dari 100 item nyata
skala100 = persen

print(
    f"total={total} selesai={selesai} in_progress={in_progress} "
    f"tersisa={tersisa} persen={persen} skala100={skala100}/{100}"
)
print(
    f"Antrian {selesai}/{total} ({persen}%) — "
    f"Selesai: {selesai} | Sedang: {in_progress} | Tersisa: {tersisa} "
    f"(skala TG: {skala100}/100)"
)
PY
