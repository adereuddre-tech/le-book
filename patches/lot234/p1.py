# Lot 234 : frein sur la facture d'exécution entière. Le lot 232 n'agissait que sur le terme d'impact (7 % de la facture à
# l'encours de départ) : la fourchette, qui domine, croît linéairement avec l'encours, donc rien ne freinait. Désormais la
# facture entière (fourchette + impact) d'un ordre est multipliée par (encours / encours de départ)^BRK au-dessus de
# l'encours de départ (jamais en dessous) : coût total d'un ordre en notionnel^(1+BRK). Même frein pour les concurrents.
s=open("index.html",encoding="utf-8").read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:100]); s=s.replace(o,n)
rep("function tcost(dk,i){","/* lot 234 */\nlet BRK=0.25;\nfunction brake(A){const a0=(S&&S.aum0)||0.1;return Math.pow(Math.max(1,(A===undefined?S.nav:A)/a0),BRK)}\nfunction tcost(dk,i){")
rep("depthMult(x,bn)*impScale())*TCK;   /* lot 232 */","depthMult(x,bn)*impScale())*TCK*brake();   /* lot 232 ; lot 234 : frein sur la facture entière */")
rep("spr=Math.min(cost,bn*x.s*TCK*m*1e-4);","spr=Math.min(cost,bn*x.s*TCK*m*brake()*1e-4);")
rep("c+=d*(x.s+x.c*Math.sqrt(bn)*impScale())*TCK*RIVB.exec*1e-4}","c+=d*(x.s+x.c*Math.sqrt(bn)*impScale())*TCK*brake()*RIVB.exec*1e-4}")
open('index.html','w',encoding='utf-8').write(s);print('lot234 ok')
