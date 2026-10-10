p='index.html';s=open(p,encoding='utf-8').read()
def rep(o,n,k=1):
    global s;c=s.count(o);assert c==k,(o[:60],c);s=s.replace(o,n)
rep("""{who:"Victoria",hi:"Le ministre m'appelle encore. Pour avoir mon avis.",full:"Victoria « Black Book » Ashworth",role:"ancienne directrice de cabinet d'un ministre des Finances\"""",
    """{who:"Victoria",hi:"Mon successeur m'appelle encore. Pour avoir mon avis.",full:"Victoria « Black Book » Ashworth",role:"ancienne ministre des Finances\"""")
open(p,'w',encoding='utf-8').write(s)
