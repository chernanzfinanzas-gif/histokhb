#!/usr/bin/env python3
"""Sincronía exacta por dictado (para audios donde las pausas engañan): dicta el audio en trozos de 10 s con
Gemini (gemini-3.5-transcribe, clave de AI Studio), y busca en el dictado dónde empieza cada párrafo.
Uso: GEMINI_API_KEY_FILE=… python3 herramientas/sincro_dictado.py audio/<código>-<nivel>.mp3
Escribe el resultado en datos/sincro.json (sustituye la entrada de ese audio)."""
import sys, os, json, re, base64, time, subprocess, tempfile, unicodedata, difflib, urllib.request
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sincro
def norm(s): return re.sub(r'[^a-z0-9ñ ]', ' ', ''.join(c for c in unicodedata.normalize('NFD', s.lower()) if unicodedata.category(c) != 'Mn'))
def dicta(mp3, a, d, k):
    t = tempfile.mktemp(suffix='.mp3')
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-ss', str(a), '-t', str(d), '-i', mp3, '-ac', '1', '-ar', '16000', '-b:a', '32k', t])
    body = {"contents": [{"parts": [{"inline_data": {"mime_type": "audio/mp3", "data": base64.b64encode(open(t, 'rb').read()).decode()}}, {"text": "Transcribe"}]}]}
    for i in range(6):
        try:
            r = urllib.request.Request('https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-transcribe:generateContent', json.dumps(body).encode(), {'Content-Type': 'application/json', 'x-goog-api-key': k})
            return json.load(urllib.request.urlopen(r, timeout=90))['candidates'][0]['content']['parts'][0]['audioTranscription']['text']
        except Exception as e:
            time.sleep(10 * (i + 1))
    return ''
PASO = float(os.environ.get('PASO', '20')); ESPERA = float(os.environ.get('ESPERA', '8'))
if __name__ == '__main__':
    mp3 = sys.argv[1]; k = open(os.environ['GEMINI_API_KEY_FILE']).read().strip()
    b = os.path.basename(mp3)[:-4]; cod, nivel = b.rsplit('-', 1)
    h, cab = sincro.texto(cod, nivel); els = sincro.elementos(h)
    tot = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', mp3], capture_output=True, text=True).stdout)
    # palabras dictadas con su segundo aproximado (repartidas de forma uniforme dentro de cada trozo de 10 s)
    W = []; a = 0.0
    while a < tot:
        txt = norm(dicta(mp3, a, PASO, k)).split(); d = min(PASO, tot - a)
        W += [(w, a + d * (i + 0.5) / max(1, len(txt))) for i, w in enumerate(txt)]
        print(f'{a:6.0f} s · {len(txt)} palabras', flush=True); a += PASO; time.sleep(ESPERA)
    pal = [w for w, _ in W]; ts = []; desde = 0
    for e in els:
        q = norm(e).split()[:6]; mejor = (0, None)
        for i in range(desde, len(pal) - len(q) + 1):
            r = difflib.SequenceMatcher(None, q, pal[i:i + len(q)]).ratio()
            if r > mejor[0]: mejor = (r, i)
            if r == 1: break
        i = mejor[1] if mejor[0] >= 0.5 else None
        if i is None: ts.append(None); continue
        ts.append(round(max(0, W[i][1] - 0.4), 2)); desde = i + 1
    S = json.load(open(sincro.OUT, encoding='utf-8')); viejo = S.get(f'{cod}|{nivel}', [])
    ts = [t if t is not None else (viejo[j] if j < len(viejo) else 0) for j, t in enumerate(ts)]
    for j, (e, t) in enumerate(zip(els, ts)): print(f'{t:7.1f}  (antes {viejo[j] if j < len(viejo) else "-":>6})  {e[:45]}')
    S[f'{cod}|{nivel}'] = ts
    json.dump(dict(sorted(S.items())), open(sincro.OUT, 'w', encoding='utf-8'), separators=(',', ':'))
