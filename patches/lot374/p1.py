import re
p="index.html";s=open(p,encoding="utf-8").read()
def rep(o,n,k=1):
    global s;c=s.count(o);assert c==k,(o[:70],c);s=s.replace(o,n)
# Accueil et création du fonds : qui paie quoi, accidents, coûts d'impact, capital de départ à jour (lot 348 : ×0,8)
a=s.index("const PROFILES=[");b=s.index("const SIZES=[")
blk=s[a:b]
blk=blk.replace("capital de départ +0,5 M$","capital de départ +0,4 M$").replace("capital de départ +1 M$","capital de départ +0,8 M$")
blk=blk.replace("coûts d'exécution","coûts d'impact").replace("coûts de transaction","coûts d'impact")
s=s[:a]+blk+s[b:]
rep("""Votre société paie l'équipe, les ordres et les bonus.`;""","""Votre société paie l'équipe, le courtage et les bonus ; le fonds paie la fourchette et l'impact de vos ordres.`;""")
rep("""commissions de gestion et de performance, moins l'équipe, les ordres et les bonus.""","""commissions de gestion et de performance, moins l'équipe, le courtage et les bonus.""")
rep("""Chocs</b><span>Le prime broker vérifie la marge après chaque événement. Des événements extrêmes peuvent frapper chaque trimestre ; votre veille les sent venir de 10 à 95 % des fois, selon votre style, vos équipes et leur moral, et une protection s'achète en début de trimestre.""",
    """Chocs</b><span>Événements extrêmes, accidents de levier, appels de marge : un choc peut frapper chaque trimestre, plus souvent et plus fort quand votre risque monte. Votre veille sent venir les extrêmes, et une protection s'achète en début de trimestre.""")
rep("""Chaque changement de position paie une demi-fourchette plus un impact qui croît en racine carrée du notionnel (plus vite dans les carnets étroits). La facture entière est ensuite freinée par la taille : au-delà de 100 M$ d'encours, × (encours / 100 M$)<sup>0,35</sup> — deux fois plus cher à 700 M$. Elle est multipliée par votre front office, votre style, le moral du desk, la liquidité du régime et le taux au jour le jour ; sans trader sur la classe, l'ordre passe par un courtier, ×3.""",
    """Chaque changement de position paie une demi-fourchette plus un impact qui croît en racine carrée du notionnel (plus vite dans les carnets étroits). L'impact est freiné par la taille : au-delà de 100 M$ d'encours, × (encours / 100 M$)<sup>0,35</sup> — deux fois plus cher à 700 M$. Il est multiplié par votre front office, votre style, le moral du desk, la liquidité du régime et le taux au jour le jour ; sans trader sur la classe, l'ordre passe par un courtier, ×3. Le fonds paie fourchette et impact ; votre société paie le courtage, ${dec(COMB,1)} pb du notionnel.""")
rep("""["Coûts d'exécution",p=>f(p.tcMult)]""","""["Coûts d'impact",p=>f(p.tcMult)]""")
open(p,"w",encoding="utf-8").write(s)
