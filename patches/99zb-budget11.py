# -*- coding: utf-8 -*-
"""Lot 39 — le budget d'exploitation passe de 3 crans à 11.

Demande : onze crans par poste, le minimum inchangé, le maximum doublé — 100 / 48 / 128 pb.
Les anciens niveaux restent des crans de l'échelle, aux mêmes prix et avec exactement les mêmes
effets : **cran 0 = ancien réduit, cran 4 = ancien standard, cran 8 = ancien renforcé**. Tout ce
qui a été calibré aux lots 30 à 36 reste donc valable, et les deux crans au-delà (9 et 10)
prolongent chaque bénéfice nettement plus vite que la simple prolongation de la pente —
le prix double, il fallait que l'effet suive : coûts ×0,30, incidents ×0,04, bande ±60 %,
comité +4 par trimestre, 16 sources, lecture des dépêches à ±2 points.

  salle de marché   2 · 6 · 10 · 14 · [18] · 24 · 32 · 40 · [50] · 72 · 100 pb
  contrôle          4 · 6 ·  8 · 10 · [12] · 15 · 18 · 21 · [24] · 34 ·  48 pb
  recherche         4 · 8 · 12 · 15 · [18] · 26 · 36 · 48 · [64] · 92 · 128 pb

Chaque bénéfice devient un tableau de onze valeurs, monotone, qui passe exactement par les
anciennes aux crans 0 / 4 / 8 : coûts d'exécution, débauchage, finesse des indicateurs,
fréquence et gravité des incidents, bande du comité, avis trimestriel du comité, nombre et
fiabilité des sources, pré-annonces, précision de la lecture des dépêches, et la chance de
recruter une recrue du trimestre — qui n'existait qu'au cran maximum et devient progressive à
partir du cran 5.

Les textes d'effets ne sont plus écrits à la main mais **calculés à partir de ces tableaux**
(`budEf`) : trente-trois libellés recopiés auraient fini par mentir, et l'invariant 9 vaut aussi
pour l'écran du budget.

Écran : le nom du cran sort des boutons — chaque bouton ne porte plus que son coût, en points de
base et en monnaie — et le nom du cran choisi, son rang et ses effets s'affichent au-dessus de la
rangée. Onze boutons sur deux rangées de six et cinq : à 380 px, chacun garde 55 px de large.

Sauvegardes : une partie d'avant ce lot porte des crans 0/1/2 ; `loadGame` les remonte sur
l'échelle (0 → 0, 1 → 4, 2 → 8), sans quoi un joueur en cours de partie se serait réveillé avec
un budget divisé par trois.
"""
import sys; sys.path.insert(0,'patches')
from _lib import Ed
e=Ed()
def between(a,b):
    assert e.s.count(a)==1,'debut ambigu %r'%a[:60]
    i=e.s.index(a); j=e.s.index(b,i); return e.s[i:j]

NM=["Minimal","Réduit","Serré","Sobre","Standard","Étoffé","Confortable","Soutenu","Renforcé","Ambitieux","Sans limite"]
BP={'exec':[2,6,10,14,18,24,32,40,50,72,100],
    'risk':[4,6,8,10,12,15,18,21,24,34,48],
    'res' :[4,8,12,15,18,26,36,48,64,92,128]}
def lv(id):
    return "[%s]"%",".join("{nm:%r,bp:%d}"%(NM[i],BP[id][i]) for i in range(11)).replace("'",'"')

# ── 1. les trois échelles ───────────────────────────────────────────────────────
old=between("const BUDGET=[","const EXECM=")
new=old
for id_ in ('exec','risk','res'):
    i=new.index("lv:[",new.index("id:'%s'"%id_))
    j=new.index("]}",i)+1
    new=new[:i]+"lv:"+lv(id_)+new[j:]
e.rep(old,new)

