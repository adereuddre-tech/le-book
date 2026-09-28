# Lot 94c : neuf anecdotes de milieu de trimestre pour le back office (Maître Lettrage, Josiane Suspens, l'inspecteur
# Tatillon), tirées seulement si la personne est dans l'équipe. Effets classiques : comité, confiance, trésorerie,
# coûts du trimestre, débauchage, risque binaire.
s=open('index.html',encoding='utf-8').read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:90]); s=s.replace(o,n)
A=r'''const TRADER_MID=[
 {who:"Maître Lettrage · expert-comptable",t:"« Vos frais de taxi de Londres n'ont aucun justificatif »",p:"Maître Lettrage a épinglé une note de frais de Boris. Quatorze courses, un seul reçu, en cyrillique.",
  ch:[{b:"Rembourser quand même",s:"−2 pb, le desk apprécie : débauchage −10 %.",e:{cash:-0.0002,poach:-0.1}},{b:"Refuser le remboursement",s:"Comité +2, débauchage +10 %.",e:{rc:2,poach:0.1}}]},
 {who:"Maître Lettrage · expert-comptable",t:"« La clôture comptable a trois jours de retard »",p:"Les investisseurs attendent leur valeur liquidative. Maître Lettrage propose des intérimaires, ou de tout signer lui-même cette nuit.",
  ch:[{b:"Payer les intérimaires",s:"−3 pb, investisseurs +1.",e:{cash:-0.0003,lp:1}},{b:"Le laisser signer cette nuit",s:"25 % de risque d'erreur de valorisation : −0,2 %.",e:{risk:[0.25,-0.002],riskMsg:"Une ligne de swap valorisée deux fois",safeTxt:"Tout tombe juste. Il a dormi sur place."}},{b:"Publier en retard",s:"Investisseurs −2.",e:{lp:-2}}]},
 {who:"Maître Lettrage · expert-comptable",t:"« Le fisc luxembourgeois nous pose une question »",p:"« Une seule. Elle fait onze pages. »",
  ch:[{b:"Prendre un cabinet",s:"−4 pb, comité +2.",e:{cash:-0.0004,rc:2}},{b:"Répondre nous-mêmes",s:"20 % de risque de redressement : −0,3 %.",e:{risk:[0.2,-0.003],riskMsg:"Le fisc n'a pas aimé la page sept",safeTxt:"Réponse acceptée sans commentaire."}}]},
 {who:"Josiane Suspens · back office",t:"« Trois opérations d'hier ne sont toujours pas rapprochées »",p:"Josiane Suspens tient un tableau des suspens. Il est rouge. « Soit on appelle les contreparties une par une, soit on attend qu'elles se manifestent. »",
  ch:[{b:"Appeler une par une",s:"−1 pb, comité +2.",e:{cash:-0.0001,rc:2}},{b:"Attendre",s:"30 % de risque de pénalité de règlement : −0,15 %.",e:{risk:[0.3,-0.0015],riskMsg:"Un défaut de livraison facturé",safeTxt:"Les contreparties rappellent d'elles-mêmes."}}]},
 {who:"Josiane Suspens · back office",t:"« Le dépositaire change de système ce week-end »",p:"« Ils disent que rien ne changera. Ils disent toujours ça. »",
  ch:[{b:"Doubler les contrôles lundi",s:"Coûts +3 %, comité +2.",e:{tcMult:1.03,rc:2}},{b:"Leur faire confiance",s:"25 % de risque de règlement raté : −0,2 %.",e:{risk:[0.25,-0.002],riskMsg:"Des titres livrés au mauvais compte",safeTxt:"Lundi, tout est là."}}]},
 {who:"Josiane Suspens · back office",t:"« Quelqu'un a saisi 10 000 contrats au lieu de 1 000 »",p:"Elle l'a vu avant l'envoi. « Je ne dis pas qui. Mais c'est la troisième fois que c'est le même. »",
  ch:[{b:"Installer une double validation",s:"Coûts +2 %, comité +3.",e:{tcMult:1.02,rc:3}},{b:"La remercier et passer à autre chose",s:"Comité +1.",e:{rc:1}}]},
 {who:"L'inspecteur Tatillon · conformité",t:"« Qui a déjeuné avec le trésorier d'une banque centrale ? »",p:"L'inspecteur Tatillon a trouvé une note de restaurant. Il ne soupçonne personne. Il veut juste un nom.",
  ch:[{b:"Ouvrir une enquête interne",s:"−2 pb, comité +4, débauchage +10 %.",e:{cash:-0.0002,rc:4,poach:0.1}},{b:"C'était un déjeuner amical",s:"Comité −2.",e:{rc:-2}}]},
 {who:"L'inspecteur Tatillon · conformité",t:"« Votre lettre aux investisseurs contient le mot garanti »",p:"« Une seule fois, page trois. Il suffit d'une fois. »",
  ch:[{b:"Corriger et renvoyer",s:"Investisseurs −1, comité +3.",e:{lp:-1,rc:3}},{b:"Laisser, personne ne lit la page trois",s:"20 % de risque de rappel à l'ordre : −0,2 %.",e:{risk:[0.2,-0.002],riskMsg:"Le régulateur lit la page trois",safeTxt:"Personne ne lit la page trois."}}]},
 {who:"L'inspecteur Tatillon · conformité",t:"« J'ai relu tous vos contrats de courtage »",p:"« Tous. Un de vos courtiers vous facture une recherche que personne ne lit. »",
  ch:[{b:"Renégocier",s:"Coûts −4 %, comité +1.",e:{tcMult:0.96,rc:1}},{b:"Garder : ils nous invitent à Wimbledon",s:"Comité −3.",e:{rc:-3}}]},
'''
rep("const TRADER_MID=[\n",A)
rep("function persoOk(e){if(/Marie-Alpha/.test(e.who||'')&&!here(6))return false;","function persoOk(e){const w=e.who||'';if(/Marie-Alpha/.test(w)&&!here(6))return false;if((/Lettrage/.test(w)&&S.bud.bo<1)||(/Josiane/.test(w)&&S.bud.bo<2)||(/Tatillon/.test(w)&&S.bud.bo<4))return false;")
open('index.html','w',encoding='utf-8').write(s);print('ok')
