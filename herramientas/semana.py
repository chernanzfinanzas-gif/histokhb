#!/usr/bin/env python3
"""«Esta semana, hace un tiempo» — genera datos/semana.json.

Junta:
  1. los hechos revisados a mano (herramientas/semana_revisados.json), y
  2. los que aparezcan en fichas NUEVAS: busca fechas tipo «26 de octubre de 1909»
     en la Sincronía, las fichas de época y los desarrollos, y añade las que no
     se hayan visto antes (marcadas "auto", con el título de su ficha).
Se ejecuta solo en cada publicación (workflow publicar-hosting) y a mano con:
  python3 herramientas/semana.py
"""
import json, re, html, glob, os, datetime
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(R, 'datos')
def J(p): return json.load(open(p, encoding='utf-8'))

MESES = ['enero','febrero','marzo','abril','mayo','junio','julio','agosto','septiembre','octubre','noviembre','diciembre']
PAT = re.compile(r'\b(\d{1,2})(?:º)? de (' + '|'.join(MESES) + r')(?: de(?:l año)? (\d{3,4}))?', re.I)
FIESTA = re.compile(r'\b(cada|se celebra|celebran|festividad|fiesta|aniversario|conmemora)', re.I)
TAG = re.compile(r'<[^>]+>')
def limpio(s): return re.sub(r'\s+', ' ', html.unescape(TAG.sub(' ', s))).strip()
ANIO_HOY = datetime.date.today().year

def frase_de(p, i):
    """La frase del párrafo que contiene la posición i, recortada a ~160 caracteres."""
    a = max(p.rfind('. ', 0, i), p.rfind('? ', 0, i), p.rfind('! ', 0, i))
    a = 0 if a < 0 else a + 2
    b = min([x for x in (p.find('. ', i), p.find('? ', i), p.find('! ', i)) if x >= 0] or [len(p)])
    f = p[a:b + 1].strip()
    if len(f) > 160:
        f = f[:f.rfind(' ', 0, 157)] + '…'
    return f

base = J(os.path.join(R, 'herramientas', 'semana_revisados.json'))
vistos = {tuple(v) for v in base['vistos']}
salida = [h for h in base['hechos'] if not h.get('nota')]  # las dudosas no se publican
ya = {(h['k'], h['m'], h['d']) for h in base['hechos']}

ev = J(os.path.join(D, 'sinc-eventos.json'))['ev']
titulo_s = {f"{r}|{e[0]}": e[1] for r, a in ev.items() for e in a}
idx = J(os.path.join(D, 'indice.json'))['fichas']
des = J(os.path.join(D, 'desarrollos.json'))

textos = []  # (k, año_ficha, título, html)
for f in glob.glob(os.path.join(D, 'sinc-det-*.json')):
    for key, v in J(f).items():
        if isinstance(v, str) and key in titulo_s:
            textos.append(('s:' + key, int(key.rsplit('|', 1)[1]), titulo_s[key], v))
for f in glob.glob(os.path.join(D, 'fichas-*.json')):
    for fid, v in J(f).items():
        if fid in idx and isinstance(v, dict):
            textos.append(('f:' + fid, None, idx[fid]['t'], (v.get('g') or '') + ' ' + (v.get('p') or '')))
for did, v in des.items():
    if isinstance(v, dict):
        textos.append(('d:' + did, None, v.get('t', ''), v.get('h', '')))

nuevos = 0
for k, anio_f, tit, h in textos:
    for parr in re.split(r'</p>|<br\s*/?>|</h4>', h):
        p = limpio(parr)
        for m in PAT.finditer(p):
            dia, mes = int(m.group(1)), MESES.index(m.group(2).lower()) + 1
            if not 1 <= dia <= 31: continue
            if (k, mes, dia) in vistos or (k, mes, dia) in ya: continue
            anio = int(m.group(3)) if m.group(3) else anio_f
            if anio is None or anio > ANIO_HOY: continue
            antes = p[max(0, m.start() - 40):m.start()]
            if FIESTA.search(antes) or (not m.group(3) and FIESTA.search(p)): continue
            ya.add((k, mes, dia)); nuevos += 1
            zona = k[2:].rsplit('|', 1)[0] if k.startswith('s:') else ''
            frase = frase_de(p, m.start())
            salida.append({'m': mes, 'd': dia, 'a': anio, 'z': zona, 't': frase, 'f': tit, 'k': k, 'auto': 1})

salida.sort(key=lambda h: (h['m'], h['d'], h['a']))
for h in salida: h.pop('nota', None)
json.dump(salida, open(os.path.join(D, 'semana.json'), 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
print(f"semana.json: {len(salida)} hechos ({nuevos} nuevos automáticos)")
