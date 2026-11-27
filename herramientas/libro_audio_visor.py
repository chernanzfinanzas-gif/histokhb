#!/usr/bin/env python3
"""Mete en el visor de un libro los audios hechos con libro_audio.py:
rellena CAPS (a, d) y SYNC con audio/<id>.json. Si hay algún audio, muestra el botón 🎧.
Uso: python3 herramientas/libro_audio_visor.py <carpeta del libro>
"""
import json, os, re, sys
c = sys.argv[1]; f = os.path.join(c, 'index.html'); p = open(f, encoding='utf-8').read()
m = re.search(r'const CAPS=(\[.*?\]);', p, re.S); caps = json.loads(m.group(1))
sync = {}
for x in caps:
    j = os.path.join(c, 'audio', x['id'] + '.json')
    if os.path.exists(j):
        d = json.load(open(j)); x['a'] = 'audio/' + x['id'] + '.mp3?v=' + str(int(os.path.getmtime(os.path.join(c, 'audio', x['id'] + '.mp3')))); x['d'] = d['d']; sync[x['id']] = d['sync']
p = p.replace(m.group(0), 'const CAPS=' + json.dumps(caps, ensure_ascii=False) + ';', 1)
p = re.sub(r'const SYNC=\{.*?\};', lambda _: 'const SYNC=' + json.dumps(sync) + ';', p, count=1, flags=re.S)
if sync:
    p = p.replace('#bAud,.esc,#mini{display:none!important}', '')
open(f, 'w', encoding='utf-8').write(p)
print(len(sync), 'capítulos con audio:', ', '.join(sync))
