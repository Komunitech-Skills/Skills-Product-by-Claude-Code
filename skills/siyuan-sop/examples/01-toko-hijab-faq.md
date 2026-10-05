# Skenario 01 — Toko hijab online: buat 2 dokumen FAQ + cari (normal)

**Penguji:** pembuat skill (BUKAN penguji independen), 2026-09-26. **Kernel SiYuan resmi v3.8.5**
(biner Linux resmi dari GitHub Releases, dijalankan headless oleh pembuat di sandbox terisolasi,
workspace kosong baru). Data fiktif: "Toko Hijab Cantik".

## Permintaan pengguna
> "Simpan FAQ ongkir dan kebijakan retur toko hijab saya ke SiYuan. Ongkirnya: dihitung otomatis pas checkout sesuai berat & kota, bisa COD kalau areanya didukung kurir. Returnya: bisa asal maksimal 3 hari setelah barang diterima, belum dipakai, label masih ada."

## Langkah agent
1. `daftar-buku` → menemukan buku catatan "Toko Hijab Cantik" (id `20260926095006-e9vdel5`).
2. Pratinjau dokumen pertama:
   ```
   $ python3 scripts/siyuan.py buat --notebook 20260926095006-e9vdel5 --path "/FAQ/Ongkos Kirim" \
       --md "**P: Berapa ongkirnya?**
   J: Ongkir dihitung otomatis oleh sistem checkout sesuai berat & kota tujuan.

   **P: Apakah bisa COD?**
   J: Bisa untuk area yang didukung kurir (dicek otomatis saat checkout)."
   ```
   ```
   PRATINJAU BUAT DOKUMEN
   Buku catatan: 20260926095006-e9vdel5
   Path: /FAQ/Ongkos Kirim
   Aksi: BARU
   Isi (197 karakter): ...
   Simpan ke SiYuan? Jalankan ulang dengan --ya.
   ```
3. Pengguna menjawab "ya" → perintah sama + `--ya`:
   ```
   TERSIMPAN: dokumen '/FAQ/Ongkos Kirim' dibuat di SiYuan (id 20260926095015-42dhvd7).
   ```
4. Dokumen kedua langsung dengan `--ya` (pengguna sudah menyetujui pola yang sama di pesan awal):
   ```
   TERSIMPAN: dokumen '/FAQ/Kebijakan Retur' dibuat di SiYuan (id 20260926095016-2lsub79).
   ```
5. Pengguna lalu bertanya: "coba cari 'retur' di basis pengetahuan saya."
   ```
   $ python3 scripts/siyuan.py cari "retur"
   HASIL PENCARIAN 'retur' (1 dokumen)
   - Kebijakan Retur  [/FAQ/Kebijakan Retur]
       ...Kebijakan Retur...
   ```

## Catatan temuan (dipakai untuk memperbaiki SKILL.md/script)
- **Jeda pengindeksan:** pada percobaan pertama, `cari "retur"` dijalankan **sesaat** setelah dokumen
  dibuat dan sempat menjawab "Tidak ada dokumen yang cocok" - dicoba ulang ~2 detik kemudian dan
  berhasil ketemu. SiYuan memperbarui indeks pencarian sedikit tertunda dari waktu tulis. Sudah
  dicatat di `SKILL.md` §Batasan.
- Isi FAQ **tidak** diawali baris `# Ongkos Kirim`/`# Kebijakan Retur` (judul sudah otomatis dari
  SiYuan) - lihat `references/template-sop-faq.md`.

## Jawaban agent ke pengguna
> "Sudah tersimpan di SiYuan: FAQ Ongkos Kirim dan FAQ Kebijakan Retur (folder /FAQ). Sudah saya coba cari 'retur' dan ketemu dokumennya. Mau saya tambahkan FAQ lain?"
