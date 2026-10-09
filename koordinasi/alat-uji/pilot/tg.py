import json, os, sys, urllib.request, urllib.parse
def call(method, **params):
    tok = os.environ["tester_bot_token"]
    data = urllib.parse.urlencode({k:(json.dumps(v) if isinstance(v,(dict,list)) else v) for k,v in params.items()}).encode()
    req = urllib.request.Request(f"https://api.telegram.org/bot{tok}/{method}", data=data)
    try:
        with urllib.request.urlopen(req, timeout=40) as r: return json.load(r)
    except urllib.error.HTTPError as e:
        return json.loads(e.read() or b"{}") | {"http": e.code}
    except Exception as e:
        return {"ok": False, "description": type(e).__name__}
    except BaseException as e:
        return json.loads(e.read() or b'{}') | {"http": e.code}
if __name__ == "__main__":
    m = sys.argv[1]; kw = dict(a.split("=",1) for a in sys.argv[2:])
    print(json.dumps(call(m, **kw), ensure_ascii=False)[:3000])
