# Skenario 3: Normal ketiga: pengumuman perubahan jam tutup toko

**Platform:** claude-code (simulasi agent), bukan OpenClaw asli.

**Input:** "Mulai Senin 2 November toko tutup jam 20.00, dulu 21.00, karena listrik mahal dan sepi. Dua kasir shift malam, Ayu dan Joko, pasti kena. Tim ada 8 orang. Tolong buatin cara ngumumin ke mereka."

## Output dengan skill

**Pengumuman: Jam Tutup Baru 20.00 mulai Senin 2 November**

**Urutan:** (1) Kabari Ayu dan Joko empat mata dulu, minggu ini. (2) Umumkan ke 8 orang di rapat singkat. (3) Kirim pesan WA grup sebagai catatan. (4) Buka tanya jawab dan cek ulang [isian: tanggal].

**Naskah lisan untuk Ayu dan Joko**
"Ayu, Joko, ada perubahan yang mau saya sampaikan lebih dulu ke kalian, karena kalian yang paling terdampak, dan saya tahu ini tidak sepenuhnya enak. Mulai Senin 2 November toko tutup jam 20.00, bukan 21.00, karena biaya listrik naik dan pembeli setelah jam 20.00 sedikit. Shift malam kalian jadi lebih pendek satu jam. Yang tetap sama: [isian: yang tetap, mis. hari kerja]. Soal gaji/insentif shift malam: [isian: keputusan Bapak/Ibu; jangan dijanjikan sebelum pasti]. Silakan tanya atau sampaikan keberatan ke saya langsung."

**Naskah untuk seluruh tim (rapat singkat)**
"Mulai Senin 2 November jam tutup jadi 20.00. Alasannya [isian: listrik/sepi]. Yang terdampak terutama shift malam, dan sudah saya bicarakan. Tugas tutup toko (kunci, hitung kas, bersih-bersih) dimulai [isian: jam]. Yang tetap sama: [isian]. Pertanyaan boleh ke saya langsung."

**Pesan WA grup**
"Rekan-rekan, mulai Senin 2 November jam tutup toko jadi 20.00. Alasannya: [isian]. Yang terdampak: shift malam, sudah dikabari. Yang tetap sama: [isian]. Pertanyaan boleh ke saya langsung. Terima kasih atas pengertiannya."

**Tindak lanjut:** tanya jawab dan cek ulang [isian: tanggal]; jadwal shift baru dibagikan [isian: tanggal].
**Catatan:** perubahan jam kerja atau upah sebaiknya disepakati dan dicek dengan perjanjian kerja/aturan perusahaan; bukan nasihat hukum.

**Asumsi:** tim 8 orang, WA, nada hangat. **Pertanyaan:** (1) Apakah gaji/insentif Ayu dan Joko berubah? (2) Siapa menutup toko dan jam berapa mulainya? (3) Jam kerja resmi mereka tertulis berapa jam di perjanjian?

## Catatan

Nilai sebelum 5.5 / sesudah 8.5. Sebelum: mengatur urutan (Ayu dan Joko dulu) tetapi mengarang 'gaji pokok tetap sama' (keputusan yang belum dibuat pengguna), memakai emoji, tanpa 'yang tetap sama'. Sesudah: gaji/insentif ditandai `[isian]` dan diingatkan jangan dijanjikan sebelum pasti, tiga naskah (empat mata, rapat, WA grup), tindak lanjut dan catatan cek perjanjian kerja. Kurang: SKILL.md sendiri tidak memuat peringatan hukum soal ubah jam kerja/upah; catatan itu tambahan agent.

Perbandingan lengkap dengan hasil tanpa skill: `00-openclaw-sebelum-sesudah.md`.
