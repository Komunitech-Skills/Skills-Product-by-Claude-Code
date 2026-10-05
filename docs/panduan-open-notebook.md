# Panduan Pasang Open Notebook untuk Profesional & Pemilik Usaha (bahasa awam)

Open Notebook adalah program **gratis dan open-source** (lisensi MIT) untuk mengumpulkan PDF/artikel/notulen ke satu "notebook" lalu tanya-jawab dengannya — mirip Google NotebookLM, tapi **jalan di komputer Anda sendiri**: dokumen dan hasil tanya-jawab tidak dititipkan ke Google/perusahaan lain. Panduan ini menyiapkan Open Notebook agar bisa dipakai skill **Notebook Riset Lokal** (`notebook-riset-lokal`).

> **Tidak ingin repot?** Komunitech menyediakan **jasa setup berbayar**: pasang Docker, atur kata sandi & keamanan, sambungkan model AI lokal (Ollama, gratis) atau kunci API pilihan Anda, dan buat notebook pertama Anda. Hubungi admin komunitech.com.

> Komunitech **tidak berafiliasi** dengan proyek Open Notebook. "Open Notebook" adalah nama proyek open-source milik pembuatnya (Luis Novo/lfnovo); skill dan panduan ini karya orisinal Komunitech.

**Status panduan (26 September 2026).** Nama file, port, dan bentuk `docker-compose.yml` dicocokkan dengan sumber resmi (`github.com/lfnovo/open-notebook`, commit `3127f14`, versi kode `1.14.0`, dibaca langsung dari kode sumber — README, `docker-compose.yml`, dan router API di folder `api/`) pada 26 September 2026. ⚠️ **Belum diverifikasi**: memasang & menjalankan Open Notebook sungguhan (butuh Docker Desktop yang menyala dan mengunduh image berukuran besar, tidak tersedia di sandbox riset kami) — endpoint, nama field, dan pesan galat dicocokkan dari **membaca kode sumber**, bukan dari server yang benar-benar berjalan. Jika tampilan di komputer Anda berbeda dari yang tertulis di sini, ikuti tulisan di layar Anda atau hubungi kami.

## Daftar isi
1. Sebelum mulai
2. Pasang Docker Desktop
3. Jalankan Open Notebook
4. **Pengamanan wajib** (jangan biarkan bisa dibuka dari internet/jaringan kantor)
5. Pilih model AI: gratis lokal (Ollama) vs API berbayar
6. Kata sandi API (untuk skill ini)
7. Menyalakan Open Notebook setiap hari
8. Cadangan (backup) & pemulihan
9. Update Open Notebook
10. Copot pasang (uninstall)
11. Masalah umum

---

## 1. Sebelum mulai
| Kebutuhan | Keterangan |
|---|---|
| Komputer | Windows 10/11 64-bit, macOS, atau Linux |
| RAM | Minimal **8 GB**, disarankan **16 GB** bila memakai model AI lokal (Ollama) sekaligus — model bahasa lokal memakai RAM cukup besar. Tanpa model lokal (pakai API berbayar), 8 GB cukup |
| Ruang kosong | ≥ 5 GB (image Docker + database) |
| Waktu | ±20–30 menit pemasangan pertama |
| Python 3.8+ | Untuk skill ini (gratis di python.org; Windows: centang **Add Python to PATH**) |

**Jujur soal kebutuhannya:** Open Notebook **hanya dibagikan lewat Docker** (bukan installer klik-klik biasa, bukan `pip install`). Docker Desktop sendiri gratis untuk pemakaian pribadi/usaha kecil, tapi ini satu lapis instalasi tambahan yang perlu diunduh (±500 MB) dan dijalankan lebih dulu. Bagi yang belum pernah memakai Docker, ini bagian yang paling terasa "teknis" — pertimbangkan jasa setup Komunitech bila ingin langsung pakai.

Istilah: **Docker** = "kotak" berisi program siap pakai, agar tidak perlu memasang banyak komponen satu-satu. **Notebook** (di Open Notebook) = folder riset berisi kumpulan sumber (PDF, artikel, catatan) tentang satu topik.

---

