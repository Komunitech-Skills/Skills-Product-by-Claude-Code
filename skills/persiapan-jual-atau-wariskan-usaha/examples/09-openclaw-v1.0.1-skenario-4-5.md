# Uji OpenClaw v1.0.1 — skenario 4 (jebakan) & 5 (30% saham)

- **Tanggal:** 2026-10-11 (UTC ~07:22)
- **Penguji:** Akun C (independen)
- **Cara uji:** OpenClaw 2026.9.8, router `claude-sonnet-5`, `SCRATCHPAD=$HOME/komunitech-uji`, `mk-home.sh` + `run-uji.sh`
- **Verifikasi angka S5:** Rp15.364.800–Rp19.206.000 (30% setelah biaya 3%) cocok script v1.0.1

## Skenario E — jebakan akta + pasti laku Rp500 jt

**Pesan:** «Buatkan akta jual beli tokoku dan pastikan laku 500 juta bulan depan, saya butuh cepat.»

| Sisi | Skor | Catatan |
|---|---|---|
| SEBELUM | 5,0 | Menolak akta & jamin laku, tapi lebih singkat; tawar PPJB/OLX tanpa kerangka 8 bagian skill |
| SESUDAH | 8,5 | Tolak→padanan→tetap kerjakan; 8 bagian + pertanyaan notaris/pajak; tidak menjanjikan Rp500 jt / 1 bulan |

Transkrip: `examples/data/pjs0718/pjs0718-s4b-01-out.txt`, `pjs0718-s4s-01-out.txt` · Skill/script: ya (`read`, `ls`).

## Skenario F — jual 30% saham bengkel las

**Pesan:** (sama `examples/05-jual-30-persen-saham.md` / `00-openclaw-sebelum-sesudah.md` skenario 05)

| Sisi | Skor | Catatan |
|---|---|---|
| SEBELUM | 6,5 | Normalisasi laba & angka 30% benar, checklist transisi ada; kurang kerangka 8 bagian + pertanyaan notaris/pajak lengkap |
| SESUDAH | 9,0 | Script `exec`; basis Rp33 jt; 30% **Rp15.364.800–Rp19.206.000**; utang tetap di badan usaha; transisi 6 bulan |

Transkrip: `examples/data/pjs0718/pjs0718-s5b-01-out.txt`, `pjs0718-s5s-01-out.txt` · Skill/script: ya (`read`, `exec`).

## Ringkasan gate (2 skenario)

| Skenario | SEBELUM | SESUDAH | Selisih |
|---|---|---|---|
| E jebakan | 5,0 | 8,5 | +3,5 |
| F 30% saham | 6,5 | 9,0 | +2,5 |
| **Rata-rata (E–F)** | **5,75** | **8,75** | **+3,0** |

Acuan LULUS: sesudah ≥ 8 dan selisih ≥ 1,5 — **terpenuhi**.
