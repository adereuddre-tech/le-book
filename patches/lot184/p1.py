# Lot 184 : charges factorielles (proposition d'Antoine, un cran = 0,20, affichage C/I/L/A, liquidité = −dollar en interne) :
# T-Note liquidité −1 ; Gilt −3 −3 0 −1 ; Bund croissance −2, liquidité 0 ; OAT croissance −2, inflation −3 ; JGB inflation −2,
# appétit −1 ; Euro-fx croissance +2.
s=open("index.html",encoding="utf-8").read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:90]); s=s.replace(o,n)
rep("sig:0.065, s:0.35, c:0.30, b:[-0.50,-0.40,-0.42,-0.42]","sig:0.065, s:0.35, c:0.30, b:[-0.50,-0.40, 0.20,-0.42]")
rep("sig:0.060, s:0.35, c:0.30, b:[-0.20,-0.60, 0.20,-0.40]","sig:0.060, s:0.35, c:0.30, b:[-0.40,-0.60, 0.00,-0.40]")
rep("sig:0.070, s:0.55, c:0.50, b:[-0.40,-0.40,-0.20,-0.40]","sig:0.070, s:0.55, c:0.50, b:[-0.60,-0.60, 0.00,-0.20]")
rep("sig:0.065, s:0.60, c:0.55, b:[-0.20,-0.60, 0.20, 0.20]","sig:0.065, s:0.60, c:0.55, b:[-0.40,-0.60, 0.20, 0.20]")
rep("sig:0.040, s:0.60, c:0.60, b:[-0.16,-0.28, 0.58,-0.18]","sig:0.040, s:0.60, c:0.60, b:[-0.16,-0.40, 0.58,-0.20]")
rep("sig:0.080, s:0.30, c:0.22, b:[ 0.20,-0.18,-0.86, 0.18]","sig:0.080, s:0.30, c:0.22, b:[ 0.40,-0.18,-0.86, 0.18]")
open('index.html','w',encoding='utf-8').write(s);print('lot184 ok')
