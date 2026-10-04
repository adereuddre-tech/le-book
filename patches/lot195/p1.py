# Lot 195 : objectifs « concurrent nommé » rattachés au concurrent du moment. « La Citadelle tombe », « Pont-Levis dans le
# rétroviseur » et « Plus malin que Médaillon » visaient Citadelle Nord, Pont-Levis et Médaillon d'Or, souvent absents depuis
# le tirage des noms (lot 154) : l'objectif était alors impossible. Chacun vise désormais le concurrent du même style
# (flux, fondamental, quant), nom et texte recalculés ; identifiant stable (id) pour la sauvegarde et l'historique.
s=open("index.html",encoding="utf-8").read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:90]); s=s.replace(o,n)
rep(''' {nm:"Pont-Levis dans le rétroviseur",d:"Faire mieux que Pont-Levis Associés ce trimestre.",t:c=>c.beat('Pont-Levis Associés'),b:0.05},
 {nm:"Plus malin que Médaillon",d:"Faire mieux que Médaillon d'Or ce trimestre.",t:c=>c.beat("Médaillon d'Or"),b:0.08},
 {nm:"La Citadelle tombe",d:"Faire mieux que Citadelle Nord ce trimestre.",t:c=>c.beat('Citadelle Nord'),b:0.06},''',
''' /* lot 195 : le concurrent du même style, quel que soit son nom */
 {id:"Pont-Levis dans le rétroviseur",rs:'fonda',get nm(){const r=rivSty('fonda');return !r||r.nm==='Pont-Levis Associés'?'Pont-Levis dans le rétroviseur':r.nm+' dans le rétroviseur'},get d(){return 'Faire mieux que '+((rivSty('fonda')||{}).nm||'le concurrent fondamental')+' ce trimestre.'},t:c=>c.beatSty('fonda'),b:0.05},
 {id:"Plus malin que Médaillon",rs:'syst',get nm(){const r=rivSty('syst');return !r||r.nm==="Médaillon d'Or"?'Plus malin que Médaillon':'Plus malin que '+r.nm},get d(){return 'Faire mieux que '+((rivSty('syst')||{}).nm||'le concurrent quant')+' ce trimestre.'},t:c=>c.beatSty('syst'),b:0.08},
 {id:"La Citadelle tombe",rs:'flux',get nm(){const r=rivSty('flux');return !r||r.nm==='Citadelle Nord'?'La Citadelle tombe':r.nm+' tombe'},get d(){return 'Faire mieux que '+((rivSty('flux')||{}).nm||'le concurrent flux')+' ce trimestre.'},t:c=>c.beatSty('flux'),b:0.06},''')
rep("const GOALB=0.25;","const GOALB=0.25;\nfunction rivSty(st){const R=S.rivals||[];return R.find(x=>x.style===st&&!x.closed)||R.find(x=>x.style===st)||null}   /* lot 195 */")
rep("  beat:nm=>{const r=S.rivals.find(x=>x.nm===nm);return r?o.qTotal>r.last:false},",
    "  beat:nm=>{const r=S.rivals.find(x=>x.nm===nm);return r?o.qTotal>r.last:false},\n  beatSty:st=>{const r=rivSty(st);return r?o.qTotal>r.last:false},")
rep("preOk=g=>(!g.sym||","preOk=g=>(!g.rs||rivSty(g.rs))&&(!g.sym||")
rep("const gav=QGOALS.filter(g=>!S.usedGoals.includes(g.nm)&&preOk(g));\n S.goal=pick(gav.length?gav:QGOALS.filter(preOk));S.usedGoals.push(S.goal.nm);",
    "const gav=QGOALS.filter(g=>!S.usedGoals.includes(g.id||g.nm)&&preOk(g));\n S.goal=pick(gav.length?gav:QGOALS.filter(preOk));S.usedGoals.push(S.goal.id||S.goal.nm);")
rep("if(S.goal&&S.goal.nm)S.goal=QGOALS.find(g=>g.nm===S.goal.nm)||null;",
    "if(S.goal&&S.goal.nm)S.goal=QGOALS.find(g=>(S.goal.id&&g.id===S.goal.id)||g.nm===S.goal.nm)||null;")
open('index.html','w',encoding='utf-8').write(s);print('lot195 ok')