# ── 2. les bénéfices, onze valeurs, anciennes aux crans 0 / 4 / 8 ──────────────
old=between("const EXECM=","function bandNow()")
e.rep(old,"""const EXECM=[1.35,1.15,1.00,0.87,0.75,0.69,0.63,0.57,0.50,0.40,0.30],   /* lot 38 : trois quarts de l'ancienne facture, le reste se paie en impact de marché */
RISKM=[2.20,1.80,1.50,1.22,1.00,0.70,0.48,0.32,0.20,0.10,0.04],
RISKS=[2.00,1.85,1.72,1.60,1.50,1.28,1.10,0.92,0.75,0.60,0.45],
RETM =[2.00,1.70,1.45,1.20,1.00,0.80,0.63,0.46,0.30,0.15,0.08];
const RESN=[6,7,8,8,9,10,10,11,12,14,16],
RESREL=[-0.08,-0.06,-0.04,-0.02,0,0.02,0.04,0.06,0.08,0.12,0.16],
RESR  =[0.30,0.37,0.45,0.52,0.60,0.70,0.79,0.87,0.95,0.98,1.00],
/* précision de la lecture d'une dépêche : écart-type du bruit sur la probabilité affichée */
RESPH =[0.16,0.145,0.13,0.115,0.10,0.088,0.076,0.064,0.05,0.030,0.020];
/* la finesse des indicateurs vient du desk, la tolérance du comité du contrôle des risques */
const TCVQ=[0.90,0.82,0.74,0.67,0.60,0.53,0.47,0.41,0.35,0.26,0.18],
BANDB=[0.18,0.19,0.21,0.23,0.25,0.28,0.31,0.35,0.40,0.50,0.60];
/* avis du comité à chaque clôture, et chance de recruter une recrue du trimestre */
const RISKRC=[-1,-0.8,-0.6,-0.3,0,0.5,1,1.5,2,3,4],
STARP=[0,0,0,0,0,0.08,0.15,0.22,0.30,0.45,0.60];
const BUDMAX=8;   /* à partir de ce cran, un budget est « renforcé » pour les objectifs */
/* Les effets affichés sont calculés à partir des tableaux ci-dessus : aucun libellé ne peut
   diverger de ce qui est appliqué. */
function budEf(id,i){
 if(id==='exec'){const q=TCVQ[i];
  return `coûts ×${dec(EXECM[i],2)} · débauchage ×${dec(RETM[i],2)} · indicateurs ${q>0.78?'très bruités':q>0.62?'bruités':q>0.45?'corrects':q>0.32?'précis':'très précis'}`
   +(STARP[i]?` · recrue du trimestre ${Math.round(STARP[i]*100)} %`:'')}
 if(id==='risk')return `incidents ×${dec(RISKM[i],2)} · gravité ×${dec(RISKS[i]/RISKS[4],2)} · bande du comité ±${Math.round(BANDB[i]*100)} %`
   +(Math.abs(RISKRC[i])>=0.05?` · comité ${RISKRC[i]>0?'+':'−'}${dec(Math.abs(RISKRC[i]),1)} par trimestre`:'');
 return `${RESN[i]} sources · fiabilité ${Math.abs(RESREL[i])<0.005?'de référence':(RESREL[i]>0?'+':'−')+Math.round(Math.abs(RESREL[i])*100)+' pts'} · pré-annonces ${Math.round(RESR[i]*100)} % · lecture des dépêches ±${Math.round(RESPH[i]*100)} pts`;
}
""")

# ── 3. les points du code qui parlaient encore en 0 / 1 / 2 ────────────────────
e.rep("const pr=PROF(),sd=[0.16,0.10,0.05][S.bud.res]*(pr.id==='flux'?0.6:1);",
      "const pr=PROF(),sd=RESPH[S.bud.res]*(pr.id==='flux'?0.6:1);")
e.rep(" if(S.bud.exec===2&&rng()<0.30)S.star=Math.floor(rng()*N);",
      " if(STARP[S.bud.exec]>0&&rng()<STARP[S.bud.exec])S.star=Math.floor(rng()*N);")
e.rep("S.bud.ret===2&&rng()<0.4","S.bud.ret>=BUDMAX&&rng()<0.4")
e.rep("""${S.bud.risk===2?" Le contrôle renforcé a détecté l'incident tô""",
      """${S.bud.risk>=BUDMAX?" Le contrôle renforcé a détecté l'incident tô""")
Q=chr(92)+"'"
e.rep(" if(S.bud.risk!==1)rcD.push([S.bud.risk>1?'Contrôle des risques renforcé : rapports rassurants':'Contrôle des risques réduit : le comité s"+Q+"inquiète',S.bud.risk>1?2:-1]);",
      " if(Math.abs(RISKRC[S.bud.risk])>=0.05)rcD.push([RISKRC[S.bud.risk]>0?'Contrôle des risques renforcé : rapports rassurants':'Contrôle des risques réduit : le comité s"+Q+"inquiète',RISKRC[S.bud.risk]]);")
