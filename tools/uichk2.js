const fs=require('fs'),{JSDOM}=require('jsdom');
const dom=new JSDOM(fs.readFileSync('index.html','utf8'),{runScripts:'dangerously',url:'https://x/',
 beforeParse(w){w.scrollTo=()=>{};const st=w.setTimeout;w.setTimeout=(f,t)=>{try{f()}catch(e){}return 0}}});
const w=dom.window,d=w.document;
setTimeout(()=>{try{console.log(w.eval(`(()=>{
 const o=[];
 /* 1. ecran de creation, premiere partie */
 fundName='Test';screenSetup();
 o.push('titre : '+document.querySelector('h1').textContent);
 o.push('sous-titre : '+document.querySelector('.sub').textContent);
 o.push('texte d intro visible ? '+(document.getElementById('introprose').style.display!=='none'?'OUI (probleme)':'non, en pop-up'));
 o.push('boutons « ? » par choix : '+document.querySelectorAll('.hintq').length+' ; anciens encarts dores : '+document.querySelectorAll('.flag').length);
 o.push('pop-up d intro ouverte a la 1re partie ? '+(document.getElementById('modal')?'oui':'non'));
 o.push('groupes de choix : '+document.querySelectorAll('.pickgrp').length);
 /* 2. tutoriel apres une partie */
 markTutoSeen();
 o.push('apres une partie, tutoSeen() = '+tutoSeen());
 /* 3. tuiles de jauge */
 newGame(4,'fonda','std','inhouse','std','mid','com','normal');S.fundName='T';
 S.phase='events';S.lastG={lp:-6,rc:2,lp0:68,rc0:70};
 document.getElementById('app').innerHTML=statusBar();
 const lp=document.querySelector('[data-gauge=lp]'),rc=document.querySelector('[data-gauge=rc]');
 o.push('tuile investisseurs : classes « '+lp.className+' » style « '+lp.getAttribute('style')+' »');
 o.push('tuile comite        : classes « '+rc.className+' » style « '+rc.getAttribute('style')+' »');
 o.push('fleche investisseurs : '+lp.querySelector('span b').textContent);
 return o.join('\\n')})()`))}catch(e){console.log('ERR',e.message)}dom.window.close()},1400);