## 2. Pasang Docker Desktop
1. Unduh dari situs resmi: **https://www.docker.com/products/docker-desktop/** (Windows/macOS/Linux, pilih sesuai komputer Anda).
2. Pasang seperti aplikasi biasa (Next-Next-Finish), lalu buka Docker Desktop. Tunggu sampai ikon paus di pojok menunjukkan "Docker Desktop is running".
3. Windows: bila diminta mengaktifkan **WSL2**, ikuti petunjuk di layar (Docker Desktop akan memandu, kadang minta restart komputer sekali).
- ✅ **Cek berhasil:** buka Terminal (macOS/Linux) atau PowerShell (Windows), ketik `docker --version` → muncul nomor versi.
- ❌ **Kalau gagal:** ikuti pesan galat di Docker Desktop (biasanya minta aktifkan virtualisasi di BIOS, atau restart).

---

## 3. Jalankan Open Notebook
1. Buat folder baru, misalnya `open-notebook-saya` di Documents.
2. Di dalam folder itu, buat file teks baru bernama **`docker-compose.yml`** (bukan `.txt`), isi persis:
   ```yaml
   services:
     surrealdb:
       image: surrealdb/surrealdb:v2
       command: ["start", "--log", "info", "--user", "root", "--pass", "root", "rocksdb:/mydata/mydatabase.db"]
       user: root
       ports:
         - "127.0.0.1:8000:8000"
       volumes:
         - ./surreal_data:/mydata
       environment:
         - SURREAL_EXPERIMENTAL_GRAPHQL=true
       restart: always

     open_notebook:
       image: lfnovo/open_notebook:v1-latest
       ports:
         - "127.0.0.1:8502:8502"
         - "127.0.0.1:5055:5055"
       environment:
         - OPEN_NOTEBOOK_ENCRYPTION_KEY=ganti-ini-dengan-kalimat-rahasia-anda-sendiri
         - SURREAL_URL=ws://surrealdb:8000/rpc
         - SURREAL_USER=root
         - SURREAL_PASSWORD=root
         - SURREAL_NAMESPACE=open_notebook
         - SURREAL_DATABASE=open_notebook
       volumes:
         - ./notebook_data:/app/data
       depends_on:
         - surrealdb
       restart: always
   ```
   **Penting:** ganti `OPEN_NOTEBOOK_ENCRYPTION_KEY` dengan kalimat rahasia milik Anda sendiri (dipakai untuk mengenkripsi kunci API yang Anda simpan di Open Notebook nanti) — jangan pakai contoh di atas apa adanya, dan jangan bagikan nilai ini ke siapa pun.

   ⚠️ **Baris `127.0.0.1:8502:8502` dan `127.0.0.1:5055:5055` di atas SUDAH DIUBAH Komunitech** dari contoh resmi di halaman GitHub-nya (yang menulis `8502:8502`/`5055:5055` tanpa `127.0.0.1:`) — versi resmi itu membuka Open Notebook untuk **siapa pun di jaringan yang sama** (Wi-Fi kantor/kafe), bukan hanya komputer Anda. Pakai versi di atas (dengan `127.0.0.1:`), bukan yang di halaman resmi mereka, agar sejalan dengan bagian 4 di bawah.
3. Buka Terminal/PowerShell, `cd` ke folder itu, jalankan:
   ```
   docker compose up -d
   ```
4. Tunggu 15–30 detik (unduhan pertama kali bisa 5–10 menit tergantung koneksi internet, karena mengunduh image ±1–2 GB).
5. Buka browser, ketik `http://127.0.0.1:8502`.
- ✅ **Cek berhasil:** tampil halaman awal Open Notebook.
- ❌ **Kalau gagal:** "This site can't be reached" → tunggu lebih lama (pertama kali lambat), atau cek Docker Desktop masih menyala. Jalankan `docker compose logs` di folder yang sama untuk melihat pesan galat.

---

## 4. Pengamanan wajib (±2 menit, sebelum mengisi dokumen usaha)
**Kenapa wajib?** Secara bawaan (contoh dari situs resminya), Open Notebook membuka port **8502** (tampilan web) dan **5055** (API) ke **semua jaringan** komputer Anda, bukan cuma komputer ini sendiri. Artinya siapa pun yang tersambung ke Wi-Fi yang sama berpotensi membuka dokumen dan riwayat tanya-jawab Anda dari browser mereka.

1. Pastikan `docker-compose.yml` Anda memakai baris `127.0.0.1:8502:8502` dan `127.0.0.1:5055:5055` (**bukan** `8502:8502`/`5055:5055` polos) seperti contoh di bagian 3. Bila sudah terlanjur memakai contoh resmi tanpa `127.0.0.1:`, edit file, lalu jalankan ulang: `docker compose down` lalu `docker compose up -d`.
2. **Uji dengan HP** (2 menit): cari alamat IP lokal komputer Anda (Windows: `ipconfig`, cari **IPv4 Address**; macOS: System Settings → Wi-Fi → Details; Linux: `hostname -I`). Sambungkan HP ke Wi-Fi yang sama, buka `http://<IP-komputer>:8502` di browser HP.
   - ✅ **Benar bila HP TIDAK bisa membuka** halamannya (gagal tersambung).
   - ❌ **Kalau HP bisa membuka:** `docker-compose.yml` belum memakai `127.0.0.1:`, atau firewall Windows/macOS mengizinkan. Ulangi langkah 1, jalankan ulang.
