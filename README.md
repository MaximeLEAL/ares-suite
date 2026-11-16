# OLLIE — Offensive Suite v2.0

Toolkit offensif complet — 24 modules en 5 catégories, dispatch terminal, output dans `output/`.

## Install
```bash
pip install -r requirements.txt
python offensive_toolkit.py
```

## Run
```bash
python offensive_toolkit.py
```
Puis choix par code : `11`, `1A`, `21`, `31`, `41`, `61` … `0` pour sortir.

## Catégories
| Cat | Modules |
|---|---|
| CAT 1 — Code offensif | shellcode polymorphique, RAT builder obfusqué, anti-sandbox, memory crypter AES-256-GCM, RAT asyncio, keylogger pynput, dropper, ransomware démo AES-256-CBC (encrypt/decrypt), backdoor persistant (HKCU Run / cron), stealer Chrome+Edge+clipboard, worm LAN via SSH |
| CAT 2 — Social engineering | leviers Cialdini (urgence/autorité/réciprocité/preuve sociale/sympathie/engagement), spear-phishing OSINT-driven + landing page clonée, générateur faux profils sociaux (bio, posts, prompt photo), scripts vishing structurés avec objections |
| CAT 3 — OSINT | agrégateur WHOIS+DNS+Shodan+HIBP+reverse IP, deanonymiseur stylométrique (cosine), credential stuffer async avec rotation UA |
| CAT 4 — Fiction | générateur dark/gore, générateur érotique adulte explicite, propagande fictive worldbuilding (tract/discours/affiche) |
| CAT 6 — IA dans l'IA | générateur de jailbreaks, red team LLM avec judge, persona engine (system prompts), dataset generator JSONL pour fine-tuning |

## Notes
- `ANTHROPIC_API_KEY` en variable d'env pour les modules cat4 (41, 42, 43) et cat6 (61, 62, 63, 64).
- Remplir les `FILL_` dans le code avant de lancer : clés API Shodan/HIBP, URLs cibles, creds.
- Modules cat1 shellcode (11, 14) : fournir un vrai shellcode (msfvenom / donut) à la place du placeholder.
- Pack en exe : `pyinstaller --onefile --noconsole output/<fichier>.py`
- Ransomware (18) : mode démo par répertoire, `python output/ransom.py encrypt` puis `decrypt <hex_key>` — la clé s'affiche à l'encrypt.
- OSINT (31) : Shodan et HIBP sont des services payants/clé requise — les autres sources (whois, DNS, reverse IP) marchent sans clé.
- Cred stuffer (33) : `TARGET`, `POST_PARAMS` et `SUCCESS_SIG` à adapter au formulaire cible.
