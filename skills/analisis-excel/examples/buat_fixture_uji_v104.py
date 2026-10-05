#!/usr/bin/env python3
"""Fixture uji ulang v1.0.4 (penguji independen ke-5). Python standar, deterministik.
Fokus: ekspor NYATA yang umum di Indonesia (Shopee/Tokopedia/TikTok Shop, mutasi BCA/Mandiri, Google Form,
CSV dari Excel) dengan judul laporan di atas, catatan kaki/Total di bawah, kolom kosong di tengah, baris kurang sel,
kutip nyasar. Bentuk file meniru pola umum ekspor (bukan salinan file asli). kunci-v104.json = kunci independen
(dihitung dari data sumber di script ini, tanpa membaca kode skill). Pakai: python3 buat_fixture_uji_v104.py [folder]"""
import csv, io, json, random, sys
from pathlib import Path

O = Path(sys.argv[1] if len(sys.argv) > 1 else "fixture-v104"); O.mkdir(parents=True, exist_ok=True)
r = random.Random(20260927); K = {}


def rp_id(n):  # 1250000 -> "1.250.000"
    return f"{n:,}".replace(",", ".")


def csvtext(rows, delim=",", term="\r\n"):
    b = io.StringIO(); w = csv.writer(b, delimiter=delim, lineterminator=term); w.writerows(rows); return b.getvalue()


def simpan(nama, teks, enc="utf-8"):
    (O / nama).write_bytes(teks.encode(enc))


PROD = ["Kaos Polos Hitam, L", "Hijab Segi Empat Motif", "Tumbler 500ml", "Sandal Jepit Anak", "Kopi Bubuk 250gr"]

# N1 Shopee-like: 3 baris judul laporan di atas, header, 20 data, baris kosong, baris Total (label kolom 1, lengkap),
#    catatan kaki 1 sel "Dicetak oleh ...". Harapan pengguna: 20 baris, total benar.
rows = []; tot = 0
for i in range(20):
    q = r.randint(1, 4); h = r.choice([35000, 49900, 75000, 120000]); t = q * h; tot += t
    rows.append([f"2609{r.randint(10,99)}XK{i:04d}", f"2026-09-{r.randint(1,28):02d} 1{r.randint(0,9)}:{r.randint(10,59)}",
                 r.choice(PROD), q, h, t, r.choice(["Selesai", "Selesai", "Dikirim"])])
hdr = ["No. Pesanan", "Waktu Pesanan Dibuat", "Nama Produk", "Jumlah", "Harga Awal", "Total Pembayaran", "Status Pesanan"]
simpan("N1-shopee-judul-catatan-kaki.csv",
       "Laporan Pesanan Toko Berkah Jaya\r\nPeriode: 01-09-2026 s/d 30-09-2026\r\n\r\n" + csvtext([hdr] + rows)
       + "\r\n" + csvtext([["Total", "", "", sum(x[3] for x in rows), "", tot, ""]]) + "Dicetak oleh: admin@tokoberkah pada 30-09-2026 21:05\r\n")
K["N1"] = {"baris": 20, "total_pembayaran": tot, "qty": sum(x[3] for x in rows),
           "harapan": "20 baris & total benar; baris Total dilewati; catatan kaki diabaikan ATAU GAGAL dengan jalan keluar jelas"}

# N2 Tokopedia-like: angka teks "Rp1.250.000" berkutip, 1 baris judul, catatan kaki 2 baris (1 sel dan 2 sel)
rows = []; tot = 0
for i in range(15):
    t = r.randint(3, 60) * 5000; tot += t
    rows.append([f"INV/20260915/MPL/{3000+i}", f"{r.randint(1,30):02d}-09-2026", r.choice(PROD), f"Rp{rp_id(t)}", "Pesanan Selesai"])
hdr = ["Nomor Invoice", "Tanggal Pembayaran", "Nama Produk", "Total Penjualan (IDR)", "Status Terakhir"]
simpan("N2-tokopedia-rp-catatan-2-baris.csv", "Daftar Transaksi - Toko Sumber Rejeki\r\n" + csvtext([hdr] + rows)
       + "\r\n" + csvtext([["Catatan: data diambil dari Seller Center"], ["Jumlah pesanan:", "15"]]))