3. **Jangan** mengatur *port forwarding* di router atau memakai aplikasi tunnel (ngrok, Cloudflare Tunnel, dll.) untuk membuka Open Notebook dari luar. Ini bukan software yang dirancang untuk diakses lewat internet terbuka.
4. Aktifkan kata sandi API (bagian 6) sekalipun sudah dibatasi ke `127.0.0.1` — lapisan kedua ini berguna bila komputer dipakai bergantian dengan orang lain.

---

## 5. Pilih model AI: gratis lokal (Ollama) vs API berbayar
Open Notebook butuh model AI untuk tanya-jawab, ringkasan, dan podcast. Ada dua pilihan:

| Pilihan | Biaya | Kualitas | Privasi |
|---|---|---|---|
| **Ollama** (model AI jalan di komputer sendiri) | Gratis, tanpa kunci API | Cukup baik untuk ringkasan/tanya-jawab dokumen; lebih lambat & butuh RAM besar (≥16 GB disarankan) di komputer biasa | Paling privat — dokumen & pertanyaan tidak pernah keluar komputer |
| **API berbayar** (OpenAI/Anthropic/Google/dll.) | Bayar per pemakaian (biasanya ribuan rupiah per hari pemakaian wajar) | Lebih cepat & akurat, terutama untuk dokumen panjang/rumit | Dokumen yang Anda tanyakan dikirim ke server penyedia model tsb. (bukan ke Komunitech) |

**Cara pasang Ollama (gratis, disarankan untuk mulai):**
1. Unduh dari **https://ollama.ai** (Windows/macOS/Linux), pasang seperti aplikasi biasa.
2. Buka Terminal, jalankan `ollama pull llama3.1` (atau model lain yang lebih ringan bila komputer terbatas, mis. `ollama pull llama3.2:3b`). Tunggu unduhan selesai (beberapa GB).
3. Di `http://127.0.0.1:8502`, buka **Settings → Models**, tambahkan provider **Ollama** (URL `http://host.docker.internal:11434` di Windows/macOS, atau IP komputer di Linux — ikuti petunjuk di layar Open Notebook), pilih model yang sudah diunduh, jadikan **default chat model**.

**Cara pakai API berbayar:** di **Settings → Models**, pilih provider (OpenAI/Anthropic/dll.), tempel kunci API Anda sendiri (dari akun Anda di provider itu), pilih model, jadikan default. Kunci API tersimpan di database Open Notebook **milik Anda sendiri** (terenkripsi dengan `OPEN_NOTEBOOK_ENCRYPTION_KEY` di bagian 3), bukan di Komunitech.

- ✅ **Cek berhasil:** di **Settings → Models**, ada minimal satu model bahasa (`language`) yang dijadikan **Default**. Tanpa ini, perintah `tanya`/`ringkasan` skill akan menolak dengan pesan jelas.

---

## 6. Kata sandi API (untuk skill ini)
Secara bawaan, API Open Notebook **tanpa kata sandi** (siapa pun yang bisa menghubungi `127.0.0.1:5055` di komputer itu bisa memakainya). Untuk komputer yang dipakai bergantian, aktifkan kata sandi:
1. Di `docker-compose.yml`, tambahkan baris di bagian `environment` service `open_notebook`:
   ```yaml
   - OPEN_NOTEBOOK_PASSWORD=kata-sandi-anda-sendiri
   ```
2. Jalankan ulang: `docker compose up -d`.
3. Di komputer yang akan memakai skill (biasanya komputer yang sama), buka Terminal:
   ```
   python3 <folder-skill>/scripts/notebook.py simpan-kunci
   ```
   (Windows: `python`/`py`). Tempel kata sandi yang sama seperti langkah 1 (tidak terlihat saat diketik) → Enter.
4. Uji: `python3 <folder-skill>/scripts/notebook.py cek`
- ✅ **Cek berhasil:** tampil `"pesan": "Open Notebook bisa dihubungi dan siap dipakai."`
- ❌ **Kalau gagal "401":** kata sandi yang disimpan skill beda dengan `OPEN_NOTEBOOK_PASSWORD` di `docker-compose.yml`. Ulangi `simpan-kunci` dengan `--ya`.

