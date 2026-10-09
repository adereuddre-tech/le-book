p='index.html';s=open(p,encoding='utf-8').read()
def rep(o,n,k=1):
    global s;c=s.count(o);assert c==k,(o[:60],c);s=s.replace(o,n)
rep("""const app=document.getElementById('app');""","""const app=document.getElementById('app');
/* lot 267 : glossaire au toucher — la première occurrence d'un terme dans chaque note devient soulignée ; un toucher ouvre sa définition */
const GLOSS={
 'portage':"Ce que rapporte une position si les prix ne bougent pas : l'écart de taux entre deux devises, la pente d'une courbe, le coût de stockage d'une matière première.",
 'tendance':"Le signal qui parie que ce qui a monté continuera de monter. Il gagne dans les marchés qui bougent longtemps dans le même sens, perd dans les retournements.",
 'fourchette':"L'écart entre le prix auquel on peut acheter et celui auquel on peut vendre. Chaque ordre en paie la moitié.",
 'impact de marché':"Le prix qui bouge contre vous pendant que vous exécutez : plus l'ordre est gros par rapport au carnet, plus il pèse.",
 'unité de risque':"La taille standard d'une position : 2,5 % de volatilité annuelle à elle seule, quel que soit le marché.",
 'gate':"Clause qui limite les rachats d'un trimestre à une part de l'encours ; le reste attend le trimestre suivant. Les investisseurs n'aiment pas.",
 'surlevier':"Au-delà de ±3 unités, le notionnel dépasse ce que le marché absorbe sans broncher : marge, impact et risque d'accident montent vite.",
 'vol ex-ante':"La volatilité attendue du book avant qu'il ne bouge, calculée sur les corrélations entre marchés.",
 'collatéral':"Le cash du fonds déposé en garantie ou placé en attendant ; il rapporte le taux du jour, plus ce que rapporte le placement choisi.",
 'appel de marge':"Le prime broker exige plus de garanties quand la marge utilisée dépasse son seuil : apporter du cash ou couper le book.",
 'commission de performance':"La part des gains du fonds au-dessus de son plus haut historique qui revient au gérant.",
 'plus haut historique':"Le meilleur niveau atteint par le fonds ; tant qu'il n'est pas dépassé, pas de commission de performance.",
 'carton jaune':"Avertissement du comité des risques ; deux jaunes font un rouge, qui impose des contraintes le trimestre suivant.",
 'contre-pied':"Prendre la position inverse du mouvement ou de la foule : on fournit la liquidité que les autres cherchent.",
 'événement extrême':"Un choc rare et violent (guerre, krach, faillite d'une banque, squeeze…), calculé sur votre book. La veille peut le sentir venir ; une protection s'achète en début de trimestre.",
 'drain de volatilité':"Ce qu'une forte volatilité coûte à la performance composée : perdre 50 % puis gagner 50 % laisse à −25 %."};
const GLRX=new RegExp('(^|[^\\\\wÀ-ÿ])('+Object.keys(GLOSS).sort((a,b)=>b.length-a.length).map(k=>k.replace(/[-]/g,'\\\\-')).join('|')+')(?![\\\\wÀ-ÿ])','i');
function glossMark(root){if(!root)return;const els=root.querySelectorAll('p.note,.kv>span,details>p,.note');
 els.forEach(el=>{if(el.dataset.gl||el.closest('button,.card,.evstep,#modal'))return;el.dataset.gl=1;
  const w=document.createTreeWalker(el,NodeFilter.SHOW_TEXT);let n;const done=new Set();
  while((n=w.nextNode())){if(n.parentElement.closest('.gl,b,a,button'))continue;const m=GLRX.exec(n.nodeValue);if(!m)continue;const key=m[2].toLowerCase();if(done.has(key))continue;
   done.add(key);const i=m.index+m[1].length,r=n.splitText(i);r.splitText(m[2].length);const sp=document.createElement('span');sp.className='gl';sp.dataset.g=key;sp.textContent=r.nodeValue;r.replaceWith(sp);w.currentNode=sp}})}
if(typeof MutationObserver!=='undefined'&&app){let gq=false;new MutationObserver(()=>{if(gq)return;gq=true;Promise.resolve().then(()=>{gq=false;try{glossMark(app)}catch(e){}})}).observe(app,{childList:true,subtree:true});
 app.addEventListener('click',e=>{const g=e.target.closest&&e.target.closest('.gl');if(!g)return;e.preventDefault();e.stopPropagation();const k=g.dataset.g;openModal(k.charAt(0).toUpperCase()+k.slice(1),`<p>${GLOSS[k]||''}</p>`)},true)}""")
rep(""".csum{""",""".gl{border-bottom:1px dotted var(--gold);cursor:help}
.csum{""")
open(p,'w',encoding='utf-8').write(s)
