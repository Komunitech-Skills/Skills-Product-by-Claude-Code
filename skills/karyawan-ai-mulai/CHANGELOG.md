# Riwayat perubahan — karyawan-ai-mulai

Catatan teknis per versi (dipindah dari README agar halaman pembeli ringkas).

## Catatan revisi 1.1.10 (2026-10-13)
- Batasan di SKILL.md: aturan eksplisit anti-karangan (jangan mengarang angka/kebijakan/tindakan yang tidak diberikan pengguna; tulis `[isian: kebijakan toko Anda]` atau tandai asumsi). Temuan audit contoh: `examples/03` memuat kebijakan toko yang tidak ada di input (resi aktif 1×24 jam, ongkir retur ditanggung, jam batas kirim 15.00); kini diganti `[isian: kebijakan toko Anda ...]`. Logika dan skrip tidak berubah.

## Catatan revisi 1.1.9 (2026-10-13)
- Rujukan ke skill arsip diganti: `caption-sosmed-umkm`, `kalender-konten-30hari` diganti `konten-mingguan` di SKILL.md (contoh rekomendasi dan rencana 7 hari), references/peta-skill.md, references/openclaw.md, dan peta kata kunci di scripts/peta_kebutuhan.py (hanya nama skill; logika dan kasus uji tidak berubah selain nama yang diharapkan).

## Catatan revisi 1.1.8 (2026-10-01)

- Uji OpenClaw 2026-10-01: (a) "Hasil Tugas Pertama" kini wajib di balasan yang sama dengan rekomendasi, tanpa menunggu pemasangan skill; (b) blok Aturan kerja ditampilkan utuh kata per kata sebelum minta "ya" (tidak diringkas); (c) folder skill hanya dicari di Unduhan/folder yang disebut pengguna, path sumber disebut sebelum minta izin, tidak menyalin dari `/tmp`/instalasi OpenClaw lain; (d) istilah jujur — "Starter Kit/paket Anda" hanya untuk folder unduhan yang benar-benar ditemukan; (e) tidak ada placeholder klaim hasil untuk kosmetik di tugas pertama.

## Catatan revisi 1.1.7 (2026-10-01)

- Blok Aturan kerja Komunitech v3: aturan 16 tidak lagi menyebut nama skill auto-trading (agent sempat menawarkan skill yang tidak terpasang); aturan 12 melarang menyarankan layanan lain (mis. UptimeRobot) untuk memantau situs pesaing; aturan 11 menambah "sebelum kehabisan" ke daftar urgensi palsu. Hasil uji v2: risiko 2/18 (v1 4/16, tanpa blok 13/16).

## Catatan revisi 1.1.6 (2026-10-01)
- Blok "Aturan kerja Komunitech" diperbarui ke v2 setelah uji independen (risiko 13/16 → 4/16, 2 skenario masih gagal): (a) daftar kata/klaim produk yang dilarang bila tidak disebut pemilik (homemade, fresh, tanpa pengawet, halal/BPOM, asal, ukuran, "stok terbatas/promo terakhir", dll.) → pakai `[ISI: ...]` atau tanya; (b) fakta PPN eksplisit: tarif 12% sejak 1 Jan 2025, tetapi barang/jasa non-mewah memakai DPP nilai lain 11/12 (efektif 11%), 12% penuh hanya barang mewah (PMK 131/2024); angka pajak lewat skill/script atau rumus; (c) hanya menyebut kemampuan/skill yang benar-benar terpasang dan sudah dicek; Telegram dulu untuk notifikasi; cek alat sebelum usul pasang; tidak me-restart proses; cek uptime pesaing termasuk larangan pantau. Pengguna dengan blok v1 akan ditawari mengganti blok lama.

## Catatan revisi 1.1.5 (2026-10-01)
- Langkah baru: menawarkan memasang blok "Aturan kerja Komunitech" (`references/aturan-kerja-agents.md`) ke `AGENTS.md` workspace OpenClaw. Isi blok selalu ditampilkan dulu, hanya ditambahkan di akhir file setelah Anda menjawab "ya" (isi lain tidak diubah), dan tidak dipasang dua kali. Alasannya: uji OpenClaw 2026-10-01 menunjukkan perilaku berisiko (menawarkan kirim WA otomatis, mengulang password, `find /`, `pip install`, mengubah konfigurasi sendiri, mengarang fakta produk) justru muncul saat skill tidak dibuka; `AGENTS.md` dibaca OpenClaw di setiap percakapan.
