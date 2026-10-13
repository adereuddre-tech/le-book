p="index.html";s=open(p,encoding="utf-8").read()
def rep(o,n,k=1):
    global s;c=s.count(o);assert c==k,(o[:70],c);s=s.replace(o,n)
# les tuyaux entrent d'office dans les prévisions : Victoria dans la lecture des facteurs, les marchés annoncés dans l'attendu
rep("""up=(S.rBase[i]>0)===(u<rel);return {who,sym:INSTR[i].sym,nm:INSTR[i].nm,up}}""","""up=(S.rBase[i]>0)===(u<rel);return {who,sym:INSTR[i].sym,nm:INSTR[i].nm,up,rel,i}}""")
rep("""  (S.pwTips=S.pwTips||[]).push({who:'Victoria',nm:`Le facteur « ${FACT[k].nm.toLowerCase()} »`,up:up===(FSG[k]>0),q:S.q})}""",
    """  (S.pwTips=S.pwTips||[]).push({who:'Victoria',nm:`Le facteur « ${FACT[k].nm.toLowerCase()} »`,up:up===(FSG[k]>0),q:S.q,fk:k});S.vic={q:S.q,k,up}}""")
rep(""" if(S.hunch&&HUNCHW)f[S.hunch.k]+=(S.hunch.up?1:-1)*HUNCHW;   /* lot 77 */""",""" if(S.hunch&&HUNCHW)f[S.hunch.k]+=(S.hunch.up?1:-1)*HUNCHW;   /* lot 77 */
 if(S.vic&&S.vic.q===S.q)f[S.vic.k]+=(S.vic.up?1:-1)*VICW;   /* lot 331 : l'intuition de Victoria, juste neuf fois sur dix */""")
rep("""var HUNCHW=1.4;""","""var HUNCHW=1.4,VICW=1.85;   /* Victoria : même calibrage, à 90 % au lieu de 80 % */""")
rep(""" if(S.hunch)f[S.hunch.k]+=(S.hunch.up?1:-1)*1.03;
""",""" if(S.hunch)f[S.hunch.k]+=(S.hunch.up?1:-1)*1.03;
 if(S.vic&&S.vic.q===S.q)f[S.vic.k]+=(S.vic.up?1:-1)*1.37;
""")
rep(""" if(!(S.rumors||[]).some(r=>r.bought)&&!S.hunch)return null;""",""" if(!(S.rumors||[]).some(r=>r.bought)&&!S.hunch&&!(S.vic&&S.vic.q===S.q))return null;""")
rep(""" if(rs)rs.innerHTML=b.length?""",""" if(rs)rs.innerHTML=(b.length||(S.vic&&S.vic.q===S.q))?""")
rep(""" if(rs&&S.hunch)rs.innerHTML+=""",""" if(rs&&S.vic&&S.vic.q===S.q)rs.innerHTML+=`<p class="note" style="margin:8px 0 0">🏛️ <b>Victoria</b> : <b>${FACT[S.vic.k].nm.toLowerCase()}</b> va surprendre ${(S.vic.up===(FSG[S.vic.k]>0))?'à la hausse':'à la baisse'} ce trimestre — juste neuf fois sur dix, déjà dans la lecture du desk.</p>`;
 if(rs&&S.hunch)rs.innerHTML+=""")
# attendu d'un marché : un tuyau sur son sens le recale (loi a posteriori d'une gaussienne sachant un signal juste à r)
rep(""" v+=(x.idio||0)**2;
 return {m:x.sigQ*z+kap(i,f[3]||0),s:x.sigQ*Math.sqrt(v)};
}""",""" v+=(x.idio||0)**2;
 return tipPost(i,x.sigQ*z+kap(i,f[3]||0),x.sigQ*Math.sqrt(v));
}
function tipOf(i){return (S.pwTips||[]).find(t=>t.q===S.q&&t.i===i&&t.rel)}
function tipPost(i,m,s){const t=tipOf(i);if(!t||!(s>1e-9))return {m,s,m0:m};
 const a=m/s,P=nCdf(a),ph=Math.exp(-a*a/2)/Math.sqrt(2*Math.PI),ru=t.up?t.rel:1-t.rel,rd=1-ru,Z=ru*P+rd*(1-P);
 const E1=ru*(m*P+s*ph)+rd*(m*(1-P)-s*ph),E2=ru*((m*m+s*s)*P+m*s*ph)+rd*((m*m+s*s)*(1-P)-m*s*ph),mp=E1/Z;
 return {m:mp,s:Math.sqrt(Math.max(1e-12,E2/Z-mp*mp)),m0:m,tip:t}}""")
rep("""  t:x.sigQ*SIGW.t*(e.t[i]||0)*ed,c:x.sigQ*SIGW.c*(e.c[i]||0)*ed,v:x.sigQ*SIGW.v*cv*(e.v[i]||0)*ed,cv,drift:kap(i,f[3]||0)};""",
    """  t:x.sigQ*SIGW.t*(e.t[i]||0)*ed,c:x.sigQ*SIGW.c*(e.c[i]||0)*ed,v:x.sigQ*SIGW.v*cv*(e.v[i]||0)*ed,cv,drift:kap(i,f[3]||0),tipT:tipOf(i),tip:(R=>R.m-R.m0)(expRet(i))};""")
rep("""    ...(Math.abs(XP.drift)>1e-6?[['Portage · structurel',KAPPA[x.sym]&&KAPPA[x.sym][1]?'selon l\\'appétit':'connu',pc(XP.drift)]]:[]),""",
    """    ...(Math.abs(XP.drift)>1e-6?[['Portage · structurel',KAPPA[x.sym]&&KAPPA[x.sym][1]?'selon l\\'appétit':'connu',pc(XP.drift)]]:[]),
    ...(XP.tipT?[[`Tuyau de ${XP.tipT.who}`,`${XP.tipT.up?'▲ hausse':'▼ baisse'} · ${Math.round(XP.tipT.rel*100)} %`,pc(XP.tip)]]:[]),""")
rep("""${tips.map(t=>`<div class="flag" style="margin:0 0 8px"><span>📌 <b>${t.who}</b> : ${t.nm} finira le trimestre en <b>${t.up?'hausse':'baisse'}</b>.</span></div>`).join('')}""",
    """${tips.map(t=>`<div class="flag" style="margin:0 0 8px"><span>📌 <b>${t.who}</b> : ${t.nm} finira le trimestre en <b>${t.up?'hausse':'baisse'}</b> — déjà dans ${t.fk!=null?'la lecture des facteurs':'votre attendu'}.</span></div>`).join('')}""")
open(p,'w',encoding='utf-8').write(s)
