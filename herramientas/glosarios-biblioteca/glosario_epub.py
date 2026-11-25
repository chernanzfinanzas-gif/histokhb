#!/usr/bin/env python3
"""Añade el glosario como último capítulo de un EPUB de la Biblioteca (hecho con pandoc).
Uso: glosario_epub.py original.epub glosario.py salida.epub"""
import sys, re, html, zipfile, importlib.util
orig, fglos, salida = sys.argv[1:4]
spec = importlib.util.spec_from_file_location('g', fglos); M = importlib.util.module_from_spec(spec); spec.loader.exec_module(M)
Z = zipfile.ZipFile(orig); datos = {n: Z.read(n) for n in Z.namelist()}
if 'EPUB/text/glosario.xhtml' in datos: sys.exit('ya tiene glosario')
grupos = []
for gr, t, fs, d in M.G:
    if not grupos or grupos[-1][0] != gr: grupos.append((gr, []))
    grupos[-1][1].append((t, d))
e = lambda x: html.escape(x, quote=False)
num = {t: i for i, (gr, t, fs, d) in enumerate(M.G)}
cuerpo = ''.join(f'<h2>{e(gr)}</h2>\n' + ''.join(f'<div epub:type="endnote" id="g{num[t]}"><p><strong>{e(t)}.</strong> {e(d)}</p></div>\n' for t, d in ents) for gr, ents in grupos)
x = f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" lang="es-ES" xml:lang="es-ES">
<head>
  <meta charset="utf-8" />
  <title>Glosario</title>
  <link rel="stylesheet" type="text/css" href="../styles/stylesheet1.css" />
</head>
<body epub:type="backmatter">
<section id="glosario" class="level1" epub:type="glossary">
<h1>Glosario</h1>
<p><em>Explicación de los nombres y palabras del texto que pueden necesitar una aclaración.</em></p>
{cuerpo}</section>
</body>
</html>
'''
datos['EPUB/text/glosario.xhtml'] = x.encode('utf-8')
# ---- enlazar la primera aparición de cada término en cada capítulo ----
NOCAP = getattr(M, 'NOCAP', set()); FORMAS = []
for i, (gr, t, fs, d) in enumerate(M.G):
    for f_ in fs:
        FORMAS.append((f_, i))
        if f_[0].islower() and f_ not in NOCAP: FORMAS.append((f_[0].upper() + f_[1:], i))
for f_ in getattr(M, 'IGNORA', []): FORMAS.append((f_, -1))
FORMAS.sort(key=lambda p: -len(p[0])); FIDX = dict(FORMAS)
LT = r'\wÁÉÍÓÚÜÑáéíóúüñʉ’\''
RX = re.compile(r'(?<![' + LT + r'])(' + '|'.join(re.escape(html.escape(x, quote=False)) for x, _ in FORMAS) + r')(?![' + LT + r'])')
FIDX.update({html.escape(x, quote=False): i for x, i in FORMAS})
SALTA = ('h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'a', 'title', 'head', 'figcaption', 'table', 'nav')
total = 0
for n in list(datos):
    if not re.match(r'EPUB/text/ch\d+\.xhtml$', n): continue
    x0 = datos[n].decode('utf-8')
    h1 = re.search(r'<h1[^>]*>(.*?)</h1>', x0, re.S)
    if h1 and re.search(r'Notas|Glosario|Fuentes', h1.group(1)): continue
    usados = set(); pila = []; out = []
    cuerpo_ini = x0.index('<body')
    for tok in re.split(r'(<[^>]+>)', x0[cuerpo_ini:]):
        if tok.startswith('<'):
            m = re.match(r'<(/?)([a-zA-Z0-9]+)', tok)
            if m:
                cierra, nom = m.group(1), m.group(2).lower()
                if not cierra and not tok.endswith('/>') and (nom in SALTA or (pila and nom == pila[-1])): pila.append(nom)
                elif cierra and pila and nom == pila[-1]: pila.pop()
            out.append(tok); continue
        if pila or not tok.strip(): out.append(tok); continue
        def rep(m):
            global total
            i = FIDX[m.group(1)]
            if i < 0 or i in usados: return m.group(1)
            usados.add(i); total += 1
            return f'<a epub:type="noteref" class="gl" href="glosario.xhtml#g{i}">{m.group(1)}</a>'
        out.append(RX.sub(rep, tok))
    x1 = x0[:cuerpo_ini] + ''.join(out)
    if 'xmlns:epub' not in x1: x1 = x1.replace('<html ', '<html xmlns:epub="http://www.idpf.org/2007/ops" ', 1)
    datos[n] = x1.encode('utf-8')
css = datos['EPUB/styles/stylesheet1.css'].decode('utf-8') + '\na.gl{color:inherit;text-decoration:none;border-bottom:1px dotted}\n'
datos['EPUB/styles/stylesheet1.css'] = css.encode('utf-8')
print('enlaces a términos:', total)

opf = datos['EPUB/content.opf'].decode('utf-8')
opf = opf.replace('</manifest>', '    <item id="glosario_xhtml" href="text/glosario.xhtml" media-type="application/xhtml+xml" />\n  </manifest>', 1)
opf = opf.replace('</spine>', '  <itemref idref="glosario_xhtml" />\n  </spine>', 1)
datos['EPUB/content.opf'] = opf.encode('utf-8')
ncx = datos['EPUB/toc.ncx'].decode('utf-8')
k = len(re.findall(r'<navPoint ', ncx)) + 1
ncx = ncx.replace('</navMap>', f'  <navPoint id="navPoint-{k}">\n      <navLabel>\n        <text>Glosario</text>\n      </navLabel>\n      <content src="text/glosario.xhtml" />\n    </navPoint>\n  </navMap>', 1)
datos['EPUB/toc.ncx'] = ncx.encode('utf-8')
nav = datos['EPUB/nav.xhtml'].decode('utf-8')
i = nav.index('</ol></nav>') if '</ol></nav>' in nav else nav.index('</ol>')
nav = nav[:i] + '<li id="toc-li-glosario"><a href="text/glosario.xhtml">Glosario</a></li>' + nav[i:]
datos['EPUB/nav.xhtml'] = nav.encode('utf-8')
with zipfile.ZipFile(salida, 'w') as W:
    W.writestr(zipfile.ZipInfo('mimetype'), datos.pop('mimetype'), compress_type=zipfile.ZIP_STORED)
    for n in Z.namelist():
        if n in datos: W.writestr(n, datos.pop(n), compress_type=zipfile.ZIP_DEFLATED)
    for n, b in datos.items(): W.writestr(n, b, compress_type=zipfile.ZIP_DEFLATED)
print(salida, 'ok')
