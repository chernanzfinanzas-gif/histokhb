#!/usr/bin/env python3
"""Audiolibro de un libro de la Biblioteca con la voz de Gemini (AI Studio).

Uso: python3 herramientas/libro_audio.py <carpeta del libro> [ids de capítulo…]
  Lee index.html, toma de cada sección .cap los elementos p, h2 y li (sin línea de tiempo,
  figuras ni botones), los lee por trozos y deja audio/<id>.mp3 y audio/<id>.json con el
  segundo en que empieza cada elemento.
Claves: /home/claude/.claves/aistudio.txt (gratis) y aistudio-pago.txt (pago).
Primero gasta la gratis; si se agota, sigue con la de pago sin pasar de TOPE_PAGO_SEG en el mes
(contador en herramientas/gasto_pago.json).
"""
import base64, json, os, re, subprocess, sys, time, urllib.request, urllib.error, datetime
from bs4 import BeautifulSoup

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GASTO = os.path.join(R, 'herramientas', 'gasto_pago.json')
VOZ = os.environ.get('VOZ_LIBRO', 'Aoede')
MODELO = os.environ.get('GEMINI_TTS_MODEL', 'gemini-2.5-flash-preview-tts')
TROZO = int(os.environ.get('TROZO', '1600'))
TOPE = float(os.environ.get('TOPE_PAGO_SEG', '24000'))
CL = '/home/claude/.claves/'
claves = [('gratis', open(CL + 'aistudio.txt').read().strip()), ('pago', open(CL + 'aistudio-pago.txt').read().strip())]
PROMPT = 'Lee en español de España, con voz cálida y pausada de narradora de audiolibro de historia, haciendo una pausa clara entre párrafos:\n\n'
mes = datetime.date.today().strftime('%Y-%m')

def log(*a): print(time.strftime('%H:%M:%S'), *a, flush=True)

def gasto(add=0):
    g = json.load(open(GASTO)) if os.path.exists(GASTO) else {}
    if add:
        g[mes] = round(g.get(mes, 0) + add, 1); json.dump(g, open(GASTO, 'w'), indent=1)
    return g.get(mes, 0)

def tts(texto):
    """Devuelve (pcm, cuál). Gratis primero; ante 429 pasa a pago."""
    global claves
    while claves:
        cual, k = claves[0]
        if cual == 'pago' and gasto() >= TOPE:
            raise SystemExit('TOPE de pago alcanzado este mes: paro.')
        body = json.dumps({'contents': [{'parts': [{'text': PROMPT + texto}]}],
            'generationConfig': {'responseModalities': ['AUDIO'], 'speechConfig': {'voiceConfig': {'prebuiltVoiceConfig': {'voiceName': VOZ}}}}}).encode()
        req = urllib.request.Request(f'https://generativelanguage.googleapis.com/v1beta/models/{MODELO}:generateContent', body,
            {'Content-Type': 'application/json', 'x-goog-api-key': k})
        for intento in range(4):
            try:
                d = json.load(urllib.request.urlopen(req, timeout=300))
                pcm = base64.b64decode(d['candidates'][0]['content']['parts'][0]['inlineData']['data'])
                return pcm, cual
            except urllib.error.HTTPError as e:
                msg = e.read().decode('utf-8', 'ignore')[:300]
                if e.code == 429:
                    if 'PerDay' in msg or 'per day' in msg.lower() or intento == 3:
                        log('cupo agotado en clave', cual); claves = claves[1:]; break
                    time.sleep(40); continue
                if e.code >= 500: time.sleep(15); continue
                raise SystemExit(f'Error {e.code}: {msg}')
            except (KeyError, IndexError):
                time.sleep(10); continue
            except Exception as e:
                log('fallo de red', type(e).__name__); time.sleep(20); continue
    raise SystemExit('Sin claves con cupo: paro.')

def silencios(wav):
    o = subprocess.run(['ffmpeg', '-hide_banner', '-i', wav, '-af', 'silencedetect=n=-40dB:d=0.35', '-f', 'null', '-'], capture_output=True, text=True).stderr
    ini = [float(x) for x in re.findall(r'silence_start: ([\d.]+)', o)]
    fin = [float(x) for x in re.findall(r'silence_end: ([\d.]+)', o)]
    return [(a + b) / 2 for a, b in zip(ini, fin)]