K["N2"] = {"baris": 15, "total": tot, "harapan": "15 baris, total benar; 2 baris catatan kaki tidak dihitung"}

# N3 TikTok Shop-like: baris ke-2 = deskripsi kolom (teks), tanpa judul/footer
rows = []; tot = 0
for i in range(18):
    q = r.randint(1, 3); t = q * r.choice([25000, 59000, 89000]); tot += t
    rows.append([f"5770{r.randint(10**9, 10**10-1)}", "Completed", r.choice(PROD), q, t, f"09/{r.randint(1,28):02d}/2026 10:{r.randint(10,59)}:00 AM"])
hdr = ["Order ID", "Order Status", "Product Name", "Quantity", "Order Amount", "Created Time"]
desc = ["Platform unique order ID.", "Current order status.", "Product name.", "SKU quantity.", "Total order amount.", "Order created time."]
simpan("N3-tiktok-baris-deskripsi.csv", csvtext([hdr, desc] + rows))
K["N3"] = {"baris": 18, "total": tot, "qty": sum(x[3] for x in rows),
           "harapan": "total benar; baris deskripsi dilaporkan (nilai tidak valid) atau diabaikan; tanggal m/d/Y"}

# N4 BCA-like mutasi: metadata di atas, kolom tanpa judul (CR/DB) di tengah, saldo di bawah (2-3 sel)
saldo_awal = 12500000; rows = []; cr = db = 0; s = saldo_awal
for i in range(16):
    j = r.randint(2, 300) * 5000; k = r.choice(["CR", "DB", "DB"])
    if k == "CR": cr += j; s += j
    else: db += j; s -= j
    rows.append([f"'{r.randint(1,28):02d}/09", r.choice(["TRSF E-BANKING CR 2509/FTSCY/WS95051", "TARIKAN ATM 25/09", "BYR VIA E-BANKING PLN", "KR OTOMATIS LLG-ANDI"]),
                 "'0000", f"{j}.00", k, f"{s}.00"])
rows.sort(key=lambda x: x[0])
meta = [["No. rekening :", "'1234567890"], ["Nama :", "TOKO CONTOH"], ["Periode :", "01/09/2026 - 30/09/2026"], ["Kode Mata Uang :", "Rp"], []]
foot = [[], ["Saldo Awal :", f"{saldo_awal}.00"], ["Mutasi Kredit :", f"{cr}.00", str(sum(1 for x in rows if x[4] == 'CR'))],
        ["Mutasi Debet :", f"{db}.00", str(sum(1 for x in rows if x[4] == 'DB'))], ["Saldo Akhir :", f"{s}.00"]]
simpan("N4-bca-mutasi.csv", csvtext(meta + [["Tanggal Transaksi", "Keterangan", "Cabang", "Jumlah", "", "Saldo"]] + rows + foot))
K["N4"] = {"baris": 16, "jumlah_semua": cr + db, "kredit_CR": cr, "debet_DB": db, "saldo_akhir": s,
           "harapan": "16 baris; kolom tanpa judul (CR/DB) tetap terbaca; catatan saldo di bawah tidak jadi data"}

# N5 Mandiri-like: judul kolom ganda "Description", angka format EN "1,500,000.00" berkutip, koma di ujung tiap baris
rows = []; deb = kre = 0
for i in range(14):
    j = r.randint(1, 400) * 2500
    if r.random() < 0.5: d, c = j, 0; deb += j
    else: d, c = 0, j; kre += j
    rows.append(["1370012345678", f"{r.randint(1,28):02d}/09/26", f"{r.randint(1,28):02d}/09/26", "8" + str(r.randint(100, 999)),
                 r.choice(["Transfer Ke", "Pembayaran QRIS", "Transfer Dari"]), r.choice(["BUDI S", "WARUNG SARI", "PT ABC"]),
                 f"REF{r.randint(10**6, 10**7)}", f"{d:,.2f}", f"{c:,.2f}", ""])
simpan("N5-mandiri-kolom-ganda.csv", csvtext([["Account No", "Date", "Val. Date", "Transaction Code", "Description", "Description",
                                                "Reference No.", "Debit", "Credit", ""]] + rows))
K["N5"] = {"baris": 14, "debit": deb, "credit": kre,
           "harapan": "Debit & Credit benar (format 1,500,000.00); dua kolom 'Description' dibedakan"}

