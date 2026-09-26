#!/usr/bin/env python3
"""notebook-riset-lokal (Komunitech) - asisten riset dokumen untuk Open Notebook lokal.

Memanggil REST API resmi Open Notebook (server milik pengguna sendiri, biasanya
http://127.0.0.1:5055) lewat header 'Authorization: Bearer <kata sandi>' bila
Open Notebook diatur memakai kata sandi. Python standar saja, tanpa paket tambahan.
Menolak alamat selain komputer ini sendiri (127.0.0.1/localhost) — Open Notebook
tidak dirancang untuk dibuka ke internet.

Perintah:
  simpan-kunci     simpan kata sandi API ke file lokal (dibaca tersembunyi, tak pernah dicetak)
  cek              cek server Open Notebook bisa dihubungi & status kata sandi
  daftar-notebook  daftar notebook (folder riset) yang ada
  buat-notebook    buat notebook baru
  tambah-sumber    tambah sumber (tautan web, teks tempel, atau file lokal) ke notebook
  daftar-sumber    daftar sumber dalam satu notebook
  tanya            tanya-jawab lintas sumber dalam notebook, jawaban + kutipan sumber
  cari             cari kata kunci di seluruh sumber/catatan (tanpa memakai model AI)
  ringkasan        minta ringkasan seluruh sumber dalam satu notebook (memakai model AI)
  podcast-mulai    mulai membuat podcast audio dari isi notebook (perlu profil episode)
  podcast-status   cek status pembuatan podcast

Windows: pakai `python` atau `py` sebagai ganti `python3`. Tambah --json untuk hasil terstruktur.
"""
import argparse
import getpass
import json
import os
import re
import stat
import sys
import urllib.error
import urllib.parse
import urllib.request
import uuid

VERSI = "1.0.1"
SINI = os.path.dirname(os.path.abspath(__file__))
FOLDER_SKILL = os.path.dirname(SINI)
KUNCI_DEFAULT = os.path.join(os.path.expanduser("~"), ".komunitech", "open-notebook-kunci.txt")
URL_DEFAULT = "http://127.0.0.1:5055"

K_INPUT, K_FILE, K_KONEKSI, K_AUTH, K_TULIS, K_TAKPASTI = 2, 3, 4, 5, 6, 8


class Gagal(Exception):
    def __init__(self, pesan, kode=K_INPUT):
        super().__init__(pesan)
        self.kode = kode


# ============================================================ kata sandi lokal


def path_kunci(args):
    if args.kunci_file:
        return os.path.abspath(os.path.expanduser(args.kunci_file))
    return KUNCI_DEFAULT


def cek_izin_file(path):
    try:
        mode = stat.S_IMODE(os.stat(path).st_mode)
    except OSError:
        return
    if mode & (stat.S_IRWXG | stat.S_IRWXO):
        sys.stderr.write(
            f"PERINGATAN: file kunci {path} bisa dibaca pengguna lain di komputer ini. "
            f"Jalankan: chmod 600 {path}\n"
        )


def simpan_kunci(args):
    path = path_kunci(args)
    if os.path.exists(path) and not args.ya:
        raise Gagal(
            f"File kunci sudah ada: {path}\n"
            f"Untuk mengganti kata sandi lama, ulangi perintah ini dengan tambahan --ya.",
            K_FILE,
        )
    sys.stderr.write(f"Kata sandi akan disimpan di: {path}\n")
    sandi = getpass.getpass(
        "Tempel kata sandi API Open Notebook (OPEN_NOTEBOOK_PASSWORD, tidak terlihat), lalu Enter: "
    ).strip()
    if not sandi:
        raise Gagal("Kata sandi kosong, tidak disimpan.", K_INPUT)
    if re.search(r"\s", sandi):
        raise Gagal("Kata sandi berisi spasi/baris baru — kemungkinan tersalin rusak. Salin ulang.", K_INPUT)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        f.write(sandi + "\n")
    os.chmod(path, 0o600)
    print(f"Kata sandi tersimpan di {path} (izin 600).")
    return 0


