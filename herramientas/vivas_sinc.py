#!/usr/bin/env python3
"""Vídeo de Gemini para una lámina de «El mundo a la vez» (datos/laminas-sinc.json).

Cada lámina es de una zona y un siglo y sale en todas sus fichas (6-12), así que el vídeo también:
laminas-sinc.json → "_vivas": {"img/laminas/s-xxx.webp": "img/vivas/s-xxx.mp4"}. La app (slamHtml) lo pone
en lugar de la imagen; con «reducir movimiento» o ahorro de datos se queda la imagen.

Uso:  python3 herramientas/vivas_sinc.py s-egipto-a1200 /ruta/al/video-de-gemini.mp4
Después: python3 herramientas/medios.py subir img/vivas/s-egipto-a1200.mp4
Comprueba que Gemini no ha redibujado: compara el primer fotograma con la lámina (diferencia media, % ).
"""
import json, os, subprocess, sys
import numpy as np
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def gris(src, ss=None):
    a = (['-ss', str(ss)] if ss is not None else []) + ['-i', src]
    r = subprocess.run(['ffmpeg', '-v', 'error', *a, '-frames:v', '1', '-vf', 'scale=320:180', '-f', 'rawvideo', '-pix_fmt', 'gray', '-'], capture_output=True).stdout
    return np.frombuffer(r, np.uint8).astype(float)

if __name__ == '__main__':
    nom, vid = sys.argv[1], sys.argv[2]
    lam = f'img/laminas/{nom}.webp'; out = f'img/vivas/{nom}.mp4'
    p = os.path.join(R, 'datos', 'laminas-sinc.json'); L = json.load(open(p, encoding='utf-8'))
    assert lam in L.values() or lam in L.get('_fichas', {}).values(), f'{lam} no es una lámina de «El mundo a la vez»'
    os.makedirs(os.path.join(R, 'img', 'vivas'), exist_ok=True)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', vid, '-an', '-vf', 'scale=854:-2', '-c:v', 'libx264', '-crf', '28', '-preset', 'slow',
                    '-pix_fmt', 'yuv420p', '-movflags', '+faststart', os.path.join(R, out)], check=True)
    d = np.abs(gris(os.path.join(R, lam)) - gris(os.path.join(R, out))).mean() / 2.55
    L.setdefault('_vivas', {})[lam] = out
    json.dump(L, open(p, 'w', encoding='utf-8'), ensure_ascii=False)
    n = sum(1 for k, v in L.items() if k != '_vivas' and v == lam)
    print(f'{out} · {os.path.getsize(os.path.join(R, out)) // 1024} KB · primer fotograma frente a la lámina: {d:.1f} %'
          f'{"  ← OJO: puede haber redibujado" if d > 8 else ""}')
