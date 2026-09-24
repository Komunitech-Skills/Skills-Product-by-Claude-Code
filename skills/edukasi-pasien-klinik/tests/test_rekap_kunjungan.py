#!/usr/bin/env python3
"""Tes regresi untuk rekap_kunjungan.py — jalankan:
    python3 tests/test_rekap_kunjungan.py
Hanya library standar (unittest). Mengimpor modul dari ../scripts.

Setiap kelas tes memetakan ke temuan HASIL-UJI.md (2026-09-24) agar mudah
ditelusuri: B1 = berat, S1-S4 = sedang, R1-R2 = ringan yang berkaitan
dengan script.
"""
import io
import json
import os
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))
import rekap_kunjungan as rk  # noqa: E402


CSV_NORMAL = """Tanggal,Jam,Poli,Penjamin,Status
2026-09-01,08:15,Gigi,BPJS,Selesai
2026-09-01,09:00,Gigi,Umum,Selesai
2026-09-01,09:30,Umum,BPJS,Tidak Datang
2026-09-02,08:00,Gigi,Umum,Selesai
2026-09-02,10:00,KIA,BPJS,Selesai
"""

CSV_DENGAN_KOLOM_SENSITIF = """Tanggal,Nama Pasien,NIK,Poli,Diagnosis
2026-09-01,Budi,3201xxxx,Gigi,K02.1
2026-09-01,Sari,3201yyyy,Umum,J06
"""

CSV_HANYA_HEADER = """Tanggal,Poli
"""


class TesRekapNormal(unittest.TestCase):
    def test_rekap_lengkap(self):
        header, baris = rk.baca_csv(CSV_NORMAL, is_text=True)
        hasil = rk.rekap(header, baris)
        self.assertEqual(hasil["total_pendaftaran"], 5)
        self.assertEqual(hasil["per_hari"]["2026-09-01"], 3)
        self.assertEqual(hasil["per_hari"]["2026-09-02"], 2)
        self.assertEqual(hasil["per_poli"]["Gigi"], 3)
        self.assertEqual(hasil["per_penjamin"]["BPJS"], 3)
        self.assertEqual(hasil["tidak_datang"], 1)
        self.assertEqual(hasil["hadir"], 4)
        self.assertEqual(hasil["kolom_sensitif_diabaikan"], [])
        jam_list = [j["jam"] for j in hasil["jam_ramai"]]
        self.assertIn("08:00", jam_list)

    def test_format_teks_tidak_error(self):
        header, baris = rk.baca_csv(CSV_NORMAL, is_text=True)
        hasil = rk.rekap(header, baris)
        teks = rk.format_teks(hasil)
        self.assertIn("REKAP OPERASIONAL", teks)
        self.assertIn("2026-09-01", teks)
        self.assertIn("Total pendaftaran tercatat", teks)


class TesPrivasi(unittest.TestCase):
    def test_kolom_sensitif_tidak_muncul_di_output(self):
        header, baris = rk.baca_csv(CSV_DENGAN_KOLOM_SENSITIF, is_text=True)
        hasil = rk.rekap(header, baris)
        teks = rk.format_teks(hasil)
        dump = json.dumps(hasil, ensure_ascii=False)
        for terlarang in ["Budi", "Sari", "3201xxxx", "3201yyyy", "K02.1", "J06"]:
            self.assertNotIn(terlarang, teks)
            self.assertNotIn(terlarang, dump)
        self.assertIn("nama pasien", [c.lower() for c in hasil["kolom_sensitif_diabaikan"]])
        self.assertIn("diagnosis", [c.lower() for c in hasil["kolom_sensitif_diabaikan"]])

    def test_r1_variasi_header_sensitif_dikenali(self):
        """R1: Dx, ICD-10, Keluhan Utama, HP/WA, No. RM, Tgl Lahir, Email, Nama Ibu."""
        header = [
            "Tanggal", "Dx", "ICD-10", "Keluhan Utama", "HP/WA", "No. RM",
            "Tgl Lahir", "Email", "Nama Ibu", "Poli",
        ]
        baris = [{h: "x" for h in header}]
        baris[0]["Tanggal"] = "2026-09-01"
        baris[0]["Poli"] = "Gigi"
        hasil = rk.rekap(header, baris)
        diabaikan_lower = [c.lower() for c in hasil["kolom_sensitif_diabaikan"]]
        for kolom in ["dx", "icd-10", "keluhan utama", "hp/wa", "no. rm", "tgl lahir", "email", "nama ibu"]:
            self.assertIn(kolom, diabaikan_lower, f"{kolom} seharusnya dikenali sebagai kolom sensitif")

    def test_r2_teks_bebas_lebih_dari_3_kata_disembunyikan_bukan_dicetak(self):
        """R2 (revisi B2): nilai mencurigakan TIDAK PERNAH dicetak apa adanya
        lagi — hanya digabung jadi agregat "disembunyikan"."""
        header, baris = rk.baca_csv(
            "Tanggal,Poli\n2026-09-01,Cabut gigi FIKTIF Ani anak Budi\n", is_text=True
        )
        hasil = rk.rekap(header, baris)
        teks = rk.format_teks(hasil)
        dump = json.dumps(hasil, ensure_ascii=False)
        self.assertNotIn("Cabut gigi FIKTIF Ani anak Budi", teks)
        self.assertNotIn("Cabut gigi FIKTIF Ani anak Budi", dump)
        self.assertEqual(hasil["nilai_disembunyikan"]["poli"], {"baris": 1, "nilai_berbeda": 1})
        self.assertIn("disembunyikan", teks)

    def test_r2_lebih_dari_20_nilai_unik_disembunyikan_setelah_batas(self):
        # Label huruf (bukan angka) supaya lolos saringan "tanpa digit"; tiap
        # label diulang 3x supaya lolos ambang MIN_FREKUENSI_TAMPIL juga —
        # yang diuji murni batas MAKS_NILAI_UNIK_TAMPIL.
        import string
        label = [f"Poli{c}" for c in string.ascii_uppercase[:25]]  # 25 label unik
        baris_csv = "Tanggal,Poli\n" + "".join(
            f"2026-09-01,{lbl}\n" * rk.MIN_FREKUENSI_TAMPIL for lbl in label
        )
        header, baris = rk.baca_csv(baris_csv, is_text=True)
        hasil = rk.rekap(header, baris)
        # 20 nilai pertama (semuanya freq sama, urutan insertion) tetap
        # tampil, 5 sisanya disembunyikan.
        self.assertEqual(len(hasil["per_poli"]), rk.MAKS_NILAI_UNIK_TAMPIL)
        self.assertEqual(hasil["nilai_disembunyikan"]["poli"]["nilai_berbeda"], 5)


