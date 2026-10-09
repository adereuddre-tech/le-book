p='index.html';s=open(p,encoding='utf-8').read()
def rep(o,n,k=1):
    global s;c=s.count(o);assert c==k,(o[:60],c);s=s.replace(o,n)
rep("""/* lot 66 : accident de levier. Tout est tiré avant l'affichage : les montants des boutons sont appliqués tels quels. */
function tailDraw(){""","""/* lot 275 : visibilité. L'empreinte d'une ligne est son notionnel rapporté à la profondeur du carnet. Au-delà de 1 % :
   une vente à découvert est déclarée (publique) — risque de short squeeze ; un achat avec plus de 20 % de marge utilisée
   est vu du prime broker — risque de liquidation forcée (Archegos, 2021). Probabilité par ligne : 4 % + l'empreinte, plafonnée. */
const VIS={thr:0.01,p0:0.04,pk:1.0,pmax:0.35,Hs:2.5,Hl:2.0};
function footprint(i,k){const d=DEPTH[INSTR[i].sym];return d?Math.abs(notionalBn((k||S.k)[i],i))/d:0}
function visList(k){k=k||S.k;const m=marginPct(k),L=[];for(let i=0;i<N;i++){if(!k[i])continue;const f=footprint(i,k);if(f<VIS.thr)continue;
  if(k[i]<0)L.push({i,f,kind:'short',p:Math.min(VIS.pmax,VIS.p0+VIS.pk*f)});
  else if(m>MGZ.watch)L.push({i,f,kind:'long',p:Math.min(VIS.pmax,(VIS.p0+VIS.pk*f)*Math.min(2.5,m/MGZ.watch))})}return L}
function visP(k){return 1-visList(k).reduce((a,v)=>a*(1-v.p),1)}
const VISEV={short:{t:"Short squeeze : votre vente déclarée devient une cible",who:"Desk · alerte",vis:1,sev:[1,1],
  p:"Votre position vendeuse est publique depuis sa déclaration. Des acheteurs coordonnés l'ont repérée ; chaque hausse force d'autres vendeurs à racheter, et le prix s'envole contre vous.",
  o:["Tenir la ligne et attendre que la fièvre retombe","Racheter la moitié dans la tempête","Acheter des options d'achat pour plafonner la perte"]},
 long:{t:"Liquidation forcée : le prime broker vend votre ligne",who:"Prime broker · appel urgent",vis:1,mg:1,sev:[1,1],
  p:"Le prime broker a vu votre position acheteuse, grosse et financée à crédit. Le prix a baissé : il exige des garanties tout de suite, et commence à vendre lui-même — au pire prix, devant tout le marché.",
  o:["Apporter du collatéral et laisser faire","Vendre vous-même la moitié avant lui","Négocier un délai contre une commission"]}};
/* lot 66 : accident de levier. Tout est tiré avant l'affichage : les montants des boutons sont appliqués tels quels. */
function tailDraw(){
 {const V=visList(S.k),u=prng32(hash32('vis'+S.q,S.seed));for(const v of V){if(u()<v.p){const w=weights(S.k),i=v.i,H=v.kind==='short'?VIS.Hs:VIS.Hl,
   L=Math.min(0.6,Math.abs(w[i])*INSTR[i].sigQ*H*crowd(riskShown(w).total)),d=Math.trunc(S.k[i]/2)-S.k[i],imp=d?tcost(d,i).cost*urgM(URG.tail,i):0;
   return {i:0,ev:Object.assign({},VISEV[v.kind],{t:VISEV[v.kind].t+` · ${INSTR[i].sym}`}),pos:i,vis:v.kind,fp:v.f,sp:riskShown(w).total,L,good:u()<0.5,imp:imp/S.nav,mgu:marginPct(S.k)}}}}   /* lot 275 */""")
rep(""" const ev=TAILEV[te.i]||TAILEV[0],O=tailOpts(te),nav=S.nav,L=te.L;""",""" const ev=te.ev||TAILEV[te.i]||TAILEV[0],O=tailOpts(te),nav=S.nav,L=te.L;""")
rep(""" const LAB={hold:ev.o[0],cut25:'Couper un quart du book',cut:ev.o[1],cut75:'Couper les trois quarts du book',cut100:'Tout solder',hedge:ev.o[2]};""",
    """ const LAB={hold:ev.o[0],cut25:te.pos!=null?'Couper un quart de la ligne':'Couper un quart du book',cut:ev.o[1],cut75:te.pos!=null?'Couper les trois quarts de la ligne':'Couper les trois quarts du book',cut100:te.pos!=null?'Solder la ligne':'Tout solder',hedge:ev.o[2]};""")
rep(""" const kOf=o=>S.k.map(v=>o.x===0.5||o.x===1?Math.trunc(v*(1-o.x)):Math.sign(v)*Math.round(Math.abs(v)*(1-o.x)));""",
    """ const kOf=o=>S.k.map((v,j)=>te.pos!=null&&j!==te.pos?v:(o.x===0.5||o.x===1?Math.trunc(v*(1-o.x)):Math.sign(v)*Math.round(Math.abs(v)*(1-o.x))));   /* lot 275 : accident sur une ligne */""")
rep("""   <p class="note">${te.byMg?`Appel de marge""","""   <p class="note">${te.vis?(te.vis==='short'?`Votre vente sur ${INSTR[te.pos].nm} pèse ${dec(te.fp*100,1)} % de la profondeur du carnet : au-delà de ${Math.round(VIS.thr*100)} %, elle est déclarée et tout le marché la voit.`:`Votre achat sur ${INSTR[te.pos].nm} pèse ${dec(te.fp*100,1)} % de la profondeur du carnet, avec ${Math.round(te.mgu*100)} % de marge utilisée : le prime broker l'a dans le collimateur.`):te.byMg?`Appel de marge""")
# affichage : les lignes visibles sous la jauge de levier
rep(""" el.innerHTML=`<div class="kv"><span><b>Levier</b> · marge utilisée""",""" const V=visList(S.k),pv=visP(S.k);
 el.innerHTML=`<div class="kv"><span><b>Levier</b> · marge utilisée""")
rep("""Pour la faire baisser : moins de notionnel, surtout sur les marchés à forte marge (actions, matières premières, crypto).</p>`}""",
    """Pour la faire baisser : moins de notionnel, surtout sur les marchés à forte marge (actions, matières premières, crypto).</p>
  ${V.length?`<div class="kv" style="margin-top:6px"><span><b>👁 Positions visibles du marché</b></span><b style="color:var(--short)">accident ${Math.round(pv*100)} %</b></div>${V.map(v=>`<p class="note" style="margin:2px 0 0">${v.kind==='short'?'Vente déclarée':'Achat à crédit repéré'} · <b>${INSTR[v.i].sym}</b> ${S.k[v.i]>0?'+':''}${S.k[v.i]} — ${dec(v.f*100,1)} % du carnet : ${v.kind==='short'?'short squeeze':'liquidation forcée'} ${Math.round(v.p*100)} %</p>`).join('')}<p class="note" style="margin:4px 0 0">Une ligne devient visible au-delà de ${Math.round(VIS.thr*100)} % de la profondeur de son carnet (les marchés étroits d'abord, et tous quand le fonds grossit). Une vente est alors déclarée ; un achat, vu du prime broker dès ${Math.round(MGZ.watch*100)} % de marge.</p>`:''}`}""")
open(p,'w',encoding='utf-8').write(s)