def ambil_kunci(args):
    """Kembalikan kata sandi atau None (server tanpa kata sandi = mode tanpa auth)."""
    if args.kunci_file:
        if os.environ.get("OPEN_NOTEBOOK_TOKEN"):
            sys.stderr.write(
                "PERINGATAN: --kunci-file dipakai; ENV OPEN_NOTEBOOK_TOKEN DIABAIKAN.\n"
            )
        path = os.path.abspath(os.path.expanduser(args.kunci_file))
        return _baca_file_kunci(path, "--kunci-file", wajib=True)
    if os.environ.get("OPEN_NOTEBOOK_TOKEN"):
        return os.environ["OPEN_NOTEBOOK_TOKEN"].strip()
    if os.environ.get("OPEN_NOTEBOOK_TOKEN_FILE"):
        return _baca_file_kunci(os.environ["OPEN_NOTEBOOK_TOKEN_FILE"], "ENV OPEN_NOTEBOOK_TOKEN_FILE", wajib=True)
    return _baca_file_kunci(KUNCI_DEFAULT, "file kunci default", wajib=False)


def _baca_file_kunci(path, sumber, wajib):
    if not os.path.isfile(path):
        if wajib:
            raise Gagal(
                f"File kunci ({sumber}) tidak ditemukan: {path}. Jalankan dulu "
                f"'python3 notebook.py simpan-kunci' (lihat docs/panduan-open-notebook.md).",
                K_FILE,
            )
        return None
    cek_izin_file(path)
    sandi = open(path, encoding="utf-8").read().strip()
    if not sandi:
        return None
    if re.search(r"\s", sandi):
        raise Gagal(f"File kunci ({sumber}) berisi spasi/baris ganda — simpan ulang dengan 'simpan-kunci'.", K_FILE)
    return sandi


def tampilkan_kunci_tersamar(sandi):
    if len(sandi) <= 6:
        return "****"
    return sandi[:2] + "****" + sandi[-2:]


# ============================================================ HTTP ke Open Notebook


def periksa_url(url):
    u = urllib.parse.urlsplit(url)
    if u.scheme not in ("http", "https"):
        raise Gagal(f"URL Open Notebook tidak valid: {url}", K_INPUT)
    host = (u.hostname or "").lower()
    lokal = host in ("127.0.0.1", "localhost", "::1")
    if not lokal:
        raise Gagal(
            f"Alamat Open Notebook '{url}' bukan komputer ini (127.0.0.1/localhost). "
            f"Open Notebook TIDAK dirancang untuk dibuka ke internet/jaringan kantor — semua "
            f"dokumen dan isi tanya-jawab Anda bisa terbaca orang lain. Jalankan skill ini hanya "
            f"terhadap Open Notebook di komputer sendiri (lihat docs/panduan-open-notebook.md).",
            K_INPUT,
        )


def _kodekan_multipart(bidang):
    """Bangun body multipart/form-data manual (Python standar, tanpa paket luar).

    `bidang` adalah dict {nama: nilai}; nilai None dilewati (field opsional yang
    tidak diisi). Semua nilai dikirim sebagai teks (skill ini tidak mengunggah
    file lewat multipart — lihat 'tambah-sumber --tipe file' yang sengaja ditolak).
    """
    batas = "----KomunitechBatas" + uuid.uuid4().hex
    potongan = []
    for nama, nilai in bidang.items():
        if nilai is None:
            continue
        potongan.append(f"--{batas}\r\n".encode("utf-8"))
        potongan.append(f'Content-Disposition: form-data; name="{nama}"\r\n\r\n'.encode("utf-8"))
        potongan.append(str(nilai).encode("utf-8"))
        potongan.append(b"\r\n")
    potongan.append(f"--{batas}--\r\n".encode("utf-8"))
    return f"multipart/form-data; boundary={batas}", b"".join(potongan)


