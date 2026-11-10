#!/usr/bin/env python3
"""Voces de la sección «Inglés con historia» (datos/ingles.json) con Gemini-TTS de AI Studio.

Cada tema tiene tres niveles (easy, medium, hard) y cada nivel una lista de frases [inglés, castellano].
Se graba cada nivel en UNA petición, con una pausa tras cada frase; luego se buscan esas pausas para saber
en qué segundo empieza cada frase (la app resalta la frase que suena y deja oír una sola).
Sale audio/en-<tema>-<nivel>.mp3 a 96 kbps (a 48 se pierden las consonantes finales y las sibilantes).

Uso:  GEMINI_API_KEY_FILE=/ruta/aistudio.txt python3 herramientas/voces_ingles.py balmis [otro…]
      NIVELES=easy,hard ...  (solo esos niveles)
Después: python3 herramientas/medios.py subir audio/en-<tema>-*.mp3   (y git checkout datos/sincro.json)
"""
import base64, json, os, re, subprocess, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import voces as V
from comun import REPO, TMP

P = {'easy': "Read this in clear, standard British English for an adult who is learning English (level A2): slowly and very clearly, "
             "pronouncing the end of every word, with a pause of about one second after each sentence. Calm and friendly, like a good teacher.",
     'medium': "Read this in clear, standard British English for an intermediate learner (level B1): a little slower than normal conversation, "
               "very clear, with a pause of about one second after each sentence. Warm and interested, like a documentary narrator.",
     'hard': "Read this in natural, standard British English at a normal documentary pace, warm and clear, "
             "with a short pause of about one second after each sentence."}
VOCES_EN = ['Iapetus', 'Aoede', 'Achird', 'Despina']
MALO = ('british english', 'learner', 'documentary', 'teacher', 'pause of about', 'level a2', 'level b1')

def oye_en(dst, a, d, clave):
    """Dictado en inglés de d segundos desde a (para comprobar si Gemini ha leído la instrucción)."""
    import requests, tempfile
    t = tempfile.mktemp(suffix='.mp3')
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-ss', str(a), '-t', str(d), '-i', dst, '-ac', '1', '-ar', '16000', '-b:a', '32k', t])
    au = {"inline_data": {"mime_type": "audio/mp3", "data": base64.b64encode(open(t, 'rb').read()).decode()}}
    for m in list(V.MODELOS_OIDO):
        b = {"contents": [{"parts": [au, {"text": "Transcribe" if 'transcribe' in m else "Transcribe this English audio literally. Only the text."}]}]}
        try:
            r = requests.post(f"https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent", headers={"x-goog-api-key": clave}, json=b, timeout=120)
            if r.ok:
                pt = r.json()['candidates'][0]['content']['parts'][0]
                x = (pt.get('audioTranscription') or {}).get('text') or pt.get('text') or ''
                if x.strip(): return x.lower()
        except Exception: pass
    return None

def dur(p):
    return float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', p], capture_output=True, text=True).stdout)

def silencios(p, d=0.3):
    r = subprocess.run(['ffmpeg', '-hide_banner', '-i', p, '-af', f'silencedetect=noise=-35dB:d={d}', '-f', 'null', '-'], capture_output=True, text=True).stderr
    a = [float(x) for x in re.findall(r'silence_start: ([\d.]+)', r)]; b = [float(x) for x in re.findall(r'silence_end: ([\d.]+)', r)]
    return list(zip(a, b))

def cortes(w, frases):
    """Segundo en que empieza cada frase. Candidatas: todas las pausas (≥0,12 s) que no son la del principio ni la del final.
    Cada corte se busca cerca de donde caería si la voz fuera pareja (proporcional a las letras), prefiriendo las pausas
    largas: así una coma no se confunde con un punto."""
    D = dur(w); cand = [(a, b) for a, b in silencios(w, 0.12) if a > 0.3 and b < D - 0.3]
    if len(cand) < len(frases) - 1: return None
    L = [len(f) for f in frases]; tot = sum(L); t = [0.0]; acc = 0; usadas = set()
    for i in range(len(frases) - 1):
        acc += L[i]; e = D * acc / tot
        mejor = min((c for c in cand if c[1] > t[-1] + 0.5 and c not in usadas),
                    key=lambda ab: abs(ab[1] - e) - 3 * (ab[1] - ab[0]), default=None)
        if mejor is None: return None
        usadas.add(mejor); t.append(round(mejor[1] - 0.12, 2))
    return t

def graba(tema, k, nv, voz, clave):
    frases = [f[0] for f in nv['fr']]
    w = os.path.join(TMP, f'en-{tema}-{k}.wav')
    for q in (w, w[:-4] + '.lb.wav'):   # nunca reutilizar un intento anterior (ni su copia limpia)
        if os.path.exists(q): os.remove(q)
    if not V.tts_aistudio('\n\n'.join(frases), voz, P[k], w, clave): return None
    x = oye_en(w, 0, 6, clave)
    if x is None: print('ERR: sin cupo de dictado para comprobar la instrucción', tema, k); os.remove(w); return None
    if any(m in x for m in MALO): print('ERR: ha leído la instrucción en voz alta', tema, k); os.remove(w); return None
    w = V.limpia_bordes(w); D = dur(w)
    car = sum(len(f) for f in frases)
    if car / D > 22: print(f'ERR: audio incompleto ({car / D:.1f} letras/s)', tema, k); return None
    if any(b - a > 6 for a, b in silencios(w, 6)): print('ERR: silencio de más de 6 s', tema, k); return None
    # comienzo de cada frase (ver cortes)
    t = cortes(w, frases)
    if t is None: print(f'ERR: no encuentro las pausas entre frases', tema, k); return None
    out = f'audio/en-{tema}-{k}.mp3'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', w, '-ac', '1', '-b:a', '96k', os.path.join(REPO, out)], check=True)
    return {'audio': out, 'voz': voz, 's': round(D), 't': t}

if __name__ == '__main__':
    clave = V._clave(); assert clave, 'falta GEMINI_API_KEY_FILE'
    p = os.path.join(REPO, 'datos', 'ingles.json'); I = json.load(open(p, encoding='utf-8'))
    niv = (os.environ.get('NIVELES') or 'easy,medium,hard').split(',')
    temas = {t['id']: (i, t) for i, t in enumerate(I['temas'])}
    hechos = 0
    for tema in sys.argv[1:]:
        i, T = temas[tema]; voz = T.get('voz') or VOCES_EN[i % len(VOCES_EN)]
        for k in niv:
            r = graba(tema, k, T['niveles'][k], voz, clave)
            if r: T['niveles'][k].update(r); hechos += 1; print('OK', tema, k, r['s'], 's')
            else: print('FALTA', tema, k)
            json.dump(I, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('FIN', hechos)