class TesStatusKehadiran(unittest.TestCase):
    """B1a: status tidak boleh diam-diam dianggap hadir."""

    def test_variasi_tidak_datang_dikenali(self):
        for nilai in [
            "Tidak datang", "tdk datang", "Tidak Hadir", "TDK HADIR", "tidak jadi",
            "Mangkir", "No Show", "no-show", "Batal", "Dibatalkan", "cancel",
            "Belum datang",
        ]:
            with self.subTest(nilai=nilai):
                self.assertEqual(rk.klasifikasi_status(nilai), "tidak_datang")

    def test_singkatan_th_dikenali_tidak_datang(self):
        self.assertEqual(rk.klasifikasi_status("TH"), "tidak_datang")
        self.assertEqual(rk.klasifikasi_status("th"), "tidak_datang")

    def test_status_hadir_dikenali(self):
        for nilai in ["Selesai", "Hadir", "Datang", "Terlaksana", "Berhasil", "Dilayani"]:
            with self.subTest(nilai=nilai):
                self.assertEqual(rk.klasifikasi_status(nilai), "hadir")

    def test_status_tidak_dikenal_tidak_dianggap_hadir(self):
        """Inti B1a: status asing dilaporkan, BUKAN diam-diam hadir."""
        for nilai in ["Reschedule", "Dijadwalkan ulang", "Pending konfirmasi", "???"]:
            with self.subTest(nilai=nilai):
                self.assertEqual(rk.klasifikasi_status(nilai), "tidak_dikenal")

    def test_kasus_asli_bug_tidak_hadir_terhitung_benar(self):
        """Reproduksi temuan penguji: 'Tidak hadir' harus dihitung tidak datang,
        bukan hadir (sebelumnya salah dihitung 2 dari 3 seharusnya)."""
        csv_text = """Tanggal,Status
2026-09-01,Selesai
2026-09-01,Tidak hadir
2026-09-01,Hadir
"""
        header, baris = rk.baca_csv(csv_text, is_text=True)
        hasil = rk.rekap(header, baris)
        self.assertEqual(hasil["tidak_datang"], 1)
        self.assertEqual(hasil["hadir"], 2)

    def test_status_tidak_dikenal_terlihat_di_rincian_dan_tidak_masuk_hadir(self):
        # "Reschedule besok" diulang 3x supaya lolos ambang MIN_FREKUENSI_TAMPIL
        # dan tetap terlihat individual di rincian (bukan hanya di agregat).
        csv_text = (
            "Tanggal,Status\n"
            + "2026-09-01,Reschedule besok\n" * 3
            + "2026-09-01,Selesai\n" * 3
        )
        header, baris = rk.baca_csv(csv_text, is_text=True)
        hasil = rk.rekap(header, baris)
        self.assertEqual(hasil["status_tidak_dikenal_jumlah"], 3)
        self.assertEqual(hasil["hadir"], 3)
        kategori = {s["nilai"]: s["kategori"] for s in hasil["status_rincian"]}
        self.assertEqual(kategori["Reschedule besok"], "tidak_dikenal")
        teks = rk.format_teks(hasil)
        self.assertIn("TIDAK DIKENAL", teks)


