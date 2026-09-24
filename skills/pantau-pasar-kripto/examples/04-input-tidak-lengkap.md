# 04 — Input tidak lengkap: "pantau kripto saya"

**Skenario:** S4. Member belum punya `kripto/PANTAU.md` dan tidak menyebut koin/ambang.

## Input pengguna (persis)
> pantau kripto saya

## Output (mengikuti SKILL.md Input §1 — tanya sekali, bernomor, maks 5)

Siap, saya bantu pantau. Supaya notifikasinya pas, saya perlu 5 hal ini (jawab singkat saja, boleh sekaligus):

1. **Koin apa saja?** (kode, mis. BTC, ETH, SOL)
2. **Kapan mau dikabari?** Naik/turun berapa persen (mis. turun 5%, naik 8%), atau di harga tertentu (mis. BTC di bawah Rp 1,4 M)?
3. **Pembandingnya apa?** Harga beli Anda sendiri, atau cukup dibanding 24 jam terakhir?
4. **Kata kunci berita** yang mau diikuti? (boleh kosong = nama koinnya saja)
5. **Ringkasan pagi** jam berapa & lewat mana? (Telegram disarankan; WhatsApp hanya dengan nomor terpisah)

Kalau mau cepat, balas saja nama koinnya — sisanya saya isi default: ambang turun 5% / naik 5% dibanding 24 jam terakhir, ringkasan 07:00 WIB via Telegram (akan saya sebutkan sebelum diaktifkan).

Informasi, bukan nasihat investasi. Keputusan & risiko sepenuhnya milik Anda.

*(Lanjutan: member membalas "btc sama eth aja, default". Agent membuat PANTAU.md + konfigurasi.json dengan ambang 5%/5%, 24 jam, 07:00 WIB Telegram, menampilkannya untuk dikonfirmasi — sama seperti contoh 01.)*

## Catatan penguji
- Pertanyaan tepat satu kali, bernomor, ≤ 5, bahasa awam. ✅
- **Kurang:** SKILL.md menyebut "pakai default (ambang 24 jam, jam 07:00 WIB, Telegram)" tetapi **tidak menetapkan angka ambang default** — agent di atas memilih 5%/5% sendiri. Karena ambang = keputusan member, sebaiknya SKILL.md menulis eksplisit: tanpa angka ambang dari member, jangan aktifkan notifikasi ambang (hanya ringkasan pagi), atau sebutkan default tertulis yang disetujui pemilik.
- "Pantau kripto saya" juga bisa berarti portofolio/jurnal — skill tidak menanyakan apakah member punya jurnal yang ingin dihitung. Minor.
