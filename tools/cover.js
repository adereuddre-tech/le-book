/* cover.js — audit statique des effets d'événement.
   Trois questions :
   1. Une clé d'effet utilisée par une anecdote est-elle lue par le code qui l'applique ?
      Une clé que personne ne lit est un effet mort : le joueur paie ou croit gagner, rien
      n'arrive. C'est la famille du bug « ancien du desk ».
   2. Un effet de jauge dépasse-t-il ±15 ? `gauge()` borne à ±15 sans le dire : au-delà,
      le texte promet plus que ce qui est appliqué.
   3. Un effet de trésorerie dépasse-t-il une borne plausible de l'encours ?
   Usage : node tools/cover.js [fichier] */
const fs=require('fs');
const src=fs.readFileSync(process.argv[2]||'index.html','utf8');

/* toutes les accolades d'effet e:{...} du fichier, avec le libellé et le texte du choix */
const CH=/\{b:"((?:[^"\\]|\\.)*)",s:"((?:[^"\\]|\\.)*)",e:\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}\}/g;
const choices=[];
for(const m of src.matchAll(CH)) choices.push({b:m[1],s:m[2],e:m[3],at:m.index});

/* clés lues par le code : e.xxx, e['xxx'] */
const read=new Set();
for(const m of src.matchAll(/\be\.([A-Za-z_]\w*)/g)) read.add(m[1]);
for(const m of src.matchAll(/\be\[['"](\w+)['"]\]/g)) read.add(m[1]);

const used=new Map();
choices.forEach(c=>{
  for(const m of c.e.matchAll(/(^|,)\s*([A-Za-z_]\w*)\s*:/g)){
    const k=m[2];
    if(!used.has(k))used.set(k,[]);
    used.get(k).push(c);
  }
});

const dead=[...used.keys()].filter(k=>!read.has(k)).sort();
console.log('=== 1. clés d\'effet jamais lues par le code (effet mort) ===');
if(!dead.length)console.log(' aucune — toutes les clés utilisées sont traitées quelque part');
dead.forEach(k=>{
  const ex=used.get(k).slice(0,3).map(c=>`« ${c.b} »`).join(' / ');
  console.log(`  ${k} — ${used.get(k).length} choix : ${ex}`);
});

console.log('\n=== 2. effets de jauge au-delà de la borne ±15 de gauge() ===');
let n2=0;
choices.forEach(c=>{
  for(const m of c.e.matchAll(/(^|,)\s*(lp|rc)\s*:\s*(-?[\d.]+)/g)){
    const v=parseFloat(m[3]);
    if(Math.abs(v)>15){n2++;console.log(`  ${m[2]}:${v} tronqué à ${v>0?15:-15} — « ${c.b} » : ${c.s.slice(0,60)}`)}
  }
});
if(!n2)console.log(' aucun — toutes les jauges annoncées sont applicables telles quelles');

console.log('\n=== 3. effets de trésorerie hors bande plausible (|cash| > 3 % de l\'encours) ===');
let n3=0;
choices.forEach(c=>{
  for(const m of c.e.matchAll(/(^|,)\s*cash\s*:\s*(-?[\d.]+)/g)){
    const v=parseFloat(m[2]);
    if(Math.abs(v)>0.03){n3++;console.log(`  cash:${v} = ${(v*1e4).toFixed(0)} pb — « ${c.b} » : ${c.s.slice(0,60)}`)}
  }
});
if(!n3)console.log(' aucun');

console.log(`\n${choices.length} choix analysés, ${used.size} clés d'effet distinctes, ${read.size} clés lues par le code.`);
