# mythos.py — animation d'intro mythologique grecque pour ARES
# temple qui s'élève, éclair de Zeus, laurier, titre doré, méandre
# stdlib only — appelé par ares_toolkit.py au lancement
import os, sys, time, random, shutil

def _c(code): return f"\033[{code}m"
GOLD = _c("93"); MARBLE = _c("97"); RED = _c("91"); CYAN = _c("96")
DIM = _c("90"); X = _c("0"); B = _c("1"); FLASH_BG = _c("107")

def clear():
    sys.stdout.write("\033[2J\033[3J\033[H"); sys.stdout.flush()

def width(): return shutil.get_terminal_size().columns
def height(): return shutil.get_terminal_size().lines

def meander(n):
    """frise grecque — motif méandre"""
    unit = "⊔⊓"
    return (unit * (n // 2))[:n]

def frame(text, color=GOLD):
    w = max(width() - 4, len(text) + 10)
    bar = meander(w)
    print(f"{DIM}{bar}{X}")
    print(f"{color}{B}{text.center(w)}{X}")
    print(f"{DIM}{bar}{X}")

def lightning_bolt(color=GOLD):
    """l'éclair de Zeus se dessine du haut de l'écran jusqu'au sol"""
    cols, rows = width(), height()
    cx = cols // 2
    bolt = [(0, 0, "╲"), (1, 1, "╲"), (2, 2, "╱"), (1, 3, "╱"),
            (0, 4, "╲"), (1, 5, "╲"), (-1, 6, "╱"), (0, 7, "╲"),
            (2, 8, "╲"), (1, 9, "╱"), (0, 10, "⚡")]
    top = 2
    for i, (dx, dy, ch) in enumerate(bolt):
        sys.stdout.write("\033[H")
        for r in range(dy):
            print()
        line = " " * max(0, cx + dx - 1)
        for j in range(i + 1):
            ddx, ddy, cch = bolt[j]
            if ddy == dy or j == i:
                line += (GOLD + B + cch if j == i else "  ")
        print(line)
        time.sleep(0.06)

def temple_rise():
    """le temple s'élève : les colonnes poussent du sol au fronton"""
    cols = width()
    COL = """    ╔══╗      ╔══╗      ╔══╗      ╔══╗
    ║  ║      ║  ║      ║  ║      ║  ║
    ║  ║      ║  ║      ║  ║      ║  ║
   ╔╧══╧╗    ╔╧══╧╗    ╔╧══╧╗    ╔╧══╧╗
  ╔╧════╧╗  ╔╧════╧╗  ╔╧════╧╗  ╔╧════╧╗
 ╔╧══════╧╗╔╧══════╧╗╔╧══════╧╗╔╧══════╧╗"""
    lines = COL.split("\n")
    print()
    for ln in lines:
        print(MARBLE + ln + X)
        time.sleep(0.18)
    print(DIM + "    —— OLYMPE, SOMMET DE L'ARÈTE ——" + X)
    time.sleep(0.4)

def laurel():
    """couronne de laurier qui se dessine autour du titre"""
    L = r"""
        ,@@@@@@@@@,
     @@@@@@@@@@@@@@@@@@@
    @@@@@@@@@@@@@@@@@@@@@@@
   @@@@ ϟ  A R E S  ϟ @@@@
    @@@@@@@@@@@@@@@@@@@@@@@
     @@@@@@@@@@@@@@@@@@@
        '@@@@@@@@@'
    """
    for ln in L.split("\n"):
        print(GOLD + ln + X)
        time.sleep(0.08)

def zeus_flash(cycles=3):
    """éclair plein écran — la foudre de Zeus frappe le temple"""
    cols, rows = width(), height()
    for i in range(cycles):
        # flash blanc
        sys.stdout.write("\033[H" + f"{MARBLE}{'█' * cols}{X}\n" * rows + "\033[0m")
        sys.stdout.flush(); time.sleep(0.09)
        # extinction brutale
        sys.stdout.write("\033[2J\033[H\033[0m")
        sys.stdout.flush(); time.sleep(0.07)
    lightning_bolt()
    time.sleep(0.3)

def title_reveal():
    """le titre ARES en or, lettre par lettre, avec le sous-titre"""
    title = "A R E S"
    sub = "SUITE OFFENSIVE — DE LA MYTHOLOGIE À LA GUERRE"
    for i in range(1, len(title) + 1):
        print(f"\r{GOLD}{B}{title[:i]}{X}", end="", flush=True)
        time.sleep(0.14)
    print()
    time.sleep(0.2)
    for i in range(1, len(sub) + 1):
        print(f"\r{MARBLE}{sub[:i]}{X}", end="", flush=True)
        time.sleep(0.02)
    print()
    time.sleep(0.4)

def intro():
    clear()
    frame("── LE TEMPLE S'ÉLÈVE ──", DIM)
    time.sleep(0.3)
    clear()
    temple_rise()
    clear()
    zeus_flash()
    clear()
    laurel()
    title_reveal()
    frame("QUE LA GUERRE COMMENCE", RED)
    time.sleep(0.5)
    clear()

if __name__ == "__main__":
    intro()
