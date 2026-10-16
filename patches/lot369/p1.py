p="index.html";s=open(p,encoding="utf-8").read()
def rep(o,n,k=1):
    global s;c=s.count(o);assert c==k,(o[:70],c);s=s.replace(o,n)
# A2 : extrêmes un peu plus fréquents (dépêches extrêmes 15 → 20 %, plancher des scénarios 10 → 13 %) ;
#      le sang-froid du desk règle la gestion de crise : choc immédiat subi et gap de crise ×0,7 (moral 100) … ×1,4 (moral 0).
# Positions visibles sans seuil : 1 % + empreinte par ligne ; achats selon la marge, sans plancher ; fuites et pertes × sang-froid.
rep("const XPROB=0.15;","const XPROB=0.20;   /* lot 369 : 0,15 → 0,20 */")
rep("function stressP(){return Math.min(0.32,0.10+0.20*","function stressP(){return Math.min(0.35,0.13+0.20*")
rep("return STRGAP*g*(sc&&sc.ext?2:1)*crowd(riskShown(w).total)*(S&&S.prof==='rv'?1.5:1)}",
    "return STRGAP*g*(sc&&sc.ext?2:1)*crowd(riskShown(w).total)*(S&&S.prof==='rv'?1.5:1)*(S&&S.bud?motS():1)}   /* lot 369 : sang-froid */")
rep("const bo=0.5+0.5*((S.bud&&TAILM[S.bud.risk])||1),cr=v<0?crowd(riskShown(w).total):1;return bo*(0.5*v*cr-stressGap(k,sc))+XCONT*v}",
    "const bo=0.5+0.5*((S.bud&&TAILM[S.bud.risk])||1),cr=v<0?crowd(riskShown(w).total)*(S.bud?motS():1):1;return bo*(0.5*v*cr-stressGap(k,sc))+XCONT*v}   /* lot 369 : sang-froid sur le choc subi */")
rep("if(ev.stress){imm*=0.5+0.5*(TAILM[S.bud.risk]||1);if(imm<0)imm*=crowd(riskShown(w).total);",
    "if(ev.stress){imm*=0.5+0.5*(TAILM[S.bud.risk]||1);if(imm<0)imm*=crowd(riskShown(w).total)*motS();")
# visibilité
rep("const VIS={thr:0.02,kMin:3,p0:0.04,pk:1.0,pmax:0.35,Hs:2.5,Hl:2.0};","const VIS={thr:0,kMin:1,p0:0.01,pk:1.0,pmax:0.35,Hs:2.5,Hl:2.0,show:0.02};   /* lot 369 : plus de seuil (avant : ±3 et 2 % du carnet ; 4 % de base) */")
rep("""function visList(k){k=k||S.k;const m=marginPct(k),L=[];for(let i=0;i<N;i++){if(Math.abs(k[i])<VIS.kMin)continue;const f=footprint(i,k);if(f<VIS.thr)continue;
  if(k[i]<0)L.push({i,f,kind:'short',p:Math.min(VIS.pmax,VIS.p0+VIS.pk*f)*(boH(11)?0.7:1)});
  else if(m>MGZ.watch)L.push({i,f,kind:'long',p:Math.min(VIS.pmax,(VIS.p0+VIS.pk*f)*Math.min(2.5,m/MGZ.watch))*(boH(11)?0.7:1)})}return L}""",
"""function visList(k){k=k||S.k;const m=marginPct(k),L=[],ms=S&&S.bud?motS():1;for(let i=0;i<N;i++){if(Math.abs(k[i])<VIS.kMin)continue;const f=footprint(i,k);
  if(k[i]<0)L.push({i,f,kind:'short',p:Math.min(VIS.pmax,(VIS.p0+VIS.pk*f)*ms)*(boH(11)?0.7:1)});
  else if(m>0)L.push({i,f,kind:'long',p:Math.min(VIS.pmax,(VIS.p0+VIS.pk*f)*Math.min(2.5,m/MGZ.watch)*ms)*(boH(11)?0.7:1)})}return L}   /* lot 369 : sans seuil, × sang-froid */""")
rep("L=Math.min(0.6,Math.abs(w[i])*INSTR[i].sigQ*H*crowd(riskShown(w).total)),d=Math.trunc(S.k[i]/2)-S.k[i]",
    "L=Math.min(0.6,Math.abs(w[i])*INSTR[i].sigQ*H*crowd(riskShown(w).total)*motS()),d=Math.trunc(S.k[i]/2)-S.k[i]")
rep("L=Math.min(0.6,Math.abs(w[v.i])*INSTR[v.i].sigQ*H*crowd(sp));vl+=v.p*0.8*L;","L=Math.min(0.6,Math.abs(w[v.i])*INSTR[v.i].sigQ*H*crowd(sp)*motS());vl+=v.p*0.8*L;")
rep("""${V.map(v=>`<p class="note" style="margin:2px 0 0">""","""${V.filter(v=>v.p>=VIS.show).sort((a,b)=>b.p-a.p).slice(0,4).map(v=>`<p class="note" style="margin:2px 0 0">""")
rep("""Une ligne devient visible à partir de ±${VIS.kMin} unités et au-delà de ${Math.round(VIS.thr*100)} % de la profondeur de son carnet (les marchés étroits d'abord, et tous quand le fonds grossit). Une vente est alors déclarée ; un achat, vu du prime broker dès ${Math.round(MGZ.watch*100)} % de marge.""",
    """Toute ligne finit par se voir : ${Math.round(VIS.p0*100)} % par trimestre, plus son poids dans la profondeur du carnet (les marchés étroits d'abord, et tous quand le fonds grossit). Une vente est déclarée ; un achat est vu du prime broker en proportion de la marge utilisée. Le sang-froid du desk (×${dec(motS(),2)}) règle les fuites et la gravité ; seules les lignes à ${Math.round(VIS.show*100)} % ou plus sont listées.""")
rep("""pèse ${dec(te.fp*100,1)} % de la profondeur du carnet : à partir de ±${VIS.kMin} unités et au-delà de ${Math.round(VIS.thr*100)} %, elle est déclarée et tout le marché la voit.`""",
    """pèse ${dec(te.fp*100,1)} % de la profondeur du carnet : elle est déclarée, et le marché a fini par la voir.`""")
rep("""Au-delà de 2 % et à partir de ±3 (lot 333) :""","""Lot 369 : plus de seuil (avant : 2 % et ±3, lot 333) :""")
open(p,"w",encoding="utf-8").write(s)