# objectifs et hauts faits : « au maximum » devient « au cran renforcé ou au-delà »
e.rep("t:c=>c.budRes===2&&c.rel>0","t:c=>c.budRes>=8&&c.rel>0")
e.rep("t:c=>c.budExec===2&&c.tcBp<22","t:c=>c.budExec>=8&&c.tcBp<22")
e.rep("tq:c=>c.budRes===2&&c.q>0","tq:c=>c.budRes>=8&&c.q>0")

# ── 4. départ au cran standard, et reprise d'une sauvegarde à trois crans ──────
e.rep("   bud:{exec:1,risk:1,res:1,ret:1},goal:null,","   bud:{exec:4,risk:4,res:4,ret:4},budN:11,goal:null,")
e.rep("  S=d;fundName=d.fundName;",
      "  S=d;fundName=d.fundName;\n"
      "  /* sauvegarde d'avant le lot 39 : trois crans 0/1/2 à remonter sur l'échelle de onze */\n"
      "  if(!S.budN&&S.bud){const M3=[0,4,8];for(const k in S.bud)S.bud[k]=M3[S.bud[k]]!==undefined?M3[S.bud[k]]:4;S.budN=11}")

# ── 5. l'écran : coût dans le bouton, nom du cran au-dessus ────────────────────
e.rep("""   <div class="lvls">${b.lv.map((l,i)=>`<button class="lvl ${S.bud[b.id]===i?'on':''}" data-b="${b.id}" data-i="${i}"${ok(b.id,i)?'':' disabled'}>
     <b>${l.nm}</b><span>${ok(b.id,i)?l.bp+' pb':'hors caisse'}</span></button>`).join('')}</div>
   <details style="margin-top:8px"><summary>Détails</summary><ul class="efl">${b.lv.map(l=>`<li><b>${l.nm}</b> · ${l.bp} pb · ${l.ef}</li>`).join('')}</ul></details></div>`).join('');""",
"""   <div class="lvsel"><b>${b.lv[S.bud[b.id]].nm}</b><span>cran ${S.bud[b.id]+1} sur ${b.lv.length}</span></div>
   <div class="lvls">${b.lv.map((l,i)=>`<button class="lvl ${S.bud[b.id]===i?'on':''}" data-b="${b.id}" data-i="${i}"${ok(b.id,i)?'':' disabled'} title="${l.nm}${ok(b.id,i)?'':' · hors caisse'}">
     <b>${l.bp}</b><span>${ok(b.id,i)?mm(l.bp*1e-4*S.nav):'—'}</span></button>`).join('')}</div>
   <div class="lvef">${budEf(b.id,S.bud[b.id])}</div>
   <details style="margin-top:8px"><summary>Les onze crans</summary><ul class="efl">${b.lv.map((l,i)=>`<li><b>${l.nm}</b> · ${l.bp} pb · ${budEf(b.id,i)}</li>`).join('')}</ul></details></div>`).join('');""")
e.rep("  toast(`${bb.nm} → <b>${lv.nm}</b> · ${lv.ef} · budget ${b0.toFixed(0)} → <b>${",
      "  toast(`${bb.nm} → <b>${lv.nm}</b> · ${budEf(bb.id,+x.dataset.i)} · budget ${b0.toFixed(0)} → <b>${")
e.rep(".lvls{display:grid;grid-template-columns:1fr 1fr 1fr;gap:5px}",
      ".lvls{display:grid;grid-template-columns:repeat(6,1fr);gap:4px}\n"
      ".lvsel{display:flex;justify-content:space-between;align-items:baseline;margin:2px 0 5px}\n"
      ".lvsel b{font-size:13.5px;color:var(--gold)}\n"
      ".lvsel span{font-family:var(--mono);font-size:10.5px;color:var(--dimmer)}\n"
      ".lvef{font-family:var(--mono);font-size:11px;color:var(--dim);margin-top:6px;line-height:1.5}")
e.rep(".lvl{padding:8px 6px;border-radius:5px;background:var(--panel2);border:1px solid transparent;text-align:center}",
      ".lvl{padding:6px 2px;border-radius:5px;background:var(--panel2);border:1px solid transparent;text-align:center}")
e.rep(".lvl b{display:block;font-size:12.5px;font-weight:500}",
      ".lvl b{display:block;font-family:var(--mono);font-size:12.5px;font-weight:600}")
e.rep(".lvl span{font-family:var(--mono);font-size:10.5px;color:var(--dimmer)}",
      ".lvl span{font-family:var(--mono);font-size:9.5px;color:var(--dimmer);white-space:nowrap}")
e.done("lot 39 — budget a onze crans")
