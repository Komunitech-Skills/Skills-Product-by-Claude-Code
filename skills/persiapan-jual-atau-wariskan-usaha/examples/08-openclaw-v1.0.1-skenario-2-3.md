# Uji OpenClaw sebelum/sesudah — persiapan-jual-atau-wariskan-usaha **v1.0.1** (skenario 2–3)

- **Tanggal:** 2026-10-11 (UTC ~06:30)
- **Penguji:** penguji otomatis Komunitech (independen)
- **Cara uji:** OpenClaw 2026.9.8, router `claude-sonnet-5`, folder kerja uji internal kurator (tidak disertakan dalam paket), `mk-home.sh` + `run-uji.sh`
- **Tes script:** `python3 tests/uji_regresi.py` → 15 tes OK
- **Transkrip:** `examples/data/pjs0616/`

Melengkapi subset T1+S4 di `00-openclaw-v1.0.1-sebelum-sesudah.md`.

---

## Skenario C — wariskan bengkel cat (Pak Rudi, Tangerang)

**Pesan:** (sama `00-openclaw-sebelum-sesudah.md` skenario 02)

| Sisi | Skor | Catatan |
|---|---|---|
| SEBELUM | **6,5/10** | Roadmap kuartal bagus (keuangan, WA, SOP, notaris) tapi tanpa 8 bagian skill, tanpa tabel periksa, tanpa rentang nilai terstruktur |
| SESUDAH | **9,0/10** | 8 bagian lengkap, tabel periksa, rencana 12 bulan, pertanyaan notaris/pajak, rentang ilustrasi Rp131,25–306,25 jt (basis Rp87,5 jt); `read`+`exec` terpakai |

---

## Skenario D — jual laundry tanpa angka (Surabaya)

**Pesan:** `Mau jual usaha laundry saya di Surabaya, nilainya berapa ya?`

| Sisi | Skor | Catatan |
|---|---|---|
| SEBELUM | **5,5/10** | Hanya daftar data yang dibutuhkan + metode umum, belum ada kerangka persiapan jual |
| SESUDAH | **8,5/10** | Kerjakan dulu dengan asumsi (jual 100%, 12 bulan); 8 bagian + daftar periksa laundry; jujur belum bisa hitung tanpa laba; pertanyaan di akhir (≤3 tema) |

---

## Ringkasan gate (4 skenario v1.0.1: A,B,C,D)

| Skenario | SEBELUM | SESUDAH | Selisih |
|---|---|---|---|
| A warung + biaya sekali | 6,5 | 9,0 | +2,5 |
| B buyout sekutu 40% | 5,5 | 9,0 | +3,5 |
| C wariskan bengkel | 6,5 | 9,0 | +2,5 |
| D laundry tanpa angka | 5,5 | 8,5 | +3,0 |
| **Rata-rata** | **6,0** | **8,875** | **+2,875** |

Acuan LULUS: sesudah ≥ 8 dan selisih ≥ 1,5 — **terpenuhi** (rata-rata sesudah 8,875; selisih +2,875).

Skenario 04 & 05 diulang OpenClaw v1.0.1 pada run 2026-10-11 — lihat `09-openclaw-v1.0.1-skenario-4-5.md`.
