p="index.html";s=open(p,encoding="utf-8").read()
def rep(o,n,k=1):
    global s;c=s.count(o);assert c==k,(o[:70],c);s=s.replace(o,n)
# intuition intégrée étendue : Sir Mervyn (liquidité, 85 %), Priya (une action, 85 %), traders (+2 pts de fiabilité sur leur classe)
rep("""S.vic={q:S.q,k,up}}""","""S.vic={q:S.q,k,up}}
 if(here(9)&&S.f){const k=2,ok=prng32(hash32('mer'+S.q,S.seed))()<0.85,up=(S.f[k]>0)===ok;   /* lot 336 : Sir Mervyn */
  (S.pwTips=S.pwTips||[]).push({who:'Sir Mervyn',nm:`Le facteur « ${FACT[k].nm.toLowerCase()} »`,up:up===(FSG[k]>0),q:S.q,fk:k});S.mer={q:S.q,k,up}}""")
rep(""" genRumors();
 let pInc=""",""" genRumors();
 if(here(8)){const t=pwTip('Actions',0.85,'Priya');if(t)(S.pwTips=S.pwTips||[]).push(Object.assign(t,{q:S.q}))}   /* lot 336 : Priya */
 let pInc=""")
rep("""function pwTip(cls,rel,who){const c=[];for(let i=0;i<N;i++)if(mktOpen(i)&&INSTR[i].grp===cls)c.push(i);""","""function pwTip(cls,rel,who){const c=[];for(let i=0;i<N;i++)if(mktOpen(i)&&INSTR[i].grp===cls&&!tipOf(i))c.push(i);""")
rep(""" if(S.vic&&S.vic.q===S.q)f[S.vic.k]+=(S.vic.up?1:-1)*VICW;""",""" if(S.vic&&S.vic.q===S.q)f[S.vic.k]+=(S.vic.up?1:-1)*VICW;
 if(S.mer&&S.mer.q===S.q)f[S.mer.k]+=(S.mer.up?1:-1)*MERW;   /* lot 336 : Sir Mervyn, juste 85 fois sur 100 */""")
rep("""var HUNCHW=1.4,VICW=1.85;""","""var HUNCHW=1.4,VICW=1.85,MERW=1.63;""")
rep(""" if(S.vic&&S.vic.q===S.q)f[S.vic.k]+=(S.vic.up?1:-1)*1.37;""",""" if(S.vic&&S.vic.q===S.q)f[S.vic.k]+=(S.vic.up?1:-1)*1.37;
 if(S.mer&&S.mer.q===S.q)f[S.mer.k]+=(S.mer.up?1:-1)*1.2;""")
rep("""&&!S.hunch&&!(S.vic&&S.vic.q===S.q))return null;""","""&&!S.hunch&&!(S.vic&&S.vic.q===S.q)&&!(S.mer&&S.mer.q===S.q))return null;""")
rep(""" if(rs)rs.innerHTML=(b.length||(S.vic&&S.vic.q===S.q))?""",""" if(rs)rs.innerHTML=(b.length||(S.vic&&S.vic.q===S.q)||(S.mer&&S.mer.q===S.q))?""")
rep(""" if(rs&&S.hunch)rs.innerHTML+=""",""" if(rs&&S.mer&&S.mer.q===S.q)rs.innerHTML+=`<p class="note" style="margin:8px 0 0">🏛️ <b>Sir Mervyn</b> : <b>${FACT[S.mer.k].nm.toLowerCase()}</b> va surprendre ${(S.mer.up===(FSG[S.mer.k]>0))?'à la hausse':'à la baisse'} ce trimestre — juste 85 fois sur 100, déjà dans la lecture du desk.</p>`;
 if(rs&&S.hunch)rs.innerHTML+=""")
rep("""pw:"bruit des signaux tendance, portage et valeur ×0,75\"""","""pw:"bruit des signaux tendance, portage et valeur ×0,75 ; chaque trimestre, le sens d'une action ou d'un indice, juste 85 fois sur 100, déjà dans votre attendu\"""")
rep("""pw:"sur les dépêches de banques centrales et de taux, la probabilité de suite est donnée exacte\"""","""pw:"sur les dépêches de banques centrales et de taux, la probabilité de suite est donnée exacte ; chaque trimestre, le sens de la liquidité, juste 85 fois sur 100, déjà dans la lecture du desk\"""")
# sources : le trader de la classe la plus touchée ajoute 2 points de fiabilité
rep("""   const p=Math.max(0.35,Math.min(0.95,RELP[r.rel]+relB));""","""   const tr=rumTrd(r.v),p=Math.max(0.35,Math.min(0.95,RELP[r.rel]+relB+(tr?0.02:0)));""")
rep("""   used.add(r.t);out.push({...r,truth:wantTrue,p});""","""   used.add(r.t);out.push({...r,truth:wantTrue,p,trd:tr||undefined});""")
rep("""function genRumors(){""","""/* lot 336 : la classe la plus touchée par une rumeur ; si son trader est là, il en connaît les acteurs (+2 pts de fiabilité) */
function rumTrd(v){let bi=-1,bv=0;for(let i=0;i<N;i++){const z=Math.abs(INSTR[i].b.reduce((a,b,k)=>a+b*(v[k]||0),0));if(z>bv){bv=z;bi=i}}
 if(bi<0)return null;const p=TRD[INSTR[bi].grp];return p!==undefined&&here(p)?FOP[p].who:null}
function genRumors(){""")
rep("""${r.sure?'<i class="sure">✓ vérifiée</i>':''}""","""${r.sure?'<i class="sure">✓ vérifiée</i>':''}${r.trd?`<i>+2 pts · ${r.trd}</i>`:''}""")
open(p,'w',encoding='utf-8').write(s)
