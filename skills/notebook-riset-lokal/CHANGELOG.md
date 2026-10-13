# Riwayat perubahan — notebook-riset-lokal

Catatan teknis per versi (dipindah dari README agar halaman pembeli ringkas).

## Catatan revisi 1.0.7 (2026-10-01)
Hasil uji sebelum/sesudah di OpenClaw (`examples/00-openclaw-sebelum-sesudah.md`):
- Bagian baru **Keamanan & akses dari komputer lain** di SKILL.md: 127.0.0.1 = komputer itu sendiri (tidak perlu VPN; saran "VPN lalu buka 127.0.0.1" dihapus karena keliru).
- Status kata sandi **diperiksa** lewat `cek` (field `auth_aktif`), bukan diklaim "tanpa autentikasi". Fakta `OPEN_NOTEBOOK_PASSWORD` dicocokkan dengan dokumentasi resmi Open Notebook (`docs/5-CONFIGURATION/security.md`: tanpa variabel ini autentikasi mati; bila diisi, web & API minta kata sandi; sifatnya pengaman dasar).
- Agent tidak lagi menawarkan memasang VPN/Tailscale/tunnel; akses dari luar hanya disebut sebagai opsi lanjutan dengan peringatan keamanan.
- Bahasa awam: tidak menyebut nama perintah ke pengguna.
