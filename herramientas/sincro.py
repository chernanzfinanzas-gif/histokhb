#!/usr/bin/env python3
"""Sincronía exacta texto-voz: busca en cada audio las pausas entre párrafos y guarda el segundo
en que empieza cada párrafo en datos/sincro.json  {"<código>|<nivel>": [s0, s1, …]}.
La app la usa para resaltar y desplazar el texto; si un audio no está aquí, sigue estimando por letras.

Uso:  python3 herramientas/sincro.py audio/des-baler-dg.mp3 …   (o una carpeta con los mp3)
El orden de párrafos es el mismo que usa la app (p, h4, li, .tt; sin bibliografía ni botones).
"""
import json, os, re, subprocess, sys, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(R, 'datos', 'sincro.json')

def J(p):
    with open(p, encoding='utf-8') as f: return json.load(f)

_TXT = {}
def texto(cod, nivel):
    """HTML del texto que se leyó y cabecera leída antes (título en los desarrollos)."""
    if nivel in ('d', 'dg'):
        D = _TXT.setdefault('des', J(os.path.join(R, 'datos', 'desarrollos.json')))
        d = D[cod]; return (d['hg'] if nivel == 'dg' else d['h']), d['t']
    idx = _TXT.setdefault('idx', J(os.path.join(R, 'datos', 'indice.json')))
    sec = idx['fichas'][cod]['sec']
    F = _TXT.setdefault(sec, J(os.path.join(R, 'datos', f'fichas-{sec}.json')))
    return F[cod][nivel], None

def elementos(h, largos=False):
    """Párrafos en el orden de la app (audSyncBuild): p, h4, li y .tt que no contienen otros.
    Con largos=True devuelve también las letras que de verdad se leen en cada uno (como voces.py:
    el recuadro infantil se lee «Y ahora, para los más pequeños.» y la cronología empieza por «Cronología.»)."""
    h = re.sub(r'<div class="biblio">.*?</div>', '', h, flags=re.S)
    h = re.sub(r'<button[^>]*>.*?</button>', '', h, flags=re.S)
    out, lg = [], []; crono = [m.start() for m in re.finditer(r'<ul class="crono">', h)]
    for m in re.finditer(r'<(p|h4|li)(?:\s[^>]*)?>(.*?)</\1>|<div class="tt">(.*?)</div>', h, re.S):
        inner = m.group(2) if m.group(2) is not None else m.group(3)
        if inner is None or re.search(r'<(p|li)[\s>]', inner): continue
        t = html.unescape(re.sub(r'<[^>]+>', '', inner)).strip()
        if not t: continue
        L = 32 if m.group(3) is not None else len(t)
        if m.group(1) == 'li' and any(0 <= m.start() - c < 25 for c in crono): L += 12
        out.append(t); lg.append(L)
    return (out, lg) if largos else out

def pausas(mp3):
    r = subprocess.run(['ffmpeg', '-hide_banner', '-i', mp3, '-af', 'silencedetect=noise=-35dB:d=0.15', '-f', 'null', '-'],
                       capture_output=True, text=True).stderr
    fin = [float(x) for x in re.findall(r'silence_end: ([\d.]+)', r)]
    dur = [float(x) for x in re.findall(r'silence_duration: ([\d.]+)', r)]
    tot = float(re.findall(r'Duration: (\d+):(\d+):([\d.]+)', r) and
                (lambda h, m, s: int(h) * 3600 + int(m) * 60 + float(s))(*re.findall(r'Duration: (\d+):(\d+):([\d.]+)', r)[0]))
    return list(zip(fin, dur)), tot

