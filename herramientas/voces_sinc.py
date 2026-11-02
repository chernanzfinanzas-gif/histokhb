# Voz de las fichas de sincronía (las de «El mundo a la vez»), con la misma voz y receta que voces.py.
# Uso:  GEMINI_API_KEY_FILE=… HILOS=1 python3 herramientas/voces_sinc.py "Grecia|-461" "China|-221" …
# Sus claves llevan espacios, barras y «|», así que el mp3 se llama audio/s-<código corto>-s.mp3 y la app lo
# encuentra por el campo f_s de datos/audio.json. La sincronía párrafo a párrafo va en datos/sincro.json
# con la clave «<región>|<año>|s». Después: python3 herramientas/medios.py subir audio/s-*.mp3
import sys,os,json,hashlib,random
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import voces,sincro,silabas as S
from comun import REPO,J

def codigo(k): return 's-'+hashlib.md5(k.encode()).hexdigest()[:8]
def detalle():
    D={}
    for f in ('pre','ant','med','mod','con'): D.update(J(f'datos/sinc-det-{f}.json'))
    return D

if __name__=='__main__':
    D=detalle(); claves=sys.argv[1:]; hechos={}
    for k in claves:
        if k not in D: print('NO EXISTE',k); continue
        voz=voces.VOCES[int(hashlib.md5(k.encode()).hexdigest(),16)%len(voces.VOCES)]
        if voz=='Leda': voz='Aoede'          # Leda es la voz de niños
        d=voces.genera(codigo(k),'s',D[k],voz,'48k',None)
        print(('OK ' if d else 'FALTA ')+k,flush=True)
        if not d: continue
        mp3=os.path.join(REPO,'audio',codigo(k)+'-s.mp3')
        els=sincro.elementos(D[k]); P,tot=sincro.pausas(mp3); db,_=S.envolvente(mp3); pk=S.nucleos(db)
        ts=sincro.alinear(sincro.previstos(els,None,pk,tot),P,tot)
        hechos[k]=(d,voz,ts)
    if not hechos: sys.exit(0)
    M=J('datos/audio.json'); F=M.setdefault('fichas',{})
    SQ=J('datos/sincro.json')
    for k,(d,voz,ts) in hechos.items():
        F[k]={'s':d,'voz_s':voz,'f_s':f'audio/{codigo(k)}-s.mp3'}
        if ts: SQ[k+'|s']=ts
    json.dump(M,open(os.path.join(REPO,'datos','audio.json'),'w',encoding='utf-8'),ensure_ascii=False)
    json.dump(dict(sorted(SQ.items())),open(os.path.join(REPO,'datos','sincro.json'),'w',encoding='utf-8'),separators=(',',':'))
    print('FIN',len(hechos),'de',len(claves))
