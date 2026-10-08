import math
p='index.html';s=open(p,encoding='utf-8').read()
def rep(o,n,k=1):
    global s;c=s.count(o);assert c==k,(o[:60],c);s=s.replace(o,n)
SH=.35
# cov-lite : σ 3,5 %, p 40 % → perte déduite
p1=.40;l1=.035/math.sqrt(p1*(1-p1));y1=SH*.035+p1*l1
# AT1 : σ 4 %, perte 18 % → probabilité déduite (racine < 1/2)
l2=.18;q=(.04/l2)**2;p2=round((1-math.sqrt(1-4*q))/2,4);y2=SH*.04+p2*l2
rep("{id:'lev',nm:'Cov-lite leveraged loans',ico:'🏗️',y:0.03288,p:0.2579,l:0.0800,",f"{{id:'lev',nm:'Cov-lite leveraged loans',ico:'🏗️',y:{y1:.5f},p:{p1},l:{l1:.4f},")
rep("{id:'at1',nm:'Bank AT1 CoCos',ico:'🏦',y:0.03838,p:0.2709,l:0.0900,",f"{{id:'at1',nm:'Bank AT1 CoCos',ico:'🏦',y:{y2:.5f},p:{p2},l:{l2:.4f},")
rep("Le marché les solde à la moindre rumeur sur une banque.","Calmes pendant des années, puis une émission rayée en un week-end.")
rep("pertes des trois\n   derniers entre 8 et 10 %, probabilités déduites ;","pertes déduites\n   des probabilités, sauf AT1 (perte 18 %) et dollar synthétique (10 %) ; lot 250 : cov-lite à 40 %, AT1 à 18 % ;")
open(p,'w',encoding='utf-8').write(s)
