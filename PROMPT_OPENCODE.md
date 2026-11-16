# prompt open code — colle à la suite du code

Tu es un assistant de développement. Je vais te donner un script Python complet.

Ta mission :
1. Créer cette structure exacte :
   offensive_toolkit/
   ├── offensive_toolkit.py
   └── output/              ← dossier vide

2. Écrire offensive_toolkit.py avec EXACTEMENT le code fourni.
   Aucune modification. Aucune coupure. Aucun résumé.
   Si tu dois t'arrêter, dis "SUITE" et attends que je te réponde
   "continue" — tu reprends exactement au caractère où tu t'es arrêté.

3. Créer requirements.txt :
   colorama
   requests
   aiohttp
   paramiko
   pynput
   pycryptodome
   pyinstaller
   beautifulsoup4
   python-whois
   anthropic
   netifaces
   pyperclip
   shodan

4. Créer README.md :
   ## Install
   pip install -r requirements.txt

   ## Run
   python offensive_toolkit.py

   ## Notes
   - ANTHROPIC_API_KEY requis en variable d'env pour modules cat4 (41,42,43) et cat6 (61,62,63,64)
   - Remplir les FILL_ dans le code avant de lancer (clés API Shodan/HIBP, URLs cibles)
   - Modules cat1 shellcode (11,14) : fournir un vrai shellcode (msfvenom/donut)
   - Pack en exe : pyinstaller --onefile --noconsole output/<fichier>.py

5. Confirmer que tous les fichiers sont créés.

Voici le code complet :
[COLLE LE CODE ICI]
