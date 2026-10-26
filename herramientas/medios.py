#!/usr/bin/env python3
"""Audios y vídeos de HistoKHB - Historia Total: viven en el hosting, NO en el repositorio.

Los .mp3 (audio/) y .mp4 (img/vivas/) están en .gitignore. Las copias completas son:
  · el hosting (historiatotal.es), que es lo que usa la app;
  · la carpeta «Historia Universal\\Multimedia» del PC de Carlos (se pone al día con
    «Actualizar copia (1 clic).bat» de esa carpeta, que compara con datos/medios.json).

datos/medios.json = {ruta: [bytes, md5]} de todos los audios y vídeos publicados.

Uso en una sesión, después de generar audios o vídeos (voces.py, animar.py…):
    python3 herramientas/medios.py subir audio/med5-8-p.mp3 img/vivas/xxx.mp4 …
    python3 herramientas/medios.py subir            # sin rutas: todos los que haya en audio/ e img/vivas/
  Los deja en la rama «buzon-medios» y los sube a GitHub. El workflow los copia al hosting,
  apunta su huella en datos/medios.json y vacía el buzón. Sube el buzón ANTES que main.

Uso en el workflow (no a mano):
    python3 herramientas/medios.py recoger   # trae al árbol los ficheros del buzón y actualiza medios.json
"""
import hashlib, json, os, subprocess, sys, glob, shutil, tempfile
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAN = os.path.join(R, 'datos', 'medios.json')
RAMA = 'buzon-medios'

def sh(*a, **k): return subprocess.run(a, cwd=k.pop('cwd', R), check=k.pop('check', True), capture_output=True, text=True, **k)
def md5(p):
    h = hashlib.md5()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''): h.update(b)
    return h.hexdigest()
def es_medio(p): return (p.startswith('audio/') and p.endswith('.mp3')) or (p.startswith('img/vivas/') and p.endswith('.mp4'))

def subir(rutas):
    rutas = rutas or sorted(os.path.relpath(p, R) for p in glob.glob(os.path.join(R, 'audio', '*.mp3')) + glob.glob(os.path.join(R, 'img', 'vivas', '*.mp4')))
    rutas = [r.replace('\\', '/') for r in rutas]
    malas = [r for r in rutas if not es_medio(r) or not os.path.isfile(os.path.join(R, r))]
    if malas: sys.exit('No son audios/vídeos de la app o no existen: ' + ', '.join(malas))
    if not rutas: sys.exit('No hay nada que subir.')
    man = json.load(open(MAN)) if os.path.exists(MAN) else {}
    rutas = [r for r in rutas if man.get(r, [0, ''])[1] != md5(os.path.join(R, r))]
    if not rutas: print('Todo está ya publicado (mismas huellas). Nada que subir.'); return
    wt = tempfile.mkdtemp(prefix='buzon-')
    hay = sh('git', 'ls-remote', '--heads', 'origin', RAMA).stdout.strip()
    if hay:
        sh('git', 'fetch', '-q', '--depth', '1', 'origin', f'{RAMA}:refs/remotes/origin/{RAMA}')
        sh('git', 'worktree', 'add', '-q', '--detach', wt, f'origin/{RAMA}')
    else:
        sh('git', 'worktree', 'add', '-q', '--detach', wt)
        sh('git', 'checkout', '-q', '--orphan', 'tmp-buzon', cwd=wt); sh('git', 'rm', '-rqf', '.', cwd=wt)
    try:
        for r in rutas:
            os.makedirs(os.path.dirname(os.path.join(wt, r)), exist_ok=True)
            shutil.copy2(os.path.join(R, r), os.path.join(wt, r))
        sh('git', 'add', '-f', *rutas, cwd=wt)
        sh('git', 'commit', '-q', '-m', f'Buzón: {len(rutas)} audios/vídeos', cwd=wt)
        sh('git', 'push', '-q', 'origin', f'HEAD:refs/heads/{RAMA}', cwd=wt)
        print(f'{len(rutas)} ficheros en el buzón. Al publicar pasan al hosting:', *rutas, sep='\n  ')
    finally:
        sh('git', 'worktree', 'remove', '--force', wt, check=False)

def recoger():
    """Workflow: copia al árbol los ficheros del buzón y apunta su huella. Escribe el sha procesado en /tmp/buzon.sha."""
    if not sh('git', 'ls-remote', '--heads', 'origin', RAMA).stdout.strip(): print('buzón: no existe'); return
    sh('git', 'fetch', '-q', '--depth', '1', 'origin', RAMA)
    sha = sh('git', 'rev-parse', 'FETCH_HEAD').stdout.strip()
    fs = [f for f in sh('git', 'ls-tree', '-r', '--name-only', sha).stdout.split('\n') if es_medio(f)]
    open('/tmp/buzon.sha', 'w').write(sha if fs else '')
    if not fs: print('buzón: vacío'); return
    sh('git', 'checkout', sha, '--', *fs)
    sh('git', 'reset', '-q', '--', *fs)          # que no entren en el commit de main
    man = json.load(open(MAN)) if os.path.exists(MAN) else {}
    for f in fs: man[f] = [os.path.getsize(os.path.join(R, f)), md5(os.path.join(R, f))]
    json.dump(dict(sorted(man.items())), open(MAN, 'w'), separators=(',', ':'))
    print(f'buzón: {len(fs)} ficheros recogidos', *fs, sep='\n  ')

if __name__ == '__main__':
    m = sys.argv[1] if len(sys.argv) > 1 else ''
    if m == 'subir': subir(sys.argv[2:])
    elif m == 'recoger': recoger()
    else: sys.exit(__doc__)
