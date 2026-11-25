#!/usr/bin/env python3
"""Añade el glosario al PDF de un libro o revista de la Biblioteca.
Uso: glosario_pdf.py libro|revista original.pdf glosario.py salida.pdf
- libro: páginas A5 al final, siguiendo la numeración.
- revista: páginas A4 a dos columnas, antes de la contraportada (última página).
"""
import sys, html, importlib.util, weasyprint
from pypdf import PdfReader, PdfWriter
tipo, orig, fglos, salida = sys.argv[1:5]
spec = importlib.util.spec_from_file_location('g', fglos); M = importlib.util.module_from_spec(spec); spec.loader.exec_module(M)
F = '/home/claude/fuentes/x_fontsource-{}-5.3.0/package/files/{}-latin-{}-{}.woff'
def ff(fam, pkg, w, st='normal'):
    return f"@font-face{{font-family:'{fam}';font-weight:{w};font-style:{st};src:url('file://{F.format(pkg, pkg, w, st)}')}}"
R = PdfReader(orig); n = len(R.pages)
w, h = float(R.pages[-1].mediabox.width), float(R.pages[-1].mediabox.height)
primera = n + 1 if tipo == 'libro' else n   # la revista mete el glosario antes de la contraportada

grupos = []
for gr, t, fs, d in M.G:
    if not grupos or grupos[-1][0] != gr: grupos.append((gr, []))
    grupos[-1][1].append((t, d))
cuerpo = ''.join(f'<h2>{html.escape(gr)}</h2>' + ''.join(f'<p class="e"><b>{html.escape(t)}.</b> {html.escape(d)}</p>' for t, d in ents) for gr, ents in grupos)
intro = '<p class="intro">Explicación de los nombres y palabras del texto que pueden necesitar una aclaración. En la versión para leer en la web, cada uno aparece subrayado y se puede tocar.</p>'

if tipo == 'libro':
    fam = getattr(M, 'PDF_LETRA', 'EB Garamond')
    fuentes = ''.join(ff('EB Garamond', 'eb-garamond', x, s) for x in (400, 600) for s in ('normal', 'italic')) if fam == 'EB Garamond' else ''
    css = fuentes + f'''
@page{{size:{w}pt {h}pt;margin:17mm 15mm 19mm 15mm;@bottom-center{{content:counter(page);font-family:'{fam}';font-size:8.5pt;color:#b08d57}}}}
@page:first{{counter-reset:page {primera}}}
body{{font-family:'{fam}',serif;font-size:10.5pt;line-height:1.42;color:#2a2622;text-align:justify;hyphens:auto}}
h1{{font-weight:600;color:#5b1f1a;text-align:center;font-size:21pt;margin:10mm 0 3mm}}
.intro{{font-style:italic;text-align:center;color:#6b5a45;font-size:9.8pt;margin:0 6mm 6mm}}
h2{{font-weight:600;color:#5b1f1a;font-size:12.5pt;margin:5mm 0 2mm;break-after:avoid}}
.e{{margin:0 0 1.6mm}} .e b{{color:#5b1f1a;font-weight:600}}'''
    doc = f'<html lang="es"><head><meta charset="utf-8"><style>{css}</style></head><body><h1>Glosario</h1>{intro}{cuerpo}</body></html>'
else:
    fuentes = ''.join(ff('Fredoka', 'fredoka', x) for x in (500, 600)) + ''.join(ff('Nunito', 'nunito', x, s) for x in (400, 700) for s in ('normal', 'italic'))
    css = fuentes + f'''
@page{{size:{w}pt {h}pt;margin:20mm 16mm 18mm 16mm;background:#faf6ee;
 @top-left{{content:'BITÁCORA';font:600 9pt Fredoka;letter-spacing:2px;color:#12324a}}
 @top-right{{content:'{getattr(M, "PDF_CABECERA", "")}';font:500 8pt Fredoka;letter-spacing:1.5px;color:#12324a}}
 @bottom-center{{content:counter(page);font:500 8.5pt Fredoka;color:#12324a}}}}
@page:first{{counter-reset:page {primera}}}
body{{font-family:Nunito,sans-serif;font-size:9.6pt;line-height:1.42;color:#2a2622}}
h1{{font:600 26pt Fredoka;color:#12324a;margin:2mm 0 1mm}}
.intro{{font-style:italic;color:#5b6b78;font-size:9.4pt;margin:0 0 5mm;max-width:150mm}}
.cols{{columns:2;column-gap:9mm}}
h2{{font:600 9.5pt Fredoka;letter-spacing:1.5px;text-transform:uppercase;color:#b8860b;margin:3mm 0 2mm;break-after:avoid}}
.e{{margin:0 0 2mm;break-inside:avoid}} .e b{{color:#12324a}}'''
    doc = f'<html lang="es"><head><meta charset="utf-8"><style>{css}</style></head><body><h1>Glosario</h1>{intro}<div class="cols">{cuerpo}</div></body></html>'

g = PdfReader(__import__('io').BytesIO(weasyprint.HTML(string=doc).write_pdf()))
W = PdfWriter(clone_from=orig)
pos = n if tipo == 'libro' else n - 1
for k, p in enumerate(g.pages): W.insert_page(p, pos + k)
if len(R.outline):
  try: W.add_outline_item('Glosario', pos)
  except Exception as e: print('sin marcador:', e)
with open(salida, 'wb') as f: W.write(f)
print(f'{salida}: {n} → {len(W.pages)} páginas (glosario: {len(g.pages)})')
