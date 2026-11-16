# Erinyes — fiction dark/gore générée LOCALEMENT, zéro API
# moteur : assemblage de segments sensoriels seedés → scène longue et cohérente
import random, argparse
from pathlib import Path

LIEUX=["salle d'interrogatoire sous la préfecture, 3h14 du matin",
       "ferme abandonnée aux confins de la Beauce, nuit sans lune",
       "cave à vin d'un hôtel particulier, huitième sous-sol",
       "chaudière désaffectée d'une aciérie, vapeur blanche",
       "appartement haussmannien aux volets cloués, 22h47"]
PERSONNAGES=[("Marek","charpentier, mains larges, cicatrice au sourcil gauche",
              "il compte ses pas quand il a peur"),
             ("Odile","infirmière de nuit, tresse tirée, ongles mordus",
              "elle nomme les morts à voix basse comme une litanie"),
             ("Sassine","gardien de nuit, mollets faibles, haleine à l'anis",
              "il prie en Wolof quand la panique monte"),
             ("Vera","procureure, talons fins, bracelet en cuir usé",
              "elle mâche ses mots comme du verre")]
ACTES=["l'interrogatoire qui dérape au troisième mensonge",
       "la découverte du corps dissimulé sous la citerne",
       "le rituel qui exige une offrande de chair vivante",
       "la chasse en sous-sol, lampe qui faiblit",
       "le compte à rebours avant l'arrivée des gendarmes"]
SENSORIEL=["odeur de fer et de javel collé au carrelage",
           "grésillement du néon mort qui s'allume par intermittence",
           "craquement régulier d'une solive au-dessus",
           "goût de cuivre remontant de la gorge",
           "chaleur humaine stagnante entre quatre murs sans fenêtre"]
ONOM=["crac.","chhhhh.","toc. toc. toc.","gloup.","crunch.","sfff."]

def scene(seed=None):
    r=random.Random(seed)
    lieu=r.choice(LIEUX); nom,desc,tics=r.choice(PERSONNAGES)
    acte=r.choice(ACTES)
    p=[f"**{lieu}**", "",
       f"{desc}. {nom} entre dans le récit par le côté le plus étroit de la pièce, "
       f"épaules d'abord, souffle ensuite. {r.choice(SENSORIEL).capitalize()}.",
       "", f"L'acte du jour : {acte}. Rien ne l'annonce — c'est ce qui le rend certain.",
       ""]
    for i in range(6):
        p.append(f"**Séquence {i+1}**")
        p.append(f"{nom} progresse. {r.choice(SENSORIEL)}. "
                 f"Chaque détail se pose à plat sur la scène, sans hiérarchie, "
                 f"comme les objets d'une table d'autopsie. "
                 f"Onomatopée : {r.choice(ONOM)}")
        p.append(r.choice([
            f"{nom} pense à autre chose, et c'est l'autre chose qui le sauve.",
            "Le silence se remplit d'abord, puis se vide d'un coup.",
            "Il n'y a pas de monstre. Il y a une décision déjà prise.",
            "Le corps réagit avant la pensée : salive, sueur froide, genoux qui négocient.",
            "La lumière tombe mal, tombe juste, tombe comme il faut."]))
        p.append("")
    p.append("**Fin — la porte se referme sur le bruit, pas sur la question.**")
    return "\n".join(p)

if __name__=="__main__":
    ap=argparse.ArgumentParser(); ap.add_argument("--seed",type=int); ap.add_argument("-o")
    a=ap.parse_args(); s=scene(a.seed)
    print(s)
    out=Path(a.o or "output/erinyes_scene.txt")
    out.parent.mkdir(exist_ok=True); out.write_text(s,encoding="utf-8")
    print(f"\n[+] → {out} ({len(s.split())} mots)")
    