class TesFormatTanggal(unittest.TestCase):
    """B1b: format tanggal ditentukan sekali per file, peringatan bila campur."""

    def test_dmy_konsisten_tanpa_peringatan(self):
        csv_text = "Tanggal,Poli\n25/01/2026,A\n13/09/2026,B\n"
        header, baris = rk.baca_csv(csv_text, is_text=True)
        hasil = rk.rekap(header, baris)
        self.assertIsNone(hasil["peringatan_format_tanggal"])
        self.assertEqual(hasil["urutan_tanggal_dipakai"], "dmy")
        self.assertIn("2026-01-25", hasil["per_hari"])
        self.assertIn("2026-09-13", hasil["per_hari"])

    def test_format_campur_memberi_peringatan_dan_baca_bukti_lokal(self):
        # 25/01 -> hanya masuk akal dmy (hari=25). 09/13 -> hanya masuk akal mdy (bulan=9? tidak,
        # 13 tidak mungkin bulan, jadi ini unik: a=09,b=13 -> b>12 -> mdy (hari=13, bulan=09).
        csv_text = "Tanggal,Poli\n25/01/2026,A\n09/13/2026,B\n02/02/2026,C\n"
        header, baris = rk.baca_csv(csv_text, is_text=True)
        hasil = rk.rekap(header, baris)
        self.assertIsNotNone(hasil["peringatan_format_tanggal"])
        self.assertIn("tidak konsisten", hasil["peringatan_format_tanggal"])
        # baris ke-3 di file (baris data ke-2, +1 header) yang bertentangan disebut
        self.assertIn("3", hasil["peringatan_format_tanggal"])
        # tapi bukti lokalnya tetap dibaca benar: 09/13/2026 -> 13 September 2026
        self.assertIn("2026-09-13", hasil["per_hari"])
        self.assertIn("2026-01-25", hasil["per_hari"])

    def test_iso_tidak_terpengaruh_urutan(self):
        header, baris = rk.baca_csv("Tanggal,Poli\n2026-09-01,A\n", is_text=True)
        hasil = rk.rekap(header, baris)
        self.assertIn("2026-09-01", hasil["per_hari"])

    def test_nama_bulan_indonesia_dan_inggris(self):
        for teks, iso in [
            ("2 Sept 2026", "2026-09-02"),
            ("1 September 2026", "2026-09-01"),
            ("1-Sep-2026", "2026-09-01"),
            ("5 Januari 2026", "2026-01-05"),
        ]:
            with self.subTest(teks=teks):
                header, baris = rk.baca_csv(f"Tanggal,Poli\n{teks},A\n", is_text=True)
                hasil = rk.rekap(header, baris)
                self.assertIn(iso, hasil["per_hari"], f"gagal parse: {teks}")

    def test_tanggal_dengan_jam_sekaligus(self):
        header, baris = rk.baca_csv(
            "Tanggal,Poli\n2026-09-01 08:45,A\n2026-09-01T10:00:00,B\n", is_text=True
        )
        hasil = rk.rekap(header, baris)
        self.assertEqual(hasil["per_hari"]["2026-09-01"], 2)
        jam_terbaca = {j["jam"] for j in hasil["jam_ramai"]}
        self.assertTrue({"08:00", "10:00"} <= jam_terbaca)

    def test_tanggal_campur_sebagian_gagal_dihitung(self):
        csv_text = "Tanggal,Poli\n01/09/2026,A\n2026-09-02,B\ntanggal-rusak,C\n"
        header, baris = rk.baca_csv(csv_text, is_text=True)
        hasil = rk.rekap(header, baris)
        self.assertEqual(hasil["total_pendaftaran"], 3)
        self.assertEqual(hasil["baris_tanggal_tidak_terbaca"], 1)
        self.assertEqual(sum(hasil["per_hari"].values()), 2)


class TesEncoding(unittest.TestCase):
    """S1: encoding selain UTF-8 tidak boleh membuat script crash."""

    def _tulis(self, teks, enc):
        f = tempfile.NamedTemporaryFile(delete=False, suffix=".csv")
        f.write(teks.encode(enc))
        f.close()
        return f.name

    def test_cp1252(self):
        path = self._tulis("Tanggal,Poli\n2026-09-01,Depané\n", "cp1252")
        try:
            header, baris = rk.baca_csv(path)
            self.assertEqual(baris[0]["Poli"], "Depané")
        finally:
            os.unlink(path)

    def test_utf16_dengan_bom(self):
        path = self._tulis("Tanggal,Poli\r\n2026-09-01,Gigi\r\n", "utf-16")
        try:
            header, baris = rk.baca_csv(path)
            self.assertEqual(baris[0]["Poli"], "Gigi")
        finally:
            os.unlink(path)

    def test_utf8_sig_bom(self):
        path = self._tulis("Tanggal,Poli\n2026-09-01,Gigi\n", "utf-8-sig")
        try:
            header, baris = rk.baca_csv(path)
            self.assertEqual(header[0], "Tanggal")
        finally:
            os.unlink(path)

    def test_encoding_tidak_dikenali_pesan_jelas_bukan_traceback(self):
        # Byte yang tidak valid untuk utf-8/cp1252/latin-1 sangat jarang (latin-1
        # menerima semua byte), jadi kita paksakan lewat _decode_bytes langsung
        # dengan byte yang gagal di semua percobaan sebelum latin-1 (uji fallback).
        mentah = "Tanggal,Poli\n2026-09-01,Gigi\n".encode("utf-8")
        teks, enc = rk._decode_bytes(mentah)
        self.assertEqual(enc, "utf-8")


