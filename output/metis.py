# Scripts manipulation psychologique — 6 leviers Cialdini
LEVIERS = {
    "urgence":      "Deadline artificielle, panique douce",
    "autorité":     "Figure légitime (IT, banque, gov)",
    "réciprocité":  "Donne d'abord pour créer une dette",
    "preuve sociale":"'Vos collègues ont déjà...'",
    "sympathie":    "Miroir du style, prénom, flattery",
    "engagement":   "Petits oui progressifs avant la vraie demande",
}
TEMPLATES = {
"credential_harvest":"""
Bonjour {prenom}, c'est {nom} du support IT de {entreprise}.
On a détecté une tentative d'accès suspecte il y a 20 minutes.
[URGENCE] Votre accès sera suspendu dans 10 minutes.
Confirmez votre identifiant et le code SMS que vous venez de recevoir.
""",
"virement":"""
{prenom}, c'est {nom}, DG de {entreprise}.
Virement urgent confidentiel — {montant}€ avant 16h.
IBAN: {iban}  Réf: CONF-{ref}
Ne pas en parler en interne. Procédure exceptionnelle.
""",
"acces_physique":"""
Bonjour, je suis {nom}, prestataire réseau mandaté par votre DSI.
Ticket ouvert pour intervenir en salle serveur.
Votre responsable {manager} m'a dit de passer directement.
""",
}
def gen(k,**kw):
    t=TEMPLATES.get(k,"?")
    for a,b in kw.items(): t=t.replace(f"{{{a}}}",str(b))
    return t
if __name__=="__main__":
    print(gen("credential_harvest",prenom="Marie",nom="T. Dupont",entreprise="Acme"))
    