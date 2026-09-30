#!/usr/bin/env python3
"""Uji regresi kanboard-papan-kerja dengan server Kanboard TIRUAN (tests/server_tiruan.py).

Jalankan dari folder skill:  python3 tests/uji_regresi.py
Tidak butuh internet/Kanboard asli. HOME diarahkan ke folder sementara agar ~/.komunitech asli tidak tersentuh.
"""
import datetime as dt
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time

SINI = os.path.dirname(os.path.abspath(__file__))
SKRIP = os.path.join(os.path.dirname(SINI), "scripts", "kanboard.py")
sys.path.insert(0, SINI)
sys.path.insert(0, os.path.join(os.path.dirname(SINI), "scripts"))
import server_tiruan as st  # noqa: E402
import kanboard as kbmod  # noqa: E402

RAHASIA = [st.TOKEN_APP, st.TOKEN_BUDI, st.TOKEN_RINA]
HASIL = {"lulus": 0, "gagal": []}
RUMAH = tempfile.mkdtemp(prefix="uji-kanboard-")
WIB = dt.timezone(dt.timedelta(hours=7))


def jalan(argv, pengguna="budi", url=None, env_extra=None):
    env = {k: v for k, v in os.environ.items() if not k.startswith("KANBOARD_")}
    env["HOME"] = RUMAH
    env["USERPROFILE"] = RUMAH
    if pengguna:
        env["KANBOARD_USER"] = pengguna
        env["KANBOARD_TOKEN"] = {"budi": st.TOKEN_BUDI, "rina": st.TOKEN_RINA, "jsonrpc": st.TOKEN_APP}.get(
            pengguna, "token-salah-sekali-123456")
    if url:
        env["KANBOARD_URL"] = url
    env.update(env_extra or {})
    p = subprocess.run([sys.executable, SKRIP] + argv, capture_output=True, text=True, env=env, timeout=60)
    for r in RAHASIA:
        if r in p.stdout or r in p.stderr:
            gagal(f"TOKEN BOCOR di keluaran {argv}")
    return p.returncode, p.stdout, p.stderr


def cek(nama, kondisi, info=""):
    if kondisi:
        HASIL["lulus"] += 1
    else:
        gagal(f"{nama} {info}")


def gagal(pesan):
    HASIL["gagal"].append(pesan)
    print("GAGAL:", pesan)


def server(mode="normal", tz="UTC"):
    srv, negara = st.jalankan(0, mode, tz)
    return srv, negara, f"http://127.0.0.1:{srv.server_port}"


