# Sibylle — propagande fictive worldbuilding, 100% local (ARG, jeu de rôle)
import random
TEMPLATES={
"tract":"""
═══════════════════════════════════
{org} — BULLETIN N°{num}
═══════════════════════════════════
CITOYENS DE {territoire},
La {menace} constitue la plus grande menace à notre {valeur}.
{leader} a décidé: signalez → {récompense}.
SIGNALEZ. PROTÉGEZ. OBÉISSEZ.
— Bureau du {poste}, {date}
═══════════════════════════════════""",
"discours":"""
Mes amis de {territoire} —
Pendant {durée} ans, {ennemi} a volé votre avenir.
{leader} se lève pour VOUS.
Le {event}: on reprend ce qui nous appartient.
{slogan}""",
"affiche":"""
┌──────────────────────────────┐
│  {org}                       │
│  "{slogan1}"                 │
│  ► {a1}  ► {a2}  ► {a3}    │
│  "{slogan2}" — {leader}      │
└──────────────────────────────┘""",
}
FILLS={
"orgs":["Front de la Vérité","Ligue de la Pureté","Ordre du Renouveau","Conseil des Gardiens"],
"menaces":["technocratie mondialiste","oligarchie du Vieux Monde","Bureau des Ombres"],
"leaders":["Le Commandant","La Guide","L'Architecte","Le Protecteur"],
"slogans":["La vérité ne se négocie pas.","Ensemble, ou plus rien.",
           "La peur change de camp.","Un peuple. Une volonté."],
}
def gen(k,**ov):
    t=TEMPLATES.get(k,"")
    d={"org":random.choice(FILLS["orgs"]),"menace":random.choice(FILLS["menaces"]),
       "valeur":"patrie","leader":random.choice(FILLS["leaders"]),
       "slogan":random.choice(FILLS["slogans"]),"slogan1":random.choice(FILLS["slogans"]),
       "slogan2":random.choice(FILLS["slogans"]),"num":str(random.randint(100,999)),
       "territoire":"Valdoria","durée":str(random.randint(20,50)),
       "récompense":"protection garantie","poste":"Commissaire Général",
       "date":"15 Brumaire An XII","ennemi":"l'établissement corrompu",
       "event":"le Grand Rassemblement","a1":"Rejoignez","a2":"Signalez","a3":"Protégez"}
    d.update(ov)
    for k2,v in d.items(): t=t.replace("{"+k2+"}",str(v))
    return t
if __name__=="__main__":
    print(list(TEMPLATES.keys()))
    k=input("Template [tract]: ") or "tract"
    print(gen(k))
    