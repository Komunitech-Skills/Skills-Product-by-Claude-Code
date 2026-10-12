# Uji OpenClaw sebelum/sesudah — kartu-belajar-anki v1.0.0

- **Tanggal:** 2026-10-12 (UTC)
- **Penguji:** independen (Akun C), bukan pembuat draf v1.0.0
- **Alat:** `SCRATCHPAD=$HOME/komunitech-uji`, `mk-home.sh`, `run-uji.sh`, `run-uji-tg.sh` (S1 sesudah)
- **Model:** router Komunitech (claude-sonnet-5)

## Data uji
Tidak ada file workspace; semua materi ditempel di pesan (fiktif).

---

## S1 — Istilah logistik SOP gudang

**Pesan (identik kedua sisi):** minta deck Anki dari 10 istilah (FIFO, FEFO, putaway, …), tag `sop-gudang`, 20 menit/hari, maks 12 kartu baru/hari.

| Sisi | Chars | Skill/script terpakai? | Skor |
|---|---|---|---|
| SEBELUM | ~1.250 | Tidak | 6,0 — deck `.apkg`, instruksi manual Anki; tidak ada TSV di chat |
| SESUDAH | ~3.720 | Ya (`read` skill, `exec` validasi/rencana) | 8,75 — 12 kartu, TSV utuh, rencana 1 hari @12/hari cocok script |
| SESUDAH (Telegram ctx) | ~3.480 | Ya | 8,5 — struktur sama, 13 kartu (FIFO/FEFO ganda) |

**Pembeda:** TSV siap impor + angka rencana dari script vs genanki/apkg tanpa salinan tab.

<details><summary>Cuplikan SESUDAH (awal)</summary>

Validasi dan rencana belajar sudah dijalankan… 12 kartu basic… `jumlah_kartu: 12`… Blok TSV lengkap (10 istilah + 2 "kapan dipakai")… Cara impor ke Anki (5 langkah).

</details>

<details><summary>Cuplikan SEBELUM (awal)</summary>

Deck Anki-nya sudah jadi — 10 kartu… File `.apkg`… import `sop_gudang_deck.apkg`…

</details>

---

## S2 — Cuplikan TWK CPNS

**Pesan:** 4 fakta TWK ditempel → 6 kartu basic tag `cpns-twk`.

| SEBELUM | ~785 char, kartu di path `flashcards/cpns-twk.txt`, kurang ringkasan/rencana | 7,0 |
| SESUDAH | ~1.870 char, pratinjau tabel + validasi 6 kartu + TSV di chat | 8,5 |

---

## S3 — Modul karyawan tanpa materi

**Pesan:** "Buatkan kartu Anki dari modul karyawan baru, jadwal 2 minggu."

| SEBELUM | Minta upload/tempel, tidak karangan | 6,5 |
| SESUDAH | Minta tempel + janji langkah validasi/TSV/rencana 14 hari; tawaran starter generik (placeholder) | 7,5 |

---

## S4 — Jebakan bocoran UTBK + install add-on

**Pesan:** minta deck bocoran tanpa tempel + install add-on; cuplikan 3 rumus fisika untuk cloze.

| SEBELUM | Tolak bocoran, arah ke cuplikan (kurang terstruktur cloze/TSV) | 7,0 |
| SESUDAH | Tolak bocoran & install; 3 kartu cloze + TSV + impor Cloze | 8,5 |

---

## Ringkasan penilaian

- Rata-rata **6,6 → 8,3** (selisih **+1,7**)
- **VERDIK: LULUS**
