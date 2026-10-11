p='index.html';s=open(p,encoding='utf-8').read()
def rep(o,n,k=1):
    global s;c=s.count(o);assert c==k,(o[:70],c);s=s.replace(o,n)
# avertissement de carton : cadre central avec liseré, plus de bandeau pleine largeur
rep(""".cardw{position:fixed;left:10px;right:10px;bottom:12px;z-index:60;padding:10px 12px;border-radius:8px;font-size:13px;line-height:1.35;color:#fff;background:#3b300c;border:2px solid #E3B341;box-shadow:0 4px 18px rgba(0,0,0,.45)}
.cardw.r{background:#3d1010;border-color:#E5483C}""",
""".cardw{position:fixed;left:50%;transform:translateX(-50%);bottom:14px;z-index:60;width:max-content;max-width:min(330px,calc(100vw - 40px));padding:8px 12px;border-radius:8px;font-size:12.5px;line-height:1.35;color:var(--txt);background:rgba(18,24,36,.96);border:1px solid rgba(227,179,65,.55);border-left:4px solid #E3B341;box-shadow:0 4px 16px rgba(0,0,0,.45)}
.cardw.r{border-color:rgba(229,72,60,.55);border-left-color:#E5483C}""")
open(p,'w',encoding='utf-8').write(s)
