
import json,random,sys
sys.path.insert(0,"/lab/cipher/grille")
import numpy as np, torch
import grille_engine as ge
Q=torch.tensor(np.load("/lab/cipher/grille/quad_en.npy"),device=ge.device())
pool=open("/lab/cipher/grille/plain_pool.txt").read()
res=[]
for label,secs,given in (("key given",120,True),("key unknown",600,False)):
  for t in range(3):
    truth=pool[6007*(t+1):6007*(t+1)+182]
    cells,sh,key=ge.plant(pool[6007*(t+1):],True,random.Random(200+t))
    top=ge.anneal(Q,cells,8192,secs,t,True,key=key if given else None)
    orb,k=ge.match_up_to_rotation(top[0]["shifts"],sh)
    kk=top[0]["key"]; order=ge.order_for(ge.unrotate(top[0]["shifts"],k),True)
    text="".join(chr(65+int(kk[cells[i]])) for i in order)
    agree=sum(a==b for a,b in zip(text,truth))/182
    r={"case":label,"seconds":secs,"plant":t,"orbits_up_to_rotation":orb,"rotation":k,"char_agreement":round(agree,3),"text":text[:60],"truth":truth[:60]}
    print(json.dumps(r),flush=True); res.append(r)
json.dump(res,open("/lab/cipher/grille/bench-2.json","w"),indent=1); print("done")
