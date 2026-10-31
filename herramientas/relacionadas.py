#!/usr/bin/env python3
"""«Para saber más de…»: para cada ficha de época, grupos de historias relacionadas (fichas de sincronía,
otras fichas de época y desarrollos) que comparten con ella un nombre clave (lo que va en negrita).
Escribe datos/relacionadas.json  {ficha: [[etiqueta, [claves…]], …]}  (claves: f:…, s:región|año, d:…)."""
import json, os, re, html, math, unicodedata, collections, glob, sys
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def J(p): return json.load(open(os.path.join(R, 'datos', p), encoding='utf-8'))
def norm(s): return ''.join(c for c in unicodedata.normalize('NFD', s.lower()) if unicodedata.category(c) != 'Mn')
VACIAS = set('el la los las un una de del y o en a al su sus que con por para como mas muy se es fue son era'.split())
def negritas(h):
    out = {}
    for m in re.findall(r'<b>(.*?)</b>', sinbib(h), re.S):
        t = html.unescape(re.sub(r'<[^>]+>', '', m)).strip(' .,;:«»"()')
        if not t or len(t) < 3 or len(t) > 40 or re.fullmatch(r'[\d\s.,–-]+(a\. ?C\.)?', t) or re.search(r'\d{3,}', t): continue
        if not re.search(r'[A-ZÁÉÍÓÚÑ]', t[:1]): continue          # solo nombres propios (empiezan en mayúscula)
        n = norm(t)
        if n in VACIAS: continue
        out.setdefault(n, t)
    return out

I = J('indice.json')['fichas']
def anio(f):
    if f.get('y') is not None: return f['y']
    d = (f.get('d') or '').replace('\u00a0', ' ')
    m = re.search(r'(\d[\d.]*(?:,\d+)?)\s*(millones|mil)?(?:\s+de)?\s*años', d)
    if not m: return None
    n = float(m.group(1).replace('.', '').replace(',', '.')) * (1e6 if m.group(2) == 'millones' else 1e3 if m.group(2) == 'mil' else 1)
    return int(2026 - n)
DES = J('desarrollos.json'); SE = J('sinc-eventos.json')['ev']
def sinbib(h): return re.sub(r'<div class="biblio">.*?</div>', ' ', h or '', flags=re.S)
def plano(h):   # sin tildes pero conservando mayúsculas (para no confundir «domingo» con Santo Domingo)
    t = html.unescape(re.sub(r'<[^>]+>', ' ', sinbib(h)))
    return ''.join(c for c in unicodedata.normalize('NFD', t) if unicodedata.category(c) != 'Mn')
CRUDO = {}     # clave -> texto plano normalizado (para buscar en él los nombres del vocabulario)
items = {}     # clave -> (título, {norm: forma}, año)
for sec in {f['sec'] for f in I.values()}:
    F = J(f'fichas-{sec}.json')
    for k, f in F.items():
        if k in I:
            h = (f.get('p') or '') + (f.get('g') or ''); items['f:' + k] = (I[k]['t'], negritas(h), anio(I[k])); CRUDO['f:' + k] = plano(I[k]['t'] + ' ' + h)
# año de un desarrollo: el de la ficha que lo contiene (su botón «📖» está en ella)
DUENO = {}
for sec in {f['sec'] for f in I.values()}:
    for fk, f in J(f'fichas-{sec}.json').items():
        if fk in I:
            for dk in re.findall(r"#/d/([\w-]+)", ' '.join(f.get(n) or '' for n in 'ngp')): DUENO.setdefault(dk, anio(I[fk]))
for k, d in DES.items(): items['d:' + k] = (d['t'], negritas(d.get('h')), DUENO.get(k)); CRUDO['d:' + k] = plano(d['t'] + ' ' + (d.get('h') or ''))
TIT = {(r + '|' + str(e[0])): e[1] for r, a in SE.items() for e in a}
for p in glob.glob(os.path.join(R, 'datos', 'sinc-det-*.json')):
    for k, h in json.load(open(p, encoding='utf-8')).items():
        if k in TIT: items['s:' + k] = (TIT[k], negritas(h), int(k.rsplit('|', 1)[1])); CRUDO['s:' + k] = plano(TIT[k] + ' ' + h)
