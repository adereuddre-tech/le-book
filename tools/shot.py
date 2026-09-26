from playwright.sync_api import sync_playwright
import sys
STOP=sys.argv[2]; SEL=sys.argv[3]; OUT=sys.argv[4]
BOT="""(stop)=>{const $=s=>document.querySelector(s);const c=e=>e.click();
if($('#tutooff')){c($('#tutooff'));return 1}
if(eval(stop))return 'STOP';
if($('#found')){c($('#found'));return 1}
if($('#go')&&$('#picks')){for(const [k,v] of Object.entries({prof:'flux',vol:'std',size:'mid',univ:'ext',dur:'normal'})){const e=$(`.card[data-key="${k}"][data-id="${v}"]`);if(e)c(e)}$('#sd').value='11';c($('#go'));return 1}
if($('#send')){const R=recoBook();S.k=R.k.map(v=>Math.max(-S.maxk,Math.min(S.maxk,Math.round(v))));if(typeof drawRows==='function')drawRows();if(typeof refreshSend==='function')refreshSend();if($('#send').disabled&&$('#fitbook'))c($('#fitbook'));c($('#send'));return 1}
const ch=document.querySelectorAll('.choice');if(ch.length){c(ch[0]);return 1}
if($('#commok')){c($('#commok'));return 1}
if($('.commgo')){c($('.commgo'));return 1}
for(const id of ['#ok','#go2','#rgo','#pgo','#nx']){const b=$(id);if(b&&!b.disabled){c(b);return 1}}
const a=[...document.querySelectorAll('button.cta,button.buy')].filter(b=>!b.disabled);if(a.length){c(a[0]);return 1}return 0}"""
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
    pg=b.new_page(viewport={'width':380,'height':800},device_scale_factor=2)
    pg.goto('file://'+__import__('os').path.abspath(sys.argv[1]))
    for i in range(400):
        if pg.evaluate(BOT,STOP)=='STOP':break
        pg.wait_for_timeout(30)
    pg.wait_for_timeout(1500)
    pg.evaluate("()=>{document.querySelectorAll('.mbox').forEach(e=>e.parentElement.remove());const t=document.getElementById('toast');if(t)t.remove()}")
    pg.query_selector(SEL).screenshot(path=OUT)
    b.close()
