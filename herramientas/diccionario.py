#!/usr/bin/env python3
"""Diccionario de HistoKHB — genera datos/dic/<letra>.json para la ventana «mantén pulsada una palabra».

Base: herramientas/diccionario_base.json  {"palabras": {palabra: {"g": general, "h": histórico (opcional), "c": científico (opcional)}}, "alias": {...}, "descartes": [...]}
Recorre los textos de la app y enlaza cada forma («conquistaron», «hidalgas»…) con su palabra de diccionario
(simplemma), así las fichas nuevas quedan cubiertas solas. Las palabras nuevas sin definición se apuntan en
herramientas/diccionario_pendientes.json (solo si está instalado wordfreq) para la siguiente tanda.
Para ampliarlo: definir las palabras de diccionario_pendientes.json con el mismo criterio
(g ≤120 caracteres en castellano llano; h ≤160 solo si tiene sentido histórico) y añadirlas a "palabras".
Se ejecuta solo en cada publicación (workflow publicar-hosting) y a mano con: python3 herramientas/diccionario.py
"""
import json, glob, os, re, html, collections, unicodedata
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(R, 'datos')
B = json.load(open(os.path.join(R, 'herramientas', 'diccionario_base.json'), encoding='utf-8'))
base, alias, descartes = B['palabras'], B.get('alias', {}), set(B.get('descartes', []))
TAG = re.compile(r'<[^>]+>')
PAL = re.compile(r"[A-Za-zÁÉÍÓÚÜÑáéíóúüñ]+")

def letra(w):
    c = w[0]
    return c if c == 'ñ' else unicodedata.normalize('NFD', c)[0]

cnt = collections.Counter(); may = collections.Counter()
def walk(o):
    if isinstance(o, dict): [walk(v) for v in o.values()]
    elif isinstance(o, list): [walk(v) for v in o]
    elif isinstance(o, str) and len(o) > 40:
        for w in PAL.findall(html.unescape(TAG.sub(' ', o))):
            cnt[w.lower()] += 1
            if w[0].isupper(): may[w.lower()] += 1
for f in glob.glob(os.path.join(D, 'fichas-*.json')) + glob.glob(os.path.join(D, 'sinc-det-*.json')) + [os.path.join(D, 'desarrollos.json')]:
    walk(json.load(open(f, encoding='utf-8')))

try:
    import simplemma
    lema = lambda w: simplemma.lemmatize(w, lang='es')
except ImportError:
    lema = lambda w: w
    print('aviso: simplemma no instalado; solo se enlazan las palabras exactas')

formas = {}
sin_def = collections.Counter()
for w, n in cnt.items():
    if len(w) < 3: continue
    l = w if w in base else lema(w)
    l = alias.get(l, l)
    if l in descartes: continue
    if l in base:
        if l != w: formas[w] = l
    elif may[w] * 2 < n:  # no cuenta los nombres propios (casi siempre con mayúscula)
        sin_def[l] += n

out = collections.defaultdict(lambda: {'f': {}, 'd': {}})
for w, l in formas.items(): out[letra(w)]['f'][w] = l
for l, e in base.items():
    v = [e['g'], e.get('h', ''), e.get('c', '')]   # general, sentido histórico, sentido científico
    while len(v) > 1 and not v[-1]: v.pop()
    out[letra(l)]['d'][l] = v
os.makedirs(os.path.join(D, 'dic'), exist_ok=True)
for f in glob.glob(os.path.join(D, 'dic', '*.json')): os.remove(f)
for k, v in out.items():
    json.dump(v, open(os.path.join(D, 'dic', k + '.json'), 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))

try:
    from wordfreq import zipf_frequency
    pend = sorted(l for l in sin_def if zipf_frequency(l, 'es') < 4.5)  # criterio de Carlos: mejor de más que de menos
    json.dump(pend, open(os.path.join(R, 'herramientas', 'diccionario_pendientes.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
    print(f'pendientes de definir: {len(pend)}')
except ImportError:
    pass
print(f'diccionario: {len(base)} palabras, {len(formas)} formas enlazadas, {len(out)} ficheros en datos/dic/')
