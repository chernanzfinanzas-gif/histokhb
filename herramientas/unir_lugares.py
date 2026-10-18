# Une las entregas del chat «lugares» (datos/lugares-nuevos/<zona>.json) a datos/lugares.json.
# Uso:  python3 herramientas/unir_lugares.py --revisar   (solo informe de problemas)
#       python3 herramientas/unir_lugares.py              (revisa y, si no hay errores graves, escribe lugares.json)
# Es idempotente: se puede volver a lanzar tras unir una rama de «contenidos» que traiga su propio lugares.json.
# Orden de aplicación: datos/lugares-nuevos/orden.txt (una zona por línea); las que no estén, al final por nombre.
import json,os,sys,math,re,glob,unicodedata
R=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TIPOS={'monumento','yacimiento','museo','castillo','iglesia','poblacion'}
CAMPOS={'nombre','provincia','comarca','lat','lon','tipo','estilo','epoca','anio','regiones_sincronia','texto','ver_alli','fuentes','eventos','ev_fijos','creada','actualizada'}
def km(a,b):
    t=math.radians; d1=t(b[0]-a[0]); d2=t(b[1]-a[1]); h=math.sin(d1/2)**2+math.cos(t(a[0]))*math.cos(t(b[0]))*math.sin(d2/2)**2; return 12742*math.asin(math.sqrt(h))
def norm(s): return re.sub(r'[^a-z0-9 ]','',unicodedata.normalize('NFD',s.lower()).encode('ascii','ignore').decode())
def toks(s): return {w for w in norm(s).split() if len(w)>3 and w not in ('iglesia','santa','santo','castillo','museo','monasterio','ermita','nuestra','senora','villa','romana')}
def zonas():
    fs=sorted(glob.glob(os.path.join(R,'datos','lugares-nuevos','*.json'))); orden=[]
    o=os.path.join(R,'datos','lugares-nuevos','orden.txt')
    if os.path.exists(o): orden=[l.strip() for l in open(o) if l.strip() and not l.startswith('#')]
    names=[os.path.basename(f)[:-5] for f in fs]
    return [z for z in orden if z in names]+[z for z in names if z not in orden]
def main(revisar):
    P=os.path.join(R,'datos','lugares.json'); D=json.load(open(P,encoding='utf-8')); L=D['lugares']; ix={l['id']:l for l in L}
    global COMUNES; from collections import Counter; cc=Counter(w for x in L for w in toks(x.get('nombre',''))); COMUNES={w for w,n in cc.items() if n>=4}
    BORR={b.get('id') for z in zonas() for b in json.load(open(os.path.join(R,'datos','lugares-nuevos',z+'.json'),encoding='utf-8')).get('borrar',[])}
    graves=[]; avisos=[]; nN=nC=nB=0
    for z in zonas():
        E=json.load(open(os.path.join(R,'datos','lugares-nuevos',z+'.json'),encoding='utf-8'))
        for l in E.get('nuevos',[]):
            i=l.get('id','?'); falta=[c for c in ('id','nombre','provincia','lat','lon','tipo','texto','fuentes') if not l.get(c)]
            if falta: graves.append(f'{z}: nuevo {i} sin {falta}'); continue
            if l['tipo'] not in TIPOS: graves.append(f'{z}: {i} tipo «{l["tipo"]}» no válido'); continue
            if not isinstance(l['texto'],dict) or not l['texto'].get('general'): graves.append(f'{z}: {i} sin texto.general'); continue
            if i in ix:
                if ix[i].get('_de')==z or ix[i].get('nombre')==l['nombre']: ix[i].update({k:v for k,v in l.items()}); continue
                graves.append(f'{z}: nuevo {i} ya existe («{ix[i]["nombre"]}»)'); continue
            for o in L:
                if o.get('lat') is None: continue
                d=km((l['lat'],l['lon']),(o['lat'],o['lon']))
                comun=(toks(l['nombre'])&toks(o['nombre']))-toks(l.get('provincia',''))-toks(l.get('comarca',''))-toks(o.get('provincia',''))-COMUNES
                if d<0.25 and comun: avisos.append(f'{z}: {i} parece duplicado de {o["id"]} ({d*1000:.0f} m)')
            n=dict(l); L.append(n); ix[i]=n; nN+=1
        for c in E.get('cambios',[]):
            i=c.get('id'); f=c.get('campos',{})
            if i not in ix:
                if i not in BORR: graves.append(f'{z}: cambio a {i}, que no existe')
                continue
            raros=set(f)-CAMPOS
            if raros: avisos.append(f'{z}: {i} campos desconocidos {sorted(raros)} (se aplican igual)')
            if 'tipo' in f and f['tipo'] not in TIPOS: graves.append(f'{z}: {i} tipo «{f["tipo"]}» no válido'); continue
            o=ix[i]
            if ('lat' in f or 'lon' in f) and o.get('lat') is not None:
                d=km((o['lat'],o['lon']),(f.get('lat',o['lat']),f.get('lon',o['lon'])))
                if d>10: avisos.append(f'{z}: {i} se mueve {d:.1f} km')
            o.update(f); nC+=1
        for b in E.get('borrar',[]):   # duplicados: {"id":x,"en":y} pasa eventos de x a y y quita x
            x,y=b.get('id'),b.get('en')
            if x not in ix: continue
            if y in ix:
                a,b2=ix[y].get('eventos') or [],ix[x].get('eventos') or []
                if isinstance(a,list) and isinstance(b2,list) and b2: ix[y]['eventos']=a+[e for e in b2 if e not in a]
            L.remove(ix.pop(x)); nB+=1
    print(f'Zonas: {", ".join(zonas())}\nNuevos: {nN} · cambios aplicados: {nC} · borrados: {nB} · total lugares: {len(L)}')
    for g in graves: print('GRAVE',g)
    for a in avisos: print('AVISO',a)
    if revisar or graves: print('No se escribe nada.' if graves else '(solo revisión)'); return 1 if graves else 0
    json.dump(D,open(P,'w',encoding='utf-8'),ensure_ascii=False,separators=(',',':')); print('lugares.json escrito'); return 0
if __name__=='__main__': sys.exit(main('--revisar' in sys.argv))
