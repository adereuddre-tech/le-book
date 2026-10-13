p="index.html";s=open(p,encoding="utf-8").read()
def rep(o,n,k=1):
    global s;c=s.count(o);assert c==k,(o[:70],c);s=s.replace(o,n)
# la page du desk s'ouvre en haut
rep("""function screenPlay(){
 tuto(2,3);""","""function screenPlay(){
 tuto(2,3);setTimeout(()=>{try{window.scrollTo(0,0)}catch(e){}},0);   /* lot 332 */""")
open(p,'w',encoding='utf-8').write(s)
