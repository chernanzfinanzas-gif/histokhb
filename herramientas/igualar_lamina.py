"""Si un vídeo de Gemini no coincide con su lámina (Gemini redibujó), la lámina pasa a ser
el primer fotograma del vídeo, para que imagen fija y vídeo encajen.
Uso: python3 herramientas/igualar_lamina.py [códigos...]  (sin códigos: todos los viva_tipo=gemini)"""
import json, subprocess, sys, os, tempfile
from PIL import Image, ImageChops, ImageStat
UMBRAL = 15
A = json.load(open('datos/audio.json'))['fichas']
cods = sys.argv[1:] or [k for k, v in A.items() if v.get('viva_tipo') == 'gemini']
for k in cods:
    vid, lam = f'img/vivas/{k}.mp4', f'img/laminas/{k}.webp'
    if not (os.path.exists(vid) and os.path.exists(lam)): print(k, 'falta vídeo o lámina'); continue
    png = os.path.join(tempfile.gettempdir(), f'{k}-f0.png')
    subprocess.run(['ffmpeg', '-v', 'quiet', '-y', '-i', vid, '-frames:v', '1', png], check=True)
    F = Image.open(png).convert('RGB'); L = Image.open(lam).convert('RGB')
    d = ImageStat.Stat(ImageChops.difference(L.convert('L').resize((160, 90)), F.convert('L').resize((160, 90)))).mean[0]
    if d <= UMBRAL: print(f'{k}: coincide ({d:.0f})'); continue
    w, h = F.size; nh = round(w * 9 / 16)
    if nh <= h: F = F.crop((0, (h - nh) // 2, w, (h - nh) // 2 + nh))
    F.resize((1000, 562), Image.LANCZOS).save(lam, 'WEBP', quality=88)
    print(f'{k}: Gemini redibujó ({d:.0f}) -> lámina sustituida por el primer fotograma')
