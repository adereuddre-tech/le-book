p='index.html';s=open(p,encoding='utf-8').read()
def rep(o,n,k=1):
    global s;c=s.count(o);assert c==k,(o[:60],c);s=s.replace(o,n)
rep("""  <div class="block"><div class="blockhead"><h2>Hauts faits de la partie</h2>""","""  ${epilogue(rank,tot)}
  <div class="block"><div class="blockhead"><h2>Hauts faits de la partie</h2>""")
rep("""function screenFinal(){""","""/* lot 273 : épilogue — que sont-ils devenus ? Une ligne par personnage, selon le parcours. */
function epilogue(rank,tot){const ch=(a,k)=>a[(hash32('epi'+k,S.seed)>>>0)%a.length],good=tot>=1.10&&!S.over,bad=!!S.over||tot<0.95,L=[];
 const me=S.over==='cash'?ch(["Vous ouvrez un cabinet de conseil en gestion des risques. Votre premier client vous demande ce que vous avez appris. Vous répondez : « la trésorerie ».","Vous écrivez un livre sur la faillite de votre société de gestion. Il se vend mieux que votre fonds."],'me')
  :S.over==='quit'?ch(["Vous rendez les clés et partez élever des chèvres dans le Larzac. Le soir, vous regardez quand même le cours du yen.","Vous rejoignez une banque privée, côté conseil. Personne ne vous demande plus de volatilité."],'me')
  :S.over?ch(["Le fonds ferme. Vous enseignez la finance de marché dans une grande école ; votre cours sur les accidents de levier fait salle comble.","Vous retournez dans une banque, à un étage où l'on ne prend pas de risque. Vous dormez mieux, paraît-il."],'me')
  :good&&rank===1?ch(["Vous lancez un deuxième fonds, plus gros. La levée est bouclée en trois semaines ; Davos vous invite à un panel sur « l'humilité en gestion ».","Un fonds souverain vous confie un mandat d'un milliard. Vous achetez une maison à Greenwich, que vous ne visitez jamais."],'me')
  :good?ch(["Le fonds continue, l'encours grossit, et les consultants vous rangent dans la colonne « solide ». C'est le plus beau compliment du métier.","Vous fêtez la fin du mandat dans un restaurant étoilé. L'addition passe en frais de gestion ; personne ne proteste."],'me')
  :bad?ch(["Les investisseurs restent, par habitude. Vous promettez « un recentrage sur nos fondamentaux », sans préciser lesquels.","Le fonds survit, amaigri. Vous passez désormais plus de temps avec le service juridique qu'avec les marchés."],'me')
  :ch(["Un mandat honnête, sans éclat. Vos investisseurs renouvellent, du bout des lèvres.","Ni gloire ni désastre : la lettre de fin de mandat tient en une page, et c'est très bien ainsi."],'me');
 L.push(['🧑‍💼','Vous',me]);
 const FATE={1:[good?"Dwight monte son propre desk de courtage à la voix. Ses clients ne l'ont jamais vu, seulement entendu.":"Dwight retourne chez un courtier ; il raconte encore votre fonds au téléphone, en exagérant."],
  2:[good?"Ingrid prend la tête des taux d'un fonds souverain nordique. Elle ne sourit toujours pas, mais elle gagne.":"Ingrid rejoint la Banque centrale. Elle vous envoie ses vœux, sans un mot de plus."],
  3:[good?"Boris vend son algorithme à une banque américaine et achète un club de hockey.":"L'algorithme de Boris est racheté pour un dollar symbolique. Boris en écrit un autre, « bien meilleur »."],
  4:[good?"Tuco achète un pétrolier d'occasion à Rotterdam et le rebaptise du nom de votre fonds.":"Tuco ouvre un restaurant de chili près du port. Les traders y viennent pour les tuyaux, pas pour le chili."],
  5:[good?"Winnie dirige le bureau de Hong Kong d'un grand fonds macro. Elle dort encore moins qu'avant.":"Winnie retourne à Hong Kong et monte une boutique sur les exotiques, sans comité des risques."],
  6:[good?"Sœur Marie-Alpha publie « Prier pour la normalité », best-seller des librairies financières.":"Sœur Marie-Alpha regagne son couvent. Elle y a installé un terminal, pour la prière du matin."],
  7:[good?"Le professeur Onésime obtient sa propre émission. Il y explique la récession, qu'il n'a toujours pas vue venir.":"Onésime est nommé dans un comité d'experts. Il y prévoit tout, avec retard."]};
 for(let p=1;p<=7;p++){if(here(p)&&FATE[p])L.push([FOP[p].ic,FOP[p].who,FATE[p][0]])}
 (gonesL()||[]).filter(g=>!here(g.p)).slice(0,2).forEach(g=>{if(FOP[g.p])L.push([FOP[g.p].ic,FOP[g.p].who,`Débauché(e) par ${g.boss||'un concurrent'} pendant le mandat, ${FOP[g.p].who} y fait carrière et ne vous rappelle pas.`])});
 const bo=S.bud&&S.bud.bo||0;L.push([BOP[bo].ic||'🏢',BOP[bo].who,bo===0?"Le loyer augmente de 12 % au renouvellement du bail. Rien d'autre n'a changé.":bo>=4?"Le back office est cité en exemple par le régulateur. Personne ne sait ce que cela veut dire, mais c'est flatteur.":"Le back office archive le mandat dans quarante-trois classeurs, rapprochés à l'euro près."]);
 const R=(S.rivals||[]).slice().sort((a,b)=>(b.cum||0)-(a.cum||0));
 if(R[0])L.push(['🏢',R[0].nm,`${R[0].boss} ${(R[0].cum||1)>tot?"termine devant vous et le fait savoir à chaque dîner en ville.":"termine derrière vous et explique à la presse que « ce n'était pas une compétition »."}`]);
 if(R.length>1){const w=R[R.length-1];L.push(['🏚️',w.nm,w.closed?`Le fonds de ${w.boss} a fermé. ${w.boss} enseigne désormais la gestion des risques.`:`${w.boss} finit dernier et se reconvertit dans les cryptoactifs.`])}
 return `<div class="block"><div class="blockhead"><h2>Que sont-ils devenus ?</h2><span class="hint">épilogue</span></div>
  ${L.map(x=>`<div class="epi"><span class="eic">${x[0]}</span><span><b>${x[1]}</b> — ${x[2]}</span></div>`).join('')}</div>`}
function screenFinal(){""")
rep(""".pwl{""",""".epi{display:flex;gap:8px;font-size:13px;line-height:1.45;margin:6px 0;color:var(--txt)}.epi .eic{flex:0 0 auto}
.pwl{""")
open(p,'w',encoding='utf-8').write(s)
