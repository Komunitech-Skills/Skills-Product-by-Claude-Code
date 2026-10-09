import os,json,subprocess,time
tok=os.environ['bot_token']; C='-1004407409583'
sk=['rapikan-data-berantakan','aktifkan-kembali-pelanggan','triase-keluhan-pelanggan','tangani-keberatan-pelanggan','kelayakan-investasi-usaha']
m={}
for n in sk:
  for sisi,lab in (('sebelum','TANPA skill'),('sesudah','DENGAN skill')):
    for a in range(4):
      r=subprocess.run(['curl','-s','-X','POST',f'https://api.telegram.org/bot{tok}/createForumTopic','--data-urlencode',f'chat_id={C}','--data-urlencode',f'name=G11 {n} — {lab}'],capture_output=True,text=True)
      if r.stdout.strip(): break
      time.sleep(3)
    d=json.loads(r.stdout) if r.stdout.strip() else {}
    if d.get('ok'): m[f'{n}|{sisi}']=d['result']['message_thread_id']
    else: print('FAIL',n,sisi,d.get('description'))
    time.sleep(1.5)
json.dump(m,open('topik-g11.json','w'),indent=1); print(m)
