s=open('index.html',encoding='utf-8').read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:90]); s=s.replace(o,n)
rep("<em>Budget</em> : les postes choisis en début de trimestre.","<em>Budget</em> : les salaires du front et du back office, choisis en début de trimestre, et les indemnités quand vous licenciez.")
open('index.html','w',encoding='utf-8').write(s);print('ok')
