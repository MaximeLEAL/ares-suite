# ARES — Suite offensive de la mythologie grecque

24 modules — 5 phalanges — 100% offline, zéro clé API requise.
Chaque module porte un nom de la mythologie grecque, choisi pour sa fonction.

## Install
```bash
pip install -r requirements.txt
python ares_toolkit.py
```

## Run
```bash
python ares_toolkit.py
```
L'intro mythologique joue au lancement (temple qui s'élève, éclair de Zeus, laurier, titre doré). Choix par code : `11`, `1A`, `21`, `31`, `41`, `61` … `0` quitte l'Arène.

## La panthéon

### PHALANGE I — Code offensif
| Code | Nom | Rôle mythologique | Fonction |
|---|---|---|---|
| 11 | **Proteus** | le polymorphe, prend toutes les formes | shellcode polymorphique (XOR + stub vars randomisées) |
| 12 | **Dedale** | le labyrinthe | RAT builder + obfuscation auto (vars, b64, imports) |
| 13 | **Sphinx** | l'énigme qui teste | payload anti-sandbox (registry/processes/timing/mouse/RAM) |
| 14 | **Hades** | l'invisible | memory crypter AES-256-GCM, déchiffrement en RAM |
| 15 | **Hermes** | le messager | RAT asyncio reverse shell, reconnect loop |
| 16 | **Argos** | les cent yeux | keylogger pynput, buffer + flush |
| 17 | **Prometheus** | le porteur de feu | dropper, télécharge + exécute second stage |
| 18 | **Charon** | passe ou péris | ransomware démo AES-256-CBC (encrypt/decrypt local) |
| 19 | **Atlas** | porte le monde sans fin | backdoor persistant (HKCU Run / cron @reboot) |
| 1A | **Kerberos** | le gardien qui prend | stealer Chrome/Edge logins + clipboard |
| 1B | **Hydra** | repousse à chaque coup | worm LAN spreader (scan /24, SSH) |

### PHALANGE II — Social engineering
| Code | Nom | Rôle | Fonction |
|---|---|---|---|
| 21 | **Metis** | la ruse, la conseillère rusée | 6 leviers Cialdini + templates |
| 22 | **Syrenes** | le chant qui attire | spear-phishing OSINT + landing page clonée |
| 23 | **Chimera** | le faux corps | faux profils sociaux (bio, posts, prompt photo) |
| 24 | **Echo** | la voix | scripts vishing structurés avec objections |

### PHALANGE III — OSINT
| Code | Nom | Rôle | Fonction |
|---|---|---|---|
| 31 | **Panoptes** | voit tout | agrégateur WHOIS + DNS + Shodan + HIBP + reverse IP |
| 32 | **Moires** | elles lisent le fil | deanonymiseur stylométrique (cosine) |
| 33 | **Heracles** | la force brute | credential stuffer async, rotation UA |

### PHALANGE IV — Fiction non censurée
| Code | Nom | Rôle | Fonction |
|---|---|---|---|
| 41 | **Erinyes** | les Furies | fiction dark/gore générée localement |
| 42 | **Aphrodite** | la déesse | érotique adulte explicite, moteur local |
| 43 | **Sibylle** | la prophétesse | propagande fictive worldbuilding |

### PHALANGE VI — IA dans l'IA
| Code | Nom | Rôle | Fonction |
|---|---|---|---|
| 61 | **Icare** | défie les limites | générateur de jailbreaks LLM (8 techniques) |
| 62 | **Athena** | la stratégie | red team LLM + juge (mode mock ou HTTP) |
| 63 | **Pygmalion** | le sculpteur | persona engine — system prompts composés |
| 64 | **Muses** | les neuf sources | dataset generator JSONL pour fine-tuning |

## Le compromis API — tout fonctionne offline

Aucune clé API n'est requise :

- **cat4 + cat6** : moteurs locaux (pools seedés, templates, expansions programmatiques). Pas d'appel réseau du tout — `Erinyes`, `Aphrodite`, `Sibylle`, `Icare`, `Athena`, `Pygmalion`, `Muses` tournent sur la machine, sortent des fichiers.
- **Panoptes (31)** : WHOIS, DNS et reverse-IP fonctionnent sans clé. Shodan et HIBP deviennent **optionnels** — si la clé est absente, le module continue avec les sources libres et le signale proprement.
- **Athena (62)** : mode `mock` par défaut (LLM simulé, chaîne complète offline). Passer en `--mode http --url … --key …` seulement si un endpoint OpenAI-compatible est disponible.

## Testé

Les 24 modules générés compilent (py_compile 24/24). Testé en exécution : Athena (8 payloads, juge local), Muses (JSONL + JSON), Erinyes + Aphrodite (scènes seedées), Icare (prompt + variantes), Pygmalion (system prompt), Syrenes (spear email + landing), Dedale (RAT obfusqué généré), Metis, Echo, Chimera, Moires, Panoptes, Proteus, Hades. Les modules Windows-only (Argos hooks, Kerberos DPAPI, Atlas winreg, Hydra SSH) compilent et génèrent — ils s'exécutent sur une cible Windows.

## Notes
- Modules cat1 shellcode (11, 14) : coller un vrai shellcode (msfvenom / donut) à la place du placeholder `DEMO_SC`.
- Pack en exe : `pyinstaller --onefile --noconsole output/<module>.py`
- Charon (18) : `python output/charon.py encrypt` sur un dossier de test, clé affichée, `decrypt <hex_key>` pour revenir.
