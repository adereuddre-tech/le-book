# Lot 110, p3 : nettoyage du code mort des lots 102-104 — redeem(), midFlows(), midYellow(), la ligne de pénalité de
# risque désactivée, RDM et RISKCAP (plus lus). RISKLP/RISKQ/RDMFK restent : les concurrents s'en servent.
s=open('index.html',encoding='utf-8').read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:90]); s=s.replace(o,n)
def cutfn(name):
    global s; i=s.index('\nfunction '+name+'(');j=s.index('\nfunction ',i+5);s=s[:i]+s[j:]
for f in ['redeem','midFlows','midYellow']:cutfn(f)
rep(" const flowLines=[];midFlows(total,flowLines);"," const flowLines=[];")
import re
m=re.search(r"\n if\(false\)lpD\.push\(\[`Risque ex ante[^\n]*\n",s);assert m;s=s[:m.start()]+"\n"+s[m.end():]
rep("const RDM={lp0:0.015,lpk:0.002,dd0:0.04,ddk:0.20,low:0.01},RDMFK=0.15;","const RDMFK=0.15;")
rep("const RISKCAP={y:0.30,r:0.45};\n","")
for n in ['redeem(','midFlows(','midYellow(','RDM.','RISKCAP']:assert n not in s,n
open('index.html','w',encoding='utf-8').write(s);print('lot110 p3 ok')