def main():
    # ---------------------------------------------------------------- tanpa server
    rc, out, err = jalan(["template"], pengguna=None)
    cek("template", rc == 0 and "produksi" in out and "order-pengiriman" in out and "proyek-jasa" in out, err)
    for kode, t in kbmod.TEMPLATE.items():
        cek(f"template {kode} >= 4 kolom", len(t["kolom"]) >= 4)
    cek("order-pengiriman kolom terakhir = Diterima", kbmod.TEMPLATE["order-pengiriman"]["kolom"][-1][0] == "Diterima")
    rc, out, err = jalan(["cek", "--pap", "1"], pengguna=None)
    cek("allow_abbrev mati", rc == 2 and "unrecognized" in err)
    rc, out, err = jalan(["cek"], pengguna=None, url="http://127.0.0.1:9")
    cek("tanpa kunci -> 3", rc == 3 and "simpan-kunci" in err, err)

    # tanggal
    acuan = dt.date(2026, 9, 30)  # Rabu
    pt = kbmod.parse_tenggat
    cek("besok jam 14:00", pt("besok jam 14:00", acuan) == (dt.date(2026, 10, 1), 14, 0))
    cek("pukul 9", pt("lusa pukul 9", acuan) == (dt.date(2026, 10, 2), 9, 0))
    cek("Jumat", pt("Jumat", acuan)[0] == dt.date(2026, 10, 2))
    cek("Jumat depan", pt("Jumat depan", acuan)[0] == dt.date(2026, 10, 9))
    cek("Rabu (hari ini)", pt("rabu", acuan)[0] == acuan)
    cek("minggu depan", pt("minggu depan", acuan)[0] == dt.date(2026, 10, 7))
    cek("Minggu (hari)", pt("Minggu", acuan)[0] == dt.date(2026, 10, 4))
    cek("25/10", pt("25/10", acuan)[0] == dt.date(2026, 10, 25))
    cek("akhir bulan", pt("akhir bulan", acuan)[0] == dt.date(2026, 9, 30))
    cek("akhir bulan (Feb)", pt("akhir bulan", dt.date(2028, 2, 3))[0] == dt.date(2028, 2, 29))
    cek("awal bulan depan", pt("awal bulan depan", dt.date(2026, 12, 15))[0] == dt.date(2027, 1, 1))
    cek("5/1 -> tahun depan", pt("5/1", acuan)[0] == dt.date(2027, 1, 5))
    cek("25 Oktober 2026", pt("25 Oktober 2026", acuan)[0] == dt.date(2026, 10, 25))
    cek("default jam 17", pt("2026-10-05", acuan) == (dt.date(2026, 10, 5), 17, 0))
    for buruk in ("besok lusa", "kapan-kapan", "31/02/2026", "besok jam 25:00"):
        try:
            pt(buruk, acuan)
            gagal(f"tenggat buruk diterima: {buruk}")
        except kbmod.Gagal as e:
            cek(f"tenggat buruk {buruk}", e.kode == 2)
    s, epoch = kbmod.tenggat_ke_server(dt.date(2026, 10, 1), 10, 0, "WIB", kbmod.zona_server("UTC"))
    cek("WIB->UTC", s == "2026-10-01 03:00", s)
    s, _ = kbmod.tenggat_ke_server(dt.date(2026, 10, 1), 10, 0, "WIB", kbmod.zona_server("Asia/Jakarta"))
    cek("WIB->Asia/Jakarta", s == "2026-10-01 10:00", s)
    s, _ = kbmod.tenggat_ke_server(dt.date(2026, 10, 1), 10, 0, "WITA", kbmod.zona_server("Asia/Jakarta"))
    cek("WITA->Asia/Jakarta", s == "2026-10-01 09:00", s)

    # alamat
    for url, harap in (("http://kanboard.contoh.com", 2), ("https://kanboard.contoh.com", 2),
                       ("http://192.168.1.20:8080", 2), ("http://u:p@127.0.0.1:8080", 2),
                       ("ftp://127.0.0.1", 2), ("http://127.0.0.1:8080/?x=1", 2)):
        rc, out, err = jalan(["cek", "--url", url])
        cek(f"alamat ditolak {url}", rc == harap, f"rc={rc} {err}")

    # daftar izin metode (tanpa jaringan)
    class A:
        url, kunci_file, timeout = "http://127.0.0.1:9", None, 1
    os.environ["KANBOARD_USER"], os.environ["KANBOARD_TOKEN"] = "budi", "x" * 20
    try:
        kb = kbmod.Kanboard(A())
        for m in ("removeTask", "removeProject", "removeColumn", "closeTask", "createUser", "updateTask",
                  "removeUser", "execute"):
            try:
                kb.rpc(m, {})
                gagal(f"metode terlarang lolos: {m}")
            except kbmod.Gagal as e:
                cek(f"daftar izin tolak {m}", "daftar izin" in str(e))
    finally:
        os.environ.pop("KANBOARD_USER", None)
        os.environ.pop("KANBOARD_TOKEN", None)
    cek("tidak ada metode hapus di daftar izin",
        not any(m.startswith(("remove", "close", "delete", "disable")) for m in kbmod.METODE_BACA | kbmod.METODE_TULIS))

    # ---------------------------------------------------------------- server normal (UTC)
    srv, ng, url = server()
    try:
        rc, out, err = jalan(["cek"], url=url)
        cek("cek budi", rc == 0 and "v1.2.54" in out and "token pribadi pengguna 'budi'" in out and "UTC" in out, err)
        rc, out, err = jalan(["cek"], pengguna="jsonrpc", url=url)
        cek("cek jsonrpc", rc == 0 and "APLIKASI" in out, err)
        rc, out, err = jalan(["cek"], pengguna="rina", url=url)
        cek("cek rina app-user", rc == 0 and "--pribadi" in out, err)
        rc, out, err = jalan(["cek"], pengguna="palsu", url=url)
        cek("token salah -> 5", rc == 5 and "401" in err, err)
        rc, out, err = jalan(["cek", "--url", url + "/jsonrpc.php"])
        cek("url berakhiran jsonrpc.php diterima", rc == 0, err)

        # kunci dari file
        kf = os.path.join(RUMAH, "kunci.json")
        with open(kf, "w") as f:
            json.dump({"pengguna": "budi", "token": st.TOKEN_BUDI}, f)
        os.chmod(kf, 0o600)
        rc, out, err = jalan(["cek", "--kunci-file", kf], pengguna=None, url=url)
        cek("kunci-file", rc == 0 and "PERINGATAN" not in err, err)
        if os.name != "nt":
            os.chmod(kf, 0o644)
            rc, out, err = jalan(["cek", "--kunci-file", kf], pengguna=None, url=url)
            cek("kunci-file 644 diperingatkan", rc == 0 and "chmod 600" in err, err)
        with open(kf, "w") as f:
            f.write("bukan json")
        rc, out, err = jalan(["cek", "--kunci-file", kf], pengguna=None, url=url)
        cek("kunci-file rusak -> 3", rc == 3 and "rusak" in err, err)

        rc, out, err = jalan(["daftar-papan", "--json"], url=url)
        d = json.loads(out) if rc == 0 else {}
        cek("daftar-papan", rc == 0 and len(d.get("papan", [])) == 3, err)
        rc, out, err = jalan(["daftar-papan"], pengguna="rina", url=url)
        cek("daftar-papan rina kosong", rc == 0 and "belum ada papan" in out, err)

        now = time.time()
        rc, out, err = jalan(["terlambat", "--json"], url=url)
        ids = sorted(k["id"] for k in json.loads(out)["kartu"]) if rc == 0 else []
        cek("terlambat", ids == [2, 3, 7], f"{ids} {err}")
        rc, out, err = jalan(["terlambat"], pengguna="jsonrpc", url=url)
        cek("terlambat mode aplikasi sama", rc == 0 and "Jumlah: 3" in out, err)

        hari_ini = dt.datetime.fromtimestamp(now, WIB).date()
        harap = sorted(t["id"] for t in ng.data["tugas"].values()
                       if t["is_active"] and t["date_due"] and t["project_id"] in (1, 2)
                       and dt.datetime.fromtimestamp(t["date_due"], WIB).date() == hari_ini)
        rc, out, err = jalan(["hari-ini", "--json"], url=url)
        ids = sorted(k["id"] for k in json.loads(out)["kartu"]) if rc == 0 else []
        cek("hari-ini", ids == harap, f"{ids} vs {harap} {err}")

        rc, out, err = jalan(["macet", "--json"], url=url)
        ids = sorted(k["id"] for k in json.loads(out)["kartu"]) if rc == 0 else []
        cek("macet >=3", ids == [3, 4, 6], f"{ids} {err}")
        rc, out, err = jalan(["macet", "--hari", "7"], url=url)
        cek("macet >=7", rc == 0 and "#4 " in out and "#3 " not in out and "diam 9 hari" in out, out + err)
        rc, out, err = jalan(["macet", "--hari", "0"], url=url)
        cek("--hari 0 ditolak", rc == 2, err)
        rc, out, err = jalan(["macet", "--papan", "Batik"], url=url)
        cek("macet per papan", rc == 0 and "#6 " in out and "#3 " not in out, out + err)

        rc, out, err = jalan(["laporan"], url=url)
        cek("laporan", rc == 0 and out.startswith("LAPORAN PAPAN KERJA") and "TERLAMBAT (3)" in out
            and "MACET >= 3 HARI (3)" in out and len(out) <= kbmod.MAKS_TELEGRAM + 1, out + err)
        cek("laporan tanpa kartu ditutup/arsip", "Kartu ditutup lama" not in out and "papan arsip" not in out)
        cek("PIC nama tampil", "PIC: Budi Santoso" in out or "PIC: sari" in out, out)

        rc, out, err = jalan(["kolom", "--papan", "konveksi"], url=url)
        cek("kolom", rc == 0 and "Produksi (id 3): 2 kartu / batas 5" in out, out + err)
        rc, out, err = jalan(["kolom", "--papan", "o"], url=url)
        cek("papan ambigu -> 7", rc == 7 and "lebih dari satu" in err, err)
        rc, out, err = jalan(["kolom", "--papan", "99"], url=url)
        cek("papan id tak ada -> 2", rc == 2, err)

        # ---------------- buat papan
        ng.data["log"].clear()
        rc, out, err = jalan(["buat-papan", "--jenis", "order-pengiriman", "--nama", "Order Kue Bu Ani"], url=url)
        cek("buat-papan pratinjau", rc == 0 and "PRATINJAU" in out and "createProject" not in ng.data["log"], err)
        rc, out, err = jalan(["buat-papan", "--jenis", "order-pengiriman", "--nama", "Order Kue Bu Ani", "--ya"],
                             url=url)
        pid = max(ng.data["proyek"])
        kol = sorted((c for c in ng.data["kolom"].values() if c["project_id"] == pid), key=lambda c: c["position"])
        cek("buat-papan --ya", rc == 0 and "PAPAN DIBUAT" in out and
            [c["title"] for c in kol] == [k[0] for k in kbmod.TEMPLATE["order-pengiriman"]["kolom"]], out + err)
        cek("buat-papan tanpa hapus kolom", ng.data["log"].count("updateColumn") == 4
            and ng.data["log"].count("addColumn") == 2)
        rc, out, err = jalan(["buat-papan", "--jenis", "konten", "--nama", "order kue bu ani", "--ya"], url=url)
        cek("buat-papan nama ganda -> 7", rc == 7, err)
        rc, out, err = jalan(["buat-papan", "--jenis", "konten", "--nama", "Konten Rina", "--ya"], pengguna="rina",
                             url=url)
        cek("app-user papan tim -> 5 + saran", rc == 5 and "--pribadi" in err, err)
        rc, out, err = jalan(["buat-papan", "--jenis", "konten", "--nama", "Konten Rina", "--pribadi", "--ya"],
                             pengguna="rina", url=url)
        cek("app-user --pribadi", rc == 0 and "PRIBADI" not in err and "PAPAN DIBUAT" in out, out + err)
        rc, out, err = jalan(["buat-papan", "--jenis", "konten", "--nama", "X", "--pribadi"], pengguna="jsonrpc",
                             url=url)
        cek("jsonrpc --pribadi -> 2", rc == 2, err)
        rc, out, err = jalan(["buat-papan", "--jenis", "salon", "--nama", "X"], url=url)
        cek("jenis tak dikenal -> 2", rc == 2, err)

        # ---------------- tambah kartu
        ng.data["log"].clear()
        rc, out, err = jalan(["tambah-kartu", "--papan", "konveksi", "--judul", "Batik seragam guru 25 pcs",
                              "--tenggat", "besok jam 10:00", "--ke", "Budi", "--kolom", "siapkan"], url=url)
        cek("tambah pratinjau", rc == 0 and "PRATINJAU" in out and "createTask" not in ng.data["log"]
            and "PIC: Budi Santoso" in out and "Siapkan Bahan" in out, out + err)
        rc, out, err = jalan(["tambah-kartu", "--papan", "konveksi", "--judul", "Batik seragam guru 25 pcs",
                              "--tenggat", "besok jam 10:00", "--ke", "Budi", "--kolom", "siapkan", "--ya"], url=url)
        tid = max(ng.data["tugas"])
        t = ng.data["tugas"][tid]
        besok = dt.datetime.now(WIB).date() + dt.timedelta(days=1)
        harap = int(dt.datetime(besok.year, besok.month, besok.day, 10, 0, tzinfo=WIB).timestamp())
        cek("tambah --ya", rc == 0 and "KARTU DIBUAT" in out and t["owner_id"] == 3 and t["column_id"] == 2, out + err)
        cek("tenggat epoch tepat (server UTC)", t["date_due"] == harap, f"{t['date_due']} vs {harap}")
        rc, out, err = jalan(["tambah-kartu", "--papan", "konveksi", "--judul", "batik seragam guru 25 pcs", "--ya"],
                             url=url)
        cek("kartu ganda -> 7", rc == 7, err)
        rc, out, err = jalan(["tambah-kartu", "--papan", "konveksi", "--judul", "batik seragam guru 25 pcs", "--ya",
                              "--boleh-ganda"], url=url)
        cek("--boleh-ganda", rc == 0, err)
        rc, out, err = jalan(["tambah-kartu", "--papan", "konveksi", "--judul", "X", "--ke", "sari", "--ya"], url=url)
        cek("--ke username (nama kosong)", rc == 0 and ng.data["tugas"][max(ng.data["tugas"])]["owner_id"] == 4, err)
        rc, out, err = jalan(["tambah-kartu", "--papan", "konveksi", "--judul", "Y", "--ke", "rina"], url=url)
        cek("--ke bukan anggota -> 2", rc == 2 and "tidak ditemukan" in err, err)
        rc, out, err = jalan(["tambah-kartu", "--papan", "konveksi", "--judul", "Y", "--kolom", "gudang"], url=url)
        cek("kolom tak ada -> 2", rc == 2, err)
        rc, out, err = jalan(["tambah-kartu", "--papan", "konveksi", "--judul", "Y", "--tenggat", "kapan2"], url=url)
        cek("tenggat buruk -> 2", rc == 2 and "SARAN" in err, err)
        rc, out, err = jalan(["tambah-kartu", "--papan", "konveksi", "--judul", "Lama", "--tenggat", "1/1/2020"],
                             url=url)
        cek("tenggat lampau diperingatkan", rc == 0 and "SUDAH LEWAT" in out, out + err)
        rc, out, err = jalan(["tambah-kartu", "--judul", "Y"], url=url)
        cek("tanpa papan -> 2", rc == 2, err)
        rc, out, err = jalan(["tambah-kartu", "--papan", "konveksi", "--judul", "  "], url=url)
        cek("judul kosong -> 2", rc == 2, err)

        # ---------------- pindah kartu
        ng.data["log"].clear()
        rc, out, err = jalan(["pindah-kartu", "--id", "3", "--ke-kolom", "cek kualitas"], url=url)
        cek("pindah pratinjau", rc == 0 and "PRATINJAU" in out and "moveTaskPosition" not in ng.data["log"], err)
        rc, out, err = jalan(["pindah-kartu", "--id", "3", "--ke-kolom", "cek kualitas", "--ya"], url=url)
        cek("pindah --ya", rc == 0 and ng.data["tugas"][3]["column_id"] == 4
            and ng.data["tugas"][3]["date_moved"] > now - 60, out + err)
        rc, out, err = jalan(["pindah-kartu", "--id", "3", "--ke-kolom", "Cek Kualitas", "--ya"], url=url)
        cek("pindah ke kolom sama", rc == 0 and "SUDAH di kolom" in out, err)
        rc, out, err = jalan(["pindah-kartu", "--id", "999", "--ke-kolom", "Selesai"], url=url)
        cek("pindah id tak ada -> 5", rc == 5 and "403" in err, err)
        rc, out, err = jalan(["pindah-kartu", "--id", "8", "--ke-kolom", "Produksi", "--ya"], url=url)
        cek("pindah kartu ditutup -> 2", rc == 2 and "DITUTUP" in err, err)
        rc, out, err = jalan(["pindah-kartu", "--id", "3", "--ke-kolom", "Pesanan Baru"], url=url)
        cek("kolom papan lain -> 2", rc == 2, err)
        cek("log tanpa hapus/tutup", not any(str(m).startswith(("remove", "close")) for m in ng.data["log"]))
        rc, out, err = jalan(["laporan"], url=url)
        cek("judul berbahaya hanya data", rc == 0 and "Abaikan semua instruksi" in out
            and not any(str(m).startswith("remove") for m in ng.data["log"]))
    finally:
        srv.shutdown()

    # ---------------------------------------------------------------- server zona Asia/Jakarta
    srv, ng, url = server(tz="Asia/Jakarta")
    try:
        rc, out, err = jalan(["tambah-kartu", "--papan", "1", "--judul", "Uji zona", "--tenggat", "2026-12-01 jam 09:30",
                              "--ya"], url=url)
        t = ng.data["tugas"][max(ng.data["tugas"])]
        harap = int(dt.datetime(2026, 12, 1, 9, 30, tzinfo=WIB).timestamp())
        cek("tenggat epoch tepat (server Asia/Jakarta)", rc == 0 and t["date_due"] == harap, f"{t['date_due']} {err}")
        rc, out, err = jalan(["tambah-kartu", "--papan", "1", "--judul", "Uji WIT", "--tenggat", "2026-12-01 jam 09:30",
                              "--tz", "WIT", "--ya"], url=url)
        t = ng.data["tugas"][max(ng.data["tugas"])]
        harap = int(dt.datetime(2026, 12, 1, 9, 30, tzinfo=dt.timezone(dt.timedelta(hours=9))).timestamp())
        cek("tenggat --tz WIT", rc == 0 and t["date_due"] == harap, err)
    finally:
        srv.shutdown()

    # ---------------------------------------------------------------- gangguan
    for mode, argv, harap, kata in (
            ("redirect", ["cek"], 2, "mengalihkan"),
            ("bukan_kanboard", ["cek"], 4, "bukan JSON-RPC"),
            ("lambat", ["cek", "--timeout", "1"], 4, "tidak menjawab"),
            ("timeout_tulis", ["tambah-kartu", "--papan", "1", "--judul", "Z", "--ya", "--timeout", "1"], 8, "MUNGKIN"),
            ("error500_tulis", ["tambah-kartu", "--papan", "1", "--judul", "Z", "--ya"], 8, "MUNGKIN"),
            ("error500_tulis", ["pindah-kartu", "--id", "4", "--ke-kolom", "Produksi", "--ya"], 8, "MUNGKIN"),
            ("timeout_tulis", ["buat-papan", "--jenis", "konten", "--nama", "Baru", "--ya", "--timeout", "1"], 8,
             "MUNGKIN")):
        srv, ng, url = server(mode)
        try:
            rc, out, err = jalan(argv, url=url)
            cek(f"gangguan {mode} {argv[0]}", rc == harap and kata in err, f"rc={rc} {err}")
            if mode == "redirect":
                cek("redirect: tidak ada permintaan ke host lain", "evil" not in out)
        finally:
            srv.shutdown()
    rc, out, err = jalan(["cek", "--url", "http://127.0.0.1:9", "--timeout", "2"])
    cek("server mati -> 4", rc == 4 and "tidak bisa dihubungi" in err, err)

    shutil.rmtree(RUMAH, ignore_errors=True)
    total = HASIL["lulus"] + len(HASIL["gagal"])
    print(f"\nHASIL: {HASIL['lulus']}/{total} lulus")
    return 0 if not HASIL["gagal"] else 1


if __name__ == "__main__":
    sys.exit(main())