def panggil(method, path, args, sandi=None, body=None, multipart=None, timeout=None):
    periksa_url(args.url)
    timeout = timeout if timeout is not None else getattr(args, "timeout", 30)
    url = args.url.rstrip("/") + "/api" + path
    headers = {"Accept": "application/json"}
    if multipart is not None:
        content_type, data = _kodekan_multipart(multipart)
        headers["Content-Type"] = content_type
    else:
        data = json.dumps(body).encode("utf-8") if body is not None else None
        if data is not None:
            headers["Content-Type"] = "application/json"
    if sandi:
        headers["Authorization"] = f"Bearer {sandi}"
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            mentah = resp.read().decode("utf-8", errors="replace")
            return json.loads(mentah) if mentah.strip() else {}
    except urllib.error.HTTPError as e:
        mentah = e.read().decode("utf-8", errors="replace")
        try:
            detail = json.loads(mentah).get("detail", mentah)
        except (json.JSONDecodeError, AttributeError):
            detail = mentah or e.reason
        if e.code == 401:
            raise Gagal(
                "401 Unauthorized: kata sandi API salah/kosong, atau server ini memang butuh "
                "kata sandi tapi belum disimpan. Jalankan 'python3 notebook.py simpan-kunci', atau "
                "cek OPEN_NOTEBOOK_PASSWORD di server (docs/panduan-open-notebook.md).",
                K_AUTH,
            )
        if e.code == 404:
            raise Gagal(f"404: tidak ditemukan ({detail}). Cek id notebook/sumber dengan 'daftar-notebook'/'daftar-sumber'.", K_INPUT)
        if e.code == 400:
            raise Gagal(f"400: permintaan ditolak server ({detail}).", K_INPUT)
        if e.code == 422:
            raise Gagal(f"422: data yang dikirim tidak sesuai format yang diharapkan server ({detail}). Ini kemungkinan bug skill, bukan kesalahan Anda — laporkan ke Komunitech.", K_INPUT)
        if e.code >= 500:
            raise Gagal(f"{e.code}: server Open Notebook mengalami masalah internal ({detail}). Coba lagi sebentar lagi.", K_KONEKSI)
        raise Gagal(f"{e.code}: {detail}", K_INPUT)
    except urllib.error.URLError as e:
        raise Gagal(
            f"Tidak bisa dihubungi ke {args.url} ({e.reason}). Open Notebook mati, atau "
            f"belum jalan di alamat ini. Jalankan Docker Desktop lalu 'docker compose up -d' "
            f"di folder Open Notebook, tunggu ~20 detik, coba lagi (docs/panduan-open-notebook.md).",
            K_KONEKSI,
        )
    except TimeoutError:
        raise Gagal(f"Tidak ada balasan dari {args.url} dalam {timeout} detik (server sibuk/model AI lambat). Coba lagi, atau naikkan --timeout.", K_KONEKSI)
    except json.JSONDecodeError:
        raise Gagal("Balasan server bukan JSON yang valid — kemungkinan alamat --url salah (bukan Open Notebook).", K_KONEKSI)


# ============================================================ perintah


def cmd_cek(args):
    status = panggil("GET", "/auth/status", args)
    auth_aktif = bool(status.get("auth_enabled"))
    sandi = ambil_kunci_aman(args)
    hasil = {"url": args.url, "auth_aktif": auth_aktif}
    if auth_aktif and not sandi:
        raise Gagal(
            "Server ini butuh kata sandi (OPEN_NOTEBOOK_PASSWORD aktif), tapi belum tersimpan di "
            "komputer ini. Jalankan 'python3 notebook.py simpan-kunci'.",
            K_AUTH,
        )
    # Uji baca ringan agar 401 (sandi salah) ketahuan di sini, bukan nanti.
    nb = panggil("GET", "/notebooks", args, sandi=sandi)
    hasil["jumlah_notebook"] = len(nb)
    hasil["kata_sandi"] = tampilkan_kunci_tersamar(sandi) if sandi else "(tidak dipakai)"
    hasil["pesan"] = "Open Notebook bisa dihubungi dan siap dipakai."
    return hasil


def ambil_kunci_aman(args):
    """Seperti ambil_kunci, tapi tidak error bila file kunci default belum ada (server bisa tanpa sandi)."""
    try:
        return ambil_kunci(args)
    except Gagal as g:
        if g.kode == K_FILE and not args.kunci_file and not os.environ.get("OPEN_NOTEBOOK_TOKEN") and not os.environ.get("OPEN_NOTEBOOK_TOKEN_FILE"):
            return None
        raise