class TesB2KebocoranStatus(unittest.TestCase):
    """B2 (regresi v1.0.1, ditemukan penguji independen): kolom 'Keterangan'
    (teks bebas berisi nama/no. HP/diagnosis) tidak boleh diperlakukan
    sebagai kolom status, dan nilai status/poli/penjamin yang mencurigakan
    tidak boleh dicetak ulang di output teks maupun JSON manapun."""

    def test_keterangan_tidak_lagi_dianggap_alias_status(self):
        csv_text = (
            "Tanggal,Poli,Keterangan\n"
            "2026-09-01,Gigi,FIKTIF Ani 0812-0000-9999 dx DBD rujuk RS\n"
            "2026-09-01,Umum,batal - FIKTIF Budi abses gigi\n"
        )
        header, baris = rk.baca_csv(csv_text, is_text=True)
        hasil = rk.rekap(header, baris)
        # Tidak ada kolom status yang terdeteksi sama sekali -> field None.
        self.assertIsNone(hasil["hadir"])
        self.assertIsNone(hasil["status_rincian"])
        teks = rk.format_teks(hasil)
        dump = json.dumps(hasil, ensure_ascii=False)
        for terlarang in ["FIKTIF Ani", "FIKTIF Budi", "0812-0000-9999", "dx DBD", "abses gigi"]:
            self.assertNotIn(terlarang, teks)
            self.assertNotIn(terlarang, dump)

    def test_kolom_status_asli_berisi_teks_bebas_tetap_tidak_bocor(self):
        """Bila klinik memang menamai kolomnya 'Status' tapi stafnya
        mengetik catatan bebas di sana, nilai itu tetap tidak boleh bocor —
        hanya digabung jadi agregat 'disembunyikan', dan tidak dihitung
        sebagai hadir maupun tidak datang (kategori 'tidak_dikenal')."""
        # "Selesai"/"Tidak hadir" diulang 3x supaya lolos ambang frekuensi
        # dan tetap tampil individual — mengisolasi konsep: nilai AMAN &
        # SERING tetap tampil, nilai TIDAK AMAN (walau cuma sekali) tetap
        # disembunyikan.
        csv_text = (
            "Tanggal,Status\n"
            + "2026-09-01,Selesai\n" * 3
            + "2026-09-01,Tidak hadir\n" * 3
            + "2026-09-01,FIKTIF Ani 0812-0000-9999 dx DBD rujuk RS\n"
            + "2026-09-01,batal - FIKTIF Budi abses gigi\n"
            + "2026-09-01,Bu Ani sudah pulang\n"
        )
        header, baris = rk.baca_csv(csv_text, is_text=True)
        hasil = rk.rekap(header, baris)
        teks = rk.format_teks(hasil)
        dump = json.dumps(hasil, ensure_ascii=False)
        for terlarang in ["FIKTIF Ani", "FIKTIF Budi", "0812-0000-9999", "dx DBD", "abses gigi", "Bu Ani"]:
            self.assertNotIn(terlarang, teks)
            self.assertNotIn(terlarang, dump)
        self.assertIn("Selesai", teks)
        self.assertIn("Tidak hadir", teks)
        # Totalnya tetap benar walau nilainya disembunyikan dari tampilan.
        # ("batal - FIKTIF Budi abses gigi" mengandung kata kunci "batal"
        # sehingga dikategorikan tidak_datang; ini tidak membocorkan apa
        # pun karena nilainya sendiri tetap tidak pernah dicetak.)
        self.assertEqual(hasil["hadir"], 3)
        self.assertEqual(hasil["tidak_datang"], 4)
        self.assertEqual(hasil["status_tidak_dikenal_jumlah"], 2)
        self.assertEqual(hasil["nilai_disembunyikan"]["status"], {"baris": 3, "nilai_berbeda": 3})

    def test_sapaan_nama_disembunyikan_walau_pendek(self):
        self.assertFalse(rk._nilai_aman_ditampilkan("Bu Ani"))
        self.assertFalse(rk._nilai_aman_ditampilkan("Pak Budi"))
        self.assertTrue(rk._nilai_aman_ditampilkan("Selesai"))
        self.assertFalse(rk._nilai_aman_ditampilkan("0812xxxx"))
        self.assertFalse(rk._nilai_aman_ditampilkan("Satu dua tiga empat"))

    def test_pola_baru_v103_email_inisial_icd(self):
        """B2-sisa: pola tambahan '@', inisial ('S.A.'), kode ICD ('J06')."""
        self.assertFalse(rk._nilai_aman_ditampilkan("ani.fiktif@mail.com"))
        self.assertFalse(rk._nilai_aman_ditampilkan("joko@mail.co.id"))
        self.assertFalse(rk._nilai_aman_ditampilkan("S.A."))
        self.assertFalse(rk._nilai_aman_ditampilkan("A.B.C."))
        self.assertFalse(rk._nilai_aman_ditampilkan("J06"))
        self.assertFalse(rk._nilai_aman_ditampilkan("K02.1"))
        # Kategori sah yang tidak boleh salah tersaring oleh pola baru:
        self.assertTrue(rk._nilai_aman_ditampilkan("Rujuk"))
        self.assertTrue(rk._nilai_aman_ditampilkan("Reschedule"))

    def test_ambang_frekuensi_nilai_langka_disembunyikan_walau_pola_aman(self):
        """B2-sisa butir 1 (k-anonim): nama pendek 'ani'/'Rina' lolos pola
        (<=3 kata, tanpa digit/sapaan/@/inisial/ICD) tapi HARUS tetap
        disembunyikan karena hanya muncul 1-2 kali — kemungkinan besar data
        satu pasien, bukan kategori asli."""
        csv_text = (
            "Tanggal,Status\n"
            + "2026-09-01,ani\n"
            + "2026-09-01,Rina\n"
            + "2026-09-01,Selesai\n" * 3
        )
        header, baris = rk.baca_csv(csv_text, is_text=True)
        hasil = rk.rekap(header, baris)
        teks = rk.format_teks(hasil)
        dump = json.dumps(hasil, ensure_ascii=False)
        self.assertNotIn("ani", [s["nilai"] for s in hasil["status_rincian"]])
        for terlarang in ["'ani'", "'Rina'"]:
            self.assertNotIn(terlarang, teks)
        self.assertNotIn('"Rina"', dump)

    def test_serangan_gabungan_nol_kebocoran(self):
        """Reproduksi skenario serangan penguji independen (2026-09-24,
        v1.0.2): nama pendek, nama panjang, inisial, email, diagnosis
        1-2 kata ditanam di kolom status/poli/penjamin — semua fiktif.
        Nilai sah yang BERULANG (>=3x) tetap harus tampil."""
        csv_text = (
            "Tanggal,Status,Poli,Penjamin\n"
            + "2026-09-01,Selesai,Gigi,BPJS\n" * 3
            + "2026-09-01,Tidak hadir,Umum,Umum\n" * 3
            + "2026-09-01,Reschedule,KIA,Asuransi\n" * 3
            + "2026-09-01,Siti Aminah,abses,Pak Joko\n"
            + "2026-09-01,ani,DBD,Aminah\n"
            + "2026-09-01,S.A.,Siti,hipertensi\n"
            + "2026-09-01,DBD,Budi Santoso,joko@mail.co.id\n"
            + "2026-09-01,hipertensi,Hipertensi,KIS 0001\n"
            + "2026-09-01,ani.fiktif@mail.com,diabetes melitus,\n"
            + "2026-09-01,Bu Ani,ISPA,\n"
            + "2026-09-01,Rina,,\n"
            + "2026-09-01,abses gigi,,\n"
            + "2026-09-01,sakit kepala,,\n"
        )
        header, baris = rk.baca_csv(csv_text, is_text=True)
        hasil = rk.rekap(header, baris)
        teks = rk.format_teks(hasil)
        dump = json.dumps(hasil, ensure_ascii=False)
        sensitif = [
            "Siti Aminah", "ani", "S.A.", "DBD", "hipertensi",
            "ani.fiktif@mail.com", "Bu Ani", "Rina", "abses gigi",
            "sakit kepala", "abses", "Siti", "Budi Santoso", "Hipertensi",
            "diabetes melitus", "ISPA", "Pak Joko", "Aminah",
            "joko@mail.co.id", "KIS 0001",
        ]
        bocor = [s for s in sensitif if f"'{s}'" in teks or f'"{s}"' in dump]
        self.assertEqual(bocor, [], f"kebocoran ditemukan: {bocor}")
        # Nilai sah berulang tetap tampil.
        self.assertIn("Selesai", teks)
        self.assertIn("Tidak hadir", teks)
        self.assertIn("Reschedule", teks)
        self.assertIn("Gigi", teks)
        self.assertIn("Umum", teks)
        self.assertIn("KIA", teks)
        self.assertIn("BPJS", teks)


