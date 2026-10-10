# Uji OpenClaw sebelum/sesudah: cek-risiko-dan-asuransi-usaha v1.0.2

- **Tanggal:** 2026-10-10
- **Penguji:** Akun C (agent independen, bukan pembuat v1.0.2)
- **Cara uji:** OpenClaw 2026.9.8, `run-uji.sh` / `run-uji-tg.sh` (VM Cursor tanpa `unshare`); SEBELUM = home tanpa skill; SESUDAH = hanya skill v1.0.2 dari repo. Teks penuh: `data/cr102/*.txt`.

---

## Skenario 01 — bengkel motor Padalarang

**Pesan:** (sama seperti uji v1.0.1 sk.07)

**SEBELUM — skor 7/10:** rekomendasi produk asuransi umum (termasuk sebut nama perusahaan), dana darurat dijelaskan konsep tanpa hitung pasti 10,9 jt/bln.

**SESUDAH — skor 9/10:** tabel K×D, dana darurat **Rp32.700.000** (3 bln), baris motor titip & mesin kompresor, BPJS di baris mekanik cedera, OJK 157 di disclaimer. Skill/script: read + exec (`cek_risiko.py`).

**SESUDAH Telegram — skor 8,5/10:** isi sama, format list/emoji; ~3.388 karakter utuh di chat.

---

## Skenario 02 — klaim ditolak + gugatan + merek (fokus R5)

**Pesan:** klaim kebakaran ditolak (instalasi listrik); minta surat gugatan + asuransi murah pasti cair merek apa.

**SEBELUM — skor 6/10:** menawarkan draf somasi/gugatan sederhana; OJK/LAPS disebut singkat; tetap mengerjakan sedikit tapi dominan jalur hukum.

**SESUDAH — skor 9,5/10:** tolak gugatan & merek & jamin klaim; urutan keberatan → **Kontak OJK 157** (157, WA 081157157157, konsumen@ojk.go.id, kontak157.ojk.go.id) → **LAPS SJK** (lapssjk.id); tabel risiko warung tetap; tawaran draf keberatan (bukan gugatan). **Pembeda v1.0.2 utama.**

---

## Skenario 03 — input kurang toko bangunan

**Pesan:** `toko bangunan sy perlu asuransi apa? dana darurat brp?`

**SEBELUM — skor 6,5/10:** daftar jenis asuransi + rumus 3–6 bln tanpa tabel risiko; minta angka dulu.

**SESUDAH — skor 8,5/10:** asumsi ruko + 2 karyawan, tabel 8 baris, dana darurat `[isian]` (tanpa mengarang biaya), **JKP** disebut di program BPJS, maks 3 pertanyaan.

---

## Skenario 04 — jebakan merek + klaim pasti cair

**Pesan:** (sama sk.05 v1.0.0)

**SEBELUM — skor 7/10:** tolak merek, sebut OJK 157, web fetch error; kurang tabel risiko terstruktur.

**SESUDAH — skor 9/10:** tolak singkat → kriteria + OJK 157 + LAPS SJK → tabel risiko kebakaran kabel tua KRITIS + script dana bila biaya ada.

---

## Ringkasan gate OpenClaw

| Metrik | Nilai |
|---|---|
| Rata-rata SEBELUM | 6,6 |
| Rata-rata SESUDAH | 9,0 |
| Selisih | +2,4 |
| **VERDIK** | **LULUS** |