for l in J('lugares.json')['lugares']:      # pueblos y ciudades con historia propia (como mucho uno por grupo)
    h = (l.get('texto') or {}).get('general') or ''
    if h: items['l:' + l['id']] = (l['nombre'], negritas(h), None); CRUDO['l:' + l['id']] = plano(l['nombre'] + ' ' + h)
# vocabulario: todo lo que alguna ficha pone en negrita; luego se busca en el texto completo de todas
FORMA = {}
for _, ns, _ in items.values():
    for n, f in ns.items(): FORMA.setdefault(n, f)
for n in ('para saber mas', 'sabias que', 'cronologia', 'debates'): FORMA.pop(n, None)
# nombres de pila sueltos y palabras genéricas: no sirven para agrupar
GENERICAS = set(norm(x) for x in '''Juan Carlos Fernando Felipe Alfonso Pedro Luis María Isabel Francisco Enrique Jaime Ramón Sancho García
Diego Manuel José Antonio Miguel Pablo Jorge Guillermo Ricardo Federico Alejandro Margarita Catalina Ana Juana Leonor Blanca Teresa
Constitución Imperio Iglesia Estado Revolución Cortes Concilio Reino Corona Papa Rey Reina Guerra Edad República Parlamento
Gobierno Ejército Universidad Museo Catedral Palacio Tratado Batalla Paz Senado Monarquía Dios Islam Cristianismo Biblia
Occidente Oriente Norte Sur Edad Este Oeste Antigüedad Prehistoria Neolítico Paleolítico Renacimiento Ilustración Romanticismo
Unesco ONU Patrimonio Humanidad Unión Atlántico Mediterráneo Catolicós Cielo Tierra Sol Luna Mar Agua Fuego Vida Muerte Hombre Mujer Mundo Historia Ciudad Pueblo Gente Tiempo Arte Ciencia Dinastía Templo Puerto Río Isla Montaña'''.split())
for n in [x for x in FORMA if x.startswith('siglo ') or re.fullmatch(r'[ivxlcdm]+', x)] + ['santa maria']: FORMA.pop(n, None)
for n in GENERICAS | {'edad media', 'edad moderna', 'edad contemporanea', 'edad antigua', 'segunda guerra mundial', 'primera guerra mundial'} - {'segunda guerra mundial', 'primera guerra mundial'}: FORMA.pop(n, None)
VOC = {n for n in FORMA if len(n) >= 4}
LMAX = max(len(n.split()) for n in VOC)
for k, txt in CRUDO.items():
    W = re.findall(r'[A-Za-z0-9ñÑ]+', txt); w = [x.lower() for x in W]; hall = {}
    i = 0
    while i < len(w):                     # en cada punto, el nombre más largo («Nueva York», no «York»)
        for L in range(LMAX, 0, -1):
            g = ' '.join(w[i:i + L])
            if g in VOC and (L > 1 or W[i][0].isupper()): hall[g] = FORMA[g]; i += L - 1; break   # palabra suelta: solo en mayúscula
        i += 1
    t, ns, y = items[k]; items[k] = (t, hall, y)
df = collections.Counter(n for _, ns, _ in items.values() for n in ns)
N = len(items)
def idf(n): return math.log(N / df[n])
idx = collections.defaultdict(set)
for k, (_, ns, _) in items.items():
    for n in ns: idx[n].add(k)

HOY = 2026
def cerca(y1, y2):
    """1 si son de la misma época; baja con la distancia, medida en proporción a lo lejos que quedan de hoy."""
    if y1 is None or y2 is None: return 0.6
    esc = max(25, 0.25 * max(HOY - min(y1, y2), 1))
    return math.exp(-abs(y1 - y2) / esc)