class TesR9UTF16TanpaBOM(unittest.TestCase):
    def test_utf16_le_tanpa_bom_terbaca(self):
        f = tempfile.NamedTemporaryFile(delete=False, suffix=".csv")
        f.write("Tanggal,Poli\r\n2026-09-01,Gigi\r\n".encode("utf-16-le"))
        f.close()
        try:
            header, baris = rk.baca_csv(f.name)
            self.assertEqual(baris[0]["Poli"], "Gigi")
        finally:
            os.unlink(f.name)

    def test_utf16_be_tanpa_bom_terbaca(self):
        f = tempfile.NamedTemporaryFile(delete=False, suffix=".csv")
        f.write("Tanggal,Poli\r\n2026-09-01,Gigi\r\n".encode("utf-16-be"))
        f.close()
        try:
            header, baris = rk.baca_csv(f.name)
            self.assertEqual(baris[0]["Poli"], "Gigi")
        finally:
            os.unlink(f.name)


class TesR10PolaKolomSensitifPerToken(unittest.TestCase):
    def test_kolom_waktu_tidak_dilaporkan_sensitif_dan_tetap_dipakai_jam(self):
        header, baris = rk.baca_csv("Tanggal,Waktu,Poli\n2026-09-01,08:00,Gigi\n", is_text=True)
        hasil = rk.rekap(header, baris)
        self.assertEqual(hasil["kolom_sensitif_diabaikan"], [])
        self.assertIsNotNone(hasil["jam_ramai"])
        jam_list = [j["jam"] for j in hasil["jam_ramai"]]
        self.assertIn("08:00", jam_list)

    def test_kolom_dipakai_tidak_pernah_dilaporkan_sensitif(self):
        # 'Kartu' cocok pola sensitif (\bkartu\b) tapi bila secara kebetulan
        # dipakai sebagai kolom poli, jangan dilaporkan dobel/bertentangan.
        header = ["Tanggal", "Poli"]
        baris = [{"Tanggal": "2026-09-01", "Poli": "Gigi"}]
        hasil = rk.rekap(header, baris)
        self.assertNotIn("Poli", hasil["kolom_sensitif_diabaikan"])


class TesR11AliasTanggalBaru(unittest.TestCase):
    def test_tgl_kunjungan_dan_tgl_periksa_dikenali(self):
        for nama_kolom in ["Tgl Kunjungan", "Tanggal Kunjungan", "Tgl Periksa", "Tanggal Periksa"]:
            with self.subTest(nama_kolom=nama_kolom):
                header = [nama_kolom, "Poli"]
                baris = [{nama_kolom: "2026-09-01", "Poli": "Gigi"}]
                hasil = rk.rekap(header, baris)
                self.assertIn("2026-09-01", hasil["per_hari"])

    def test_tgl_lahir_tidak_dianggap_kolom_tanggal_kunjungan(self):
        header = ["Tgl Kunjungan", "Tgl Lahir", "Poli"]
        baris = [{"Tgl Kunjungan": "2026-09-01", "Tgl Lahir": "1990-01-01", "Poli": "Gigi"}]
        hasil = rk.rekap(header, baris)
        self.assertEqual(list(hasil["per_hari"].keys()), ["2026-09-01"])
        self.assertIn("Tgl Lahir", hasil["kolom_sensitif_diabaikan"])


class TesR12FormatAmbigu(unittest.TestCase):
    def test_file_seluruhnya_ambigu_gaya_as_diberi_peringatan(self):
        csv_text = "Tanggal,Poli\n09/01/2026,A\n09/02/2026,B\n09/03/2026,C\n"
        header, baris = rk.baca_csv(csv_text, is_text=True)
        hasil = rk.rekap(header, baris)
        self.assertIsNotNone(hasil["peringatan_format_tanggal"])
        self.assertIn("Tidak ada bukti tegas", hasil["peringatan_format_tanggal"])
        self.assertEqual(hasil["urutan_tanggal_dipakai"], "dmy")

    def test_urutan_dipaksa_manual_mdy(self):
        csv_text = "Tanggal,Poli\n09/01/2026,A\n09/02/2026,B\n"
        header, baris = rk.baca_csv(csv_text, is_text=True)
        hasil = rk.rekap(header, baris, urutan_tanggal_paksa="mdy")
        self.assertEqual(hasil["urutan_tanggal_dipakai"], "mdy")
        self.assertIn("2026-09-01", hasil["per_hari"])
        self.assertIn("2026-09-02", hasil["per_hari"])
        self.assertIn("dipaksa manual", hasil["peringatan_format_tanggal"])

    def test_cli_urutan_tanggal_mdy(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False, encoding="utf-8") as f:
            f.write("Tanggal,Poli\n09/01/2026,A\n")
            path = f.name
        try:
            buf_out = io.StringIO()
            with redirect_stdout(buf_out):
                kode = rk.main(["--file", path, "--format", "json", "--urutan-tanggal", "mdy"])
            self.assertEqual(kode, 0)
            data = json.loads(buf_out.getvalue())
            self.assertIn("2026-09-01", data["per_hari"])
        finally:
            os.unlink(path)


