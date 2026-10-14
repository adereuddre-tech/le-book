p="index.html";s=open(p,encoding="utf-8").read()
def rep(o,n,k=1):
    global s;c=s.count(o);assert c==k,(o[:70],c);s=s.replace(o,n)
# fourchette réaliste : demi-fourchette en pb du prix, modulée par la seule liquidité ; l'impact ne change pas ; frein de taille 0,35 → 0,40
rep("""let BRK=0.35;""","""let BRK=0.40;   /* lot 353 : 0,35 → 0,40 */
/* lot 353 : demi-fourchettes réalistes des futures, en pb du prix (un tick sur deux, liquidité normale) */
const SPR={NQ:0.15,ES:0.25,ESTX:1.0,TOPX:0.95,MXEF:1.0,TN:0.7,GBL:0.4,R:0.55,OAT:0.8,JGB:0.5,EUR:0.25,JPY:0.4,GBP:0.4,AUD:0.4,MXP:2.0,
 CL:0.7,HG:0.6,GC:0.2,KC:2.0,ZW:2.3,BTC:2.5,VX:15,EUA:1.5,BDI:25,NRAM:25};""")
rep(""" bp=(x.s+x.c*Math.pow(bnE,pw)*(pw===0.5?1:1.9)*depthMult(x,bn)*IMPC)*TCK*brake();   /* lot 235 : impact ×1,5, frein sur la facture entière */""",
    """ bp=x.c*Math.pow(bnE,pw)*(pw===0.5?1:1.9)*depthMult(x,bn)*IMPC*TCK*brake();   /* lot 235 : impact ×1,5 ; lot 353 : la fourchette n'est plus dans le multiplicateur */""")
rep(""" const cost=bn*bp*1e-4,spr=Math.min(cost,bn*x.s*TCK*m*brake()*1e-4);""",""" const sbp=(SPR[x.sym]!=null?SPR[x.sym]:x.s/4)*((S&&S.liq)||1);bp+=sbp;   /* lot 353 : demi-fourchette réaliste */
 const cost=bn*bp*1e-4,spr=bn*sbp*1e-4;""")
open(p,'w',encoding='utf-8').write(s)
