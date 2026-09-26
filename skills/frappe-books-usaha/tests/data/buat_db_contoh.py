#!/usr/bin/env python3
"""Bangun database Frappe Books TIRUAN berisi data FIKTIF untuk uji & contoh.

Skema: skema-frappe-books-v0.36.0.sql (dibangkitkan dari schemas/ resmi Frappe Books v0.36.0).
Format nilai mengikuti Frappe Books: Currency = teks presisi 11 desimal (pesa .store),
Datetime = ISO UTC 'YYYY-MM-DDTHH:MM:SS.000Z' (Date.toISOString), Check = 0/1.

Pakai:  python3 buat_db_contoh.py <keluar.books.db>
Semua nama usaha, pelanggan, pemasok, dan angka di sini FIKTIF.
"""
import os
import sqlite3
import sys
from datetime import datetime, timedelta, timezone

SINI = os.path.dirname(os.path.abspath(__file__))
WIB = timezone(timedelta(hours=7))
SISTEM = "__SYSTEM__"


def m(x):
    """Currency -> teks gaya pesa (11 desimal)."""
    return f"{x:.11f}"


def t(s):
    """'2026-09-01 00:00' waktu WIB -> ISO UTC seperti Frappe Books."""
    d = datetime.strptime(s, "%Y-%m-%d %H:%M").replace(tzinfo=WIB).astimezone(timezone.utc)
    return d.strftime("%Y-%m-%dT%H:%M:%S.000Z")


def isi(con, tabel, baris, meta=True):
    for b in baris:
        b = dict(b)
        if meta:
            b.setdefault("createdBy", SISTEM)
            b.setdefault("modifiedBy", SISTEM)
            b.setdefault("created", "2026-06-01T00:00:00.000Z")
            b.setdefault("modified", "2026-06-01T00:00:00.000Z")
        kol = ",".join(f'"{k}"' for k in b)
        con.execute(f'INSERT INTO "{tabel}" ({kol}) VALUES ({",".join("?" * len(b))})', list(b.values()))