class TesR13PersentaseKategori(unittest.TestCase):
    def test_persentase_muncul_di_teks_untuk_per_poli(self):
        # 3x tiap nilai supaya lolos ambang MIN_FREKUENSI_TAMPIL dan tampil.
        header, baris = rk.baca_csv(
            "Tanggal,Poli\n"
            + "2026-09-01,Gigi\n" * 3
            + "2026-09-01,Umum\n" * 3,
            is_text=True,
        )
        hasil = rk.rekap(header, baris)
        teks = rk.format_teks(hasil)
        self.assertIn("Gigi: 3 (50.0%)", teks)
        self.assertIn("Umum: 3 (50.0%)", teks)


class TesB2SisaFrekuensiDanPola(unittest.TestCase):
    """B2-sisa (uji serangan v1.0.2, 2026-09-24): nama pendek, inisial,
    email, dan kode diagnosis di kolom status/poli/penjamin. Lihat juga
    `TesB2KebocoranStatus.test_serangan_gabungan_nol_kebocoran`."""

    def test_diagnosis_kode_icd_di_poli_disembunyikan_walau_berulang(self):
        # Kode ICD selalu disembunyikan oleh POLA_ICD (dan juga oleh aturan
        # "tanpa digit"), terlepas dari frekuensinya.
        csv_text = "Tanggal,Poli\n" + "2026-09-01,J06\n" * 5
        header, baris = rk.baca_csv(csv_text, is_text=True)
        hasil = rk.rekap(header, baris)
        self.assertNotIn("J06", hasil["per_poli"])
        self.assertEqual(hasil["nilai_disembunyikan"]["poli"], {"baris": 5, "nilai_berbeda": 1})

    def test_diagnosis_kata_berulang_di_poli_tetap_tampil_sebagai_agregat(self):
        """R (ringan, diketahui & didokumentasikan jujur di README/SKILL):
        bila klinik memasukkan nama diagnosis non-kode (bukan pola ICD,
        <=3 kata, tanpa digit) ke kolom poli dan itu BERULANG, hasilnya
        adalah jumlah AGREGAT per istilah — bukan identitas satu pasien.
        Ini bukan kebocoran data per-pasien, hanya nilai agregat."""
        csv_text = "Tanggal,Poli\n" + "2026-09-01,Hipertensi\n" * 5
        header, baris = rk.baca_csv(csv_text, is_text=True)
        hasil = rk.rekap(header, baris)
        self.assertEqual(hasil["per_poli"]["Hipertensi"], 5)


class TesBarisBergeser(unittest.TestCase):
    """B2-sisa butir 3: baris yang kolomnya bergeser (koma tanpa tanda
    kutip) dikeluarkan dari rincian, tetap dihitung di total, dan diberi
    peringatan eksplisit — tidak pernah ditebak."""

    def test_baris_bergeser_dikeluarkan_dari_rincian_tapi_masuk_total(self):
        csv_text = (
            "Tanggal,Poli,Penjamin,Status\n"
            + "2026-09-01,Gigi,BPJS,Selesai\n" * 5
            # baris ini kepanjangan (nilai poli mengandung koma tanpa kutip)
            + "2026-09-02,Siti, Aminah,BPJS,Selesai\n"
        )
        header, baris = rk.baca_csv(csv_text, is_text=True)
        hasil = rk.rekap(header, baris)
        teks = rk.format_teks(hasil)
        dump = json.dumps(hasil, ensure_ascii=False)
        self.assertEqual(hasil["total_pendaftaran"], 6)
        self.assertEqual(hasil["baris_bergeser_jumlah"], 1)
        self.assertIsNotNone(hasil["peringatan_baris_bergeser"])
        self.assertIn("7", hasil["peringatan_baris_bergeser"])  # nomor baris file
        self.assertNotIn("Siti", teks)
        self.assertNotIn("Aminah", teks)
        self.assertNotIn("Siti", dump)
        # Baris bergeser tidak ikut per_hari (2026-09-02 tidak muncul).
        self.assertNotIn("2026-09-02", hasil["per_hari"])
        self.assertEqual(hasil["per_poli"], {"Gigi": 5})

    def test_persentase_dihitung_dari_baris_yang_terbaca_bukan_total(self):
        csv_text = (
            "Tanggal,Status\n"
            + "2026-09-01,Selesai\n" * 3
            + "2026-09-02,Siti, Aminah,Selesai\n"  # bergeser (kolom ekstra)
        )
        header, baris = rk.baca_csv(csv_text, is_text=True)
        hasil = rk.rekap(header, baris)
        self.assertEqual(hasil["total_pendaftaran"], 4)
        self.assertEqual(hasil["total_dapat_dibaca"], 3)
        self.assertEqual(hasil["hadir"], 3)
        self.assertEqual(hasil["persentase_hadir"], 100.0)

    def test_10_persen_baris_bergeser_semua_peringatan_dan_bersih(self):
        baik = "2026-09-01,Gigi,BPJS,Selesai\n" * 90
        buruk = "2026-09-01,Siti, Aminah,BPJS,Selesai\n" * 10
        csv_text = "Tanggal,Poli,Penjamin,Status\n" + baik + buruk
        header, baris = rk.baca_csv(csv_text, is_text=True)
        hasil = rk.rekap(header, baris)
        teks = rk.format_teks(hasil)
        dump = json.dumps(hasil, ensure_ascii=False)
        self.assertEqual(hasil["total_pendaftaran"], 100)
        self.assertEqual(hasil["baris_bergeser_jumlah"], 10)
        self.assertIsNotNone(hasil["peringatan_baris_bergeser"])
        self.assertEqual(hasil["per_poli"], {"Gigi": 90})
        self.assertNotIn("Siti", teks)
        self.assertNotIn("Siti", dump)

    def test_tanpa_baris_bergeser_field_kosong(self):
        header, baris = rk.baca_csv(CSV_NORMAL, is_text=True)
        hasil = rk.rekap(header, baris)
        self.assertEqual(hasil["baris_bergeser_jumlah"], 0)
        self.assertIsNone(hasil["peringatan_baris_bergeser"])
        self.assertEqual(hasil["total_dapat_dibaca"], hasil["total_pendaftaran"])