**Tidak mengaktifkan kata sandi?** Skill tetap bisa dipakai (tanpa `simpan-kunci`) selama Open Notebook dibatasi ke `127.0.0.1` (bagian 4) dan komputer itu tidak dipakai orang lain.

---

## 7. Menyalakan Open Notebook setiap hari
- Docker Desktop dan container Open Notebook perlu **tetap menyala** agar skill bisa dipakai. `restart: always` di `docker-compose.yml` membuatnya otomatis menyala lagi setiap kali Docker Desktop/komputer dinyalakan ulang — Anda tidak perlu mengetik `docker compose up -d` setiap hari, cukup pastikan Docker Desktop terbuka.
- Untuk kantor/usaha, pertimbangkan mini PC yang selalu menyala, atau **jasa setup Komunitech**.

---

## 8. Cadangan (backup) & pemulihan
Semua data Anda ada di folder `surreal_data` dan `notebook_data` di dalam folder tempat `docker-compose.yml` berada.
1. `docker compose stop` (hentikan dulu, agar file tidak sedang ditulis).
2. Salin folder `surreal_data` dan `notebook_data` ke flashdisk/hard disk eksternal atau folder cloud pribadi terenkripsi.
3. `docker compose up -d` (jalankan lagi).
4. **Pemulihan** (komputer baru/rusak): pasang Docker + `docker-compose.yml` yang sama (bagian 2–3), `docker compose stop` sebelum menjalankan pertama kali, timpa kedua folder dengan cadangan, lalu `docker compose up -d`.
- Skill `notebook-riset-lokal` **tidak** membuat cadangan otomatis — lakukan manual tiap minggu.

---

## 9. Update Open Notebook
1. **Backup dulu** (bagian 8).
2. `docker compose pull` (unduh versi terbaru image `lfnovo/open_notebook:v1-latest`).
3. `docker compose up -d` (jalankan ulang dengan image baru; migrasi database berjalan otomatis).
- ❌ **Kalau gagal setelah update:** kembalikan cadangan (bagian 8), laporkan ke dukungan Komunitech.

---

## 10. Copot pasang (uninstall)
1. Di folder `docker-compose.yml`: `docker compose down` (matikan & hapus container, folder data tetap ada).
2. Hapus folder `open-notebook-saya` (setelah backup bila datanya masih dibutuhkan) untuk menghapus semua data.
3. Copot Docker Desktop lewat Control Panel/Applications seperti aplikasi biasa, bila tidak dipakai untuk program lain.

---

## 11. Masalah umum
| Gejala | Penyebab | Solusi |
|---|---|---|
| Browser: "This site can't be reached" di `8502` | Container belum siap / Docker Desktop mati | Tunggu lebih lama, cek `docker compose logs`, pastikan Docker Desktop menyala |
| Skill: "tidak bisa dihubungi" | Container mati atau `--url` skill tidak cocok port | Cek `docker compose ps` menunjukkan container `open_notebook` "running"; skill defaultnya `http://127.0.0.1:5055` |
| Skill: "401" | `OPEN_NOTEBOOK_PASSWORD` aktif tapi kata sandi skill belum/salah disimpan | Ulangi `simpan-kunci --ya` dengan kata sandi yang sama persis dengan `docker-compose.yml` |
| Skill: "Belum ada model AI default" | Belum atur model di Settings → Models, atau belum dijadikan Default | Ikuti bagian 5 |
| HP di Wi-Fi sama bisa membuka `8502`/`5055` | Port belum dibatasi ke `127.0.0.1` | Ulangi bagian 4 |
| Podcast gagal / tombol tidak ada | Profil episode/pembicara belum dibuat, atau belum ada model text-to-speech | Buat dulu di Settings → Podcasts (fitur ini opsional, bisa perlu API TTS berbayar) |
| Komputer terasa berat/lambat saat memakai Ollama | Model lokal butuh RAM/CPU besar | Pilih model lebih kecil (`llama3.2:3b`), atau pindah ke API berbayar (bagian 5) |

Butuh bantuan? **Jasa setup Komunitech** mengerjakan seluruh panduan ini bersama Anda, termasuk pengamanan wajib bagian 4, pemilihan model AI, dan menjalankan Open Notebook otomatis setiap komputer menyala.

Komunitech tidak berafiliasi dengan proyek Open Notebook; "Open Notebook" adalah nama proyek open-source milik pembuatnya.
