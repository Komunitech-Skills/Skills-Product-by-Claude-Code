"""Bangun file .grist (SQLite) TIRUAN untuk uji regresi & contoh pemakaian.

PENTING (kejujuran, lihat research/sources/grist-2026-09-26.md): file ini BUKAN hasil ekspor
Grist sungguhan (lingkungan pembuatan skill ini tidak bisa menjalankan Grist). Skema tabel
metadata (`_grist_Tables`, `_grist_Tables_column`) dan aturan "tabel data pengguna = tabel
SQLite biasa bernama tableId, kolom `id INTEGER PRIMARY KEY`" disalin STRUKTURNYA (nama tabel,
nama & tipe kolom) dari kode sumber resmi `grist-core` v1.7.19 yang dibaca langsung:
  - sandbox/grist/schema.py (fungsi schema_create_actions, tabel _grist_Tables & _grist_Tables_column)
  - app/server/lib/DocStorage.ts baris ~1113 (CREATE TABLE <tableId> (id INTEGER PRIMARY KEY, ...))
Tidak ada baris kode Grist yang disalin ke sini - hanya nama tabel/kolom (fakta format file,
bukan ciptaan kreatif) dipakai supaya pembacaan read-only oleh grist.py bisa diuji dengan file
yang strukturnya sama seperti dokumen Grist asli.
"""
import sqlite3
from pathlib import Path

# Kolom _grist_Tables (persis urutan & nama di schema.py, minus kolom "id" bawaan SQLite).
_KOLOM_GRIST_TABLES = [
    "tableId", "primaryViewId", "summarySourceTable", "onDemand",
    "rawViewSectionRef", "recordCardViewSectionRef",
]
# Kolom _grist_Tables_column (persis urutan & nama di schema.py, minus "id").
_KOLOM_GRIST_TABLES_COLUMN = [
    "parentId", "parentPos", "colId", "type", "widgetOptions", "isFormula", "formula",
    "label", "description", "untieColIdFromLabel", "summarySourceCol", "displayCol",
    "visibleCol", "rules", "reverseCol", "recalcWhen", "recalcDeps",
]


def _buat_metadata(con):
    con.execute(
        "CREATE TABLE _grist_DocInfo (id INTEGER PRIMARY KEY, docId TEXT, peers TEXT, "
        "basketId TEXT, schemaVersion INTEGER, timezone TEXT, documentSettings TEXT)"
    )
    con.execute(
        "INSERT INTO _grist_DocInfo (id, schemaVersion, timezone) VALUES (1, 46, 'Asia/Jakarta')"
    )
    con.execute(
        f"CREATE TABLE _grist_Tables (id INTEGER PRIMARY KEY, {', '.join(_KOLOM_GRIST_TABLES)})"
    )
    con.execute(
        f"CREATE TABLE _grist_Tables_column (id INTEGER PRIMARY KEY, {', '.join(_KOLOM_GRIST_TABLES_COLUMN)})"
    )


def _daftarkan_tabel(con, next_id, table_id, kolom):
    """kolom: list of (colId, type, label, isFormula, formula). Kembalikan id berikutnya yang bebas."""
    con.execute(
        "INSERT INTO _grist_Tables (id, tableId, primaryViewId, summarySourceTable, onDemand, "
        "rawViewSectionRef, recordCardViewSectionRef) VALUES (?, ?, 0, 0, 0, 0, 0)",
        (next_id, table_id),
    )
    parent_id = next_id
    col_row_id = next_id * 100  # supaya tidak bentrok antar tabel, hanya kebutuhan uji ini
    for pos, (col_id, tipe, label, is_formula, formula) in enumerate(kolom, start=1):
        con.execute(
            "INSERT INTO _grist_Tables_column (id, parentId, parentPos, colId, type, "
            "widgetOptions, isFormula, formula, label, description, untieColIdFromLabel, "
            "summarySourceCol, displayCol, visibleCol, rules, reverseCol, recalcWhen, recalcDeps) "
            "VALUES (?, ?, ?, ?, ?, '', ?, ?, ?, '', 0, 0, 0, 0, NULL, 0, 0, NULL)",
            (col_row_id, parent_id, pos, col_id, tipe, int(is_formula), formula, label),
        )
        col_row_id += 1
    col_spec = ", ".join(f'"{c}" ' + ("REAL" if t in ("Numeric", "Date", "DateTime") else
                                       "INTEGER" if t in ("Int", "Bool") else "TEXT")
                          for c, t, *_ in kolom)
    con.execute(f'CREATE TABLE "{table_id}" (id INTEGER PRIMARY KEY, {col_spec})')
    return next_id + 1


