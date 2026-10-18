# Une los DATOS de una rama de «contenidos» a main sin pisar otros capítulos.
# Uso: python3 herramientas/unir_capitulo.py <rama> <cap> [des-a,des-b,...]
# Regla: lo del capítulo <cap> (sus fichas, sus desarrollos y sus audios) se toma de la rama;
# todo lo demás se queda como en main, y de la rama solo se SUMAN entradas nuevas o elementos nuevos de listas
# (nunca se borra ni se cambia nada de otros capítulos). Después: python3 herramientas/unir_lugares.py
import json,subprocess,sys,os
R=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
rama,cap=sys.argv[1],sys.argv[2]; DES=set(sys.argv[3].split(',')) if len(sys.argv)>3 and sys.argv[3] else set()
def J(ref,f):
    o=subprocess.run(['git','-C',R,'show',f'{ref}:datos/{f}'],capture_output=True,text=True)
    return json.loads(o.stdout) if o.returncode==0 else None
base=subprocess.run(['git','-C',R,'merge-base','HEAD',rama],capture_output=True,text=True).stdout.strip()
def suma(b,o,t):
    if isinstance(o,dict) and isinstance(t,dict):
        r=dict(o)
        for k,v in t.items():
            if k not in o:
                if b is None or not isinstance(b,dict) or k not in b: r[k]=v
            else: r[k]=suma(b.get(k) if isinstance(b,dict) else None,o[k],v)
        return r
    if isinstance(o,list) and isinstance(t,list) and all(not isinstance(x,(dict,list)) for x in o+t):
        return o+[x for x in t if x not in o and (not isinstance(b,list) or x not in b)]
    return o
mio=lambda k: k.startswith(cap+'-') or k in DES
out={}
# indice
o,t,b=J('HEAD','indice.json'),J(rama,'indice.json'),J(base,'indice.json')
ct={c['id']:c for c in t['capitulos']}
o['capitulos']=[ct[c['id']] if c['id']==cap and cap in ct else c for c in o['capitulos']]
if cap in ct and cap not in [c['id'] for c in o['capitulos']]: o['capitulos'].append(ct[cap])
o['fichas']={k:v for k,v in o['fichas'].items() if not mio(k)}|{k:v for k,v in t['fichas'].items() if mio(k)}
out['indice.json']=o
# fichas de la sección del capítulo y desarrollos
for f in [x for x in os.listdir(os.path.join(R,'datos')) if x.startswith('fichas-')]+['desarrollos.json','buscar.json']:
    o,t,b=J('HEAD',f),J(rama,f),J(base,f)
    if t is None or o is None: continue
    r={k:v for k,v in o.items() if not mio(k)}|{k:v for k,v in t.items() if mio(k)}
    for k,v in t.items():
        if k not in r and (b is None or k not in b): r[k]=v
    out[f]=r
# audio
o,t=J('HEAD','audio.json'),J(rama,'audio.json')
o['fichas']={k:v for k,v in o['fichas'].items() if not mio(k)}|{k:v for k,v in t['fichas'].items() if mio(k)}
out['audio.json']=o
# etiquetas y lugares: se suma
out['etiquetas.json']=suma(J(base,'etiquetas.json'),J('HEAD','etiquetas.json'),J(rama,'etiquetas.json'))
o,t,b=J('HEAD','lugares.json'),J(rama,'lugares.json'),J(base,'lugares.json')
oi={l['id']:l for l in o['lugares']}; bi={l['id']:l for l in b['lugares']} if b else {}
for l in t['lugares']:
    if l['id'] not in oi:
        if l['id'] not in bi: o['lugares'].append(l)
    else: oi[l['id']].update(suma(bi.get(l['id']),oi[l['id']],l))
out['lugares.json']=o
for f,d in out.items():
    json.dump(d,open(os.path.join(R,'datos',f),'w',encoding='utf-8'),ensure_ascii=False,**({'indent':1} if f=='audio.json' else {'separators':(',',':')}))
print('unido',cap,'desde',rama,'·',', '.join(out))
