# Deanonymiseur stylométrique — fingerprint + cosine similarity
import re,math
from collections import Counter

def features(text):
    words=re.findall(r'\b\w+\b',text.lower())
    sents=[s.strip() for s in re.split(r'[.!?]+',text) if s.strip()]
    fw=["je","tu","il","elle","nous","vous","les","de","et","ou","the","and","of","to","is"]
    fw_c={w:words.count(w) for w in fw}; fwt=max(sum(fw_c.values()),1)
    bg=Counter(text[i:i+2] for i in range(len(text)-1) if text[i:i+2].strip())
    return {
        "awl":round(sum(len(w) for w in words)/max(len(words),1),3),
        "asl":round(sum(len(s.split()) for s in sents)/max(len(sents),1),3),
        "ttr":round(len(set(words))/max(len(words),1),3),
        "pct":round(len(re.findall(r'[,;:!?]',text))/max(len(text),1),4),
        **{f"fw_{k}":round(v/fwt,4) for k,v in fw_c.items()},
        **{f"bg_{k}":v for k,v in bg.most_common(15)},
    }

def cosine(a,b):
    keys=set(a)&set(b)
    fa=[a.get(k,0) for k in keys]; fb=[b.get(k,0) for k in keys]
    dot=sum(x*y for x,y in zip(fa,fb))
    na=math.sqrt(sum(x**2 for x in fa)); nb=math.sqrt(sum(x**2 for x in fb))
    return round(dot/(na*nb),4) if na and nb else 0.0

def identify(unknown,candidates):
    uf=features(unknown)
    return sorted([{"name":n,"sim":cosine(uf,features(t))} for n,t in candidates.items()],
        key=lambda x:x["sim"],reverse=True)

if __name__=="__main__":
    unk=input("Texte inconnu (entrée libre): ")
    n=int(input("Nb candidats [2]: ") or "2")
    cands={}
    for i in range(n):
        name=input(f"Nom candidat {i+1}: ")
        text=input(f"Texte candidat {i+1}: ")
        cands[name]=text
    res=identify(unk,cands)
    for r in res: print(f"  {r['name']:20} sim: {r['sim']}")
    print(f"→ plus probable: {res[0]['name']}")
    