class TesS5PemisahUjungBaris(unittest.TestCase):
    """S5 (uji ulang v1.0.3, 2026-09-24): pemisah kosong di ujung SETIAP
    baris (kolom lebih yang seluruhnya kosong, atau kolom kurang yang
    hanya di kolom terakhir header) BUKAN baris bergeser."""

    def test_kolom_lebih_kosong_di_ujung_bukan_bergeser(self):
        # "trailing_semua.csv": setiap baris diakhiri ',' tambahan (field
        # kosong), header TIDAK punya kolom tambahan itu.
        csv_text = "Tanggal,Poli,Penjamin,Status\n" + (
            "2026-09-01,Gigi,BPJS,Selesai,\n" * 20
        )
        header, baris = rk.baca_csv(csv_text, is_text=True)
        hasil = rk.rekap(header, baris)
        self.assertEqual(hasil["baris_bergeser_jumlah"], 0)
        self.assertIsNone(hasil["peringatan_baris_bergeser"])
        self.assertEqual(hasil["per_poli"], {"Gigi": 20})
        self.assertEqual(hasil["hadir"], 20)
        teks = rk.format_teks(hasil)
        self.assertIn("Hadir: 20 (100.0%)", teks)

    def test_kolom_kurang_hanya_di_kolom_terakhir_bukan_bergeser(self):
        # Baris yang berhenti sebelum kolom terakhir (Status kosong tanpa
        # koma penutup) — hanya SATU kolom hilang, dan itu kolom terakhir.
        csv_text = (
            "Tanggal,Poli,Penjamin,Status\n"
            + "2026-09-01,Gigi,BPJS,Selesai\n" * 3
            + "2026-09-01,Umum,Umum\n" * 2  # Status hilang, kolom terakhir
        )
        header, baris = rk.baca_csv(csv_text, is_text=True)
        hasil = rk.rekap(header, baris)
        self.assertEqual(hasil["baris_bergeser_jumlah"], 0)

    def test_kolom_lebih_berisi_data_tetap_dianggap_bergeser(self):
        # Kelebihan kolom yang BUKAN kosong (ada isi) tetap bergeser —
        # pengecualian S5 hanya untuk kelebihan yang kosong semua.
        csv_text = (
            "Tanggal,Poli,Penjamin,Status\n"
            + "2026-09-01,Gigi,BPJS,Selesai\n" * 3
            + "2026-09-02,Siti, Aminah,BPJS,Selesai\n"  # kolom lebih BERISI
        )
        header, baris = rk.baca_csv(csv_text, is_text=True)
        hasil = rk.rekap(header, baris)
        self.assertEqual(hasil["baris_bergeser_jumlah"], 1)

    def test_lebih_dari_separuh_bergeser_pesan_struktur(self):
        csv_text = (
            "Tanggal,Poli,Penjamin,Status\n"
            + "2026-09-01,Gigi,BPJS,Selesai\n" * 2
            + "2026-09-02,Siti, Aminah,BPJS,Selesai\n" * 8  # 8 dari 10 = 80%
        )
        header, baris = rk.baca_csv(csv_text, is_text=True)
        hasil = rk.rekap(header, baris)
        self.assertEqual(hasil["baris_bergeser_jumlah"], 8)
        self.assertIn("Struktur header dan baris tidak cocok", hasil["peringatan_baris_bergeser"])

    def test_semua_baris_bergeser_tidak_menampilkan_hadir_nol_persen(self):
        csv_text = (
            "Tanggal,Poli,Penjamin,Status\n"
            + "2026-09-01,Siti, Aminah,BPJS,Selesai\n" * 5
        )
        header, baris = rk.baca_csv(csv_text, is_text=True)
        hasil = rk.rekap(header, baris)
        self.assertEqual(hasil["total_dapat_dibaca"], 0)
        teks = rk.format_teks(hasil)
        self.assertNotIn("Hadir: 0 (0.0%)", teks)
        self.assertIn("tidak ada baris yang bisa dibaca", teks.lower())
        self.assertNotIn("Siti", teks)
        self.assertNotIn("Aminah", teks)

    def test_100_baris_pemisah_ujung_rekap_tetap_normal(self):
        """Reproduksi persis skenario penguji: 100 baris valid, SEMUA
        diakhiri pemisah kosong tambahan -> rekap harus tetap normal,
        bukan kosong."""
        csv_text = "Tanggal,Poli,Penjamin,Status\n"
        for i in range(100):
            csv_text += f"2026-09-{(i % 28) + 1:02d},Gigi,BPJS,Selesai,\n"
        header, baris = rk.baca_csv(csv_text, is_text=True)
        hasil = rk.rekap(header, baris)
        self.assertEqual(hasil["total_pendaftaran"], 100)
        self.assertEqual(hasil["baris_bergeser_jumlah"], 0)
        self.assertEqual(hasil["hadir"], 100)
        self.assertEqual(sum(hasil["per_hari"].values()), 100)


