#!/usr/bin/env python3
"""Cetak DRAF perintah jadwal OpenClaw siap tempel untuk pemilik (v1.0.9).

Dipakai bila pembuatan jadwal oleh agent GAGAL atau tidak tersedia (tool jadwal ditolak,
Gateway/kanal belum siap). Agent TIDAK mencari CLI/berkas dan TIDAK mencoba ulang: cukup
jalankan script ini sekali, tempel hasilnya ke pengguna, lalu berhenti.

Path skill di draf = lokasi standar milik member: `~/.openclaw/skills/pantau-pasar-kripto`
(Windows: `%USERPROFILE%\\.openclaw\\skills\\pantau-pasar-kripto`), BUKAN path lokasi script ini
(bisa path lingkungan uji). Ganti dengan `--folder-skill <path>` bila skill dipasang di tempat lain.
Python standar saja, lintas OS.

Pakai:
  python3 draf_jadwal.py --jam-ringkasan 06:30 --cek-per-jam
  python3 draf_jadwal.py --jam-ringkasan 07:00 --chat-id 123456 --workspace /home/saya/kerja
  (Windows: python atau py)
"""

import argparse
import json
import os
import re
import sys

NAMA_SKILL = "pantau-pasar-kripto"


def folder_skill_default(windows=None):
    """Lokasi standar skill di komputer member (tanpa mengekspansi ~ ke path mesin ini)."""
    if windows is None:
        windows = os.name == "nt"
    if windows:
        return "%USERPROFILE%\\.openclaw\\skills\\" + NAMA_SKILL
    return "~/.openclaw/skills/" + NAMA_SKILL


def gabung(folder, *bagian):
    sep = "\\" if "\\" in folder else "/"
    return sep.join([folder.rstrip("/\\")] + list(bagian))


def parse_jam(teks):
    m = re.fullmatch(r"\s*(\d{1,2})[:.](\d{2})\s*(WIB)?\s*", teks or "", re.IGNORECASE)
    if not m:
        raise ValueError(f"Jam '{teks}' tidak dikenali -- tulis seperti 06:30 atau 07.00.")
    jam, menit = int(m.group(1)), int(m.group(2))
    if jam > 23 or menit > 59:
        raise ValueError(f"Jam '{teks}' di luar 00:00-23:59.")
    return jam, menit


def susun(args):
    py = args.python
    tujuan = args.chat_id or "<ID chat Telegram pemilik>"
    ws = args.workspace or "<folder-workspace-member>"
    folder = getattr(args, "folder_skill", None) or folder_skill_default()
    skrip_dir = gabung(folder, "scripts")
    bagian = []
    if args.cek_per_jam:
        argv = [py, gabung(skrip_dir, "cek_dan_lapor.py"), "--konfigurasi",
                "kripto/konfigurasi.json", "--state", "kripto/state.json"]
        bagian.append(
            "# 1) Cek ambang tiap jam (diam bila tidak ada ambang terlewati)\n"
            'openclaw automations add --cron "0 * * * *" --tz "Asia/Jakarta" \\\n'
            '  --name "Cek ambang kripto (per jam)" --session isolated \\\n'
            f"  --command-argv '{json.dumps(argv)}' \\\n"
            f'  --command-cwd "{ws}" \\\n'
            f'  --announce --channel telegram --to "{tujuan}"'
        )
    if args.jam_ringkasan:
        jam, menit = parse_jam(args.jam_ringkasan)
        pesan = (
            f"Jalankan '{py} {gabung(skrip_dir, 'cek_ambang.py')} --konfigurasi "
            "kripto/konfigurasi.json --state kripto/state.json --keluaran teks' untuk harga. "
            "Cari berita terbaru untuk kata kunci di kripto/PANTAU.md bila ada akses web; "
            "setiap judul wajib URL artikel asli (bukan redirect news.google.com), rapikan dengan "
            f"'{py} {gabung(skrip_dir, 'rapikan_berita.py')}'. Ikuti Langkah B SKILL.md "
            "pantau-pasar-kripto, tanpa sinyal/target harga, akhiri dengan disclaimer."
        )
        nomor = "2" if args.cek_per_jam else "1"
        bagian.append(
            f"# {nomor}) Ringkasan pagi {jam:02d}:{menit:02d} WIB\n"
            f'openclaw automations add "{menit} {jam} * * *" \\\n'
            f"  {json.dumps(pesan, ensure_ascii=False)} \\\n"
            '  --tz "Asia/Jakarta" --name "Ringkasan pagi kripto" --session isolated \\\n'
            f'  --announce --channel telegram --to "{tujuan}"'
        )
    if not bagian:
        raise ValueError("Pilih minimal satu: --cek-per-jam dan/atau --jam-ringkasan HH:MM.")
    kepala = (
        "Jadwal belum bisa saya pasang dari sini. Berikut DRAF perintah siap tempel untuk "
        "dipasang pemilik (Terminal di komputer Gateway) atau lewat jasa setup Komunitech.\n"
        "Syarat: Gateway menyala & kanal Telegram sudah terhubung (PANDUAN Bab 4).\n"
        "Ganti teks di dalam <...> bila masih ada. Bila perintah tidak mengenali '~', ganti dengan "
        "folder home Anda (Windows: %USERPROFILE%). Setelah dipasang, cek: "
        "openclaw automations list --all\n"
    )
    return kepala + "\n```bash\n" + "\n\n".join(bagian) + "\n```"


def main(argv=None):
    ap = argparse.ArgumentParser(description="Draf perintah jadwal OpenClaw (siap tempel).")
    ap.add_argument("--cek-per-jam", action="store_true", help="Sertakan job cek ambang tiap jam.")
    ap.add_argument("--jam-ringkasan", default=None, help="Jam ringkasan pagi WIB, mis. 06:30.")
    ap.add_argument("--chat-id", default=None, help="ID chat Telegram pemilik (opsional).")
    ap.add_argument("--workspace", default=None, help="Folder kerja berisi kripto/ (opsional).")
    ap.add_argument("--python", default="python3",
                    help="Perintah Python di mesin Gateway (Windows: python).")
    ap.add_argument("--folder-skill", default=None,
                    help="Folder skill di mesin Gateway (default ~/.openclaw/skills/pantau-pasar-kripto).")
    args = ap.parse_args(argv)
    try:
        print(susun(args))
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
