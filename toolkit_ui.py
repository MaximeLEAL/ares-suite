# toolkit_ui.py — helpers partagés (write_file, ask)
import os, textwrap
from colorama import Fore, Style, init
init(autoreset=True)

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