def huecos(wav, letras, dur):
    """Motivo si la voz se cortó o balbucea (ritmo normal ~16 letras por segundo de voz); '' si está bien."""
    o = subprocess.run(['ffmpeg', '-hide_banner', '-i', wav, '-af', 'silencedetect=n=-40dB:d=0.3', '-f', 'null', '-'], capture_output=True, text=True).stderr
    sil = [float(x) for x in re.findall(r'silence_duration: ([\d.]+)', o)]
    voz = max(1, dur - sum(sil)); r = letras / voz
    if letras > 200 and not 11 <= r <= 22: return f'ritmo {r:.0f} letras/s'
    if max(sil or [0]) > 6: return f'silencio de {max(sil):.0f} s'
    return ''

def elementos(sec):
    L = [e for e in sec.select('p,h2,li') if not e.find_parent(class_='linea') and not e.find_parent('figure')
         and not e.find_parent(class_='esc') and 'esc' not in (e.get('class') or [])]
    return [re.sub(r'\s+', ' ', e.get_text(' ', strip=True)) for e in L]

def trozos(textos):
    """Agrupa elementos enteros hasta TROZO letras. Devuelve [(primer índice, [textos])]."""
    out, cur, i0 = [], [], 0
    for i, t in enumerate(textos):
        if cur and sum(len(x) for x in cur) + len(t) > TROZO:
            out.append((i0, cur)); cur, i0 = [], i
        cur.append(t)
    if cur: out.append((i0, cur))
    return out

def capitulo(carpeta, sec, cid):
    aud = os.path.join(carpeta, 'audio'); os.makedirs(aud, exist_ok=True)
    mp3 = os.path.join(aud, cid + '.mp3')
    if os.path.exists(mp3) and os.path.exists(mp3[:-4] + '.json'):
        log(cid, 'ya hecho'); return
    h1 = sec.find('h1'); tit = h1.get_text(' ', strip=True) if h1 else ''
    num = re.match(r'cap(\d+)', cid)
    cab = (f'Capítulo {int(num.group(1))}. ' if num else '') + tit + '.'
    T = elementos(sec)
    tmp = os.path.join('/home/claude/tmp-audio', cid); os.makedirs(tmp, exist_ok=True)
    inicio = [0.0] * len(T); t0 = 0.0; wavs = []
    # cabecera sola (título del capítulo)
    grupos = [(-1, [cab])] + trozos(T)
    for n, (i0, txts) in enumerate(grupos):
        wav = os.path.join(tmp, f'{n:03d}.wav')
        intento = 0
        while not os.path.exists(wav):
            intento += 1
            pcm, cual = tts('\n\n'.join(txts))
            subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 's16le', '-ar', '24000', '-ac', '1', '-i', '-', wav], input=pcm, check=True)
            dur = len(pcm) / 48000
            if cual == 'pago': gasto(dur)
            log(cid, f'trozo {n+1}/{len(grupos)}', f'{dur:.0f} s', cual, f'(pago mes: {gasto()/60:.0f} min)')
            malo = huecos(wav, sum(len(x) for x in txts), dur)
            if malo and intento < 3:
                log(cid, 'trozo defectuoso,', malo, ': repito'); os.remove(wav)
        dur = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', wav], capture_output=True, text=True).stdout)
        if i0 >= 0:
            # reparto por letras y ajuste a la pausa más cercana
            tot = sum(len(x) for x in txts); acc = 0; S = [s for s in silencios(wav) if 0.8 < s < dur - 1.5]; prev = 0.0
            for j, x in enumerate(txts):
                est = dur * acc / tot
                if j:
                    cerca = [s for s in S if abs(s - est) < 3 and s > prev + 0.8]
                    if cerca: est = min(cerca, key=lambda s: abs(s - est))
                    est = max(est, prev + 0.8)
                inicio[i0 + j] = round(t0 + (0 if j == 0 else est), 2); prev = 0 if j == 0 else est; acc += len(x)
        t0 += dur; wavs.append(wav)
    lista = os.path.join(tmp, 'lista.txt')
    open(lista, 'w').write(''.join(f"file '{w}'\n" for w in wavs))
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', lista, '-ac', '1', '-ar', '24000', '-b:a', '64k', mp3], check=True)
    json.dump({'sync': inicio, 'd': round(t0, 1)}, open(mp3[:-4] + '.json', 'w'))
    log(cid, 'HECHO', f'{t0/60:.1f} min')

def main():
    carpeta = os.path.abspath(sys.argv[1]); quiero = sys.argv[2:]
    s = BeautifulSoup(open(os.path.join(carpeta, 'index.html')).read(), 'html.parser')
    for sec in s.select('.cap'):
        cid = sec.get('id', '')[2:]
        if quiero and cid not in quiero: continue
        capitulo(carpeta, sec, cid)

if __name__ == '__main__':
    main()