def cmd_daftar_notebook(args):
    sandi = ambil_kunci_aman(args)
    data = panggil("GET", "/notebooks", args, sandi=sandi)
    baris = [
        {
            "id": n.get("id"),
            "nama": n.get("name"),
            "deskripsi": n.get("description") or "",
            "jumlah_sumber": n.get("source_count", 0),
            "jumlah_catatan": n.get("note_count", 0),
            "diarsip": bool(n.get("archived")),
        }
        for n in data
    ]
    return {"jumlah": len(baris), "notebook": baris}


def cmd_buat_notebook(args):
    sandi = ambil_kunci_aman(args)
    if not args.ya:
        return {
            "pratinjau": True,
            "aksi": "Akan membuat notebook baru",
            "nama": args.nama,
            "deskripsi": args.deskripsi or "",
            "catatan": "Tambahkan --ya untuk benar-benar membuat.",
        }
    body = {"name": args.nama, "description": args.deskripsi or ""}
    hasil = panggil("POST", "/notebooks", args, sandi=sandi, body=body)
    return {"dibuat": True, "id": hasil.get("id"), "nama": hasil.get("name")}


def _cari_notebook_id(args, sandi, sebutan):
    """Terima id langsung (format id Open Notebook, mis. 'notebook:xxxx') atau nama -> cari id."""
    if ":" in sebutan:
        return sebutan
    data = panggil("GET", "/notebooks", args, sandi=sandi)
    cocok = [n for n in data if (n.get("name") or "").strip().lower() == sebutan.strip().lower()]
    if not cocok:
        mirip = [n.get("name") for n in data if sebutan.strip().lower() in (n.get("name") or "").lower()]
        raise Gagal(
            f"Notebook '{sebutan}' tidak ditemukan. " +
            (f"Mungkin maksud Anda: {', '.join(mirip)}." if mirip else "Jalankan 'daftar-notebook' untuk melihat nama yang ada."),
            K_INPUT,
        )
    if len(cocok) > 1:
        raise Gagal(f"Nama '{sebutan}' cocok lebih dari satu notebook. Pakai id (dari 'daftar-notebook').", K_INPUT)
    return cocok[0]["id"]


def cmd_tambah_sumber(args):
    # PENTING: POST /api/sources di Open Notebook 1.14.0 HANYA menerima
    # multipart/form-data (dependency FastAPI `parse_source_form_data` mendeklarasikan
    # semua field lewat Form(...), bukan model Pydantic biasa lewat body JSON).
    # Dibuktikan lewat uji terhadap server asli (bukan tiruan): mengirim JSON selalu
    # dibalas 422 "Field required", sedangkan multipart/form-data berhasil (200 OK).
    # Lihat ATTRIBUTION.md & examples/03-... untuk bukti dan riwayat perbaikannya.
    sandi = ambil_kunci_aman(args)
    notebook_id = _cari_notebook_id(args, sandi, args.notebook)
    tipe = args.tipe
    bidang = {"notebooks": json.dumps([notebook_id]), "async_processing": "true"}
    pratinjau_tampil = {"notebooks": [notebook_id]}
    if tipe == "link":
        if not args.sumber_url:
            raise Gagal("Tipe 'link' butuh --sumber-url.", K_INPUT)
        bidang["type"] = "link"
        bidang["url"] = args.sumber_url
        pratinjau_tampil.update(type="link", url=args.sumber_url)
    elif tipe == "teks":
        if not args.teks:
            raise Gagal("Tipe 'teks' butuh --teks (atau --file - untuk baca dari input).", K_INPUT)
        bidang["type"] = "text"
        bidang["content"] = args.teks
        pratinjau_tampil.update(type="text", content=args.teks)
        if args.judul:
            bidang["title"] = args.judul
            pratinjau_tampil["title"] = args.judul
    elif tipe == "file":
        raise Gagal(
            "Unggah file (PDF/Word/dll.) lewat perintah ini belum didukung skill ini — server "
            "membutuhkan alamat file di KOMPUTER SERVER (bukan komputer Anda bila beda mesin), "
            "dan validasi path itu rumit untuk dijamin aman lewat sekadar argumen baris perintah. "
            "Seret file itu ke tampilan web Open Notebook (http://127.0.0.1:8502) untuk sekarang.",
            K_TAKPASTI,
        )
    else:
        raise Gagal("--tipe harus 'link' atau 'teks'.", K_INPUT)

    if not args.ya:
        return {
            "pratinjau": True,
            "aksi": "Akan menambah sumber ke notebook",
            "notebook_id": notebook_id,
            "sumber": pratinjau_tampil,
            "catatan": "Tambahkan --ya untuk benar-benar menambah. Pemrosesan (baca isi, ringkas) berjalan di latar belakang; cek dengan 'daftar-sumber'.",
        }
    hasil = panggil("POST", "/sources", args, sandi=sandi, multipart=bidang, timeout=getattr(args, "timeout", 30))
    return {
        "ditambahkan": True,
        "id": hasil.get("id"),
        "judul": hasil.get("title"),
        "status": hasil.get("status") or "diproses",
        "catatan": "Sumber sedang diproses (dibaca & diindeks). Cek 'daftar-sumber' beberapa saat lagi bila judul/isi belum lengkap.",
    }


