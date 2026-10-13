# Riwayat perubahan — pdf-lokal

Catatan teknis per versi (dipindah dari README agar halaman pembeli ringkas).

## Catatan revisi 1.0.5 (2026-10-01)
Dari uji sebelum/sesudah OpenClaw: tanpa Stirling-PDF yang menyala, skill membuat AI
berhenti padahal qpdf/Ghostscript sudah ada di komputer, dan merujuk panduan yang tidak
ikut di folder skill. Kini: **jalur cadangan** `scripts/pdf_cadangan.py` mendeteksi qpdf,
Ghostscript, dan pdftk yang sudah terpasang lalu langsung mengerjakan gabung, pisah,
kompres, putar, kunci (AES-256 via qpdf), dan buka kunci - tanpa pip install, tanpa unggah,
file asli tidak ditimpa. Panduan pasang Stirling-PDF diringkas ke
`references/pasang-stirling.md` (di dalam folder skill). Tes baru `tests/uji_cadangan.py`
(26 skenario: deteksi alat, pilihan fallback, input buruk, verifikasi hasil dengan qpdf).
