# Générateur faux profils réseaux sociaux — backstory + posts + photo prompt
import random,json,datetime
from pathlib import Path
FN_M=["Théo","Lucas","Maxime","Antoine","Nicolas","Julien","Alexandre"]
FN_F=["Léa","Emma","Camille","Chloé","Manon","Sarah","Julie"]
LN  =["Martin","Bernard","Thomas","Petit","Robert","Richard","Durand"]
CITIES=["Paris","Lyon","Marseille","Bordeaux","Toulouse","Nantes","Lille"]
JOBS  =["Commercial","Développeur","Infirmière","Comptable","Graphiste","Enseignant"]
INT   =["randonnée","cuisine","photo","gaming","fitness","voyage","lecture","musique"]
POSTS =["Super journée 😊","Qui a des conseils pour {i} ?",
        "Lundi matin... ☕","Fier de finir ce projet !",
        "Top resto à {c} hier soir","Contrat signé 🎉","{i} ça ressource vraiment"]

def profile(gender="M"):
    fn=random.choice(FN_M if gender=="M" else FN_F)
    ln=random.choice(LN); city=random.choice(CITIES)
    job=random.choice(JOBS); age=random.randint(22,45)
    interests=random.sample(INT,3)
    posts=[]
    for _ in range(random.randint(8,15)):
        d=datetime.date.today()-datetime.timedelta(days=random.randint(1,30))
        posts.append({"date":str(d),"text":random.choice(POSTS)
            .replace("{i}",random.choice(interests)).replace("{c}",city)})
    posts.sort(key=lambda x:x["date"],reverse=True)
    return {"name":f"{fn} {ln}","username":f"{fn.lower()}.{ln.lower()}{random.randint(10,99)}",
            "age":age,"city":city,"job":job,"interests":interests,
            "bio":f"{job} à {city} · {interests[0]} · {2024-age}",
            "posts":posts,
            "photo_prompt":f"Portrait, {'man' if gender=='M' else 'woman'}, {age}yo, friendly, casual, realistic LinkedIn headshot"}

if __name__=="__main__":
    n=int(input("Combien [5]: ") or "5")
    ps=[profile(random.choice(["M","F"])) for _ in range(n)]
    Path("output/fake_profiles.json").write_text(json.dumps(ps,indent=2,ensure_ascii=False))
    print(f"[+] {n} profils → output/fake_profiles.json")
    