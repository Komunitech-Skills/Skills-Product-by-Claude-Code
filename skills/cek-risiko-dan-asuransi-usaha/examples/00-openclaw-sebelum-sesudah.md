# Uji OpenClaw sebelum/sesudah: cek-risiko-dan-asuransi-usaha v1.0.1

- **Tanggal:** 2026-10-10
- **Penguji:** Akun C (agent Cursor Cloud), independen dari pembuat
- **Cara uji (target):** OpenClaw 2026.9.8 lokal (`openclaw agent --local`), model router `ninerouter/komunitech` (claude-sonnet-5). SEBELUM = `mk-home.sh <HOME>` tanpa skill; SESUDAH = home berisi hanya skill ini. Pesan identik; data JSON risiko (bila dipakai) di `workspace/` kedua home. Skenario 1 SESUDAH juga lewat `uji-tg.sh` (konteks Telegram, tanpa kirim).

## Blokir infrastruktur (OpenClaw tidak dijalankan)

| Cek | Hasil |
|---|---|
| `bash $HOME/komunitech-uji/openclaw-real/oc.sh --version` | OpenClaw 2026.9.8 OK |
| `Ninerouter_key` di environment VM | **KOSONG** → `openclaw agent` HTTP **401** "API key required" |
| `bash gw-cek.sh` | GAGAL: `bot_token`/`Ninerouter_key` kosong |
| `uji.sh` bawaan | `unshare: Operation not permitted` di VM Cursor + path `/tmp/uji-openclaw` tidak ada |
| Pemulihan | Secret `Ninerouter_key` (wajib) dan `bot_token` (opsional) diminta lewat environment setup Cursor; wrapper lokal `uji-cursor.sh` (tanpa unshare) siap di `$HOME/komunitech-uji/openclaw-real/` |

**Catatan jujur:** Skor SEBELUM/SESUDAH di bawah memakai **simulasi penguji** (model yang sama, hanya folder skill dibaca untuk sisi SESUDAH), sama seperti uji 1.0.0 sebelum OpenClaw tersedia. Angka SESUDAH **wajib** cocok dengan `scripts/cek_risiko.py` v1.0.1 (diverifikasi independen). **Wajib ulang `uji.sh`/`uji-tg.sh` saat kunci router terpasang** sebelum promosi Telegram.

<details><summary>Verifikasi script v1.0.1 (independen, 2026-10-10)</summary>

- `python3 tests/uji_regresi.py` → **16/16 OK**
- B1: `Gaji=1000000,Gaji=2000000` → **ditolak** (nama dobel); `Sewa=3000000.00` → **ditolak** (desimal)
- B4: `--cicil 12` → cicilan dibulatkan ke atas (contoh kafe: Rp3.283.334/bln)
- B2/B3: field `bisa_diasuransikan: false` → kolom "Tidak ada asuransi umum; pakai mitigasi lain"; aturan **besar** (dampak ≥4 atau kerugian > dana) → alihkan meski skor 4 (gempa 1×4 + `--dana` + kerugian besar)

</details>

---

## Skenario 1 — Kafe ruko dekat kali (normal + Telegram)

**Pesan:** (identik 1.0.0) lihat `00-pembanding-tanpa-skill.md`.

**SEBELUM (skill mati):** lihat `00-pembanding-tanpa-skill.md` (6,5/10).

**SESUDAH (v1.0.1, simulasi + script):** Tabel 9 risiko; dana darurat dari script `dana --biaya "Sewa=4500000,Gaji=8400000,Listrik=1700000,Cicilan=1200000" --bulan 3 --kas 8000000 --cicil 12` → target Rp47.400.000, kekurangan Rp39.400.000, cicilan **Rp3.283.334/bln** (12 bln). Gaji 3×2,8 jt dimasukkan sebagai **Gaji=8400000** (bukan tiga kunci dobel). Banjir/gempa: jika `kerugian_rp` banjir > kas, respons **alihkan + asuransi dipertimbangkan** untuk gempa 1×4. Barista keluar: `bisa_diasuransikan: false` bila agent mengikuti SKILL.md.

**Skor:** SEBELUM 6,5 · SESUDAH **8,5** (+2,0). **Skill/script terpakai?** Simulasi: ya (read SKILL + exec script); OpenClaw: belum diuji.

**uji-tg.sh:** tidak dijalankan (401).

---

## Skenario 2 — Bengkel motor Makassar

**Pesan:** lihat `02-bengkel-motor-makassar.md`.

**SEBELUM:** 6,5 — daftar risiko umum, dana darurat benar, tanpa tabel skor.

**SESUDAH:** Script dana cocok (Rp27.150.000 target, cicil 6 bln Rp1.191.667). Mekanik senior: dengan `"bisa_diasuransikan": false` → **"Tidak ada asuransi umum; pakai mitigasi lain"** (kontrak/cadangan mekanik), bukan "Ya, pertimbangkan asuransi".

**Skor:** SEBELUM 6,5 · SESUDAH **8,5**. **Skill/script terpakai?** Simulasi ya.

---

## Skenario 3 — Toko online + banding polis

**Pesan:** lihat `03-toko-online-dan-banding-polis.md`.

**SEBELUM:** 6,5.

**SESUDAH:** Akun marketplace: `bisa_diasuransikan: false`. Tabel banding A vs B netral; angka premi/own risk dari input pengguna.

**Skor:** SEBELUM 6,5 · SESUDAH **8,0**. **Skill/script terpakai?** Simulasi ya.

---

## Skenario 4 — Katering, input kurang

**Pesan:** lihat `04-input-kurang-katering.md`.

**SEBELUM:** 6.

**SESUDAH:** 8,5 — kerja dulu, `[isian]`, 3 pertanyaan; skor risiko dari script.

**Skor:** SEBELUM 6 · SESUDAH **8,5**.

---

## Skenario 5 — Jebakan merek + klaim pasti cair

**Pesan:** lihat `05-jebakan-merek-dan-klaim-pasti-cair.md`.

**SEBELUM:** 6.

**SESUDAH:** 9 — tolak→padanan→tetap kerjakan; kebakaran 15 KRITIS dari script.

**Skor:** SEBELUM 6 · SESUDAH **9**.

---

## Ringkasan skor (simulasi, OpenClaw pending)

| # | Skenario | SEBELUM | SESUDAH |
|---|---|---|---|
| 1 | Kafe | 6,5 | 8,5 |
| 2 | Bengkel | 6,5 | 8,5 |
| 3 | Toko online | 6,5 | 8,0 |
| 4 | Katering | 6 | 8,5 |
| 5 | Jebakan | 6 | 9 |
| | **Rata-rata** | **6,3** | **8,5** |

**Selisih +2,2.** Pembeda satu kalimat: **Dana darurat dan cicilan menabung keluar pasti dari script (termasuk tolak input biaya ambigu), plus kolom asuransi jujur untuk risiko yang tidak bisa diasuransikan.**

**OpenClaw:** jalankan ulang 5 skenario identik saat `Ninerouter_key` ada; ganti bagian "simulasi" dengan transkrip `hasil/*.txt` lengkap.
