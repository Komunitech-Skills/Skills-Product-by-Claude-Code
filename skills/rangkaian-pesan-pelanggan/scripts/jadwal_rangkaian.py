#!/usr/bin/env python3
"""Hitung tanggal kirim rangkaian pesan pelanggan (dikirim manual oleh pemilik, mode copilot).

Hanya library standar Python 3.8+. Tidak ada akses jaringan. Tidak mengirim apa pun.

Contoh:
  python3 jadwal_rangkaian.py --situasi sambutan --mulai 2026-10-07
  python3 jadwal_rangkaian.py --situasi ulasan --mulai 2026-10-07 --pelanggan 25 --per-hari 10
  python3 jadwal_rangkaian.py --situasi perpanjangan --mulai 2026-12-20 --libur 2026-12-25
  python3 jadwal_rangkaian.py --hari "0,2,6" --mulai 2026-10-07 --termasuk-minggu

Aturan: tanggal yang jatuh di Minggu/libur digeser (maju untuk pesan sesudah tanggal acuan,
mundur untuk pesan sebelum tanggal acuan). Satu pelanggan maksimal satu pesan per hari.
Total pesan per hari dibatasi --per-hari (default 10). Python di Windows: python atau py.
"""
import argparse
import json
import sys
from datetime import date, datetime, timedelta

HARI = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
BULAN = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli",
         "Agustus", "September", "Oktober", "November", "Desember"]

# (jarak hari dari tanggal acuan, tujuan, kanal yang cocok)
SITUASI = {
    "sambutan": ("pelanggan baru (acuan: hari pembelian pertama)", [
        (0, "Terima kasih + apa yang terjadi berikutnya", "WA / Telegram"),
        (3, "Tips pakai agar hasilnya terasa", "WA / email"),
        (10, "Tanya kabar, buka pintu untuk kendala", "WA"),
        (21, "Ajak mencoba produk/menu lain (hanya bila relevan)", "WA / email")]),
    "edukasi": ("prospek yang sudah minta info (acuan: hari mereka daftar/tanya)", [
        (0, "Sambut + janji isi rangkaian", "email / Telegram / WA"),
        (4, "Satu pengetahuan berguna #1", "email / Telegram"),
        (10, "Satu pengetahuan berguna #2 (kesalahan umum)", "email / Telegram"),
        (17, "Contoh nyata dari usaha Anda sendiri", "email / Telegram"),
        (24, "Ajakan lembut: tanya/coba/pesan", "WA / email")]),
    "keranjang": ("pesanan/keranjang tertunda di toko sendiri (acuan: hari terakhir aktif)", [
        (0, "Tawarkan bantuan menyelesaikan pesanan", "WA"),
        (1, "Jawab kemungkinan kendala (ongkir, stok, cara bayar)", "WA"),
        (3, "Penutup sopan, pesanan disimpan/dilepas", "WA")]),
    "setelah-beli": ("sesudah pembelian produk (acuan: hari beli)", [
        (0, "Konfirmasi + estimasi kirim/layanan", "WA / Telegram"),
        (2, "Barang sampai? Cara pakai singkat", "WA"),
        (7, "Cek kepuasan + pintu bantuan", "WA"),
        (14, "Tips lanjutan / perawatan", "WA / email")]),
    "ulasan": ("minta ulasan (acuan: hari barang diterima/layanan selesai)", [
        (1, "Minta ulasan jujur, satu tautan", "WA"),
        (6, "Pengingat tunggal, boleh diabaikan", "WA")]),
    "perpanjangan": ("perpanjangan/langganan (acuan: tanggal jatuh tempo)", [
        (-14, "Pengingat awal + cara perpanjang", "WA / email"),
        (-7, "Ringkasan manfaat yang sudah dipakai + opsi", "WA / email"),
        (-2, "Pengingat terakhir sebelum jatuh tempo", "WA"),
        (3, "Sudah lewat: tawarkan bantuan, tanpa menekan", "WA")]),
    "reaktivasi": ("pelanggan lama diam (acuan: hari pesan pertama; isi pesan: skill aktifkan-kembali-pelanggan)", [
        (0, "Sapaan tanpa jualan", "WA"),
        (10, "Tanya kebutuhan", "WA"),
        (24, "Penutup sopan", "WA")]),
    "peluncuran": ("peluncuran produk baru (acuan: hari peluncuran; hanya pelanggan/pengikut opt-in)", [
        (-3, "Kabar akan hadir (tanpa janji berlebihan)", "Telegram / email / WA"),
        (0, "Pengumuman resmi + cara pesan", "Telegram / email / WA"),
        (3, "Contoh pemakaian nyata", "Telegram / email"),
        (7, "Pengingat tunggal (tenggat hanya bila sungguh ada)", "WA / email")]),
}

MAKS_PESAN = 8
MAKS_CARI = 400


def gagal(pesan):
    print(f"ERROR: {pesan}", file=sys.stderr)
    sys.exit(1)