def alinear(est, P, tot):
    """est = segundo previsto de inicio de cada párrafo (por sílabas pronunciadas en el audio).
    Ajusta cada inicio a una pausa real cercana: premia pausas largas, castiga alejarse de lo previsto
    y que un tramo dure distinto de lo previsto. Devuelve None si no encaja."""
    import math, bisect
    n = len(est)
    if n == 0 or tot <= 0: return None
    C = sorted([(0.0, 3.0)] + [(t, d) for t, d in P if 0.3 < t < tot - 0.5] + [(e, 0.0) for e in est[1:] if 0.3 < e < tot - 0.5]); M = len(C); tc = [c[0] for c in C]
    pz = [min(d, 2.0) * 3.0 for _, d in C]; pz[0] = 0
    W = 15.0
    def lejos(t, e): return 0.15 * abs(t - e)
    def tramo(dt, de): return 1.5 * math.log(max(dt, 1.0) / max(de, 4.0)) ** 2 if dt > de or de > 4 else 0.0
    INF = float('inf'); dp = [dict() for _ in range(n)]
    for i in range(n):
        lo = bisect.bisect_left(tc, est[i] - W); hi = bisect.bisect_right(tc, est[i] + W)
        cand = range(lo, hi) if i else ([0] if est[0] < 1.0 else range(max(lo, 1), hi))
        for j in cand:
            if i == 0: dp[0][j] = (lejos(tc[j], est[0]) - pz[j], -1); continue
            best = (INF, -1)
            for k, (c, _) in dp[i - 1].items():
                if k >= j: continue
                v = c + tramo(tc[j] - tc[k], est[i] - est[i - 1])
                if v < best[0]: best = (v, k)
            if best[1] >= 0: dp[i][j] = (best[0] + lejos(tc[j], est[i]) - pz[j], best[1])
        if not dp[i]: return None
    j = min(dp[n - 1], key=lambda x: dp[n - 1][x][0]); res = []
    for i in range(n - 1, -1, -1): res.append(round(tc[j], 2)); j = dp[i][j][1]
    return res[::-1]

def previstos(els, cab, pk, tot):
    """Inicio previsto de cada párrafo: sílabas del texto repartidas sobre los picos de voz del audio."""
    import silabas as S
    sy = [S.silabas(x) for x in els]; lead = S.silabas(cab) if cab else 0; T = lead + sum(sy)
    out, cum = [], lead
    for x in sy:
        k = int(cum / T * len(pk)); t = pk[min(k, len(pk) - 1)] if len(pk) else cum / T * tot
        out.append(0.0 if cum == 0 else max(0.0, t - 0.25)); cum += x
    return out

def procesa(mp3, P=None, tot=None, pk=None):
    b = os.path.basename(mp3)[:-4]; cod, nivel = b.rsplit('-', 1)
    h, cab = texto(cod, nivel); els = elementos(h)
    if P is None:
        import silabas as S
        P, tot = pausas(mp3); db, _ = S.envolvente(mp3); pk = S.nucleos(db)
    return f'{cod}|{nivel}', alinear(previstos(els, cab, pk, tot), P, tot), tot, []

def lee_tsv(p):
    """Medidas hechas fuera (en el PC, para no bajar 2,4 GB de audio): nombre, duración, fin:dur;… de las
    pausas y centésimas de los picos de voz. Lo genera med.py (silabas.py + silencedetect) en Multimedia."""
    import gzip
    for l in (gzip.open(p, 'rt', encoding='utf-8') if p.endswith('.gz') else open(p, encoding='utf-8')):
        c = l.rstrip('\n').split('\t')
        if len(c) < 4 or not c[1]: continue
        P = [tuple(map(float, x.split(':'))) for x in c[2].split(';') if ':' in x]
        pk = [int(x) / 100 for x in c[3].split(',') if x]
        yield c[0], P, float(c[1]), pk

if __name__ == '__main__':
    tareas = []
    for a in sys.argv[1:]:
        if a.endswith(('.tsv', '.tsv.gz')): tareas += list(lee_tsv(a))
        elif os.path.isdir(a): tareas += [(os.path.join(a, x), None, None, None) for x in sorted(os.listdir(a)) if x.endswith('.mp3')]
        else: tareas.append((a, None, None, None))
    S = J(OUT) if os.path.exists(OUT) else {}
    ok = mal = 0; avisos = []
    sin = []
    for f, P, tot, pk in tareas:
        try:
            k, ts, tot, raro = procesa(f, P, tot, pk)
            if ts: S[k] = ts; ok += 1
            else: sin.append(k)
            avisos += [f'{k}: {r}' for r in raro]
        except Exception as e:
            mal += 1; print('  no se pudo:', os.path.basename(f), type(e).__name__, e)
    with open(OUT, 'w', encoding='utf-8') as fh: json.dump(dict(sorted(S.items())), fh, separators=(',', ':'))
    print(f'sincro: {ok} audios medidos, {mal} con error, {len(sin)} sin encajar (siguen por letras), {len(S)} en total')
    if avisos: print('Audios sospechosos:', *avisos, sep='\n  ')
