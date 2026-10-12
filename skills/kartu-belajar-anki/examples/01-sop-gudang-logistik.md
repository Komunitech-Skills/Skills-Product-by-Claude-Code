# S1 — SOP gudang (normal utama)

**Input:** 10 istilah logistik + tag sop-gudang, 20 menit/hari, maks 12 kartu baru/hari.

**Output sesudah (ringkas):** 12 kartu basic, pratinjau tabel, rencana 1 hari (12 kartu @12/hari), blok TSV 12 baris, cara impor Anki.

**Catatan:** Angka hari diverifikasi: `rencana_belajar.py --kartu 12 --menit 20 --baru-per-hari 12` → `hari_selesai_kartu_baru: 1`.