def parse_tgl(teks, nama):
    t = str(teks).strip()
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y"):
        try:
            return datetime.strptime(t, fmt).date()
        except ValueError:
            pass
    gagal(f"{nama} tidak dikenali: {teks!r}. Pakai format YYYY-MM-DD, mis. 2026-10-07")


def tgl_id(d):
    return f"{HARI[d.weekday()]}, {d.day} {BULAN[d.month - 1]} {d.year}"


def ringkas_nomor(angka):
    """[1,2,3,5] -> '1-3, 5'"""
    angka = sorted(angka)
    bagian, awal, prev = [], None, None
    for n in angka:
        if awal is None:
            awal = prev = n
        elif n == prev + 1:
            prev = n
        else:
            bagian.append((awal, prev))
            awal = prev = n
    if awal is not None:
        bagian.append((awal, prev))
    return ", ".join(str(a) if a == b else f"{a}-{b}" for a, b in bagian)


def hitung_jadwal(mulai, langkah, pelanggan=1, per_hari=10, libur=frozenset(), termasuk_minggu=False):
    """langkah: list jarak hari (boleh negatif). Mengembalikan dict hasil.

    Tiap pelanggan diproses berurutan; tiap pesan ditaruh di tanggal rencana, lalu digeser (maju bila
    jarak >= 0, mundur bila jarak < 0) sampai bukan Minggu/libur, pelanggan itu belum punya pesan
    di hari tsb, dan beban hari itu belum mencapai per_hari.
    """
    beban = {}
    jadwal = []  # jadwal[p][k] = date
    libur_hari = lambda d: d in libur or (not termasuk_minggu and d.weekday() == 6)  # noqa: E731
    semua_maju = all(j >= 0 for j in langkah)
    t_prev = 0
    for _ in range(pelanggan):
        if semua_maju:
            # Mulai pelanggan ini ditunda (hari demi hari) sampai SEMUA pesannya muat di batas harian,
            # sehingga tiap kelompok pelanggan memulai rangkaian pada hari yang sama.
            for t in range(t_prev, t_prev + MAKS_CARI * 10):
                dipakai, baris, muat = set(), [], True
                for k, jarak in enumerate(langkah):
                    d = mulai + timedelta(days=t + jarak)
                    if baris:  # jaga jarak minimal sama dengan rencana (mis. 5 hari) walau pesan sebelumnya digeser
                        d = max(d, baris[-1] + timedelta(days=jarak - langkah[k - 1]))
                    while libur_hari(d) or d in dipakai:
                        d += timedelta(days=1)
                    if beban.get(d, 0) >= per_hari:
                        muat = False
                        break
                    dipakai.add(d)
                    baris.append(d)
                if muat:
                    t_prev = t
                    break
            else:
                gagal("tidak menemukan hari kirim yang kosong; naikkan --per-hari atau kurangi --pelanggan")
        else:
            dipakai, baris = set(), []
            for k, jarak in enumerate(langkah):
                arah = -1 if jarak < 0 else 1
                d = mulai + timedelta(days=jarak)
                if baris and jarak >= 0 and langkah[k - 1] >= 0:
                    d = max(d, baris[-1] + timedelta(days=jarak - langkah[k - 1]))
                for _ in range(MAKS_CARI):
                    if not libur_hari(d) and d not in dipakai and beban.get(d, 0) < per_hari:
                        break
                    d += timedelta(days=arah)
                else:
                    gagal("tidak menemukan hari kirim yang kosong; naikkan --per-hari atau kurangi --pelanggan")
                dipakai.add(d)
                baris.append(d)
        for d in baris:
            beban[d] = beban.get(d, 0) + 1
        jadwal.append(baris)
    peringatan = []
    for i, baris in enumerate(jadwal, start=1):
        if any(b <= a for a, b in zip(baris, baris[1:])):
            peringatan.append(f"Urutan pesan pelanggan ke-{i} berubah karena banyak hari libur/penuh; periksa manual.")
            break
    return {"jadwal": jadwal, "beban": beban, "peringatan": peringatan}


