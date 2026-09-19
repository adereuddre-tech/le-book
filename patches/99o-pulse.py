# -*- coding: utf-8 -*-
"""Lot 26 (suite) — l'écusson du fonds au bout du tracé, et c'est lui qui bat.

Le point de tête masquait l'écusson. On le remplace par l'écusson lui-même, animé par une
mise à l'échelle autour de son centre : la marque respire au lieu d'être recouverte.
"""
import sys; sys.path.insert(0,'patches')
from _lib import Ed
e=Ed()
e.rep(""" const head=`<circle cx="${f(x(n-1))}" cy="${f(y(p[n-1]))}" r="3" fill="${headC}">
    <animate attributeName="r" values="3;6;3" dur="1.8s" repeatCount="indefinite"/></circle>`;""",
""" /* l'écusson du fonds marque la tête du tracé, et c'est lui qui bat */
 const hx=x(n-1),hy=y(p[n-1]);
 const head=`<g><animateTransform attributeName="transform" type="translate" dur="1.9s" repeatCount="indefinite"
    values="0 0;${f(-hx*0.18)} ${f(-hy*0.18)};0 0"/>
   <g><animateTransform attributeName="transform" type="scale" dur="1.9s" repeatCount="indefinite"
     values="1 1;1.18 1.18;1 1"/>${crestMark(S&&S.crest!==undefined?S.crest:0,hx,hy,6.2)}</g></g>`;""")
e.rep("""  <circle cx="${f(x0)}" cy="${f(y(p[from]))}" r="3.4" fill="${headC}">
   <animate attributeName="cx" values="${(()=>{const a=[];for(let j=0;j<=40;j++){const i=Math.round(from+(n-1-from)*j/40);a.push(f(x(i)))}return a.join(';')})()}" dur="${DRAW}s" fill="freeze"/>
   <animate attributeName="cy" values="${(()=>{const a=[];for(let j=0;j<=40;j++){const i=Math.round(from+(n-1-from)*j/40);a.push(f(y(p[i])))}return a.join(';')})()}" dur="${DRAW}s" fill="freeze"/>
   <animate attributeName="r" values="3;6;3" dur="1.8s" begin="${DRAW}s" repeatCount="indefinite"/></circle></svg>`;""",
"""  <g><animateTransform attributeName="transform" type="translate" dur="${DRAW}s" fill="freeze"
    values="${(()=>{const a=[];for(let j=0;j<=40;j++){const i=Math.round(from+(n-1-from)*j/40);
      a.push(f(x(i)-x(n-1))+' '+f(y(p[i])-y(p[n-1])))}return a.join(';')})()}"/>
   ${crestMark(S&&S.crest!==undefined?S.crest:0,x(n-1),y(p[n-1]),6.2)}</g></svg>`;""")
e.done("lot 26 — ecusson pulsant en tete de trace")