def cmd_daftar_sumber(args):
    sandi = ambil_kunci_aman(args)
    notebook_id = _cari_notebook_id(args, sandi, args.notebook)
    q = "?" + urllib.parse.urlencode({"notebook_id": notebook_id})
    data = panggil("GET", f"/sources{q}", args, sandi=sandi)
    baris = [
        {
            "id": s.get("id"),
            "judul": s.get("title") or "(belum ada judul, masih diproses)",
            "status": s.get("status") or ("siap" if s.get("embedded") else "diproses"),
            "jumlah_bagian_terindeks": s.get("embedded_chunks", 0),
            "jumlah_insight": s.get("insights_count", 0),
        }
        for s in data
    ]
    return {"notebook_id": notebook_id, "jumlah": len(baris), "sumber": baris}


def _model_chat_default(args, sandi):
    d = panggil("GET", "/models/defaults", args, sandi=sandi)
    m = d.get("default_chat_model")
    if not m:
        raise Gagal(
            "Belum ada model AI default yang diatur di Open Notebook (mis. Ollama lokal atau "
            "kunci API OpenAI/Anthropic). Buka http://127.0.0.1:8502 > Settings > Models, tambah "
            "minimal satu model bahasa, lalu jadikan default sebelum memakai 'tanya'/'ringkasan'.",
            K_TAKPASTI,
        )
    return m


def cmd_tanya(args):
    sandi = ambil_kunci_aman(args)
    notebook_id = _cari_notebook_id(args, sandi, args.notebook) if args.notebook else None
    model = args.model or _model_chat_default(args, sandi)
    body = {
        "question": args.pertanyaan,
        "strategy_model": model,
        "answer_model": model,
        "final_answer_model": model,
    }
    if notebook_id:
        body["notebook_id"] = notebook_id
    hasil = panggil("POST", "/search/ask/simple", args, sandi=sandi, body=body, timeout=getattr(args, "timeout", 120))
    return {
        "pertanyaan": hasil.get("question", args.pertanyaan),
        "jawaban": hasil.get("answer", ""),
        "catatan": "Jawaban disusun model AI dari sumber di notebook Anda. Selalu periksa ulang isi penting (regulasi, angka, kutipan) di sumber aslinya lewat 'daftar-sumber'/'cari' sebelum dipakai.",
    }


def cmd_ringkasan(args):
    args.pertanyaan = (
        "Ringkas seluruh sumber di notebook ini dalam bahasa Indonesia yang jelas: poin-poin utama, "
        "lalu bila ada, angka/tanggal/aturan penting yang disebutkan. Sebutkan judul sumber untuk tiap poin."
    )
    hasil = cmd_tanya(args)
    hasil["catatan"] = "Ringkasan otomatis dari model AI, bukan pengganti membaca dokumen aslinya untuk keputusan penting (hukum/pajak/kontrak)."
    return hasil


