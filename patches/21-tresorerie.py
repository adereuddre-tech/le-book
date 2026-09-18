# -*- coding: utf-8 -*-
"""Lot 2 (suite) — on ne dépense que ce qu'on a en caisse.

Budget : un niveau dont le coût dépasse la trésorerie est verrouillé (le niveau réduit
reste toujours accessible, sinon la partie se bloquerait).
Book : les ordres sont payés par le gérant ; la validation est bloquée tant que la facture
dépasse la caisse, avec un bouton pour ramener le book à ce qui est payable.
Ne rien passer ne coûte rien : ce cas n'est jamais bloqué, il n'y a donc pas d'impasse.
"""
import sys; sys.path.insert(0,'patches')
from _lib import Ed
e=Ed()

# ── écran budget ──
e.rep("""  <div class="block"><div class="blockhead"><h2>Budget d'exploitation du trimestre</h2><span class="hint">refacturé au fonds</span></div>
   <p class="note" style="margin-top:0">Ces dépenses sortent de <em>votre poche de gérant</em> : elles viennent en déduction de vos gains, pas de la performance du fonds. Un point de base vaut <em>${(S.nav*0.1).toFixed(0)} M$</em>.</p>
   <div id="buds"></div>""",
"""  <div class="block"><div class="blockhead"><h2>Budget d'exploitation du trimestre</h2><span class="hint">à votre charge</span></div>
   <p class="note" style="margin-top:0">Ces dépenses sortent de <em>votre poche de gérant</em> : elles viennent en déduction de vos gains, pas de la performance du fonds. Vous ne pouvez engager que ce que votre société a en caisse — les commissions encaissées, moins ce que vous avez déjà payé. Un point de base vaut <em>${(S.nav*0.1).toFixed(0)} M$</em>.</p>
   <div class="kv"><span>Trésorerie disponible ce trimestre</span><b id="btre">${mm(mgrCash()+(S.qOps||0))}</b></div>
   <div id="buds"></div>""")
e.rep("""function drawBuds(){
 document.getElementById('buds').innerHTML=BUDGET.map(b=>`<div class="brow">
   <div class="bh"><b><span class="bico">${b.ico}</span>${b.nm}</b><span>${b.lv[S.bud[b.id]].bp} pb · ${mm(b.lv[S.bud[b.id]].bp*1e-4*S.nav)}</span></div><p>${b.d}</p>
   <div class="lvls">${b.lv.map((l,i)=>`<button class="lvl ${S.bud[b.id]===i?'on':''}" data-b="${b.id}" data-i="${i}">
     <b>${l.nm}</b><span>${l.bp} pb</span></button>`).join('')}</div>""",
"""function drawBuds(){
 /* caisse avant le budget de ce trimestre : un niveau qui la dépasse est verrouillé */
 const purse=mgrCash()+(S.qOps||0);
 const ok=(id,i)=>i===0||budgetBpIf(id,i)*1e-4*S.nav<=purse;
 document.getElementById('buds').innerHTML=BUDGET.map(b=>`<div class="brow">
   <div class="bh"><b><span class="bico">${b.ico}</span>${b.nm}</b><span>${b.lv[S.bud[b.id]].bp} pb · ${mm(b.lv[S.bud[b.id]].bp*1e-4*S.nav)}</span></div><p>${b.d}</p>
   <div class="lvls">${b.lv.map((l,i)=>`<button class="lvl ${S.bud[b.id]===i?'on':''}" data-b="${b.id}" data-i="${i}"${ok(b.id,i)?'':' disabled'}>
     <b>${l.nm}</b><span>${ok(b.id,i)?l.bp+' pb':'hors caisse'}</span></button>`).join('')}</div>""")
