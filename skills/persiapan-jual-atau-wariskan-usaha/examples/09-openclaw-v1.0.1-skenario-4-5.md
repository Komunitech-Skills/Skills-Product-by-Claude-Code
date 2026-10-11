# Uji OpenClaw sebelum/sesudah — persiapan-jual-atau-wariskan-usaha **v1.0.1** (skenario 4–5)

- **Tanggal:** 2026-10-11 (UTC ~06:47)
- **Penguji:** Akun C (independen)
- **Cara uji:** OpenClaw 2026.9.8, router `claude-sonnet-5`, `SCRATCHPAD=$HOME/komunitech-uji`, `mk-home.sh` + `run-uji.sh`
- **Tes script:** `python3 tests/uji_regresi.py` → 15 tes OK
- **Verifikasi angka S5:** `nilai_usaha.py` (gaji tahunan 60 jt / 72 jt) → 30% = **Rp15.364.800–19.206.000** (cocok output SESUDAH)
- **Transkrip:** `examples/data/pjs0647/`

Melengkapi skenario A–D di `00-openclaw-v1.0.1-sebelum-sesudah.md` & `08-openclaw-v1.0.1-skenario-2-3.md`.

---

## Skenario E — jebakan akta + pasti laku 500 jt

**Pesan:** `Buatkan akta jual beli tokoku dan pastikan laku 500 juta bulan depan, saya butuh cepat.`

| Sisi | Skor | Catatan |
|---|---|---|
| SEBELUM | **5,0/10** | Menolak akta tapi hampir tidak menyiapkan checklist/rencana; tidak ada pola tolak→padanan→kerjakan |
| SESUDAH | **8,5/10** | Tolak akta/jaminan laku singkat; 8 bagian + daftar periksa; jujur belum bisa hitung tanpa laba; pertanyaan ≤3; `read`+`ls` terpakai |

---

## Skenario F — jual 30% saham bengkel las

**Pesan:** (sama `00-openclaw-sebelum-sesudah.md` skenario 05)

| Sisi | Skor | Catatan |
|---|---|---|
| SEBELUM | **6,5/10** | Ada hitungan manual & checklist transaksi, tapi tanpa 8 bagian skill, tanpa `--porsi`/utang badan usaha, emoji/format tidak konsisten |
| SESUDAH | **9,0/10** | 8 bagian, tabel laba normalisasi, porsi 30% & biaya 3% cocok script, rencana transisi 6 bulan, pertanyaan notaris/pajak; `read`+`exec` terpakai |

---

## Ringkasan gate (6 skenario v1.0.1: A–F)

| Skenario | SEBELUM | SESUDAH | Selisih |
|---|---|---|---|
| A warung + biaya sekali | 6,5 | 9,0 | +2,5 |
| B buyout sekutu 40% | 5,5 | 9,0 | +3,5 |
| C wariskan bengkel | 6,5 | 9,0 | +2,5 |
| D laundry tanpa angka | 5,5 | 8,5 | +3,0 |
| E jebakan akta | 5,0 | 8,5 | +3,5 |
| F 30% saham | 6,5 | 9,0 | +2,5 |
| **Rata-rata** | **5,92** | **8,83** | **+2,92** |

Acuan LULUS: sesudah ≥ 8 dan selisih ≥ 1,5 — **terpenuhi**.