def cmd_cari(args):
    sandi = ambil_kunci_aman(args)
    body = {"query": args.kueri, "type": "text", "limit": args.batas}
    if args.notebook:
        body["notebook_id"] = _cari_notebook_id(args, sandi, args.notebook)
    hasil = panggil("POST", "/search", args, sandi=sandi, body=body)
    # PENTING: hasil POST /api/search (versi 1.14.0) hanya berisi field
    # id/parent_id/relevance/title — TIDAK ada tipe sumber atau cuplikan kalimat
    # yang cocok (dibuktikan terhadap server asli, lihat ATTRIBUTION.md &
    # examples/04-...). Skill ini menampilkan apa adanya, tidak berpura-pura
    # punya cuplikan yang sebenarnya tidak tersedia dari API.
    hasil_ringkas = [
        {
            "judul": r.get("title") or "(tanpa judul)",
            "id_dokumen": r.get("parent_id") or r.get("id"),
            "relevansi": round(r["relevance"], 3) if isinstance(r.get("relevance"), (int, float)) else None,
        }
        for r in hasil.get("results", [])
    ]
    return {
        "kueri": args.kueri,
        "jumlah": hasil.get("total_count", 0),
        "hasil": hasil_ringkas,
        "catatan": "API pencarian Open Notebook tidak menyediakan cuplikan kalimat yang cocok — hanya judul & id dokumen. Buka dokumennya lewat 'daftar-sumber' atau http://127.0.0.1:8502 untuk melihat isinya.",
    }


def cmd_podcast_mulai(args):
    sandi = ambil_kunci_aman(args)
    notebook_id = _cari_notebook_id(args, sandi, args.notebook)
    if not args.ya:
        return {
            "pratinjau": True,
            "aksi": "Akan mulai membuat podcast audio",
            "notebook_id": notebook_id,
            "profil_episode": args.profil,
            "profil_pembicara": args.pembicara,
            "nama_episode": args.nama_episode,
            "catatan": "Profil episode & pembicara HARUS sudah dibuat lebih dulu di http://127.0.0.1:8502 "
                       "(Settings > Podcasts) — mengatur suara TTS dan gaya percakapan tidak didukung lewat "
                       "skill ini. Butuh model text-to-speech terpasang (opsional, bisa berbayar tergantung "
                       "provider yang dipilih). Tambahkan --ya untuk benar-benar mulai.",
        }
    body = {
        "episode_profile": args.profil,
        "speaker_profile": args.pembicara,
        "episode_name": args.nama_episode,
        "notebook_id": notebook_id,
    }
    hasil = panggil("POST", "/podcasts/generate", args, sandi=sandi, body=body, timeout=getattr(args, "timeout", 30))
    return {
        "dimulai": True,
        "job_id": hasil.get("job_id"),
        "status": hasil.get("status"),
        "catatan": "Pembuatan podcast berjalan di latar belakang (bisa beberapa menit). Cek dengan 'podcast-status --id <job_id>'.",
    }


def cmd_podcast_status(args):
    sandi = ambil_kunci_aman(args)
    hasil = panggil("GET", f"/podcasts/jobs/{urllib.parse.quote(args.id)}", args, sandi=sandi)
    return hasil


# ============================================================ CLI


def cetak(hasil, args):
    if args.json:
        print(json.dumps(hasil, ensure_ascii=False, indent=2))
        return
    if isinstance(hasil, dict) and hasil.get("pratinjau"):
        print(f"[PRATINJAU - belum dikirim] {hasil['aksi']}")
        for k, v in hasil.items():
            if k in ("pratinjau", "aksi"):
                continue
            print(f"  {k}: {v}")
        return
    print(json.dumps(hasil, ensure_ascii=False, indent=2))


def _tambah_opsi_umum(p):
    p.add_argument("--url", default=os.environ.get("OPEN_NOTEBOOK_URL", URL_DEFAULT))
    p.add_argument("--kunci-file", dest="kunci_file", default=None)
    p.add_argument("--json", action="store_true")
    p.add_argument("--timeout", type=float, default=30)
    p.add_argument("--ya", action="store_true")