# N6 Google Form: Timestamp d/m/Y H:M:S, jawaban kotak centang "Kopi, Teh" berkutip, jawaban paragraf multi-baris,
#    kolom jumlah diketik bebas (ada "50rb" dan "Rp 75.000")
rows = []; tot_valid = 0; invalid = 0
for i in range(22):
    n = r.randint(2, 30) * 5000
    gaya = r.choice(["plain", "plain", "rp", "titik"]) if i not in (5, 16) else "rb"
    if gaya == "plain": v = str(n); tot_valid += n
    elif gaya == "rp": v = f"Rp {rp_id(n)}"; tot_valid += n
    elif gaya == "titik": v = rp_id(n); tot_valid += n
    else: v = f"{n // 1000}rb"; invalid += 1
    alamat = f"Jl. Mawar No. {r.randint(1,99)}, RT 0{r.randint(1,9)}/RW 0{r.randint(1,9)}\nKel. Sukamaju, Kec. Cibinong\nKab. Bogor" if i % 3 == 0 else f"Perum Griya Asri Blok {chr(65+i%5)}{r.randint(1,20)}"
    rows.append([f"{r.randint(1,28)}/09/2026 {r.randint(7,21)}:{r.randint(10,59)}:{r.randint(10,59)}", f"Peserta {i+1:02d}",
                 alamat, r.choice(["Kopi", "Kopi, Teh", "Teh, Roti Bakar", "Kopi, Teh, Roti Bakar"]), v,
                 "Tolong dikirim sore.\nTerima kasih!" if i % 4 == 1 else ""])
simpan("N6-google-form.csv", csvtext([["Timestamp", "Nama Lengkap", "Alamat Pengiriman", "Pesanan (boleh lebih dari satu)",
                                      "Jumlah Transfer", "Catatan untuk penjual"]] + rows, term="\n"))
K["N6"] = {"baris": 22, "total_valid": tot_valid, "tidak_valid": invalid,
           "harapan": "22 baris; sel multi-baris sah terbaca; '50rb' dilaporkan tidak valid (2 nilai) atau dibaca 50000 dengan info"}

# N7 Excel ";" (regional Indonesia): kolom kosong di tengah (judul kosong), angka "1.250.000", baris ;;;;; di akhir
rows = []; tot = 0
for i in range(17):
    q = r.randint(1, 12); h = r.choice([12500, 45000, 150000]); t = q * h; tot += t
    rows.append([f"{r.randint(1,30):02d}/09/2026", r.choice(["Semen 50kg", "Paku 5cm", "Cat Tembok 5kg"]), "", str(q), rp_id(h), rp_id(t)])
simpan("N7-excel-titikkoma-kolom-kosong.csv", csvtext([["Tanggal", "Barang", "", "Qty", "Harga", "Total"]] + rows
                                                       + [["", "", "", "", "", ""]] * 3, delim=";"), enc="cp1252")
K["N7"] = {"baris": 17, "total": tot, "qty": sum(int(x[3]) for x in rows), "harapan": "17 baris, total benar, baris ;;;;; diabaikan"}

# N8 Kolom opsional di ujung kanan tidak diketik (tanpa koma di ujung) - diketik tangan/diekspor aplikasi kasir sederhana
rows = []; tot = 0
for i in range(20):
    t = r.randint(1, 50) * 1000; tot += t
    rows.append([f"2026-09-{r.randint(1,28):02d}", r.choice(["Bu Rina", "Pak Joko", "CV Sinar"]), str(t)] + (["lunas"] if i % 3 == 0 else []))
simpan("N8-kolom-catatan-opsional.csv", csvtext([["Tanggal", "Pelanggan", "Jumlah", "Catatan"]] + rows))
K["N8"] = {"baris": 20, "total": tot, "harapan": "WAJAR dibaca (sel kosong di ujung kanan, angka tidak bergeser); ditolak = (d)"}

# N9 Baris kurang sel DI TENGAH (Pelanggan terlewat) -> angka bergeser; wajib GAGAL/peringatan tegas
rows = []; tot = 0
for i in range(20):
    t = r.randint(1, 50) * 1000; tot += t
    rows.append([f"2026-09-{r.randint(1,28):02d}", r.choice(["Bu Rina", "Pak Joko"]), r.choice(["Gula", "Beras"]), str(t)])
