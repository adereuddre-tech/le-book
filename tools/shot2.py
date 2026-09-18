import sys, pathlib
from playwright.sync_api import sync_playwright
f=pathlib.Path(sys.argv[1]).resolve().as_uri()
out=sys.argv[2]; full=len(sys.argv)>3 and sys.argv[3]=='full'
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
    pg=b.new_page(viewport={'width':380,'height':820},device_scale_factor=2)
    pg.goto(f); pg.wait_for_timeout(2600)
    pg.screenshot(path=out, full_page=full)
    b.close()
print(out)