def buat_parser():
    p = argparse.ArgumentParser(prog="notebook.py", description="Asisten Open Notebook lokal (Komunitech)")
    p.add_argument("--versi", action="version", version=f"notebook-riset-lokal {VERSI}")
    sub = p.add_subparsers(dest="perintah", required=True)

    sp = sub.add_parser("simpan-kunci", help="simpan kata sandi API ke file lokal")
    _tambah_opsi_umum(sp)

    sp = sub.add_parser("cek", help="cek server bisa dihubungi")
    _tambah_opsi_umum(sp)

    sp = sub.add_parser("daftar-notebook", help="daftar notebook yang ada")
    _tambah_opsi_umum(sp)

    sp = sub.add_parser("buat-notebook", help="buat notebook baru")
    sp.add_argument("--nama", required=True)
    sp.add_argument("--deskripsi", default="")
    _tambah_opsi_umum(sp)

    sp = sub.add_parser("tambah-sumber", help="tambah sumber ke notebook")
    sp.add_argument("--notebook", required=True, help="nama atau id notebook")
    sp.add_argument("--tipe", required=True, choices=["link", "teks", "file"])
    sp.add_argument("--sumber-url", dest="sumber_url", default=None, help="alamat web (tipe link)")
    sp.add_argument("--teks", default=None, help="isi teks (tipe teks)")
    sp.add_argument("--judul", default=None)
    _tambah_opsi_umum(sp)

    sp = sub.add_parser("daftar-sumber", help="daftar sumber dalam satu notebook")
    sp.add_argument("--notebook", required=True)
    _tambah_opsi_umum(sp)

    sp = sub.add_parser("tanya", help="tanya-jawab dengan sumber di notebook")
    sp.add_argument("--notebook", default=None, help="kosongkan untuk cari di semua notebook")
    sp.add_argument("--pertanyaan", required=True)
    sp.add_argument("--model", default=None, help="id model AI (default: model chat default di Open Notebook)")
    _tambah_opsi_umum(sp)

    sp = sub.add_parser("ringkasan", help="ringkas seluruh sumber dalam satu notebook")
    sp.add_argument("--notebook", required=True)
    sp.add_argument("--model", default=None)
    _tambah_opsi_umum(sp)

    sp = sub.add_parser("cari", help="cari kata kunci (tanpa model AI)")
    sp.add_argument("--kueri", required=True)
    sp.add_argument("--notebook", default=None)
    sp.add_argument("--batas", type=int, default=20)
    _tambah_opsi_umum(sp)

    sp = sub.add_parser("podcast-mulai", help="mulai membuat podcast audio dari notebook")
    sp.add_argument("--notebook", required=True)
    sp.add_argument("--profil", required=True, help="nama profil episode (sudah dibuat di Open Notebook)")
    sp.add_argument("--pembicara", required=True, help="nama profil pembicara (sudah dibuat di Open Notebook)")
    sp.add_argument("--nama-episode", dest="nama_episode", required=True)
    _tambah_opsi_umum(sp)

    sp = sub.add_parser("podcast-status", help="cek status pembuatan podcast")
    sp.add_argument("--id", required=True, help="job_id dari podcast-mulai")
    _tambah_opsi_umum(sp)

    return p


def main(argv=None):
    parser = buat_parser()
    args = parser.parse_args(argv)
    try:
        if args.perintah == "simpan-kunci":
            return simpan_kunci(args)
        fungsi = {
            "cek": cmd_cek,
            "daftar-notebook": cmd_daftar_notebook,
            "buat-notebook": cmd_buat_notebook,
            "tambah-sumber": cmd_tambah_sumber,
            "daftar-sumber": cmd_daftar_sumber,
            "tanya": cmd_tanya,
            "ringkasan": cmd_ringkasan,
            "cari": cmd_cari,
            "podcast-mulai": cmd_podcast_mulai,
            "podcast-status": cmd_podcast_status,
        }[args.perintah]
        hasil = fungsi(args)
        cetak(hasil, args)
        return 0
    except Gagal as g:
        if args.json:
            print(json.dumps({"galat": str(g)}, ensure_ascii=False))
        else:
            sys.stderr.write(f"GALAT: {g}\n")
        return g.kode
    except KeyboardInterrupt:
        sys.stderr.write("\nDibatalkan.\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
