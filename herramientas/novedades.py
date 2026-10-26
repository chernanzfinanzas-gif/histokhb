#!/usr/bin/env python3
"""Novedades automáticas de HistoKHB - Historia Total (datos/novedades.json).

Se ejecuta solo en cada publicación (workflow publicar-hosting):
  1. CONTENIDO: compara fichas de época, desarrollos y fichas de la Sincronía con la huella de la
     publicación anterior (herramientas/novedades_huellas.json). Nueva → «nueva»; crecida de forma
     clara (≥15 % y ≥300 caracteres) → «ampliada». Las correcciones pequeñas no se anuncian.
  2. FUNCIONES DE LA APP: cualquier línea que empiece por «NOVEDAD:» en la descripción de los commits
     publicados se anuncia tal cual («NOVEDAD: Diccionario: mantén pulsada una palabra…»).
A mano: NOVEDADES_COMMITS='[{"message":"NOVEDAD: texto"}]' python3 herramientas/novedades.py
"""
import json, os, re, glob, hashlib, datetime
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(R, 'datos')
HU = os.path.join(R, 'herramientas', 'novedades_huellas.json')
def J(p):
    with open(p, encoding='utf-8') as fh: return json.load(fh)
def W(p, o):
    with open(p, 'w', encoding='utf-8') as fh: json.dump(o, fh, ensure_ascii=False, separators=(',', ':'))
TAG = re.compile(r'<[^>]+>')
def largo(s): return len(TAG.sub('', s or ''))
def huella(s): return hashlib.md5((s or '').encode()).hexdigest()[:12]

idx = J(os.path.join(D, 'indice.json'))
secc = {s['id']: s['t'] for s in idx['secciones']}
ev = J(os.path.join(D, 'sinc-eventos.json'))['ev']
tit_s = {f"{r}|{e[0]}": e[1] for r, a in ev.items() for e in a}

actual = {}   # clave -> (texto, título, sub, href)
for f in glob.glob(os.path.join(D, 'fichas-*.json')):
    for k, v in J(f).items():
        if k in idx['fichas'] and isinstance(v, dict):
            fi = idx['fichas'][k]
            actual['f:' + k] = ((v.get('n') or '') + (v.get('g') or '') + (v.get('p') or ''), fi['t'],
                                f"{secc.get(fi.get('sec'), '')} · {fi.get('d', '')}", '#/f/' + k)
for k, v in J(os.path.join(D, 'desarrollos.json')).items():
    if isinstance(v, dict):
        actual['d:' + k] = (v.get('h', ''), v.get('t', k), 'Desarrollo · ' + v.get('d', ''), '#/d/' + k)
for f in glob.glob(os.path.join(D, 'sinc-det-*.json')):
    for k, v in J(f).items():
        if isinstance(v, str) and k in tit_s:
            actual['s:' + k] = (v, tit_s[k], None, None)

items = []
previa = J(HU) if os.path.exists(HU) else None
if previa is not None:
    for k, (txt, t, sub, href) in actual.items():
        n = largo(txt)
        if k not in previa:
            tipo = 'nueva'
        else:
            h0, n0 = previa[k]
            if h0 == huella(txt) or not (n >= n0 * 1.15 and n - n0 >= 300): continue
            tipo = 'ampliada'
        it = {'k': k[2:], 't': t, 'tipo': tipo, 'lugares': []}
        if href: it['href'] = href
        if sub: it['sub'] = sub
        items.append(it)

for c in json.loads(os.environ.get('NOVEDADES_COMMITS') or '[]'):
    for linea in (c.get('message') or '').splitlines():
        m = re.match(r'\s*NOVEDAD:\s*(.+)', linea)
        if m:
            t = m.group(1).strip()
            items.append({'k': 'app-' + huella(t), 't': t, 'tipo': 'app', 'href': '#/', 'sub': 'Mejora de la app', 'lugares': []})

if items:
    N = J(os.path.join(D, 'novedades.json'))
    from zoneinfo import ZoneInfo
    hoy = datetime.datetime.now(ZoneInfo('Europe/Madrid')).strftime('%Y-%m-%d')
    dia = next((d for d in N if d['fecha'] == hoy), None)
    if not dia:
        dia = {'fecha': hoy, 'titulo': '', 'items': []}; N.append(dia)
    # La app se deduplica en 10 días (un mismo commit no se anuncia dos veces); el contenido, solo en el día.
    ya_app = {i['k'] for d in N[-10:] for i in d['items'] if i['tipo'] == 'app'}
    ya_hoy = {(i['k'], i['tipo']) for i in dia['items']}
    nuevos = [i for i in items if (i['k'] not in ya_app if i['tipo'] == 'app' else (i['k'], i['tipo']) not in ya_hoy)]
    dia['items'] = [i for i in nuevos if i['tipo'] == 'app'] + dia['items'] + [i for i in nuevos if i['tipo'] != 'app']
    hist = sum(1 for i in dia['items'] if i['tipo'] != 'app'); app = len(dia['items']) - hist
    if not dia['titulo'] or dia['titulo'] in ('Historias nuevas y ampliadas', 'Mejoras en la app', 'Historias nuevas y mejoras en la app'):
        dia['titulo'] = 'Historias nuevas y mejoras en la app' if hist and app else ('Mejoras en la app' if app else 'Historias nuevas y ampliadas')
    N = [d for d in N if d['items']][-60:]
    W(os.path.join(D, 'novedades.json'), N)
    print(f"novedades: {len(nuevos)} añadidas el {hoy} ({sum(1 for i in nuevos if i['tipo']=='app')} de la app)")
else:
    print('novedades: nada que anunciar' if previa is not None else 'novedades: primera huella guardada, no se anuncia nada')
W(HU, {k: [huella(v[0]), largo(v[0])] for k, v in actual.items()})
