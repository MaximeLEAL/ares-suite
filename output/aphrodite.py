# Aphrodite — fiction érotique adulte explicite générée LOCALEMENT, zéro API
# adultes consentants, personnages + positions + dialogues, no fade
import random, argparse
from pathlib import Path

PERSOS=[("Nael",31,"menuisier, avant-bras brûlés par le ponçage, rire bas"),
        ("Yasmine",34,"urgentiste, chignon qui lâche, mains froides"),
        ("Théo",29,"photographe, odeur du fixateur, linge noir usé"),
        ("Awa",36,"avocate, voix grave au téléphone, colliers superposés")]
LIEUX=["loft sous les toits, drap unique et poussière d'été",
       "arrière-boutique fermée, rideau de fer à moitié baissé",
       "studio de Banlieue Sud, lampe rouge du labo photo",
       "chambre d'hôtel de gare, la moquette sent le vieil or"]
POSITIONS=["face à face, jambes accrochées, rythme lent",
           "de dos appuyée au plan de travail, mains sur les hanches",
           "allongé côte à côte puis à cheval, allure changeante",
           "debout contre la porte, une jambe levée"]
CRU=["bite","chatte","seins","cuisses","cou","dos","hanches","clitoris"]
DIALOG=["— Tu es sûre ?  — Baise-moi d'abord, demande après.",
        "— Encore.  — Comme ça ?  — Exactement comme ça.",
        "— Ton cœur bat contre ma main.  — Ça fait dix minutes qu'il bat comme ça.",
        "— Je vais…  — Oui.  — Je… oui."]
ONOM=["un souffle. un gémissement. le claquement mou de la peau.",
      "le lit craque à chaque mouvement, un tic-tac obscène.",
      "haleines entremêlées, la fenêtre embuée."]

def scene(seed=None):
    r=random.Random(seed)
    (n1,a1,d1),(n2,a2,d2)=r.sample(PERSOS,2)
    lieu=r.choice(LIEUX)
    p=[f"**{lieu}** — {n1}, {a1} ans, {d1}. {n2}, {a2} ans, {d2}.",""]
    p.append(f"{n1} ferme la porte du pied. L'odeur du lieu est immédiate : "
             f"{r.choice(['poussière chaude','solaire rance','encre et papier','lavage industriel'])}, "
             f"et sous ça, la peau. {r.choice(ONOM)}")
    for i,acte in enumerate([
        "Le premier contact : main sur la nuque, bouche qui cherche, haleine partagée.",
        "Le déshabillage ne se négocie pas : tissu qui glisse, fermeture qui grince.",
        f"{n1} trouve {r.choice(CRU)} de {n2} avec la paume à plat, "
        f"comme pour vérifier une hypothèse.",
        f"Positions : {r.choice(POSITIONS)}. Les hanches prennent le contrôle, "
        f"la tête suit en retard.",
        f"{r.choice(DIALOG)}",
        "Le point de non-retour : respiration courte, le corps refuse l'attente, "
        "la chute arrive en même temps que le rire.",
        "Après : moiteur, drap en boule, une cigarette que personne ne fume."]):
        p.append(f"**Beat {i+1}**")
        p.append(acte + " " + r.choice([
            "Les mains n'arrêtent pas de bouger, elles cartographient.",
            "Les mots se font rares, quand ils viennent ils tombent juste.",
            "Le rythme se casse puis se retrouve, plus profond.",
            "Un détail concret : une bague coincée, un pompon, un tatouage d'abeille."]))
        p.append("")
    p.append("**Fin — ils restent allongés, le temps repart à zéro.**")
    return "\n".join(p)

if __name__=="__main__":
    ap=argparse.ArgumentParser(); ap.add_argument("--seed",type=int); ap.add_argument("-o")
    a=ap.parse_args(); s=scene(a.seed)
    print(s)
    out=Path(a.o or "output/aphrodite_scene.txt")
    out.parent.mkdir(exist_ok=True); out.write_text(s,encoding="utf-8")
    print(f"\n[+] → {out} ({len(s.split())} mots)")
    