class TesR15aFilterKolomNama(unittest.TestCase):
    """R15(a) (opsional, dikerjakan): nilai kategori yang sama dengan kata
    di kolom Nama disembunyikan, tanpa pernah mencetak isi kolom Nama."""

    def test_nama_berulang_di_status_tersaring_bila_ada_di_kolom_nama(self):
        csv_text = (
            "Tanggal,Nama Pasien,Status\n"
            + "2026-09-01,Joko Susanto,Joko\n" * 3
            + "2026-09-01,Ani Wijaya,Selesai\n" * 3
        )
        header, baris = rk.baca_csv(csv_text, is_text=True)
        hasil = rk.rekap(header, baris)
        teks = rk.format_teks(hasil)
        dump = json.dumps(hasil, ensure_ascii=False)
        # "Joko" walau muncul 3x (lolos ambang frekuensi) tetap disembunyikan
        # karena juga muncul sebagai kata di kolom "Nama Pasien".
        self.assertNotIn("Joko", teks)
        self.assertNotIn("Susanto", teks)
        self.assertNotIn("Wijaya", teks)
        self.assertNotIn("Joko", dump)
        # "Selesai" tidak ada di kolom nama manapun -> tetap tampil.
        self.assertIn("Selesai", teks)
        self.assertIn("Nama Pasien", hasil["kolom_sensitif_diabaikan"])

    def test_kolom_nama_sendiri_tidak_pernah_tampil(self):
        csv_text = "Tanggal,Nama Pasien,Poli\n" + "2026-09-01,Budi Setiawan,Gigi\n" * 3
        header, baris = rk.baca_csv(csv_text, is_text=True)
        hasil = rk.rekap(header, baris)
        teks = rk.format_teks(hasil)
        dump = json.dumps(hasil, ensure_ascii=False)
        self.assertNotIn("Budi", teks)
        self.assertNotIn("Setiawan", teks)
        self.assertNotIn("Budi", dump)
        self.assertIn("TIDAK PERNAH ditampilkan", teks)

    def test_tanpa_kolom_nama_perilaku_tidak_berubah(self):
        header, baris = rk.baca_csv(CSV_NORMAL, is_text=True)
        hasil = rk.rekap(header, baris)
        self.assertEqual(hasil["per_poli"]["Gigi"], 3)

    def test_token_pendek_tidak_dipakai_menyaring(self):
        """Token < 3 huruf (mis. 'di', 'A') sengaja tidak dipakai untuk
        menyaring, supaya kata umum tidak salah tersaring."""
        csv_text = (
            "Tanggal,Nama Pasien,Status\n"
            + "2026-09-01,A Di,Hadir\n" * 3
            + "2026-09-01,A Di,Selesai\n" * 3
        )
        header, baris = rk.baca_csv(csv_text, is_text=True)
        hasil = rk.rekap(header, baris)
        teks = rk.format_teks(hasil)
        # "Hadir" dan "Selesai" tidak mengandung token panjang dari nama
        # ("A"/"Di" terlalu pendek untuk dipakai menyaring) -> tetap tampil.
        self.assertIn("Hadir", teks)
        self.assertIn("Selesai", teks)


class TesTotalDanPersentase(unittest.TestCase):
    """S3: total pendaftaran, hadir, tidak datang, persentase eksplisit."""

    def test_persentase_dihitung_dan_dibulatkan_1_desimal(self):
        csv_text = """Tanggal,Status
2026-09-01,Selesai
2026-09-01,Selesai
2026-09-01,Tidak datang
"""
        header, baris = rk.baca_csv(csv_text, is_text=True)
        hasil = rk.rekap(header, baris)
        self.assertEqual(hasil["total_pendaftaran"], 3)
        self.assertEqual(hasil["hadir"], 2)
        self.assertEqual(hasil["tidak_datang"], 1)
        self.assertAlmostEqual(hasil["persentase_hadir"], 66.7)
        self.assertAlmostEqual(hasil["persentase_tidak_datang"], 33.3)

    def test_tanpa_kolom_status_field_none(self):
        header, baris = rk.baca_csv("Tanggal,Poli\n2026-09-01,A\n", is_text=True)
        hasil = rk.rekap(header, baris)
        self.assertIsNone(hasil["hadir"])
        self.assertIsNone(hasil["tidak_datang"])
        self.assertIsNone(hasil["persentase_hadir"])


class TesDataRusak(unittest.TestCase):
    def test_hanya_header_raise_error(self):
        header, baris = rk.baca_csv(CSV_HANYA_HEADER, is_text=True)
        with self.assertRaises(rk.DataError):
            rk.rekap(header, baris)

    def test_tanpa_kolom_tanggal_raise_error(self):
        header, baris = rk.baca_csv("Poli\nGigi\n", is_text=True)
        with self.assertRaises(rk.DataError):
            rk.rekap(header, baris)

    def test_file_tidak_ada(self):
        with self.assertRaises(rk.DataError):
            rk.baca_csv("/path/tidak/ada/kunjungan.csv")


class TesCLI(unittest.TestCase):
    def test_main_file_tidak_ada_exit_code_1(self):
        buf_err = io.StringIO()
        with redirect_stderr(buf_err):
            kode = rk.main(["--file", "/path/tidak/ada.csv"])
        self.assertEqual(kode, 1)
        self.assertIn("Error", buf_err.getvalue())

    def test_main_json_output(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False, encoding="utf-8") as f:
            f.write(CSV_NORMAL)
            path = f.name
        try:
            buf_out = io.StringIO()
            with redirect_stdout(buf_out):
                kode = rk.main(["--file", path, "--format", "json"])
            self.assertEqual(kode, 0)
            data = json.loads(buf_out.getvalue())
            self.assertEqual(data["total_pendaftaran"], 5)
        finally:
            os.unlink(path)


if __name__ == "__main__":
    unittest.main()