def buat_dokumen_contoh(path):
    """Tulis dokumen contoh 'Data Usaha Saya' berisi tabel Pelanggan (3 baris) & Stok (3 baris),
    memakai pola dari references/pola-tabel-umkm.md. Kembalikan path yang sama untuk kemudahan."""
    path = Path(path)
    if path.exists():
        path.unlink()
    con = sqlite3.connect(str(path))
    try:
        _buat_metadata(con)
        nid = 1
        nid = _daftarkan_tabel(con, nid, "Pelanggan", [
            ("Nama", "Text", "Nama", False, ""),
            ("Telepon", "Text", "No. WA/Telepon", False, ""),
            ("TeleponRapi", "Text", "WA Rapi", True, "rumus_wa_rapi"),
            ("Kota", "Text", "Kota", False, ""),
            ("Sumber", "Text", "Sumber", False, ""),
        ])
        nid = _daftarkan_tabel(con, nid, "Stok", [
            ("Nama", "Text", "Nama Barang", False, ""),
            ("StokMasuk", "Int", "Masuk", False, ""),
            ("StokKeluar", "Int", "Keluar", False, ""),
            ("BatasMinimum", "Int", "Batas Minimum", False, ""),
            ("StokSaatIni", "Int", "Sisa Stok", True, "rumus_sisa_stok"),
            ("Status", "Text", "Status", True, "rumus_status_stok"),
        ])
        con.executemany(
            'INSERT INTO "Pelanggan" (Nama, Telepon, TeleponRapi, Kota, Sumber) VALUES (?,?,?,?,?)',
            [
                ("Toko Maju Jaya", "0812-3456-7890", "6281234567890", "Solo", "Referensi"),
                ("Warung Bu Sari", "+62 813-1111-2222", "6281311112222", "Solo", "Walk-in"),
                ("CV Sinar Abadi", "62 821 9999 8888", "6282199998888", "Semarang", "Marketplace"),
            ],
        )
        con.executemany(
            'INSERT INTO "Stok" (Nama, StokMasuk, StokKeluar, BatasMinimum, StokSaatIni, Status) '
            "VALUES (?,?,?,?,?,?)",
            [
                ("Kopi Robusta 1kg", 100, 40, 20, 60, "AMAN"),
                ("Gula Aren 1kg", 50, 48, 10, 2, "MENIPIS"),
                ("Cup Kertas 12oz", 200, 200, 50, 0, "HABIS"),
            ],
        )
        con.commit()
    finally:
        con.close()
    return path


def buat_file_rusak(path):
    """Tulis byte acak (bukan SQLite valid) untuk uji penanganan file rusak."""
    path = Path(path)
    path.write_bytes(b"BUKAN-FILE-SQLITE-SAMA-SEKALI \x00\x01\x02" * 10)
    return path


def buat_file_sqlite_tanpa_metadata_grist(path):
    """SQLite valid, tapi tanpa tabel _grist_Tables (mis. file .db biasa yang diberi ekstensi .grist
    secara keliru)."""
    path = Path(path)
    if path.exists():
        path.unlink()
    con = sqlite3.connect(str(path))
    con.execute("CREATE TABLE Sembarang (id INTEGER PRIMARY KEY, x TEXT)")
    con.commit()
    con.close()
    return path


if __name__ == "__main__":
    import sys

    tujuan = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("contoh-usaha.grist")
    buat_dokumen_contoh(tujuan)
    print(f"Ditulis: {tujuan}")
