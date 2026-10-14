p="index.html";s=open(p,encoding="utf-8").read()
def rep(o,n,k=1):
    global s;c=s.count(o);assert c==k,(o[:70],c);s=s.replace(o,n)
# un seul cadre en bas : carton à venir et minuteur réunis ; la page réserve sa hauteur, plus rien n'est recouvert
rep("""body.tmron #app{padding-bottom:150px}""","""body.tmron #app{padding-bottom:150px}
#bdock{position:fixed;left:max(12px,calc(50% - 328px));right:max(12px,calc(50% - 328px));bottom:max(10px,env(safe-area-inset-bottom));z-index:70;
 display:none;flex-direction:column;gap:6px;padding:6px;border-radius:12px;background:rgba(15,22,34,.97);border:1px solid var(--line2);box-shadow:0 6px 22px rgba(0,0,0,.5)}
#bdock.on{display:flex}
#bdock .evtimer,#bdock .cardw{position:static!important;transform:none!important;left:auto!important;right:auto!important;bottom:auto!important;width:auto!important;max-width:none!important;box-shadow:none!important;margin:0}
#bdock .evtimer{border-radius:9px}
.tmove{animation:tk 60s linear infinite!important}   /* lot 357 : le bandeau défile toujours */""")
rep("""function clearTimer(){document.body.classList.remove('tmron');if(TID){clearInterval(TID);TID=null}
 const el=document.getElementById('evtimer');if(el)el.classList.remove('on')}""","""function clearTimer(){document.body.classList.remove('tmron');if(TID){clearInterval(TID);TID=null}
 const el=document.getElementById('evtimer');if(el)el.classList.remove('on');dockSync()}
/* lot 357 : le cadre du bas regroupe le carton à venir et le minuteur, et la page lui réserve sa hauteur */
function dockSync(){if(typeof document==='undefined')return;let d=document.getElementById('bdock');
 if(!d){d=document.createElement('div');d.id='bdock';document.body.appendChild(d)}
 const c=document.getElementById('cardw'),t=document.getElementById('evtimer');
 if(c&&c.parentNode!==d)d.insertBefore(c,d.firstChild);if(t&&t.parentNode!==d)d.appendChild(t);
 const vis=!!(c||(t&&t.classList.contains('on')));d.classList.toggle('on',vis);
 const a=document.getElementById('app');if(a)a.style.paddingBottom=vis?Math.max(100,d.offsetHeight+24)+'px':''}""")
rep(""" el.classList.add('on');document.body.classList.add('tmron');""",""" el.classList.add('on');document.body.classList.add('tmron');setTimeout(dockSync,0);""")
rep(""" if(!c){if(el)el.remove();return}if(!el){el=document.createElement('div');el.id='cardw';document.body.appendChild(el)}
 el.className='cardw '+(c.lvl>1?'r':'y');el.innerHTML=`${c.lvl>1?'🟥 <b>Carton rouge</b>':'🟨 <b>Carton jaune</b>'} à la clôture si rien ne change : ${c.txt}.`}""",
    """ if(!c){if(el)el.remove();dockSync();return}if(!el){el=document.createElement('div');el.id='cardw';document.body.appendChild(el)}
 el.className='cardw '+(c.lvl>1?'r':'y');el.innerHTML=`${c.lvl>1?'🟥 <b>Carton rouge</b>':'🟨 <b>Carton jaune</b>'} à la clôture si rien ne change : ${c.txt}.`;dockSync()}""")
open(p,'w',encoding='utf-8').write(s)
s=open(p,encoding='utf-8').read()
rep("""#bdock .evtimer{border-radius:9px}""","""#bdock .evtimer{border-radius:9px;padding:2px 10px 2px 2px!important}#bdock .tdial{transform:scale(.62);transform-origin:left center;margin:-14px -26px -14px 0}""")
open(p,'w',encoding='utf-8').write(s)
