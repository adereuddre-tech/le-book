p='index.html';s=open(p,encoding='utf-8').read()
def rep(o,n,k=1):
    global s;c=s.count(o);assert c==k,(o[:60],c);s=s.replace(o,n)
rep("const BOMAP=[0,1,3,4,5,6],NOTRD=4,","const BOMAP=[0,1,3,4,5,6],NOTRD=2,   /* lot 259 : courtier ×2 (×4 avant) */\n ")
rep("const BRK0=0.2;   /* lot 236 : seuil du frein, 200 M$ */","const BRK0=0.1;   /* lot 236 : seuil du frein ; lot 259 : 100 M$ (200 avant) */")
open(p,'w',encoding='utf-8').write(s)
