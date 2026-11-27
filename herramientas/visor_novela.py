#!/usr/bin/env python3
"""Pasa un libro de la Biblioteca al visor con audiolibro de «Señores de las llanuras».

Uso: python3 herramientas/visor_novela.py <carpeta del libro> [carpeta plantilla]
  Toma de la plantilla (por defecto biblioteca/senores-de-las-llanuras) el diseño, el modo
  páginas, el reproductor y el glosario, y mete el texto, el glosario, la portada, las
  descargas y los colores del libro. Deja el audio oculto hasta que haya capítulos grabados
  (libro_audio.py + libro_audio_visor.py lo activan). Guarda el original como index.orig.html.
"""
import json, os, re, sys, shutil
from bs4 import BeautifulSoup

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
lib = os.path.abspath(sys.argv[1]); slug = os.path.basename(lib.rstrip('/'))
pla = os.path.abspath(sys.argv[2]) if len(sys.argv) > 2 else os.path.join(R, 'biblioteca', 'senores-de-las-llanuras')
T = open(os.path.join(pla, 'index.html'), encoding='utf-8').read()
f = os.path.join(lib, 'index.html')
if not os.path.exists(os.path.join(lib, 'index.orig.html')):
    shutil.copy(f, os.path.join(lib, 'index.orig.html'))
N = open(os.path.join(lib, 'index.orig.html'), encoding='utf-8').read()
tslug = os.path.basename(pla.rstrip('/'))

def arr(p, nombre, ini='['):
    i = p.index(f'const {nombre}=') + len(f'const {nombre}=')
    v, fin = json.JSONDecoder().raw_decode(p, i)
    return i, fin, v

titulo = re.search(r'<title>(.*?)</title>', N).group(1).strip() if '<title>' in N else \
    BeautifulSoup(N, 'html.parser').select_one('.barra .tit').get_text(strip=True)
ttit = re.search(r'<title>(.*?)</title>', T).group(1).strip()

# secciones del libro, con botón de escuchar tras el título
s = BeautifulSoup(N, 'html.parser')
secs, caps = [], []
port = re.search(r'<div class="port">.*?</div>', N).group(0)
for sec in s.select('section.cap'):
    cid = sec['id'][2:]; h1 = sec.find('h1'); t = h1.get_text(' ', strip=True)
    if not re.match(r'notas|glosario|bibliograf|fuentes', t, re.I):
        m = re.match(r'cap(\d+)', cid)
        img = sec.select_one('img.lam'); img = img['src'] if img else 'img/portada.webp'
        caps.append({'id': cid, 'n': str(int(m.group(1))) if m else '', 't': t, 'img': img, 'a': '', 'd': 0})
        b = s.new_tag('button', attrs={'class': 'esc', 'onclick': f"P.play('{cid}')"})
        b.string = '▶ Escuchar el capítulo' if m else f'▶ Escuchar: {t.lower()}'
        h1.insert_after(b)
    secs.append(str(sec))

p = T
a = p.index('<section class="cap"'); b = p.rindex('</section>') + len('</section>')
p = p[:a] + '\n'.join(secs) + p[b:]
p = re.sub(r'<div class="port">.*?</div>', lambda _: port, p, count=1)
i, fin, _ = arr(p, 'CAPS'); p = p[:i] + json.dumps(caps, ensure_ascii=False) + p[fin:]
p = re.sub(r'const SYNC=\{.*?\};', 'const SYNC={};', p, count=1, flags=re.S)
i, fin, _ = arr(p, 'GL'); _, _, gl = arr(N, 'GL'); p = p[:i] + json.dumps(gl, ensure_ascii=False) + p[fin:]
primero = caps[0]['id']
pri_js = "(CAPS.find(c=>c.a)||CAPS[0]).id"   # primer capítulo con audio
rep = [
    (f'<title>{ttit}</title>', f'<title>{titulo}</title>'),
    (f'<span>{ttit.upper()}</span>', f'<span>{titulo.upper()}</span>'),
    ("P.play(P.st.cap||'intro')", f"P.play(P.st.cap||{pri_js})"),
    ("this.carga(this.st.cap||'intro')", f"this.carga(this.st.cap||{pri_js})"),
    ("this.carga('intro')", f"this.carga({pri_js})"),
    ("'Capítulo '+c.n:'Introducción'", "'Capítulo '+c.n:c.t"),
    (f"c.n?c.t:'{ttit}'", f"c.n?c.t:'{titulo}'"),
    (f"artist:'{ttit}'", f"artist:'{titulo}'"),
    ("hk_libro_llanuras", f"hk_libro_{slug}"),
    (f"b:{tslug}-", f"b:{slug}-"),
    (f"lib_{tslug}'", f"lib_{slug}'"),
    (f"{tslug}.pdf", f"{slug}.pdf"), (f"{tslug}.epub", f"{slug}.epub"),
    # colores del libro (marrón) en vez del rojo de la plantilla
    ('--rojo:#5b1f1a;--rojo2:#a8322a', '--rojo:#3b2a1a;--rojo2:#8a5a2b'), ('--titulo:#5b1f1a', '--titulo:#3b2a1a'),
    ('--papel:#1d1715', '--papel:#1b1714'), ('--titulo:#e3a79b', '--titulo:#e0c39a'), ('--rojo2:#d9705f', '--rojo2:#d09a5f'),
    ('#3d1411,#5b1f1a 45%,#2a0f0c', '#2a1d12,#3b2a1a 45%,#1d140c'), ('color:#3d1411', 'color:#2a1d12'),
]
for x, y in rep:
    if x not in p: print('aviso: no encuentro', x[:60])
    p = p.replace(x, y)
extra = 'hr{border:0;text-align:center;margin:1.2em 0}hr::after{content:"·   ·   ·";color:var(--suave)}li{margin-bottom:.3em}.ent{color:var(--suave);font-size:.9em;margin:0 0 4px}\n#bAud,.esc,#mini{display:none!important}'
fin_css = ':focus-visible{outline:2px solid var(--oro);outline-offset:2px}</style>'
assert fin_css in p, 'no encuentro el final del estilo de la plantilla'
p = p.replace(fin_css, fin_css[:-8] + '\n' + extra + '</style>', 1)
open(f, 'w', encoding='utf-8').write(p)
print(titulo, '·', len(caps), 'pistas:', ', '.join(c['id'] for c in caps))
