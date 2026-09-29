# Contoh 6 (Uji Akun B): Landing page order WA, `cek-cepat` tanpa Uptime Kuma

**Permintaan pengguna:** "Cek dong landing page order WA saya masih hidup nggak, belum sempat pasang Uptime Kuma."

**Perintah (server HTTP lokal buatan penguji sebagai pengganti landing page nyata, respons 200):**
```bash
python3 scripts/pantau.py cek-cepat http://127.0.0.1:9201 --json
```

**Keluaran nyata:**
```json
{
  "ok": true,
  "url": "http://127.0.0.1:9201",
  "kode_http": 200,
  "kategori": "OK",
  "waktu_respons_ms": 2.5,
  "ssl": null
}
```
`ssl: null` benar karena alamatnya `http://` (bukan `https://`) — sesuai dokumentasi ("SSL: - (alamat http://, bukan https://)" pada mode teks).

## Temuan audit terkait redirect (relevan untuk landing page yang biasanya pakai shortlink)
Diuji terpisah: server lokal yang mengembalikan `301` dengan header `Location` ke server 200 lain →
```
python3 scripts/pantau.py cek-cepat http://127.0.0.1:9202
HTTP    : 200 (OK)     <-- BUKAN 301
```
**Sebab:** `urllib.request.urlopen` (dipakai `cmd_cek_cepat`) **mengikuti redirect secara otomatis** sebelum kode sampai ke logika kategori `300-399 → REDIRECT` (baris `kategori = ... "REDIRECT" if 300 <= kode < 400 ...`). Akibatnya kategori "REDIRECT" pada dokumentasi `SKILL.md`/README praktis **tidak pernah tercapai** untuk redirect normal (yang punya `Location` valid dan tujuannya hidup) — pengguna hanya akan melihat status HTTP **tujuan akhir**, bukan kode 301/302 aslinya. Ini **bukan celah keamanan** (tidak ada data bocor), tapi **klaim fungsional yang meleset**: dokumentasi menyiratkan kode 3xx akan terlihat sebagai "REDIRECT", padahal pada kasus paling umum (redirect yang berfungsi) itu tidak pernah muncul. Baru terlihat sebagai galat biasa bila tujuan redirect-nya mati (diuji: redirect ke port tertutup → `GALAT: tidak bisa menghubungi ... Connection refused`, bukan pesan yang menjelaskan bahwa itu gagal karena mengikuti redirect). **Rekomendasi untuk pembuat:** perjelas di README/SKILL.md bahwa `cek-cepat` melaporkan status HTTP **setelah** mengikuti redirect (perilaku ini sebenarnya masuk akal untuk kasus "toko saya pakai shortlink ke landing page" — pengguna memang lebih peduli status akhir — tapi kalimat "kategori REDIRECT" di dokumentasi perlu diluruskan atau dihapus).

## Skenario link WA (`wa.me`) — tidak diuji langsung ke `wa.me` sungguhan
Sesuai batasan tugas (situs publik hanya dicoba sekali, dan bukan ke domain milik pihak ketiga berulang), pengujian memakai server lokal sebagai simulasi. Perilaku `cek-cepat` terhadap `wa.me` sungguhan secara teknis sama (satu request HTTP biasa) — tidak ada indikasi kode khusus yang membedakan domain.
