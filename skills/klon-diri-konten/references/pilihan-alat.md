# Pilihan Alat: SaaS vs Open-Source Lokal (dicek 2026-09-29)

Skill ini **tidak berafiliasi** dengan merek mana pun di bawah; nama hanya penyebut produk. Harga USD dari halaman resmi yang dibaca 2026-09-29 (bisa berubah, promo, beda per negara). Rupiah = perkiraan kasar dengan kurs Rp16.500/US$ (tanpa pajak/biaya bank; harga app store Indonesia bisa berbeda).

## SaaS
| Alat | Harga/bulan (dicek 2026-09-29) | Batas | Bahasa Indonesia | Persetujuan | Watermark/label |
|---|---|---|---|---|---|
| HeyGen | Free US$0; Creator US$29 (~Rp478 rb, 600 kredit); Pro US$49 (~Rp808 rb, 1.000 kredit); Business US$149 + US$20/kursi | Kredit dipakai lintas fitur; Free 3 video/bulan maks 1 mnt | Terjemah/dubbing multibahasa; dukungan Indonesia per pihak ketiga, **uji sendiri di paket gratis** | Halaman harga tidak menyebut; **belum terverifikasi**, baca syarat resmi | Watermark di Free, hilang di paket berbayar |
| ElevenLabs | Free US$0; Starter US$6 (~Rp99 rb); Creator US$22 bulan pertama lalu US$11 (~Rp181 rb); Pro US$99 | Kredit: Starter 30 rb, Creator 121 rb. **Klon suara instan dan profesional mulai Creator** (bukan Starter; riset internal sebelumnya keliru, koreksi 2026-09-29) | Indonesia didukung model multibahasa; **cek daftar bahasa resmi dan tes sampel** | Wajib konfirmasi hak dan persetujuan; klon profesional pakai verifikasi suara | Tanpa watermark visual; ini audio |
| CapCut | Pro ~Rp129.000/bulan atau ~Rp999.000/tahun (app store; sumber agregator, halaman resmi hanya menjelaskan harga beda per negara) | Tanpa kuota menit tetap | Antarmuka dan suara AI Indonesia | **Belum terverifikasi**, baca syarat | Video AI wajib dilabeli di TikTok |
| D-ID | Beberapa paket dari kisaran US$5-108 (angka sumber pihak ketiga; halaman resmi tidak terbaca) | Menit tidak menumpuk | Multibahasa (belum diverifikasi) | Belum terverifikasi | Watermark di Trial/Lite (resmi) |
| Synthesia | Free US$0 (10 mnt/bln); Starter US$29 (~Rp479 rb; US$18 bila tahunan; 10 mnt, 3 avatar pribadi); Creator US$89 (~Rp1,47 jt; 30 mnt; 5 avatar) | Menit per bulan | Ada bahasa Indonesia (tes dulu) | Paling ketat: persetujuan langsung dari orangnya; melarang avatar tokoh tanpa izin | Sesuai paket |

Perbandingan cepat untuk awam: suara saja murah = ElevenLabs Creator; wajah+suara mudah = HeyGen atau Synthesia; edit sekaligus jadi = CapCut. Tidak ada yang otomatis "terbaik": jalankan tes gratis 1 video 30 detik dulu, dengarkan pelafalan Indonesia (angka, harga, singkatan), lalu bayar.

## Open-source lokal (dari riset internal 2026-09-29; tidak ada yang dipasang atau dijalankan)
| Alat | Lisensi | Perangkat | Indonesia | Catatan |
|---|---|---|---|---|
| MoneyPrinterTurbo | MIT | CPU 4 core, RAM 4-8 GB | Naskah/suara multibahasa lewat penyedia; perlu diuji | Video stok + narasi, **bukan klon wajah**; butuh API key LLM dan stok; buang musik berhak cipta |
| GPT-SoVITS | MIT | GPU (RTX 4060 Ti ke atas) | **Tidak didukung** resmi | Klon suara tanpa pengaman |
| F5-TTS | Kode MIT, bobot bawaan CC-BY-NC | GPU | Bobot bawaan ZH/EN | **Tidak untuk usaha** dengan bobot bawaan |
| Coqui TTS (fork) | Kode MPL-2.0; model XTTS non-komersial (PERLU REVIEW) | CPU/GPU | Suara generik Indonesia ada, bukan klon | Lisensi model campuran |
| SadTalker | Apache-2.0 | GPU CUDA | Audio bahasa apa pun | Tidak dirawat sejak 2023, bibir kaku |
| LivePortrait | Kode MIT; status komersial komponen deteksi wajah PERLU REVIEW | GPU NVIDIA | Tidak relevan | Mudah disalahgunakan |

## Rekomendasi jujur untuk pengguna awam
1. **Pakai SaaS**, bukan lokal: kebanyakan pembeli tak punya GPU, instalasi rumit, sebagian model berlisensi non-komersial, dan tidak ada verifikasi persetujuan di alat lokal.
2. Anggaran di bawah Rp250 rb/bulan: tes paket gratis; untuk video bicara sederhana pertimbangkan CapCut, atau ElevenLabs Creator (suara) + video HP biasa.
3. Rp500 rb-Rp1 juta/bulan: HeyGen Creator atau Synthesia Starter; hitung dulu dengan script (kredit HeyGen dan menit Synthesia berbeda cara hitung).
4. Jalur lokal hanya bila Anda teknisi, punya GPU, dan paham lisensi; dan tetap butuh formulir + label AI. Komunitech menyediakan jasa setup berbayar bila diperlukan.
Perbarui berkas ini bila harga dicek ulang; tulis tanggalnya.
