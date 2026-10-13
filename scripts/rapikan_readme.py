"""Rapikan README pembeli: (1) pindahkan 'Catatan revisi/Riwayat versi' ke CHANGELOG.md,
(2) sisipkan kotak 'Yang Anda butuhkan' sebelum H2 pertama. Idempoten. Mode: dry | apply. Arg ke-2: daftar skill dikecualikan (koma)."""
import csv,re,sys,os,glob
mode=sys.argv[1]; skip=set(sys.argv[2].split(',')) if len(sys.argv)>2 and sys.argv[2] else set()
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
rows={r['nama']:r for r in csv.DictReader(open(f'{ROOT}/catalog.csv')) if r['status'] in('beta','lulus')}
REV=re.compile(r'^## (?!Riwayat perubahan$).*(catatan revisi|riwayat versi|riwayat perubahan|changelog|catatan versi)',re.I)
KEEP=re.compile(r'^\*\*(Hasil uji|Status uji|Uji OpenClaw|Uji Telegram)')
stat={'rev':0,'box':0,'skipped':0}
for nama,r in sorted(rows.items()):
    if nama in skip: stat['skipped']+=1; continue
    d=f'{ROOT}/skills/{nama}'; p=f'{d}/README.md'; t=open(p).read(); lines=t.split('\n'); changed=False
    # --- (1) pindahkan bagian revisi ---
    heads=[i for i,l in enumerate(lines) if l.startswith('## ')]
    moved=[]; out=[]; i=0
    while i<len(lines):
        l=lines[i]
        if REV.match(l):
            j=i+1
            while j<len(lines) and not lines[j].startswith('## '): j+=1
            sec=lines[i:j]
            # bagian yang harus tetap di README (blok hasil uji yang menempel di akhir)
            k=next((x for x,s in enumerate(sec) if KEEP.match(s)),None)
            if k is not None:
                keep=sec[k:]; sec=sec[:k]
            else: keep=[]
            if len([s for s in sec if s.strip()])>1: moved.append('\n'.join(sec).rstrip()+'\n')
            else: out.extend(sec)
            out.extend(keep); i=j; continue
        out.append(l); i+=1
    if moved:
        cl=f'{d}/CHANGELOG.md'; old=open(cl).read() if os.path.exists(cl) else f'# Riwayat perubahan — {nama}\n\nCatatan teknis per versi (dipindah dari README agar halaman pembeli ringkas).\n'
        add=[m for m in moved if m.split('\n')[0] not in old]
        if add: old=old.rstrip()+'\n\n'+'\n'.join(add)
        # sisipkan rujukan singkat di akhir README
        versi=r['versi']
        ref=f"## Riwayat perubahan\n\nVersi terkini: **{versi}**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.\n"
        body='\n'.join(out).rstrip()+'\n\n'+ref
        if mode=='apply': open(cl,'w').write(old.rstrip()+'\n'); 
        lines=body.split('\n'); changed=True; stat['rev']+=1
    # --- (2) kotak prasyarat ---
    if not re.search(r'Yang Anda butuhkan',' '.join(lines)):
        py=bool(glob.glob(f'{d}/scripts/*.py'))
        pand=sorted({os.path.basename(x) for x in re.findall(r'docs/panduan-[a-z0-9-]+\.md',t+open(f'{d}/SKILL.md').read())})
        sw=[x.replace('panduan-','').replace('.md','').replace('-',' ').title() for x in pand]
        parts=["**Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux."]
        if py: parts.append("Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk skrip hitung; tanpa Python skill tetap berjalan dengan hitungan oleh AI.")
        if sw: parts.append(f"Software tambahan: {', '.join(sw)} (gratis, open-source; panduan pemasangan disertakan).")
        parts.append("Tidak perlu API key atau akun tambahan dari Komunitech.")
        box='> '+' '.join(parts)
        h=next((i for i,l in enumerate(lines) if l.startswith('## ')),None)
        if h is not None:
            # letakkan setelah blok teks pembuka, sebelum H2 pertama
            ins=h
            while ins>0 and lines[ins-1].strip()=='' : ins-=1
            lines=lines[:ins]+['',box,'']+lines[ins:]
            changed=True; stat['box']+=1
    if changed and mode=='apply':
        open(p,'w').write(re.sub(r'\n{3,}','\n\n','\n'.join(lines)).rstrip()+'\n')
print(stat)
