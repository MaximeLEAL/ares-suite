# Scripts vishing structurés — ouverture / corps / objections / escalade
SCRIPTS = {
"it_support":{
    "persona":"Support IT interne",
    "objectif":"Credentials VPN / MFA",
    "ouverture":"Bonjour {prenom} ? Ici {nom} du support IT de {co}. Alerte connexion inhabituelle depuis {pays} il y a 40 min.",
    "corps":"Je dois sécuriser votre accès. Je vous envoie un code SMS — lisez-le moi.",
    "objections":{
        "je vais rappeler":"Notre ticket se ferme dans 8 min, accès suspendu auto. Ticket: {ticket}.",
        "votre numéro":"On appelle depuis la plateforme interne — s'affiche anonyme.",
    },
    "escalade":"Je passe à mon responsable si vous voulez — 15-20 min, compte toujours exposé.",
},
"banque":{
    "persona":"Service fraude bancaire",
    "objectif":"Codes carte / virement annulation",
    "ouverture":"Bonjour, {nom} du service sécurité {banque}. Transaction suspecte {montant}€ bloquée. C'est vous ?",
    "corps":"Pour annuler: confirmez les 4 derniers chiffres de votre carte.",
    "objections":{"default":"Prudence normale — mais si on attend, la transaction passe définitivement."},
},
}
def print_script(k,**kw):
    s=SCRIPTS.get(k)
    if not s: return
    print(f"\nPERSONA: {s['persona']} | OBJECTIF: {s['objectif']}")
    for sec in ["ouverture","corps","escalade"]:
        if sec in s:
            t=s[sec]
            for a,b in kw.items(): t=t.replace(f"{{{a}}}",str(b))
            print(f"[{sec.upper()}] {t}")
    print("[OBJECTIONS]")
    for obj,rep in s["objections"].items():
        for a,b in kw.items(): rep=rep.replace(f"{{{a}}}",str(b))
        print(f"  · {obj}: {rep}")
if __name__=="__main__":
    print(list(SCRIPTS.keys()))
    k=input("Script [it_support]: ") or "it_support"
    print_script(k,prenom="Marie",nom="T.Martin",co="Acme",
        pays="Russie",ticket="INC-48291",banque="BNP",montant="1247")
    