def main():
    p = argparse.ArgumentParser(description="Jadwal rangkaian pesan pelanggan (kirim manual)")
    p.add_argument("--situasi", choices=sorted(SITUASI), help="jenis rangkaian; atau pakai --hari sendiri")
    p.add_argument("--hari", help="jarak hari dari tanggal acuan, dipisah koma, mis. '0,3,10' atau '-14,-7,-2,3'")
    p.add_argument("--mulai", required=True, help="tanggal acuan YYYY-MM-DD (lihat arti per situasi di keluaran)")
    p.add_argument("--pelanggan", type=int, default=1, help="jumlah pelanggan yang memulai rangkaian ini (default 1)")
    p.add_argument("--per-hari", type=int, default=10, help="batas total pesan per hari dari satu nomor (default 10)")
    p.add_argument("--libur", default="", help="tanggal libur dipisah koma, mis. '2026-12-25,2026-12-26'")
    p.add_argument("--termasuk-minggu", action="store_true", help="boleh kirim hari Minggu (default tidak)")
    p.add_argument("--hari-ini", help="tanggal hari ini YYYY-MM-DD, untuk menandai jadwal yang sudah lewat")
    p.add_argument("--format", choices=["teks", "json"], default="teks")
    a = p.parse_args()

    if not a.situasi and not a.hari:
        gagal("isi --situasi (" + ", ".join(sorted(SITUASI)) + ") atau --hari")
    mulai = parse_tgl(a.mulai, "tanggal mulai")
    hari_ini = parse_tgl(a.hari_ini, "tanggal hari ini") if a.hari_ini else date.today()
    if a.hari:
        try:
            jarak = [int(x.strip()) for x in a.hari.split(",") if x.strip()]
        except ValueError:
            gagal(f"--hari harus angka dipisah koma, mis. '0,3,10' (diberikan: {a.hari!r})")
        if not jarak:
            gagal("--hari kosong")
        if len(set(jarak)) != len(jarak):
            gagal("--hari berisi jarak kembar")
        jarak = sorted(jarak)
        langkah = [(j, f"Pesan {i}", "-") for i, j in enumerate(jarak, start=1)]
        judul = "rangkaian kustom"
    else:
        judul, langkah = SITUASI[a.situasi]
    if len(langkah) > MAKS_PESAN:
        gagal(f"maksimal {MAKS_PESAN} pesan per rangkaian; lebih dari itu terkesan memaksa")
    if any(abs(j) > 120 for j, _, _ in langkah):
        gagal("jarak hari harus antara -120 dan 120")
    if not 1 <= a.pelanggan <= 2000:
        gagal("--pelanggan harus 1 sampai 2000")
    if not 1 <= a.per_hari <= 50:
        gagal("--per-hari harus 1 sampai 50")
    libur = {parse_tgl(x, "tanggal libur") for x in a.libur.split(",") if x.strip()}

    hasil = hitung_jadwal(mulai, [j for j, _, _ in langkah], a.pelanggan, a.per_hari, libur, a.termasuk_minggu)
    jadwal, beban = hasil["jadwal"], hasil["beban"]
    catatan = list(hasil["peringatan"])
    if a.per_hari > 15:
        catatan.append("Batas di atas 15 pesan per hari per nomor tidak disarankan (risiko nomor dibatasi WhatsApp).")
    catatan.append("Pelanggan yang membalas apa pun, komplain, atau minta berhenti: hentikan rangkaiannya.")
    catatan.append("Kirim jam 09.00-20.00 waktu setempat pelanggan (WIB/WITA/WIT).")

    langkah_out = []
    for k, (j, tujuan, kanal) in enumerate(langkah):
        per_tgl = {}
        for i, baris in enumerate(jadwal, start=1):
            per_tgl.setdefault(baris[k], []).append(i)
        langkah_out.append({
            "ke": k + 1, "jarak": j, "tujuan": tujuan, "kanal": kanal,
            "tanggal": [{"tanggal": d.isoformat(), "teks": tgl_id(d), "pelanggan": sorted(ns),
                         "sudah_lewat": d < hari_ini} for d, ns in sorted(per_tgl.items())]})
    if any(t["sudah_lewat"] for s in langkah_out for t in s["tanggal"]):
        catatan.append("Sebagian jadwal sudah lewat. Jangan kirim beruntun; mulai dari pesan yang sesuai keadaan hari ini.")
    out = {"situasi": a.situasi or "kustom", "arti_acuan": judul, "acuan": mulai.isoformat(),
           "pelanggan": a.pelanggan, "per_hari": a.per_hari, "langkah": langkah_out,
           "beban_harian": {d.isoformat(): n for d, n in sorted(beban.items())}, "catatan": catatan}
    if a.format == "json":
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return

    print(f"Rangkaian: {out['situasi']} | acuan (H+0): {tgl_id(mulai)} = {judul}")
    print(f"Pelanggan: {a.pelanggan} | batas {a.per_hari} pesan/hari | Minggu {'boleh' if a.termasuk_minggu else 'dilewati'}")
    print()
    print("| Pesan | Jarak | Tujuan | Kanal | Tanggal kirim (pelanggan ke-) |")
    print("|---|---|---|---|---|")
    for s in langkah_out:
        jr = f"H{s['jarak']:+d}" if s["jarak"] else "H+0"
        tg = []
        for t in s["tanggal"]:
            lewat = " [LEWAT]" if t["sudah_lewat"] else ""
            if a.pelanggan == 1:
                tg.append(f"{t['teks']}{lewat}")
            else:
                tg.append(f"{t['teks']}: pelanggan {ringkas_nomor(t['pelanggan'])} ({len(t['pelanggan'])}){lewat}")
        print(f"| {s['ke']} | {jr} | {s['tujuan']} | {s['kanal']} | {'<br>'.join(tg)} |")
    if a.pelanggan > 1:
        print()
        print("Beban per hari (pesan): " + "; ".join(f"{tgl_id(d)}: {n}" for d, n in sorted(beban.items())))
        print(f"Beban tertinggi: {max(beban.values())} pesan/hari")
    print()
    for c in catatan:
        print(f"* {c}")


if __name__ == "__main__":
    main()
