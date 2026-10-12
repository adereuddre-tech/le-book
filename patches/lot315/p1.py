p='index.html';s=open(p,encoding='utf-8').read()
def rep(o,n,k=1):
    global s;c=s.count(o);assert c==k,(o[:70],c);s=s.replace(o,n)
# un seul portage structurel par marché, même formule pour l'attendu et le réalisé
rep("""const PREM={'Actions':0.012,'Taux':0.004};""",
"""/* lot 315 : portage structurel — ce que rapporte une position si rien ne bouge, par trimestre :
   κ = κ0 + χ·a, a = appétit pour le risque (en σ, borné à [−3 ; +1,5]). Même formule pour l'attendu (appétit estimé)
   et le réalisé (appétit du trimestre). Remplace la prime par classe (PREM) et la dérive du VIX (et son multiplicateur de régime). */
const KAPPA={ES:[0.012,0],NQ:[0.012,0],ESTX:[0.012,0],TOPX:[0.012,0],MXEF:[0.012,0],TN:[0.004,0],GBL:[0.004,0],R:[0.004,0],OAT:[0.004,0],JGB:[0.004,0],VX:[-0.085,0.085/1.5]};
function kap(i,a){const k=KAPPA[INSTR[i].sym];if(!k)return 0;const aa=Math.max(-3,Math.min(1.5,a||0));return k[0]+k[1]*aa}""")
rep("""   if(x.drift)r+=x.drift*(S.truth==='crise'?-2.2:S.truth==='recession'?-0.9:1);
""","")
rep("""   r+=PREM[x.grp]||0;
   return r;""","""   r+=kap(i,S.f[3]);   /* lot 315 */
   return r;""")
rep("""function vixCarry(x,a){if(x.sym!=='VX'||!x.drift)return x.drift||0;return x.drift*Math.max(0,Math.min(1,1+a/1.5))}   /* lot 168 : a = appétit (σ) ; −1,5 σ ⇒ portage nul */""",
    """/* lot 315 : vixCarry remplacé par kap(i,a), le portage structurel de tous les marchés */""")
rep("""return {m:x.sigQ*z+vixCarry(x,f[3]||0)+(PREM[x.grp]||0),s:x.sigQ*Math.sqrt(v)};""","""return {m:x.sigQ*z+kap(i,f[3]||0),s:x.sigQ*Math.sqrt(v)};""")
rep("""cv,drift:vixCarry(x,f[3]||0)};""","""cv,drift:kap(i,f[3]||0)};""")
rep("""...(Math.abs(XP.drift)>1e-6?[['Dérive propre','',pc(XP.drift)]]:[]),""","""...(Math.abs(XP.drift)>1e-6?[['Portage structurel','',pc(XP.drift)]]:[]),""")
open(p,'w',encoding='utf-8').write(s)
s=open(p,encoding='utf-8').read()
rep(", mg:0.20, drift:-0.085}",", mg:0.20}")
open(p,'w',encoding='utf-8').write(s)