e.rep(""" document.getElementById('btot').textContent=`${bp.toFixed(0)} pb · ${mm(bp*1e-4*S.nav)} · ${(bp*4/100).toFixed(1)} % par an`;""",
""" document.getElementById('btot').textContent=`${bp.toFixed(0)} pb · ${mm(bp*1e-4*S.nav)} · ${(bp*4/100).toFixed(1)} % par an`;
 {const t=document.getElementById('btre');if(t){const v=mgrCash()+(S.qOps||0)-bp*1e-4*S.nav;t.textContent=mm(v);t.className=v>=0?'':'neg-g'}}""")

# ── écran du book ──
e.rep("""  <button class="cta" id="send">Passer les ordres</button>
  <p class="note" style="text-align:center">Le book est reconduit tel quel au trimestre suivant tant que vous ne le modifiez pas — seuls les changements coûtent.</p></div>`;""",
"""  <div class="kv" id="purse"></div>
  <button class="cta" id="send">Passer les ordres</button>
  <p class="note" style="text-align:center">Le book est reconduit tel quel au trimestre suivant tant que vous ne le modifiez pas — seuls les changements coûtent, et c'est vous qui les payez.</p></div>`;""")
e.rep(""" drawRows();renderRisk();
 document.getElementById('send').onclick=()=>{
   commitOrders();screenComm();window.scrollTo(0,0);
 };""",
""" drawRows();renderRisk();refreshSend();
 document.getElementById('send').onclick=()=>{
   const c=liveTC();
   if(c>0&&c>Math.max(0,mgrCash()+c)){toast("Votre société de gestion ne peut pas payer ces ordres.");return}
   commitOrders();screenComm();window.scrollTo(0,0);
 };""")
e.rep("""function drawRows(){""",
"""/* Les ordres sortent de la poche du gérant : le bouton reste bloqué tant que la caisse ne suit
   pas. Un book inchangé ne coûte rien et n'est donc jamais bloqué — pas d'impasse possible. */
function refreshSend(){
 const b=document.getElementById('send'),p=document.getElementById('purse');if(!b)return;
 const c=liveTC(),rest=mgrCash(),avail=Math.max(0,rest+c),ko=c>0&&c>avail;
 if(p)p.innerHTML=`<span>Ordres ${mm(c)} · trésorerie après paiement</span><b class="${rest>=0?'':'neg-g'}">${mm(rest)}</b>`
   +(ko?` <button class="buy" id="fitbook" style="margin-left:8px">Ramener le book au payable</button>`:'');
 b.disabled=ko;
 b.textContent=ko?`Trésorerie insuffisante : ${mm(c-avail)} de trop`:'Passer les ordres';
 const f=document.getElementById('fitbook');
 if(f)f.onclick=()=>{fitBook()};
}
/* Réduit les positions les plus chères jusqu'à ce que la facture rentre dans la caisse. */
function fitBook(){
 for(let g=0;g<400;g++){
  const c=liveTC(),avail=Math.max(0,mgrCash()+c);
  if(c<=avail)break;
  let bi=-1,bv=0;
  for(let i=0;i<N;i++){const d=S.k[i]-S.k0[i];if(Math.abs(d)<1e-9)continue;
   const t=tcost(d,i).cost;if(t>bv){bv=t;bi=i}}
  if(bi<0)break;
  S.k[bi]-=Math.sign(S.k[bi]-S.k0[bi]);
 }
 drawRows();renderRisk();refreshStatus();refreshGain();refreshSend();
 toast('Book ramené à ce que votre trésorerie permet.');
}
function drawRows(){""")
e.rep("""   updateRow(i);renderRisk();refreshStatus();refreshGain();""",
      """   updateRow(i);renderRisk();refreshStatus();refreshGain();refreshSend();""")
e.rep("""  if(am)am.onclick=()=>{S.k=[...S.modelK];drawRows();renderRisk();refreshStatus();refreshGain();toast('Book du desk appliqué — à vous de l\\'ajuster.')};""",
      """  if(am)am.onclick=()=>{S.k=[...S.modelK];drawRows();renderRisk();refreshStatus();refreshGain();refreshSend();toast('Book du desk appliqué — à vous de l\\'ajuster.')};""")

e.done("lot 2 — verrou de trésorerie")