def buat(path):
    if os.path.exists(path):
        os.remove(path)
    con = sqlite3.connect(path)
    with open(os.path.join(SINI, "skema-frappe-books-v0.36.0.sql"), encoding="utf-8") as f:
        con.executescript(f.read())

    isi(con, "SingleValue", [
        {"name": "sv1", "parent": "AccountingSettings", "fieldname": "companyName", "value": "Toko Kopi Nusantara (fiktif)"},
        {"name": "sv2", "parent": "AccountingSettings", "fieldname": "enableInventory", "value": "1"},
        {"name": "sv3", "parent": "SystemSettings", "fieldname": "currency", "value": "IDR"},
        {"name": "sv4", "parent": "SystemSettings", "fieldname": "version", "value": "0.36.0"},
    ])
    akun = [
        ("Aktiva", "Asset", None, 1), ("Piutang Dagang", "Asset", "Receivable", 0), ("Kas Rupiah", "Asset", "Cash", 0),
        ("Persediaan Barang", "Asset", "Stock", 0),
        ("Passiva", "Liability", None, 1), ("Hutang Dagang Dalam Negeri", "Liability", "Payable", 0),
        ("Hutang Pajak", "Liability", "Payable", 0),
        ("Stock Diterima Tapi Tidak Ditagih", "Liability", "Stock Received But Not Billed", 0),
        ("Pendapatan", "Income", None, 1), ("Penjualan", "Income", None, 0), ("Pendapatan Service", "Income", None, 0),
        ("HPP Pembelian", "Income", "Cost of Goods Sold", 0),
        ("Beban", "Expense", None, 1), ("Biaya Sewa Kantor", "Expense", None, 0),
        ("Biaya PLN Gudang & Kantor", "Expense", None, 0),
    ]
    isi(con, "Account", [{"name": n, "rootType": r, "accountType": a, "isGroup": g, "lft": i * 2, "rgt": i * 2 + 1}
                         for i, (n, r, a, g) in enumerate(akun)])
    isi(con, "UOM", [{"name": n, "isWhole": w} for n, w in
                     (("Unit", 1), ("Kg", 0), ("Gram", 0), ("Meter", 0), ("Jam", 0), ("Hari", 1))])
    isi(con, "Location", [{"name": "Toko"}, {"name": "Gudang"}])
    isi(con, "Tax", [{"name": "PPN 11% (12% x 11/12)"}])
    isi(con, "TaxDetail", [{"name": "td1", "account": "Hutang Pajak", "rate": 11, "idx": 0, "parent": "PPN 11% (12% x 11/12)",
                            "parentSchemaName": "Tax", "parentFieldname": "details"}], meta=False)
    isi(con, "Party", [
        {"name": "Toko Sinar Abadi", "role": "Customer", "phone": "+6281234567001", "outstandingAmount": m(543900)},
        {"name": "CV Maju Jaya", "role": "Customer", "phone": "+6281234567002", "outstandingAmount": m(0)},
        {"name": "Warung Bu Sari", "role": "Customer", "phone": "+6281234567003", "outstandingAmount": m(444350)},
        {"name": "PT Biji Kopi Gayo", "role": "Supplier", "outstandingAmount": m(1110000)},
        {"name": "UD Gula Manis", "role": "Supplier", "outstandingAmount": m(200000)},
    ])
    brg = [
        ("Kopi Arabika 250g", "KPA-250", "Unit", 85000, "Product", 1),
        ("Gula Aren 1kg", "GLA-1", "Kg", 32500, "Product", 1),
        ("Kopi Robusta 1kg", "KPR-1", "Unit", 150000, "Product", 1),
        ("Paper Cup 8oz", "CUP-8", "Unit", 1000, "Product", 1),
        ("Filter Kertas", "FLT-1", "Unit", 500, "Product", 1),
        ("Jasa Seduh Event", "JSE", "Jam", 500000, "Service", 0),
    ]
    isi(con, "Item", [{"name": n, "itemCode": k, "unit": u, "rate": m(r), "itemType": ty, "for": "Both",
                       "incomeAccount": "Pendapatan Service" if ty == "Service" else "Penjualan",
                       "expenseAccount": "HPP Pembelian", "trackItem": tr} for n, k, u, r, ty, tr in brg])

    # ---- invoice penjualan: (no, tgl WIB, pihak, [(barang, qty, harga, pajak?)], sisa, submitted, cancelled, returnAgainst)
    pajak = "PPN 11% (12% x 11/12)"
    sinv = [
        ("SINV-1001", "2026-07-10 10:00", "Toko Sinar Abadi", [("Kopi Arabika 250g", 3, 85000, 1), ("Gula Aren 1kg", 2, 32500, 1)], None, 1, 0, None),
        ("SINV-1002", "2026-09-01 00:00", "CV Maju Jaya", [("Kopi Robusta 1kg", 2, 150000, 0)], 0, 1, 0, None),
        ("SINV-1003", "2026-09-25 14:00", "Warung Bu Sari", [("Kopi Arabika 250g", 1, 85000, 1), ("Jasa Seduh Event", 1, 500000, 0)], 294350, 1, 0, None),
        ("SINV-1004", "2026-09-26 09:00", "Toko Sinar Abadi", [("Kopi Arabika 250g", 2, 85000, 1)], None, 1, 0, None),
        ("SINV-1005", "2026-09-26 11:00", "CV Maju Jaya", [("Kopi Robusta 1kg", 1, 150000, 0)], None, 0, 0, None),
        ("SINV-1006", "2026-09-20 10:00", "Warung Bu Sari", [("Kopi Robusta 1kg", 1, 100000, 0)], 0, 1, 1, None),
        ("SINV-1007", "2026-06-01 08:00", "Warung Bu Sari", [("Kopi Robusta 1kg", 1, 150000, 0)], None, 1, 0, None),
        ("SINV-1008", "2026-09-05 10:00", "CV Maju Jaya", [("Kopi Robusta 1kg", -1, 150000, 0)], 0, 1, 0, "SINV-1002"),
    ]
    pinv = [
        ("PINV-2001", "2026-09-03 10:00", "PT Biji Kopi Gayo", [("Kopi Arabika 250g", 20, 50000, 1)], None, 1, 0, None),
        ("PINV-2002", "2026-08-01 10:00", "UD Gula Manis", [("Gula Aren 1kg", 10, 20000, 0)], None, 1, 0, None),
    ]
    for skema, data, akun_pihak in (("SalesInvoice", sinv, "Piutang Dagang"), ("PurchaseInvoice", pinv, "Hutang Dagang Dalam Negeri")):
        for no, tg, pihak, baris, sisa, sub, bat, retur in data:
            net = sum(q * h for _, q, h, _ in baris)
            tax = sum(q * h * 11 / 100 for _, q, h, p in baris if p)
            grand = net + tax
            r = {"name": no, "numberSeries": no[:5], "party": pihak, "account": akun_pihak, "date": t(tg),
                 "netTotal": m(net), "grandTotal": m(grand), "baseGrandTotal": m(grand),
                 "outstandingAmount": m(grand if sisa is None else sisa), "exchangeRate": 1, "currency": "IDR",
                 "submitted": sub, "cancelled": bat, "returnAgainst": retur, "isReturned": 0}
            if skema == "SalesInvoice":
                r["isPOS"] = 0
            isi(con, skema, [r])
            for i, (b, q, h, p) in enumerate(baris):
                isi(con, skema + "Item", [{"name": f"{no}-{i}", "item": b, "rate": m(h), "quantity": q, "transferQuantity": q,
                                            "unitConversionFactor": 1, "amount": m(q * h), "tax": pajak if p else None,
                                            "account": "Penjualan" if skema == "SalesInvoice" else "HPP Pembelian",
                                            "idx": i, "parent": no, "parentSchemaName": skema, "parentFieldname": "items"}], meta=False)
            if tax:
                isi(con, "TaxSummary", [{"name": f"{no}-tax", "account": "Hutang Pajak", "rate": 11, "amount": m(tax), "idx": 0,
                                         "parent": no, "parentSchemaName": skema, "parentFieldname": "taxes"}], meta=False)

    # ---- buku besar (hanya yang relevan untuk laba rugi & uji zona waktu)
    ale = []

    def jurnal(tg, akun_, debit, kredit, ref, reverted=0):
        ale.append({"name": f"ALE-{len(ale) + 1:04d}", "date": t(tg), "account": akun_, "debit": m(debit), "credit": m(kredit),
                    "referenceType": "SalesInvoice", "referenceName": ref, "reverted": reverted})

    jurnal("2026-09-01 00:00", "Piutang Dagang", 300000, 0, "SINV-1002")
    jurnal("2026-09-01 00:00", "Penjualan", 0, 300000, "SINV-1002")
    jurnal("2026-09-01 00:00", "HPP Pembelian", 200000, 0, "SINV-1002")
    jurnal("2026-09-01 00:00", "Persediaan Barang", 0, 200000, "SINV-1002")
    jurnal("2026-09-05 10:00", "Penjualan", 150000, 0, "SINV-1008")
    jurnal("2026-09-05 10:00", "Piutang Dagang", 0, 150000, "SINV-1008")
    jurnal("2026-09-05 10:00", "Persediaan Barang", 100000, 0, "SINV-1008")
    jurnal("2026-09-05 10:00", "HPP Pembelian", 0, 100000, "SINV-1008")
    jurnal("2026-09-20 10:00", "Penjualan", 0, 100000, "SINV-1006", reverted=1)
    jurnal("2026-09-21 10:00", "Penjualan", 100000, 0, "SINV-1006", reverted=1)
    jurnal("2026-09-25 14:00", "Penjualan", 0, 85000, "SINV-1003")
    jurnal("2026-09-25 14:00", "Pendapatan Service", 0, 500000, "SINV-1003")
    jurnal("2026-09-25 14:00", "Hutang Pajak", 0, 9350, "SINV-1003")
    jurnal("2026-09-25 14:00", "Piutang Dagang", 594350, 0, "SINV-1003")
    jurnal("2026-09-25 14:00", "HPP Pembelian", 50000, 0, "SINV-1003")
    jurnal("2026-09-26 09:00", "Penjualan", 0, 170000, "SINV-1004")
    jurnal("2026-09-26 09:00", "Hutang Pajak", 0, 18700, "SINV-1004")
    jurnal("2026-09-26 09:00", "Piutang Dagang", 188700, 0, "SINV-1004")
    jurnal("2026-09-26 09:00", "HPP Pembelian", 100000, 0, "SINV-1004")
    jurnal("2026-09-05 08:00", "Biaya Sewa Kantor", 1000000, 0, "JV-001")
    jurnal("2026-09-15 08:00", "Biaya PLN Gudang & Kantor", 250000, 0, "JV-002")
    jurnal("2026-08-20 08:00", "Biaya PLN Gudang & Kantor", 300000, 0, "JV-003")
    jurnal("2026-10-01 00:30", "Biaya Sewa Kantor", 999999, 0, "JV-004")
    isi(con, "AccountingLedgerEntry", ale)

    sle = [("Kopi Arabika 250g", 10, "2026-07-01 08:00", "Toko"), ("Kopi Arabika 250g", -3, "2026-07-10 10:00", "Toko"),
           ("Kopi Arabika 250g", 20, "2026-09-03 10:00", "Gudang"), ("Kopi Arabika 250g", -1, "2026-09-25 14:00", "Toko"),
           ("Kopi Arabika 250g", -2, "2026-09-26 09:00", "Toko"),
           ("Gula Aren 1kg", 4, "2026-07-01 08:00", "Toko"), ("Gula Aren 1kg", -2, "2026-07-10 10:00", "Toko"),
           ("Kopi Robusta 1kg", 2, "2026-08-01 08:00", "Toko"), ("Kopi Robusta 1kg", -2, "2026-09-01 00:00", "Toko"),
           ("Kopi Robusta 1kg", 1, "2026-09-05 10:00", "Toko"),
           ("Paper Cup 8oz", 5, "2026-08-01 08:00", "Toko"), ("Paper Cup 8oz", -5, "2026-09-10 08:00", "Toko"),
           ("Filter Kertas", -1, "2026-09-11 08:00", "Toko")]
    isi(con, "StockLedgerEntry", [{"name": f"SLE-{i:04d}", "item": b, "quantity": q, "date": t(tg), "location": lok,
                                   "rate": m(0), "referenceType": "StockMovement", "referenceName": f"MAT-{i}"}
                                  for i, (b, q, tg, lok) in enumerate(sle)])
    con.commit()
    con.close()
    return path


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Pakai: python3 buat_db_contoh.py <keluar.books.db>")
        sys.exit(2)
    print(buat(sys.argv[1]))