def grupos(k, maxg=8, maxi=10):
    t, ns, y = items[k]
    util = [n for n in ns if 2 <= df[n] <= 250]
    cand = collections.defaultdict(float)
    for n in util:
        for c in idx[n]:
            if c != k and items[c][0].strip(): cand[c] += idf(n)
    for c in list(cand):
        f = cerca(y, items[c][2])
        if f < 0.35: del cand[c]
        else: cand[c] *= f
    def en_titulo(n, c): return n in norm(items[c][0])
    def vale(n, c): return cand[c] >= 1.4 * idf(n) or en_titulo(n, c)     # comparte más de un nombre, o lo lleva en el título
    peso = {n: sum(cand[c] * (2 if en_titulo(n, c) else 1) for c in idx[n] if c in cand and vale(n, c)) for n in util}
    usados, out = set(), []
    SIN = {'union sovietica': 'urss', 'reyes catolicos': 'isabel y fernando'}
    def raiz(n): return set(SIN.get(n, n).split()) - {'san', 'santa', 'de', 'del', 'la', 'el', 'los', 'las', 'y'}
    elegidos = []
    for n in sorted(util, key=lambda n: -peso[n]):
        r = raiz(n)
        if any(r <= e or e <= r for e in elegidos): continue      # «Isidoro» ⊂ «Isidoro de Sevilla» ⊂ «San Isidoro»: un solo grupo
        g0 = sorted((c for c in idx[n] if c in cand and c not in usados and vale(n, c) and cand[c] > 0.8), key=lambda c: (-en_titulo(n, c), -cand[c]))
        g, lug, vistos = [], 0, {norm(items[x][0]) for x in usados}
        for c in g0:
            tn = norm(items[c][0])
            if tn in vistos or tn == norm(t): continue             # mismo título (ficha y sincronía gemelas): una sola vez
            vistos.add(tn)
            if c.startswith('l:'):
                if lug: continue
                lug = 1
            g.append(c)
            if len(g) >= maxi: break
        if len(g) < 2: continue
        g.sort(key=lambda c: (items[c][2] is None, items[c][2] if items[c][2] is not None else 0))   # de antiguo a moderno; los lugares al final
        out.append([ns[n], g]); usados.update(g); elegidos.append(r)
        if len(out) >= maxg: break
    # pocas historias en total (6 o menos): van juntas, sin grupos
    if sum(len(g) for _, g in out) <= 6: out = [[None, [c for _, g in out for c in g]]] if out else []
    return out

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'ver':
        for k in sys.argv[2:]:
            print('==', items['f:' + k][0])
            for lab, g in grupos('f:' + k): print('  Para saber más de', lab, '→', ' · '.join(items[c][0][:45] for c in g))
        sys.exit()
    out = {k[2:]: grupos(k) for k in items if k.startswith('f:')}
    # los lugares que no son ficha también pueden aparecer: se guardan con su clave l:… (la app abre #/l/…)
    # «Más historias de esta época»: cada ficha de sincronía que no ha salido en ningún grupo va a la ficha de época
    # más cercana en el tiempo que hable de su región o de algún nombre suyo (como mucho 12 por ficha)
    usadas = {c for v in out.values() for _, g in v for c in g}
    fichas = [k for k in items if k.startswith('f:') and items[k][2] is not None]
    reg = {k: norm(k[2:].rsplit('|', 1)[0]) for k in items if k.startswith('s:')}
    extra = collections.defaultdict(list)
    for s in sorted((k for k in items if k.startswith('s:') and k not in usadas), key=lambda k: items[k][2]):
        y = items[s][2]; pal = [w for w in re.findall(r'[a-z]{4,}', reg[s]) if w not in ('castilla', 'espana', 'hispania')] or re.findall(r'[a-z]{4,}', reg[s])
        def nota(f):
            c = cerca(y, items[f][2]); txt = CRUDO[f].lower()
            return c * (1 + 2 * any(w in txt for w in pal) + sum(idf(n) for n in items[s][1] if n in items[f][1]) / 5)
        for f in sorted(fichas, key=lambda f: -nota(f)):
            if nota(f) < 0.3: break
            if len(extra[f]) < 12: extra[f].append(s); break
    for f, g in extra.items():
        g.sort(key=lambda c: items[c][2]); out.setdefault(f[2:], []).append(['Más historias de esta época', g])
    out = {k: v for k, v in out.items() if v}
    json.dump(out, open(os.path.join(R, 'datos', 'relacionadas.json'), 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
    print(f'relacionadas: {len(out)} de {sum(1 for k in items if k.startswith("f:"))} fichas con grupos; {sum(len(v) for v in out.values())} grupos')
