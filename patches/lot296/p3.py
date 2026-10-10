p='index.html';s=open(p,encoding='utf-8').read()
def rep(o,n,k=1):
    global s;c=s.count(o);assert c==k,(o[:60],c);s=s.replace(o,n)
# locaux : le débauchage devient un effet sur le moral
rep("débauchage ×1,2 : on part vite d'un garage","moral −5 : on part vite d'un garage")
rep("souscriptions +8 % ; débauchage ×0,95.","souscriptions +8 % ; moral +1.")
rep("souscriptions +12 % ; débauchage ×0,8 : vos traders aiment le quartier","souscriptions +12 % ; moral +5 : vos traders aiment le quartier")
rep("souscriptions +18 % ; débauchage ×0,75","souscriptions +18 % ; moral +6")
rep("rachats −25 %, débauchage ×0,7","rachats −25 %, moral +8")
rep("budget desk ×${dec(execMot(),2)} (bonus ${dec(bonRate(bonEff())*100,1)} %)","budget desk ×${dec(execMot(),2)} (moral ${Math.round(motV())})")
open(p,'w',encoding='utf-8').write(s)
import re
s=open(p,encoding='utf-8').read()
rep("const MORAL={t0:35,dt:10,k:0.5,cut:5,egard:30,lo:20,hi:80};","const MORAL={t0:35,dt:10,k:0.5,cut:5,egard:20,lo:20,hi:80};   /* égards : un ancien +10 % de débauchage = moral −2 */")
def f(m):
    sg,n=m.group(1),int(m.group(2));v=n//5
    return ('moral −' if sg=='+' else 'moral +')+str(v)
s,n=re.subn(r"débauchage ([+−])(\d+) %(?: ce trimestre)?",f,s)
assert n==36,n
open(p,'w',encoding='utf-8').write(s)
