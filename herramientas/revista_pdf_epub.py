#!/usr/bin/env python3
"""PDF y EPUB de una revista de la Biblioteca (Grumete o Almirante) a partir de su página web.

Uso: python3 herramientas/revista_pdf_epub.py biblioteca/<carpeta> [más carpetas…]
  · PDF (A4): la página en lectura seguida, sin barra ni botones, con las ilustraciones y el diseño.
  · EPUB: el texto limpio (sin glosario emergente ni botones), con portada e ilustraciones; se abre en Kindle.
  Deja <carpeta>/<carpeta>.pdf y <carpeta>/<carpeta>.epub.
"""
import os, re, subprocess, sys, tempfile, shutil, html
from bs4 import BeautifulSoup

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JS = r'''
const {chromium}=require('playwright');
(async()=>{const [,,url,pdf]=process.argv;const b=await chromium.launch();const p=await b.newPage({viewport:{width:820,height:1100}});
await p.route(/fonts\.(googleapis|gstatic)\.com/,r=>r.abort());await p.goto(url,{waitUntil:'load'});await p.waitForTimeout(1200);
await p.evaluate((FF)=>{try{localStorage.setItem('hk_libro_modo','0')}catch(e){};if(typeof R!=='undefined'&&R.on)R.modo(false);
 document.querySelectorAll('img[loading]').forEach(i=>i.loading='eager');
 const s=document.createElement('style');s.textContent=`${FF}.barra,.dobla,#pie,.arriba,.bpag,.dicw,.fin .btn{display:none!important}
 body{background:#fff}main{max-width:none;padding:0}figure{margin:14px 0;break-inside:avoid}figure img{max-height:85mm!important;width:auto;max-width:100%}.ind li{break-inside:avoid}.ind li a{padding:5px 0!important;font-size:15px!important}.carta p,.bienv p{font-size:14px!important}
 .port img{max-height:262mm;width:auto;margin:0 auto;box-shadow:none}.port{break-after:page}
 article,section.ind,footer.fin{break-before:page;border-top:0;margin-top:0;padding-top:0}
 h1,h2,h3,.sec{break-after:avoid}.cita,.bienv,.caja,.carta,.mito,.cifras div,.efe .d,.efe .t,.cur .c,.linea div{break-inside:avoid}
 .gl{text-decoration:none!important}a.fic{border:0}`;document.head.appendChild(s)},require('fs').readFileSync(process.env.FFFILE,'utf8'));
await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(1500);
await p.pdf({path:pdf,format:'A4',printBackground:true,margin:{top:'14mm',bottom:'16mm',left:'16mm',right:'16mm'},
 displayHeaderFooter:true,headerTemplate:'<span></span>',footerTemplate:'<div style="width:100%;text-align:center;font:9px Georgia,serif;color:#8a7350"><span class="pageNumber"></span></div>'});
await b.close()})();
'''

def epub(carpeta, slug, titulo, autor='Historia Total'):
    s = BeautifulSoup(open(os.path.join(carpeta, 'index.html'), encoding='utf-8').read(), 'html.parser')
    for sel in ['.barra', 'script', 'style', '.dobla', '#pie', '.arriba', '.btn', 'link', '.dicw', 'header.port']:
        for e in s.select(sel): e.decompose()
    for e in s.select('.gl'): e.unwrap()
    for e in s.select('a.fic'): e.decompose()           # los enlaces a fichas de la app no sirven en el Kindle
    for a in s.select('a[href^="../../"]'): a.unwrap()
    main = s.find('main') or s.body
    tmp = tempfile.mkdtemp()
    from PIL import Image
    os.makedirs(os.path.join(tmp, 'img'))
    for f in os.listdir(os.path.join(carpeta, 'img')):           # el Kindle no lee webp: todo a jpg
        if f.endswith('.webp'):
            Image.open(os.path.join(carpeta, 'img', f)).convert('RGB').save(os.path.join(tmp, 'img', f[:-5] + '.jpg'), quality=85)
    for im in s.select('img'):
        if im.get('src', '').endswith('.webp'): im['src'] = im['src'][:-5] + '.jpg'
    css = os.path.join(tmp, 'e.css')
    open(css, 'w').write('body{font-family:serif;line-height:1.5}.sec{font-size:.75em;letter-spacing:.15em;text-transform:uppercase;color:#9c7a1c}'
                         'h1{font-size:1.6em;line-height:1.15;margin:.2em 0 .4em}.subt,.ent{font-style:italic}.ent{font-weight:bold}'
                         'figure{margin:1em 0;text-align:center}figure img{max-width:100%}figcaption{font-size:.8em;font-style:italic}'
                         '.cita{margin:1em 1.2em;font-style:italic;border-left:3px solid #9c7a1c;padding-left:.8em}'
                         '.efe .d{font-weight:bold;color:#9c7a1c;margin-top:1em}.efe .d small{display:block}.mito .ver{font-weight:bold;color:#9c7a1c}'
                         '.fuentes{font-size:.8em;color:#555}.ind small{display:block;font-size:.7em;letter-spacing:.1em;text-transform:uppercase}')
    h = os.path.join(tmp, 'r.html')
    open(h, 'w', encoding='utf-8').write(f'<html><head><meta charset="utf-8"><title>{html.escape(titulo)}</title></head><body>{main.decode_contents()}</body></html>')
    out = os.path.join(carpeta, slug + '.epub')
    subprocess.run(['pandoc', h, '-f', 'html', '-o', out, '--epub-cover-image=' + os.path.join(tmp, 'img', 'portada.jpg'),
                    '--css', css, '--toc', '--toc-depth=1', '--split-level=1', '--metadata', f'title={titulo}',
                    '--metadata', f'author={autor}', '--metadata', 'lang=es-ES', '--resource-path', tmp], check=True, cwd=tmp)
    shutil.rmtree(tmp); return out

js = os.path.join(tempfile.gettempdir(), 'revista_pdf.js'); open(js, 'w').write(JS)
F = os.path.join(R, 'herramientas', 'fuentes')   # las tipografías van locales: el PDF no depende de Google Fonts
import base64
FF = ''.join(f"@font-face{{font-family:'{fam}';src:url(data:font/ttf;base64,{base64.b64encode(open(os.path.join(F, fic), 'rb').read()).decode()}) format('truetype');font-weight:100 900;font-style:{st}}}"
             for fam, fic, st in [('Fredoka', 'Fredoka.ttf', 'normal'), ('Nunito', 'Nunito.ttf', 'normal'), ('Nunito', 'Nunito-Italic.ttf', 'italic'),
                                  ('Lora', 'Lora.ttf', 'normal'), ('Lora', 'Lora-Italic.ttf', 'italic'), ('Playfair Display', 'PlayfairDisplay.ttf', 'normal')])
ff = os.path.join(tempfile.gettempdir(), 'revista_fuentes.css'); open(ff, 'w').write(FF); os.environ['FFFILE'] = ff
for c in sys.argv[1:]:
    c = os.path.abspath(c.rstrip('/')); slug = os.path.basename(c)
    t = re.search(r'<title>(.*?)</title>', open(os.path.join(c, 'index.html'), encoding='utf-8').read()).group(1)
    t = t.split(' — ')[0]
    pdf = os.path.join(c, slug + '.pdf')
    subprocess.run(['node', js, 'file://' + os.path.join(c, 'index.html'), pdf], check=True, cwd='/tmp')
    e = epub(c, slug, t)
    print(slug, '·', t, '· PDF', os.path.getsize(pdf) // 1024, 'KB · EPUB', os.path.getsize(e) // 1024, 'KB')
