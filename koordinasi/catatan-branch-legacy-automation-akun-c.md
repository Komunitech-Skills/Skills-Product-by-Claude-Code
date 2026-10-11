# Catatan — branch legacy automation Akun C

**2026-10-11:** Run automation lama sering membuat branch acak (`cursor/iterasi-otomatis-akun-c-HHMM`, suffix `-b3d3`, dll.) sehingga Run History tidak selaras dengan metadata Telegram/git.

**Keputusan:** Satu branch kanonik untuk semua run jadwal → **`cursor/iterasi-otomatis-akun-c-8b42`** (lihat `koordinasi/rutin-cursor-cloud.md`).

**Branch legacy di `origin`:** puluhan `cursor/iterasi-otomatis-akun-c-*` dari periode sebelum normalisasi. **Akun A** boleh merge yang masih berguna ke default / branch kanonik, lalu hapus branch stale — tidak wajib segera; agent Akun C **tidak** membuat branch HHMM baru.

**Branch docs one-off:** `cursor/cloud-md-8b42` (playbook automation) — merge ke kanonik atau tutup setelah PR pemilik, sesuai koordinasi Akun A.
