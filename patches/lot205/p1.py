# Lot 205 : capital de départ du joueur, par difficulté et par style. Calibration (378 parties, graines 20001–20012) :
# survie 86 % à 0 M$, 94 % à 1 M$, 86 % à 2,5 M$ — au-delà d'environ 1 M$, le capital part en équipe et en book.
# Difficulté : facile 1 M$ (0,45), moyen 0,5 M$ (0), difficile 0. Style : quant +0,5 M$ (+1), flux +0,5 M$ (0),
# fondamental 0 (le plus robuste sans capital).
s=open("index.html",encoding="utf-8").read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:100]); s=s.replace(o,n)
rep("goalMult:1,costM:0.85,seed:0.00045}","goalMult:1,costM:0.85,seed:0.001}")
rep("flowMult:1,goalMult:1,costM:1.10,seed:0}","flowMult:1,goalMult:1,costM:1.10,seed:0.0005}")
rep("const STYSEED={syst:0.0010,fonda:0,flux:0};","const STYSEED={syst:0.0005,fonda:0,flux:0.0005};   /* lot 205 */")
rep('[\"g\",\"capital de départ : 0,45 M$, plus celui de votre style\"]','[\"g\",\"capital de départ : 1 M$, plus celui de votre style\"]')
rep('[\"b\",\"pas de capital de départ au-delà de celui de votre style ; équipe 10 % plus chère\"]','[\"g\",\"capital de départ : 0,5 M$, plus celui de votre style\"],[\"b\",\"équipe 10 % plus chère\"]')
rep("['g',\"capital de départ +1 M$ ; équipe 15 % moins chère\"]","['g',\"capital de départ +0,5 M$ ; équipe 15 % moins chère\"]")
rep("['b',\"aucun capital de départ supplémentaire ; équipe 50 % plus chère\"]","['g',\"capital de départ +0,5 M$\"],['b',\"équipe 50 % plus chère\"]")
open('index.html','w',encoding='utf-8').write(s);print('lot205 ok')
