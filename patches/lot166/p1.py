# Lot 166 : « Le trimestre commence » et « Le desk vous attend » fusionnés en un seul écran, sans répétition ; lignes qui
# apparaissent une à une (animation courte).
s=open('index.html',encoding='utf-8').read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:90]); s=s.replace(o,n)
rep("  <ul class=\"plines\">${lines.map(l=>`<li>${l}</li>`).join('')}</ul>","  <ul class=\"plines\">${lines.map((l,i)=>`<li style=\"animation:evshow .32s ease both;animation-delay:${(i*0.07).toFixed(2)}s\">${l}</li>`).join('')}</ul>")
i=s.index("function phaseOpen(){");j=s.index("function phaseDesk(){",i)
s=s[:i]+'''function phaseOpen(){phaseDesk(1)}   /* lot 166 : un seul écran d'ouverture */
'''+s[j:]
rep("function phaseDesk(){\n save('phaseDesk');","const OUV=[\"Écrans allumés, café servi, tout est encore possible.\",\"Personne n'a encore rien perdu. Profitez-en.\",\"Le marché ouvre dans quelques minutes et ne vous attend pas.\",\"Trois mois devant vous, et une page blanche.\",\"Le desk est en place. On y va.\",\"Nouveau trimestre, compteur remis à zéro, mémoire longue chez les investisseurs.\",\"Tout le monde repart à égalité. Enfin, presque.\",\"Les positions dorment encore. Réveillez-les.\"];\nfunction phaseDesk(){\n save('phaseDesk');")
rep(" phase(`TRIMESTRE ${S.q+1} · LE DESK`,\"Le desk vous attend\",\n  [`🎯"," phase(`TRIMESTRE ${S.q+1} SUR ${QT()} · OUVERTURE`,`Le trimestre ${S.q+1} commence`,\n  [`<i>${OUV[((S.seed>>>0)+S.q*3)%OUV.length]}</i>`,`🎯")
rep("...(S.goal?[`🏅 <b>Objectif bonus : ${S.goal.nm}</b> — ${S.goal.d}`]:[]),","...(S.goal?[`🏅 <b>Objectif bonus : ${S.goal.nm}</b> — ${S.goal.d} Bonus de ${moneyB(goalBon(S.goal))} sur votre score.`]:[]),")
open('index.html','w',encoding='utf-8').write(s);print('lot166 ok')
