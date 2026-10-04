# Lot 204 : fin de trimestre — le grand ruban du résultat déroule le tracé du trimestre. L'animation reposait sur SMIL
# (<animate> d'un clipPath, <animateTransform> des pastilles) : sur un écran inséré dynamiquement, son départ peut être
# manqué et le tracé apparaît d'un bloc. Avec opt.js, tapeSvg n'émet plus d'animation SMIL : theatre() avance lui-même
# la fenêtre (largeur du clipPath) et les pastilles (images data-tr), sur la même horloge que le compteur ; un toucher
# saute à la fin. Le ruban en direct du trimestre garde son animation.
s=open("index.html",encoding="utf-8").read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:100]); s=s.replace(o,n)
rep("""  rmk+=anim?`<g><animateTransform attributeName="transform" type="translate" dur="${DRAW}s" fill="freeze"
    values="${Array.from({length:NS+1},(_,k)=>f(x(at(k))-ex)+' '+f(y(qi(at(k)))-ey0)).join(';')}"/>${mk}</g>`:mk;""",
"""  const trv=anim?Array.from({length:NS+1},(_,k)=>f(x(at(k))-ex)+' '+f(y(qi(at(k)))-ey0)):null;
  rmk+=anim?(opt.js?`<g class="tmk" data-tr="${trv.join(';')}" transform="translate(${trv[0]})">${mk}</g>`   /* lot 204 */
   :`<g><animateTransform attributeName="transform" type="translate" dur="${DRAW}s" fill="freeze"
    values="${trv.join(';')}"/>${mk}</g>`):mk;""")
rep("""   <rect x="0" y="-${H*4}" height="${H*9}" width="${f(x0)}">
    <animate attributeName="width" from="${f(x0)}" to="${W}" dur="${DRAW}s" fill="freeze"/></rect>
  </clipPath></defs>
  ${base}<g clip-path="url(#${id2})">${riv}${body}</g>${rmk}
  <g><animateTransform attributeName="transform" type="translate" dur="${DRAW}s" fill="freeze"
    values="${Array.from({length:NS+1},(_,k)=>f(x(at(k))-hx)+' '+f(y(p[at(k)])-hy)).join(';')}"/>${me}</g></svg>`;""",
"""   <rect x="0" y="-${H*4}" height="${H*9}" width="${f(x0)}"${opt.js?` class="tclip" data-x0="${f(x0)}" data-w="${W}"`:''}>
    ${opt.js?'':`<animate attributeName="width" from="${f(x0)}" to="${W}" dur="${DRAW}s" fill="freeze"/>`}</rect>
  </clipPath></defs>
  ${base}<g clip-path="url(#${id2})">${riv}${body}</g>${rmk}
  ${(()=>{const tr=Array.from({length:NS+1},(_,k)=>f(x(at(k))-hx)+' '+f(y(p[at(k)])-hy));
   return opt.js?`<g class="tmk" data-tr="${tr.join(';')}" transform="translate(${tr[0]})">${me}</g>`
    :`<g><animateTransform attributeName="transform" type="translate" dur="${DRAW}s" fill="freeze"
    values="${tr.join(';')}"/>${me}</g>`})()}</svg>`;""")
# theatre : avance la fenêtre et les pastilles des rubans pilotés en JS
rep("""   if(root.classList.contains('skip')||u>=1||k>kmax){put(vals[vals.length-1]);return}
   put(vals[Math.round(u*(vals.length-1))]);setTimeout(()=>tick(k+1),60)};""",
"""   const move=w=>{const cl=sv.querySelector('.tclip');if(cl)cl.setAttribute('width',(+cl.dataset.x0+(+cl.dataset.w-+cl.dataset.x0)*w).toFixed(1));
    sv.querySelectorAll('.tmk').forEach(g=>{const fr=g.dataset.tr.split(';');g.setAttribute('transform','translate('+fr[Math.round(w*(fr.length-1))]+')')})};   /* lot 204 */
   if(root.classList.contains('skip')||u>=1||k>kmax){put(vals[vals.length-1]);move(1);return}
   put(vals[Math.round(u*(vals.length-1))]);move(u);setTimeout(()=>tick(k+1),60)};""")
# le grand ruban du résultat passe en mode JS, un peu plus lent pour qu'on voie le trimestre se faire
rep("${tapeSvg(S.tape.pts,S.tape.q0||0,{h:150,anim:1,draw:3,zero:1,rivals:rivalTapes(),qs:S.tape.q0||0,ql:S.q,q0v:S.tape.pts[S.tape.pts.length-1]/(1+o.qTotal)})}",
    "${tapeSvg(S.tape.pts,S.tape.q0||0,{h:150,anim:1,draw:4,js:1,zero:1,rivals:rivalTapes(),qs:S.tape.q0||0,ql:S.q,q0v:S.tape.pts[S.tape.pts.length-1]/(1+o.qTotal)})}")
open('index.html','w',encoding='utf-8').write(s);print('lot204 ok')
