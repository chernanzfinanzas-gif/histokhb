#!/usr/bin/env python3
"""«La historia en un año» (calendario cósmico): coloca cada ficha de época en un día y hora del año,
como si los 13.800 millones de años de historia del universo cupieran en un año (1 ene 0:00 = Big Bang,
31 dic 24:00 = hoy). Escribe datos/calendario.json. Se ejecuta solo en cada publicación.

Fecha de cada ficha: su año 'y' del índice; si no tiene (Cosmos y Prehistoria), el primer
«Hace N millones/mil años» de su fecha 'd'. Las que no se pueden fechar se saltan.
"""
import json, os, re, datetime
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EDAD = 13.8e9
HOY = datetime.date.today().year
SEG_ANO = 365 * 86400

def hace(f):
    if f.get('y') is not None: return max(HOY - f['y'], 0.5)
    d = (f.get('d') or '').replace(' ', ' ')
    m = re.search(r'(\d[\d.]*(?:,\d+)?)\s*(millones|mil)?(?:\s+de)?\s*años', d)
    if not m: m = re.search(r'(\d[\d.]*(?:,\d+)?)\s*Ma\b', d); u = 'millones' if m else None
    else: u = m.group(2)
    if not m: return None
    n = float(m.group(1).replace('.', '').replace(',', '.'))
    return n * (1e6 if u == 'millones' else 1e3 if u == 'mil' else 1)

idx = json.load(open(os.path.join(R, 'datos', 'indice.json'), encoding='utf-8'))
sec = {s['id']: s['t'] for s in idx['secciones']}
out = []
for k, f in idx['fichas'].items():
    a = hace(f)
    if a is None: continue
    s = max(0.0, (1 - min(a, EDAD) / EDAD) * SEG_ANO)      # segundos desde el 1 de enero 0:00
    out.append([round(s, 3), k, round(a)])
out.sort()
json.dump({'edad': EDAD, 'seg_ano': SEG_ANO, 'f': out}, open(os.path.join(R, 'datos', 'calendario.json'), 'w', encoding='utf-8'), separators=(',', ':'))
if __name__ == '__main__':
    def fecha(s):
        t = datetime.datetime(2025, 1, 1) + datetime.timedelta(seconds=s)
        return t.strftime('%d %b %H:%M:%S')
    print(f'calendario: {len(out)} de {len(idx["fichas"])} fichas colocadas')
    for s, k, a in out[::40]: print(' ', fecha(s), k, idx['fichas'][k]['t'][:50])
