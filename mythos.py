# mythos.py — intro cinématique mythologique grecque pour ARES
# braise lente, temple qui s'élève et respire, éclair de Zeus propre,
# laurier matérialisé par scan, titre balayé, Powered by Maxime Leal
import os, sys, time, random, shutil, math

def _c(code): return f"\033[{code}m"
GOLD = _c("93"); MARBLE = _c("97"); RED = _c("91")
DIM = _c("90"); X = _c("0"); B = _c("1"); BRIGHT = _c("1;97")

POWERED = "Powered by Maxime Leal"

def clear():
    sys.stdout.write("\033[2J\033[3J\033[H"); sys.stdout.flush()

def width(): return shutil.get_terminal_size().columns
def height(): return shutil.get_terminal_size().lines

def meander(n):
    return ("⊔⊓" * (n // 2 + 1))[:n]

def bars(w):
    edge = DIM + meander(w) + X
    return edge

# ─────────────────── BRAISE — poussière qui monte ───────────────────
EMBER_CHARS = "·˙∶"

class EmberField:
    def __init__(self, cols, rows, density=0.06):
        self.cols, self.rows = cols, rows
        self.density = density
        self.d = [[random.random() for _ in range(cols)] for _ in range(rows)]

    def step(self):
        for r in range(self.rows):
            for c in range(self.cols):
                self.d[r][c] += random.uniform(-0.04, 0.05)
                if self.d[r][c] > 1: self.d[r][c] = 0

    def line(self, r):
        out = []
        for c in range(self.cols):
            v = self.d[r][c]
            out.append(f"{DIM}{random.choice(EMBER_CHARS)}{X}" if v > (1 - self.density) else " ")
        return "".join(out)

# ─────────────────── TEMPLE ───────────────────
TEMPLE = (
"                      ▄▀▀▄▀▀▄▀▀▄▀▀▄▀▀▄▀▀▄▀▀▄▀▀▄▀▀▄                    ",
"                   ▄▀▀▄▀▀▄▀▀▄▀▀▄▀▀▄▀▀▄▀▀▄▀▀▄▀▀▄▀▀▄                    ",
"        ║ ║  ║ ║  ║ ║  ║ ║  ║ ║  ║ ║  ║ ║  ║ ║  ║ ║  ║ ║            ",
"        ║ ║  ║ ║  ║ ║  ║ ║  ║ ║  ║ ║  ║ ║  ║ ║  ║ ║  ║ ║            ",
"        ║ ║  ║ ║  ║ ║  ║ ║  ║ ║  ║ ║  ║ ║  ║ ║  ║ ║  ║ ║            ",
"        ║ ║  ║ ║  ║ ║  ║ ║  ║ ║  ║ ║  ║ ║  ║ ║  ║ ║  ║ ║            ",
"        ║ ║  ║ ║  ║ ║  ║ ║  ║ ║  ║ ║  ║ ║  ║ ║  ║ ║  ║ ║            ",
"      ══╩═╩══╩═╩══╩═╩══╩═╩══╩═╩══╩═╩══╩═╩══╩═╩══╩═╩══╩═╩══          ",
)

def temple_rise():
    """les colonnes poussent du bas, braise autour, torchlight subtil"""
    cols, rows = width(), height()
    embers = EmberField(cols, rows)
    print("\n")
    for i in range(1, len(TEMPLE) + 1):
        for r in range(rows - len(TEMPLE) - 3):
            print(embers.line(r))
            embers.step()
        for ln in TEMPLE[:i]:
            flick = MARBLE if random.random() < 0.85 else DIM
            print(flick + ln + X)
        time.sleep(0.14)
        if i < len(TEMPLE):
            sys.stdout.write(f"\033[{len(TEMPLE) + 1}A\033[J")
    # respiration : le temple oscille doucement entre marbre et dim
    for f in range(10):
        breath = MARBLE if (f // 3) % 2 == 0 else DIM
        lines = [embers.line(r) for r in range(6)] + [breath + ln + X for ln in TEMPLE]
        sys.stdout.write("\033[H" + "\n".join(lines) + "\033[0m")
        embers.step()
        time.sleep(0.12)

# ─────────────────── ÉCLAIR DE ZEUS ───────────────────
BOLT = (
"                 ╲                    ",
"                  ╲                   ",
"                  ╱                   ",
"                 ╱                    ",
"                 ╲                    ",
"                  ╲                   ",
"                  ╱                   ",
"                 ╱                    ",
"                  ╲                   ",
"                 ╲                    ",
"                  ⚡                   ",
)

def zeus_strike():
    """éclair ramifié : canal sinueux + branches, rémanence dorée,
    tremblement d'impact, anneaux au sol, extinction douce"""
    cols, rows = width(), height()
    random.seed(11)

    # 1 — deux pulses propres
    for b in (MARBLE, None, BRIGHT, None):
        sys.stdout.write("\033[H")
        if b:
            sys.stdout.write(f"{b}{'█' * cols}{X}\n" * rows)
        sys.stdout.flush()
        time.sleep(0.07)
        if b is None:
            clear()
        time.sleep(0.04)

    # 2 — structure : canal principal sinueux + 2 branches qui partent en biais
    x = cols // 2
    main = []
    for r in range(10):
        x += random.choice((-1, 0, 0, 1))
        main.append((r, x))
    branches = []
    for fork_row, direction in ((2, -1), (5, +1)):
        bx = dict(main)[fork_row]
        for k in range(1, 4):
            branches.append((fork_row + k, bx + direction * k))
    cells = {}
    for r, c in main:
        cells[(r, c)] = ("╱" if r % 3 else "╲", GOLD)
    for r, c in branches:
        cells[(r, c)] = ("·" if random.random() < 0.4 else "╲", GOLD)

    top = max(2, (rows - 14) // 2)
    sys.stdout.write("\033[?25l")

    def draw(active_rows, shake=0, glow=False, override=None):
        sys.stdout.write("\033[H")
        for _ in range(top):
            print()
        for r in range(10):
            line = []
            for c in range(cols):
                if (r, c) in cells and r <= active_rows:
                    ch, col = cells[(r, c)]
                    col = override or col
                    line.append(f"{DIM}{ch}{X}" if (glow and r < active_rows)
                                else f"{B}{col}{ch}{X}")
                else:
                    line.append(" ")
            print(" " * max(0, shake) + "".join(line))
        sys.stdout.flush()

    # 3 — la foudre descend ; le canal déjà passé passe en rémanence
    for r in range(10):
        draw(r, glow=(r > 0))
        time.sleep(0.045)

    # 4 — canal complet → flash blanc du canal entier
    draw(9, glow=False, override=MARBLE)
    time.sleep(0.12)

    # 5 — impact : tremblement d'écran
    for f in range(4):
        draw(9, shake=random.choice((-1, 0, 1)), override=MARBLE)
        time.sleep(0.05)

    # 6 — anneaux au sol qui s'élargissent
    sys.stdout.write("\033[H")
    for _ in range(top):
        print()
    for r, c in main:
        if r < 9:
            print(" " * c + DIM + ("╱" if r % 3 else "╲") + X)
    for ring in (4, 9, 15, 22):
        half = cols // 2
        print(DIM + "▒" * max(0, half - ring) + GOLD + "─" * (ring * 2) + DIM + "▒" * max(0, half - ring) + X)
        time.sleep(0.09)

    # 7 — extinction : la rémanence meurt doucement
    for col in (GOLD, DIM, DIM):
        sys.stdout.write("\033[H")
        for _ in range(top):
            print()
        for r, c in main:
            if r < 9:
                print(" " * c + col + ("╱" if r % 3 else "╲") + X)
        sys.stdout.flush()
        time.sleep(0.15)
    sys.stdout.write("\033[?25h\033[0m")
    time.sleep(0.3)

# ─────────────────── LAURIER ───────────────────
LAUREL = (
"              ,@@@@@@@@@,",
"           @@@@@@@@@@@@@@@@@@",
"         @@@@@@@@@@@@@@@@@@@@@@",
"        @@@@   ϟ   ϟ   @@@@",
"         @@@@@@@@@@@@@@@@@@@@@@",
"           @@@@@@@@@@@@@@@@@@",
"              '@@@@@@@@@'",
)

def laurel_materialize():
    """le laurier se matérialise : une ligne de scan descend, les caractères se fixent"""
    print()
    for i in range(1, len(LAUREL) + 1):
        sys.stdout.write(f"\033[{len(LAUREL) + 1}A\033[J") if i > 1 else None
        for ln in LAUREL[:i]:
            # ligne en cours : d'abord du bruit puis se fixe
            if ln == LAUREL[i - 1]:
                for _ in range(2):
                    noise = "".join(random.choice("░▒@# ") if ch != " " else " " for ch in ln)
                    print("\r" + DIM + noise + X, end="", flush=True)
                    time.sleep(0.05)
                print("\r" + GOLD + ln + X)
            else:
                print(GOLD + ln + X)
        time.sleep(0.1)

# ─────────────────── TITRE ───────────────────
def title_reveal():
    """tête lumineuse qui traverse le titre, le texte se fixe derrière — or"""
    title = "A  R  E  S"
    sub = "S U I T E   O F F E N S I V E"
    sys.stdout.write("\033[?25l")
    print()
    for txt, col in [(title, GOLD + B), (sub, MARBLE)]:
        w = len(txt); p = 0
        while p <= w:
            head = txt[p] if p < w else " "
            settled = txt[:p]
            trail = "─" * max(0, w - p - 1)
            sys.stdout.write(f"\r{col}{settled}{X}{BRIGHT}{head}{X}{DIM}{trail}{X}")
            sys.stdout.flush()
            p += max(1, w // 28)
            time.sleep(0.035)
        sys.stdout.write(f"\r{col}{txt}{X}\n")
        time.sleep(0.15)
    sys.stdout.write("\033[?25h\033[0m")
    # sous-sous-titre + crédit
    slow = "DE LA MYTHOLOGIE À LA GUERRE"
    for i in range(1, len(slow) + 1):
        print(f"\r{DIM}{slow[:i]}{X}", end="", flush=True)
        time.sleep(0.02)
    print()
    for i in range(1, len(POWERED) + 1):
        print(f"\r{GOLD}{POWERED[:i]}{X}", end="", flush=True)
        time.sleep(0.03)
    print()
    time.sleep(0.4)

def intro():
    cols = width()
    clear()
    print(DIM + bars(cols) + X)
    print("\n")
    slow_line("  Delphes — avant l'aube.", 0.01)
    time.sleep(0.6)
    clear()
    print(DIM + bars(cols) + X)
    temple_rise()
    zeus_strike()
    clear()
    print(DIM + bars(cols) + X)
    laurel_materialize()
    title_reveal()
    print()
    print(DIM + bars(cols) + X)
    time.sleep(0.6)
    clear()

def slow_line(text, delay):
    for ch in text:
        sys.stdout.write(DIM + ch + X); sys.stdout.flush(); time.sleep(delay)
    print()

if __name__ == "__main__":
    intro()
