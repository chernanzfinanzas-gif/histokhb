# Láminas animadas de HistoKHB con Veo 3.1 Lite (8 s, sin sonido). Uso:
#   python3 herramientas/animar.py CAPITULO | codigo1,codigo2 | des-xxx,des-yyy
#   python3 herramientas/animar.py --camara codigo1,codigo2   (sustituye por movimiento de cámara lento, gratis)
# Escribe img/vivas/<codigo>.mp4, actualiza 'viva' en datos/audio.json y deja en herramientas/_tmp/revision.jpg
# una hoja con 3 fotogramas (inicio, mitad, final) de cada una. REVISARLA SIEMPRE: si aparece o desaparece algo,
# cambian caras/personas, sale texto, anacronismos (p. ej. bosques donde no los había) o la escena se transforma,
# pasar esa lámina a --camara. Precio orientativo ~0,40 $ por clip.
# CRITERIO (desde la Edad Antigua): Veo solo para el 10-20 % más espectacular de cada capítulo (agua, fuego, humo,
# cielos, volcanes, animales o multitudes en movimiento; máx. 1 de cada 6-7); el resto con --camara.
# 'viva_tipo' en datos/audio.json marca cuáles son de cámara, para poder mejorarlas más adelante.
import sys,os,io,json,base64,time,subprocess
from concurrent.futures import ThreadPoolExecutor
from PIL import Image,ImageDraw
from comun import REPO,PROJ,TMP,sess,J,fichas_de
L="us-central1"; M="veo-3.1-lite-generate-001"
URL=f"https://{L}-aiplatform.googleapis.com/v1/projects/{PROJ}/locations/{L}/publishers/google/models/{M}"
PROMPT=("Anima esta ilustración durante 8 segundos. Conserva EXACTAMENTE el dibujo, la composición, los colores y el estilo pintado a mano: "
 "no añadas ni quites personas, animales, objetos ni edificios, no cambies las caras ni el texto, y no lo conviertas en imagen realista ni en 3D. "
 "Cámara casi fija con un acercamiento muy lento. Movimiento suave y escaso: anima solo lo que en esta escena se movería de forma natural "
 "(agua, olas, nubes, humo, fuego, lava, estrellas que titilan, plantas mecidas por el viento, animales y personas con gestos pequeños). Sin texto nuevo. "
 "MUY IMPORTANTE: no aparece ni desaparece ningún ser vivo, planta, árbol, objeto ni elemento del paisaje; cada animal conserva exactamente su forma y especie; "
 "el encuadre no cambia y el acercamiento es mínimo; el último fotograma debe parecerse mucho al primero.")
def lamina(k):
    if k.startswith('des-'): return J('datos/desarrollos.json')[k].get('lam')
    return J('datos/indice.json')['fichas'][k].get('lam')
def fin(k,raw=None):
    out=os.path.join(REPO,'img','vivas',f'{k}.mp4'); os.makedirs(os.path.dirname(out),exist_ok=True)
    if raw: subprocess.run(['ffmpeg','-v','error','-y','-i',raw,'-an','-vf','scale=854:-2','-c:v','libx264','-crf','28','-preset','slow','-movflags','+faststart',out],check=True)
    subprocess.run(['ffmpeg','-v','error','-y','-i',out,'-vf','select=eq(n\\,0)+eq(n\\,96)+eq(n\\,185),scale=320:-1,tile=3x1','-frames:v','1',os.path.join(TMP,f'h-{k}.jpg')],check=True)
def camara(k):
    src=os.path.join(TMP,'kb.png'); Image.open(os.path.join(REPO,lamina(k))).convert('RGB').resize((2560,1440),Image.LANCZOS).save(src)
    out=os.path.join(REPO,'img','vivas',f'{k}.mp4')
    subprocess.run(['ffmpeg','-v','error','-y','-loop','1','-i',src,'-vf',"zoompan=z='1+0.08*on/192':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=192:s=854x480:fps=24,format=yuv420p",'-frames:v','192','-c:v','libx264','-crf','28','-preset','slow','-movflags','+faststart',out],check=True)
    fin(k); return 'CAMARA'
def veo(k):
    im=Image.open(os.path.join(REPO,lamina(k))).convert('RGB'); b=io.BytesIO(); im.save(b,'JPEG',quality=95)
    body={"instances":[{"prompt":PROMPT,"image":{"bytesBase64Encoded":base64.b64encode(b.getvalue()).decode(),"mimeType":"image/jpeg"}}],
          "parameters":{"durationSeconds":8,"aspectRatio":"16:9","generateAudio":False,"sampleCount":1,"resolution":"720p"}}
    for t in range(6):
        r=sess().post(URL+":predictLongRunning",json=body,timeout=120)
        if r.ok: break
        if r.status_code in (429,500,503): time.sleep(30*(t+1)); continue
        return f'ERR {r.status_code} {r.text[:120]}'
    else: return 'ERR cuota'
    op=r.json()["name"]
    for i in range(90):
        time.sleep(10); q=sess().post(URL+":fetchPredictOperation",json={"operationName":op},timeout=120).json()
        if q.get("done"):
            v=q.get("response",{}).get("videos",[])
            if "error" in q or not v: return 'ERR '+json.dumps(q.get('error',q.get('response',{})))[:150]
            raw=os.path.join(TMP,f'raw-{k}.mp4'); open(raw,'wb').write(base64.b64decode(v[0]["bytesBase64Encoded"])); fin(k,raw); return 'OK'
    return 'ERR tiempo'
if __name__=='__main__':
    cam=sys.argv[1]=='--camara'; arg=sys.argv[2] if cam else sys.argv[1]
    caps=[c['id'] for c in J('datos/indice.json')['capitulos']]
    ks=fichas_de(arg) if arg in caps else arg.split(',')
    ks=[k for k in ks if lamina(k)]
    res={}
    def run(k):
        res[k]=camara(k) if cam else veo(k); print(len(res),'/',len(ks),k,res[k],flush=True)
    with ThreadPoolExecutor(1 if cam else int(os.environ.get('HILOS','4'))) as ex: list(ex.map(run,ks))
    M=J('datos/audio.json'); F=M.setdefault('fichas',{})
    for k,r in res.items():
        if r in ('OK','CAMARA'): F.setdefault(k,{})['viva']=f'img/vivas/{k}.mp4'; F[k]['viva_tipo']='camara' if r=='CAMARA' else 'veo'
    json.dump(M,open(os.path.join(REPO,'datos','audio.json'),'w',encoding='utf-8'),ensure_ascii=False,indent=1)
    hs=[(k,os.path.join(TMP,f'h-{k}.jpg')) for k in ks if os.path.exists(os.path.join(TMP,f'h-{k}.jpg'))]
    if hs:
        ims=[Image.open(p) for _,p in hs]; w,h=ims[0].size; sh=Image.new('RGB',(w,len(ims)*(h+16)),'white'); d=ImageDraw.Draw(sh)
        for i,((k,_),im) in enumerate(zip(hs,ims)): sh.paste(im,(0,i*(h+16)+16)); d.text((4,i*(h+16)+2),k,fill='black')
        sh.save(os.path.join(TMP,'revision.jpg'),quality=78)
    print('FIN',{r:list(res.values()).count(r) for r in set(res.values())},'· revisar herramientas/_tmp/revision.jpg')
