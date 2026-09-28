P='/home/claude/le-book/index.html';s=open(P,encoding='utf-8').read()
def rep(old,new,k=1):
    global s;n=s.count(old);assert n==k,(n,old[:90]);s=s.replace(old,new)
rep("S.qMgmtM=VOL().mgmt*S.nav;S.nav-=S.qMgmtM;S.mgrFees+=S.qMgmtM;refreshGain();",
    "S.qMgmtM=VOL().mgmt*S.nav;S.nav-=S.qMgmtM;S.mgrFees+=S.qMgmtM;refreshGain();\n S.coinvBase=Math.max(0,mgrCash());   /* lot 81 : la part co-investie est fixée à l'ouverture */")
rep("function mgrCash(){return mgrNet()}","/* lot 81 : co-investissement — un dixième de la trésorerie d'ouverture suit le résultat net du fonds */\nconst COINV=0.10;\nfunction mgrCash(){return mgrNet()}")
rep(" S.mgrFees=(S.mgrFees||0)+perf*navBefore;S.mgrCosts+=tc*navBefore;refreshGain();\n S.mgrQ={fees:mgmtM+perf*navBefore,ops:S.qOps||0,rum:0,mgmt:mgmtM,perf:perf*navBefore,tc:tc*navBefore};",
    " S.mgrFees=(S.mgrFees||0)+perf*navBefore;S.mgrCosts+=tc*navBefore;\n const coinv=COINV*(S.coinvBase||0)*qTotal;if(coinv>=0)S.mgrFees+=coinv;else S.mgrCosts-=coinv;S.mgrCoinv=(S.mgrCoinv||0)+coinv;refreshGain();\n S.mgrQ={fees:mgmtM+perf*navBefore,ops:S.qOps||0,rum:0,mgmt:mgmtM,perf:perf*navBefore,tc:tc*navBefore,coinv,cb:COINV*(S.coinvBase||0)};")
rep("const UG=pickU([S.mgrQ.mgmt,S.mgrQ.perf,S.mgrQ.ops,S.mgrQ.tc||0,S.mgrQ.fees-S.mgrQ.ops]);",
    "const UG=pickU([S.mgrQ.mgmt,S.mgrQ.perf,S.mgrQ.ops,S.mgrQ.tc||0,S.mgrQ.coinv||0,S.mgrQ.fees-S.mgrQ.ops]);")
rep("<span class=\"av\">${inU(S.mgrQ.fees-S.mgrQ.ops-(S.mgrQ.tc||0),UG)}</span></div>",
    "<span class=\"av\">${inU(S.mgrQ.fees-S.mgrQ.ops-(S.mgrQ.tc||0)+(S.mgrQ.coinv||0),UG)}</span></div>")
rep("['Coûts d\\'exécution',inU(-(S.mgrQ.tc||0),UG)],['<b>Trésorerie disponible</b>'",
    "['Coûts d\\'exécution',inU(-(S.mgrQ.tc||0),UG)],[`Co-investissement (${Math.round(COINV*100)} % de la trésorerie, ${mm(S.mgrQ.cb||0)})`,inU(S.mgrQ.coinv||0,UG)],['<b>Trésorerie disponible</b>'")
rep("<b>Trésorerie</b>, c'est votre score : les commissions encaissées, moins ce que vous dépensez.",
    "<b>Trésorerie</b>, c'est votre score : les commissions encaissées, moins ce que vous dépensez. Un dixième de la trésorerie d'ouverture est investi dans le fonds et en suit les gains comme les pertes.")
rep(" const mg=v.mgmt*rv.mAum,cost=rivalCostQ(rv)*rv.mAum;"," const mg=v.mgmt*rv.mAum,cost=rivalCostQ(rv)*rv.mAum,ci=COINV*Math.max(0,rv.mgr||0)*r;   /* lot 81 : leur co-investissement */")
rep(" rv.mgr+=mg+perf-cost;"," rv.mgr+=mg+perf-cost+ci;")
open(P,'w',encoding='utf-8').write(s);print('ok')
