# Sumber resmi & hasil verifikasi (diakses 26 September 2026)

## Actual Budget
- Kode sumber: https://github.com/actualbudget/actual (lisensi **MIT**, `LICENSE.txt`, "Copyright James Long").
  Dibaca dari salinan `git clone --depth 1` commit `bfa850ca618ca78c556ded61274602f1fca7a4a4` (24 Sep 2026).
- Versi: **26.9.0** (`packages/desktop-electron/package.json` dan `packages/api/package.json`; rilis 1 Sep 2026,
  https://github.com/actualbudget/actual/releases).
- Dokumentasi (sumbernya ada di repo, `packages/docs/docs/`):
  - Impor transaksi: https://actualbudget.org/docs/transactions/importing
  - Folder data aplikasi desktop: https://actualbudget.org/docs/troubleshooting/data-folder-access
  - Struktur database: https://actualbudget.org/docs/contributing/project-details/database
  - Anggaran amplop & rollover: https://actualbudget.org/docs/budgeting/
  - Ekspor/backup: https://actualbudget.org/docs/backup-restore/backup
  - API (Node.js, `@actual-app/api`): https://actualbudget.org/docs/api/
  - Unduh aplikasi desktop: https://actualbudget.org/download

## 1. Format impor yang didukung
- Dokumentasi: "Actual supports importing **CSV, QIF, OFX, QFX and CAMT** files" (OFX/QFX dianjurkan bila bank menyediakan).
  Kode: `packages/loot-core/src/server/transactions/import/parse-file.ts` memilih parser dari ekstensi
  `.qif`, `.csv`, `.tsv`, `.ofx`, `.qfx`, `.xml` (CAMT).
- Bank besar Indonesia umumnya hanya menyediakan CSV/Excel/PDF, jadi skill ini membuat **CSV**.
- CSV diurai dengan `csv-parse`: pemisah bisa dipilih (default koma), tanda kutip `"`, BOM diabaikan.
- Pemetaan kolom otomatis (`ImportTransactionsModal.tsx`): judul yang mengandung `date`, `amount`, `category`,
  `payee`, `notes` langsung terpasang. Karena itu hasil skill memakai judul **Date, Payee, Notes, Category, Amount**.
- Format tanggal yang bisa dipilih: `YYYY MM DD`, `YY MM DD`, `MM DD YYYY`, `MM DD YY`, `DD MM YYYY`, `DD MM YY`
  (`ImportTransactionsModal/utils.ts`). Skill menulis `YYYY-MM-DD`.
- Jumlah dibaca `looselyParseAmount` (`packages/loot-core/src/shared/util.ts`): tanda desimal hanya dikenali bila
  diikuti 1–2 (atau 4–9) angka; "1.500.000" (3 angka) dibaca 1500000. Skill menulis angka **tanpa pemisah ribuan,
  titik desimal hanya bila ada sen** (mis. `-1500000`, `12345.67`) supaya tidak ada tafsir ganda.
- Kategori dari CSV dicocokkan **nama persis** (`parseCategoryFields`: `category.name === trans.category`,
  peka huruf besar/kecil). Nama tidak cocok → transaksi masuk tanpa kategori. Karena itu skill mencocokkan nama
  ke budget pengguna (`--db`).
- Duplikat: Actual mencocokkan transaksi yang mirip (tanggal berdekatan, jumlah sama, payee mirip) dan
  memperbaruinya, bukan menambah baru (dokumentasi "Avoiding duplicate transactions").

## 2. Struktur file budget lokal
- Aplikasi desktop menyimpan budget di folder data, bawaan `Documents/Actual/<Nama-Budget-xxxxxxx>/`
  (dokumentasi data-folder-access & migration). Isi folder: `db.sqlite`, `metadata.json` (`budgetName`),
  kadang `cache.sqlite`. Lokasi bisa diganti di Settings → "Actual's data directory".
- Versi web/server tidak menyimpan `db.sqlite` di folder biasa (data ada di browser/IndexedDB dan di server
  sebagai file sinkron) → skill hanya membaca budget aplikasi **desktop** atau hasil **Export** (.zip) yang diekstrak.
- `db.sqlite` = SQLite. Skema awal `packages/loot-core/default-db.sqlite` + migrasi `packages/loot-core/migrations/`.
  Tabel yang dipakai skill (nama kolom diverifikasi dari migrasi & dari budget asli buatan API 26.9.0):
  - `transactions`: `id, isParent, isChild, parent_id, acct, category, amount, description (payee), notes,
    date, starting_balance_flag, tombstone, ...`
  - `categories (id, name, is_income, cat_group, sort_order, hidden, tombstone)`,
    `category_groups (id, name, is_income, sort_order, hidden, tombstone)`
  - `category_mapping (id, transferId)`, `payee_mapping (id, targetId)`: kategori/payee yang digabung/dihapus
    dialihkan lewat tabel ini.
  - `payees (id, name, transfer_acct, tombstone)`, `accounts (id, name, offbudget, closed, tombstone)`
  - `zero_budgets` (mode amplop) / `reflect_budgets` (mode tracking): `id = "YYYYMM-<kategori>", month
    (YYYYMM, integer), category, amount, carryover`
  - `zero_budget_months (id "YYYY-MM", buffered)`, `preferences (id, value)`: `budgetType` = `envelope` (bawaan
    bila kosong) atau `tracking`.
- **Satuan uang: bilangan bulat dalam SEN.** `amountToInteger` = `Math.round(amount * 100)`
  (`shared/util.ts`); dokumentasi API: "$120.30 would be 12030". Jadi Rp 1.500.000 tersimpan `150000000`.
  Skill membagi 100 dengan `Decimal`.
- Tanggal transaksi: integer `YYYYMMDD` (`toDateRepr` di `server/models.ts`).
- Transaksi "hidup" meniru view `v_transactions_internal_alive` (`server/aql/schema/index.ts`): tidak tombstone,
  anak split hanya bila induknya hidup, kategori induk split = NULL, kategori lewat `category_mapping`.
- Rumus sisa anggaran meniru `server/budget/envelope.ts` (amplop: sisa bulan lalu yang positif selalu terbawa;
  sisa minus hanya terbawa bila "Rollover overspending"/`carryover` aktif, jika tidak memotong "To Budget" bulan
  berikutnya), `server/budget/tracking.ts` (tracking: sisa terbawa hanya bila `carryover`), dan `server/budget/base.ts`
  (jumlah terpakai hanya dari rekening **on-budget**).

## 3. Apakah membaca db.sqlite read-only aman?
- Aplikasi desktop memakai better-sqlite3 tanpa WAL (mode jurnal bawaan `delete`; budget asli buatan API: `PRAGMA
  journal_mode` = `delete`). Pembaca lain boleh membaca bersamaan; penulis mengunci sebentar saat menyimpan.
- Skill membuka file dengan URI `file:...?mode=ro` (SQLite menolak semua penulisan), mengambil kunci baca, menyalin
  isi ke memori dengan backup API, lalu menutup file. Tidak ada `-journal`/`-wal` yang dibuat (diuji: hash & waktu
  ubah file tidak berubah, tidak ada file baru di folder).
- Bila Actual sedang menulis (kunci eksklusif), skill berhenti setelah 5 detik dengan pesan "sedang dipakai, coba
  lagi" (diuji dengan kunci `BEGIN EXCLUSIVE`).
- Menulis ke db.sqlite dari luar Actual **tidak aman** (sinkronisasi memakai tabel `messages_crdt`; perubahan
  langsung tidak tercatat dan bisa hilang/merusak sinkron). Skill tidak pernah menulis; semua perubahan lewat
  aplikasi Actual (Import CSV) oleh pengguna.

## 4. Verifikasi yang dilakukan pembuat (26 September 2026)
- Dua budget ASLI dibuat dengan `@actual-app/api` **26.9.0** (paket resmi npm, dijalankan di folder sementara, tidak
  ikut paket skill) berisi data fiktif: amplop (split, transfer on/off-budget, transaksi terhapus, kategori dihapus &
  dialihkan, kategori tersembunyi, rollover minus) dan tracking. Angka `getBudgetMonth` dari Actual disimpan sebagai
  acuan; hitungan skill **sama persis** untuk semua kategori, "To Budget", total anggaran, pemasukan, dan kelebihan
  belanja bulan lalu (Juli–Oktober 2026). Lihat `tests/` (repo pengembang).
- CSV hasil `konversi` mutasi BCA fiktif diurai dengan parser CSV **server Actual** (`transactions-parse-file`), jumlah
  dibaca dengan logika `looselyParseAmount`, kategori dengan aturan nama persis, lalu diimpor lewat `importTransactions`
  ke salinan budget: 13 baris terbaca, 0 galat, semua jumlah tepat hingga sen (mis. `12345.67` → 1234567 sen); 8 baris
  yang mirip transaksi lama otomatis digabung (fitur anti-duplikat Actual), 5 baris baru ditambahkan.
- **Belum diuji:** layar Import di aplikasi desktop sungguhan (klik manual), Windows/macOS, ekspor mutasi asli terbaru
  dari masing-masing bank (contoh mutasi di tests adalah fiktif; lihat `format-bank.md`).