rows[9] = [rows[9][0], rows[9][2], rows[9][3]]
simpan("N9-sel-terlewat-tengah.csv", csvtext([["Tanggal", "Pelanggan", "Barang", "Jumlah"]] + rows))
K["N9"] = {"baris": 20, "total": tot, "baris_rusak_excel": 11, "harapan": "GAGAL / peringatan tegas baris 11"}

# N10 Kutip nyasar realistis: ukuran inci 'Pipa 3"' tanpa kutip pembungkus (kutip di tengah sel), dan
#     nama panggilan diawali kutip '"Ucup" Warung' (kutip di awal sel, tertutup di sel yang sama)
rows = []; tot = 0
for i in range(15):
    t = r.randint(1, 40) * 2500; tot += t
    b = r.choice(['Pipa PVC 3"', 'Pipa PVC 1/2"', "Lem Pipa"])
    p = '"Ucup" Warung' if i in (4, 11) else r.choice(["Toko Makmur", "Pak Haji"])
    rows.append(f"2026-09-{r.randint(1,28):02d},{p},{b},{t}")
simpan("N10-kutip-inci-panggilan.csv", "Tanggal,Pelanggan,Barang,Jumlah\n" + "\n".join(rows) + "\n")
K["N10"] = {"baris": 15, "total": tot, "harapan": "15 baris & total benar (kutip di tengah sel literal), atau peringatan jelas"}

# N11 Excel CSV dengan baris jumlah TANPA LABEL di bawah (SUM di kolom Jumlah saja) + baris "Rata-rata"
rows = []; tot = 0
for i in range(12):
    t = r.randint(10, 90) * 10000; tot += t
    rows.append([f"{r.randint(1,30):02d}/09/2026", r.choice(["ATK", "Listrik", "Transport"]), f"Nota {i+1}", str(t)])
simpan("N11-excel-sum-tanpa-label.csv", csvtext([["Tanggal", "Kategori", "Keterangan", "Jumlah"]] + rows
                                               + [["", "", "", str(tot)], ["", "", "Rata-rata", str(tot // 12)]]))
K["N11"] = {"baris": 12, "total": tot, "harapan": "total TIDAK dobel; baris SUM tanpa label & Rata-rata dilewati atau diperingatkan tegas"}

# N12 Shopee-like: catatan kaki yang jumlah selnya SAMA dengan judul (padding Excel) & label bukan 'Total'
rows = []; tot = 0
for i in range(10):
    t = r.randint(2, 40) * 5000; tot += t
    rows.append([f"2609{i:04d}AB", f"2026-09-{r.randint(1,28):02d}", r.choice(PROD), str(t)])
simpan("N12-footer-berpadding.csv", "Laporan Penghasilan Toko\n" + csvtext([["No. Pesanan", "Tanggal", "Produk", "Penghasilan"]] + rows
                                   + [["", "", "", ""], ["Dicetak oleh: admin", "", "", ""], ["Sumber: Seller Centre", "30-09-2026", "", ""]], term="\n"))
K["N12"] = {"baris": 10, "total": tot, "harapan": "10 baris, total benar; baris catatan berpadding tidak menambah angka"}

# N13 Tokopedia-like: kolom SKU berisi angka panjang & baris "Subtotal" per hari (label di kolom 2), lengkap kolomnya
rows = []; tot = 0; out = []
for d in (3, 4, 5):
    sub = 0
    for i in range(4):
        t = r.randint(2, 30) * 5000; sub += t; tot += t
        out.append([f"2026-09-{d:02d}", f"8997{r.randint(10**8, 10**9-1)}", r.choice(PROD), str(t)])
    out.append(["", "Subtotal", "", str(sub)])
simpan("N13-subtotal-per-hari.csv", csvtext([["Tanggal", "SKU", "Produk", "Nominal"]] + out))
K["N13"] = {"baris": 12, "total": tot, "harapan": "total tanpa subtotal (dilewati) atau peringatan tegas dobel; SKU = kode"}

(O / "kunci-v104.json").write_text(json.dumps(K, indent=1, ensure_ascii=False), encoding="utf-8")
print("OK", len(K), "file ->", O)
