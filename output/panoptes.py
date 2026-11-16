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
    