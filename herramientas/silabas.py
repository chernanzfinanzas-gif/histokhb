"""Cuenta sílabas en el texto y núcleos silábicos (picos de voz) en el audio, para repartir el tiempo
según lo que de verdad se pronuncia (más fiable que contar letras: los números se leen enteros y las pausas no cuentan)."""
import re, subprocess
import numpy as np
try:
    from num2words import num2words
except ImportError:
    num2words = None

V = 'aeiouáéíóúüy'
def silabas(t):
    t = t.lower()
    if num2words:
        t = re.sub(r'\d[\d.]*', lambda m: ' ' + (num2words(int(m.group().replace('.', '')), lang='es') if len(m.group().replace('.', '')) < 13 else m.group()) + ' ', t)
    t = re.sub(r'[^a-záéíóúüñ ]', ' ', t)
    n = 0
    for w in t.split():
        g = re.findall(rf'[{V}]+', w)
        n += sum(1 + (len(x) > 2) + bool(re.search(r'[aeoáéó][aeoáéó]', x)) for x in g) or 1
    return n

def envolvente(mp3, sr=8000, hop=0.01):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', mp3, '-ac', '1', '-ar', str(sr), '-f', 's16le', '-'], capture_output=True).stdout
    x = np.frombuffer(raw, np.int16).astype(np.float32) / 32768
    h = int(sr * hop); n = len(x) // h
    e = np.sqrt((x[:n * h].reshape(n, h) ** 2).mean(1) + 1e-10)
    return 20 * np.log10(e), len(x) / sr

def nucleos(db, hop=0.01):
    """Tiempos de picos de intensidad que parecen sílabas (método de De Jong y Wempe, simplificado)."""
    k = np.ones(5) / 5; d = np.convolve(db, k, 'same')
    umbral = np.median(d[d > d.max() - 50]) - 2
    pk = []
    last = -1; lastv = -1e9
    for i in range(1, len(d) - 1):
        if d[i] >= d[i - 1] and d[i] > d[i + 1] and d[i] > umbral:
            if pk:
                dip = d[pk[-1]:i].min()
                if i - pk[-1] < 8 or min(d[i], d[pk[-1]]) - dip < 2:
                    if d[i] > d[pk[-1]]: pk[-1] = i
                    continue
            pk.append(i)
    return np.array(pk) * hop
