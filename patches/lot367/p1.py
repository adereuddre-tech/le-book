p="index.html";s=open(p,encoding="utf-8").read()
def rep(o,n,k=1):
    global s;c=s.count(o);assert c==k,(o[:70],c);s=s.replace(o,n)
# P2 : effets du moral renforcés (lecture, veille, anecdotes) ; sang-froid : un seul facteur, ×1,4 à 0 de moral → ×0,7 à 100,
#      sur la fréquence des accidents internes et des fuites, et sur la gravité de toutes les crises (lots 368-369)
rep("const BONREAD=[1.40,1.20,1,0.75,0.45],BONWIN=[-0.14,-0.08,0,0.08,0.20];",
    "const BONREAD=[1.80,1.40,1,0.65,0.35],BONWIN=[-0.25,-0.12,0,0.12,0.25];   /* lot 367 : ×1,4…0,45 et −14…+20 avant */\nconst BONSF=[1.40,1.20,1,0.85,0.70];   /* lot 367 : sang-froid du desk */")
rep("function motR(m){return mclp(motI(BONREAD,motX(m)),0.45,1.4)}","function motR(m){return mclp(motI(BONREAD,motX(m)),0.35,1.8)}")
rep("function motW(m){return mclp(motI(BONWIN,motX(m)),-0.14,0.20)}","function motW(m){return mclp(motI(BONWIN,motX(m)),-0.25,0.25)}\nfunction motS(m){return mclp(motI(BONSF,motX(m)),0.7,1.4)}   /* lot 367 : sang-froid — fréquence des accidents internes et des fuites, gravité des crises */")
rep(",r=Math.min(1,(bd.bo||0)/5),b=(1.25-motR())/0.5;",",r=Math.min(1,(bd.bo||0)/5),mw=mclp((motV()-50)/50,-1,1);   /* lot 367 : moral ±18 pts pour sentir, ±12 pour identifier */")
rep("+0.15*(b-0.5)+offFx('watch',0)","+0.18*mw+offFx('watch',0)")
rep("B.i+0.30*f+0.10*(b-0.5)+","B.i+0.30*f+0.12*mw+")
# affichages
rep("""['Chances des anecdotes du desk',(bonD()>=0?'+':'−')+Math.round(Math.abs(bonD())*100)+' pts'],['Risque de débauchage ce trimestre',""",
    """['Chances des anecdotes du desk',(bonD()>=0?'+':'−')+Math.round(Math.abs(bonD())*100)+' pts'],['Sang-froid : accidents internes, fuites et gravité des crises','×'+dec(motS(),2)],['Risque de débauchage ce trimestre',""")
rep("""chances des anecdotes ${bonD()>=0?'+':'−'}${Math.round(Math.abs(bonD())*100)} pts · risque de débauchage""",
    """chances des anecdotes ${bonD()>=0?'+':'−'}${Math.round(Math.abs(bonD())*100)} pts · sang-froid ×${dec(motS(),2)} · risque de débauchage""")
rep("""   ${row('Chances des anecdotes du desk',""","""   ${row('Sang-froid (accidents, fuites, crises)','×'+dec(motS(mH),2),'×'+dec(motS(mN),2))}
   ${row('Chances des anecdotes du desk',""")
rep("""anecdotes ${motW(m)>=0?'+':'−'}${Math.round(Math.abs(motW(m))*100)} pts · débauche""","""anecdotes ${motW(m)>=0?'+':'−'}${Math.round(Math.abs(motW(m))*100)} pts · sang-froid ×${dec(motS(m),2)} · débauche""")
rep("coûts ×0,45, bruit de lecture ×0,45, anecdotes +20 pts, débauchage 0 %","coûts ×0,45, bruit de lecture ×0,35, anecdotes +25 pts, sang-froid ×0,7, débauchage 0 %")
rep("Le moral fixe quatre choses : un multiplicateur sur vos coûts d'impact de marché (ni la demi-fourchette ni le courtage), la précision de la lecture des dépêches, les chances de gagner des anecdotes du desk et le risque de débauchage.",
    "Le moral fixe cinq choses : un multiplicateur sur vos coûts d'impact de marché (ni la demi-fourchette ni le courtage), la précision de la lecture des dépêches et de la veille des extrêmes, les chances de gagner des anecdotes du desk, le sang-froid (fréquence des accidents internes et des fuites, gravité des accidents et des crises, ×1,4 à 0, ×0,7 à 100) et le risque de débauchage.")
open(p,"w",encoding="utf-8").write(s)
