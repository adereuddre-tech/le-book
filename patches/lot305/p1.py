p='index.html';s=open(p,encoding='utf-8').read()
def rep(o,n,k=1):
    global s;c=s.count(o);assert c==k,(o[:70],c);s=s.replace(o,n)
# l'échelle « jusqu'au cran j » remplace les partis par les suivants jusqu'à retrouver la masse salariale du cran
rep("""function ladderT(id,j,T){const C=teamCopy(T);C[id]=teamL(id).map((x,p)=>p===0||(p<=j&&!(id==='fo'&&goneP(p))));return C}   /* les partis ne reviennent que sur contre-offre */""",
    """function ladderT(id,j,T){const C=teamCopy(T),L=teamL(id),tg=L[j].bp;let m=0;C[id]=L.map((x,p)=>{if(p===0)return true;if(m>=tg-1e-9||(id==='fo'&&goneP(p)))return false;m+=salP(L,p);return true});return C}   /* lot 305 : les partis (qui ne reviennent que sur contre-offre) sont remplacés par les suivants */""")
open(p,'w',encoding='utf-8').write(s)
# compensation des frais d'embauche : +0,5 M$ de capital de départ à toutes les difficultés
s=open(p,encoding='utf-8').read()
rep("costM:0.85,seed:0.001}","costM:0.85,seed:0.0015}")
rep("costM:1.10,seed:0.0005}","costM:1.10,seed:0.001}")
rep("costM:1.75,seed:0}","costM:1.75,seed:0.0005}")
rep("capital de départ : 1 M$, plus celui de votre style","capital de départ : 1,5 M$, plus celui de votre style")
rep("capital de départ : 0,5 M$, plus celui de votre style","capital de départ : 1 M$, plus celui de votre style")
open(p,'w',encoding='utf-8').write(s)
s=open(p,encoding='utf-8').read()
rep('["b","aucun capital de départ, sauf celui de votre style"]','["g","capital de départ : 0,5 M$, plus celui de votre style"]')
open(p,'w',encoding='utf-8').write(s)
