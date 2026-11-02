# Voces de HistoKHB con Gemini-TTS (narrador). Uso:
# AUDIOS: no van al repo. Tras grabar → python3 herramientas/medios.py subir <rutas> (ver LEEME.md).
#   python3 herramientas/voces.py fichas CAPITULO            (las 3 voces de cada ficha del capítulo)
#   python3 herramientas/voces.py fichas codigo1,codigo2     (fichas concretas)
#   python3 herramientas/voces.py des des-xxx,des-yyy        (desarrollos del tema)
#   NIVELES=gp python3 herramientas/voces.py fichas ...     (rehacer solo esos niveles; si la ficha ya tiene voz, la conserva)
# Niños: voz Leda (cuentacuentos). General y profundo: 10 voces alternas, la misma en los dos niveles de cada ficha;
# los desarrollos usan la voz de su ficha. Escribe audio/<codigo>-<n|g|p|d>.mp3 y actualiza datos/audio.json.
# Si una petición falla por límite (429) reintenta sola; al final lista lo que falte: volver a lanzar solo eso.
# Con la clave gratuita de AI Studio: GEMINI_API_KEY_FILE=/ruta/aistudio.txt python3 herramientas/voces.py ... (HILOS=1 para no pasar del límite por minuto).
import sys,os,re,html,base64,time,subprocess,json,hashlib
from concurrent.futures import ThreadPoolExecutor
from comun import REPO,PROJ,TMP,sess,J,fichas_de,seccion_de
VOCES=["Aoede","Despina","Gacrux","Leda","Vindemiatrix","Achird","Algieba","Iapetus","Rasalgethi","Sadaltager"]
P_AD="Lee en castellano de España como el narrador de un buen documental de historia: voz cálida, cercana y pausada, con curiosidad y pequeñas pausas entre párrafos y apartados, sin dramatizar."
P_NI="Lee en castellano de España para niños de 8 a 12 años, como un cuentacuentos: voz juvenil, alegre y muy clara, despacio y con entusiasmo, con pausas entre párrafos."
def limpia(h):
    h=re.sub(r'<button[^>]*>.*?</button>','',h,flags=re.S); h=re.sub(r'<div class="biblio">.*?</div>','',h,flags=re.S)
    h=re.sub(r'<div class="tt">.*?</div>','<p>Y ahora, para los más pequeños.</p>',h,flags=re.S); h=re.sub(r'<ul class="crono">','<p>Cronología.</p><ul>',h)
    h=re.sub(r'<h4>(.*?)</h4>',r'<p>\1.</p>',h,flags=re.S)
    h=re.sub(r'<li>(.*?)</li>',lambda m:'<p>'+re.sub(r'^(<b>[^<]*</b>)',r'\1:',m.group(1))+'.</p>',h,flags=re.S)
    h=re.sub(r'</(p|div|ul)>','\n\n',h); t=html.unescape(re.sub(r'<[^>]+>','',h))
    t=re.sub(r'[\U0001F000-\U0001FFFF☀-➿️]','',t).replace('±',' más o menos ')
    for a,b in [('a. C.','antes de Cristo'),('a.C.','antes de Cristo'),('d. C.','después de Cristo'),('d.C.','después de Cristo')]: t=t.replace(a,b)
    t=re.sub(r'(?<=\d)\s?(?:aC|AC|a\.C|a\. de C\.|a de C\.?)(?![\wáéíóú])',' antes de Cristo',t); t=re.sub(r'(?<=\d)\s?(?:dC|DC|d\.C|d\. de C\.|d de C\.?)(?![\wáéíóú])',' después de Cristo',t)
    t=re.sub(r'\.\.+(?=\s|$)','.',t); t=re.sub(r':\.',':',t); t=re.sub(r'[ \t]+',' ',t)
    return [p.strip() for p in re.split(r'\n\s*\n',t) if p.strip()]
def trozos(ps,lim=int(os.environ.get('TROZO','2800'))):   # TROZO=1600: tandas cortas para que la voz no se acelere en textos largos
    out=[];cur=''
    for p in ps:
        if len((cur+'\n\n'+p).encode())>lim and cur: out.append(cur);cur=p
        else: cur=(cur+'\n\n'+p) if cur else p
    return out+([cur] if cur else [])
# Clave gratuita de Google AI Studio (desde 26-oct-2026): si existe GEMINI_API_KEY (o el fichero que diga
# GEMINI_API_KEY_FILE), se graba con la API de Gemini en vez de con Google Cloud. Mismas voces y mismas indicaciones.
def _clave():
    k=os.environ.get('GEMINI_API_KEY','').strip()
    f=os.environ.get('GEMINI_API_KEY_FILE','')
    if not k and f and os.path.exists(f): k=open(f,encoding='utf-8').read().strip()
    return k
MODELO=os.environ.get('GEMINI_TTS_MODEL','gemini-2.5-flash-preview-tts')
def tts_aistudio(text,voz,prompt,dst,clave):
    import requests,wave
    b={"contents":[{"parts":[{"text":prompt+"\n\n"+text}]}],
       "generationConfig":{"responseModalities":["AUDIO"],"speechConfig":{"voiceConfig":{"prebuiltVoiceConfig":{"voiceName":voz}}}}}
    for i in range(8):
        try:
            r=requests.post(f"https://generativelanguage.googleapis.com/v1beta/models/{MODELO}:generateContent",headers={"x-goog-api-key":clave},json=b,timeout=300)
            if r.ok:
                pcm=base64.b64decode(r.json()['candidates'][0]['content']['parts'][0]['inlineData']['data'])
                with wave.open(dst,'wb') as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(24000); w.writeframes(pcm)
                return True
            if r.status_code==429 and 'PerDay' in r.text: print('LÍMITE DIARIO de AI Studio agotado: seguir mañana',dst); return False
            if r.status_code not in (429,500,502,503,504): print('ERR',dst,r.status_code,r.text[:200]); return False
        except Exception as e: pass
        time.sleep(20*(i+1))
    print('ERR tras reintentos',dst); return False
def quita_instruccion(dst,clave):
    """Desde el 2-nov-2026 Gemini-TTS a veces LEE EN VOZ ALTA la indicación de estilo antes del texto.
    Si el dictado del principio la contiene, recorta hasta la primera pausa tras la que ya empieza el texto."""
    import sincro_dictado as SD
    malo=lambda t:any(x in t for x in ('dramatizar','castellano de espana','pausas entre','cuentacuentos','documental de historia'))
    if not malo(SD.norm(SD.dicta(dst,0,8,clave))): return True
    r=subprocess.run(['ffmpeg','-hide_banner','-t','40','-i',dst,'-af','silencedetect=noise=-35dB:d=0.25','-f','null','-'],capture_output=True,text=True).stderr
    for t in [float(x) for x in re.findall(r'silence_end: ([\d.]+)',r)]:
        if t<4: continue
        txt=SD.norm(SD.dicta(dst,t-0.05,6,clave))
        if txt.strip() and not malo(txt):
            tmp=dst+'.rec.wav'; subprocess.run(['ffmpeg','-v','error','-y','-ss',str(max(0,t-0.15)),'-i',dst,'-c:a','pcm_s16le',tmp],check=True)
            os.replace(tmp,dst); print('  instrucción leída y recortada en',round(t,1),'s:',os.path.basename(dst)); return True
    print('ERR: lee la instrucción y no sé dónde acaba',dst); os.remove(dst); return False
def tts(text,voz,prompt,dst):
    clave=_clave()
    if clave: return tts_aistudio(text,voz,prompt,dst,clave) and quita_instruccion(dst,clave)
    b={"input":{"text":text,"prompt":prompt},"voice":{"languageCode":"es-ES","name":voz,"model_name":"gemini-2.5-flash-tts"},"audioConfig":{"audioEncoding":"LINEAR16","sampleRateHertz":24000}}
    for i in range(8):
        try:
            r=sess().post("https://texttospeech.googleapis.com/v1/text:synthesize",json=b,headers={"x-goog-user-project":PROJ},timeout=300)
            if r.ok: open(dst,'wb').write(base64.b64decode(r.json()['audioContent'])); return True
            if r.status_code not in (429,500,502,503,504): print('ERR',dst,r.status_code,r.text[:150]); return False
        except Exception as e: pass
        time.sleep(20*(i+1))
    print('ERR tras reintentos',dst); return False
def limpia_bordes(w):
    """Gemini deja un chasquido de ~0,15 s al final de cada tanda (medido en la cordillera, 2-nov-2026): se corta
    y se suavizan los bordes (15 ms de entrada, 30 ms de salida) para que las costuras no crujan."""
    import numpy as np
    o=w[:-4]+'.lb.wav'
    if os.path.exists(o): return o
    raw=subprocess.run(['ffmpeg','-v','error','-i',w,'-ac','1','-ar','24000','-af','highpass=f=5000','-f','s16le','-'],capture_output=True).stdout
    x=np.frombuffer(raw,np.int16).astype(np.float32)/32768; h=120; n=len(x)//h
    if n<200: return w
    e=np.sqrt((x[:n*h].reshape(n,h)**2).mean(1)); T=len(x)/24000
    idx=[i for i in range(n-120,n) if e[i]>0.15]
    cut=idx[0]*0.005-0.02 if idx else T
    subprocess.run(['ffmpeg','-v','error','-y','-i',w,'-t',f'{cut:.3f}','-af',f'afade=t=in:d=0.015,afade=t=out:st={max(0,cut-0.03):.3f}:d=0.03','-c:a','pcm_s16le',o],check=True)
    return o
def iguala_ritmo(wavs,textos):
    """Cada tanda de Gemini sale a su propia velocidad y al juntarlas se oyen escalones (cordillera, 2-nov-2026).
    Pone todas las tandas al ritmo de la tanda mediana (sílabas por segundo), sin cambiar el tono (atempo)."""
    wavs=[limpia_bordes(w) for w in wavs]
    if len(wavs)<2: return wavs
    import silabas as S
    dur=lambda p:float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',p],capture_output=True,text=True).stdout)
    r=[S.silabas(t)/max(dur(w),1) for w,t in zip(wavs,textos)]; obj=sorted(r)[len(r)//2]; out=[]
    for w,x in zip(wavs,r):
        f=min(1.25,max(0.8,obj/x))
        if abs(f-1)<0.03: out.append(w); continue
        o=w[:-4]+f'.r{f:.3f}.wav'
        if not os.path.exists(o): subprocess.run(['ffmpeg','-v','error','-y','-i',w,'-af',f'atempo={f:.4f}','-c:a','pcm_s16le',o],check=True)
        out.append(o)
    print('  ritmo igualado por tandas:',' '.join(f'{x:.1f}' for x in r),'→',f'{obj:.1f}',flush=True); return out
def genera(cod,nivel,html_,voz,kbps,cabecera=None):
    ps=limpia(html_); ps=([cabecera+'.'] if cabecera else [])+ps
    wavs=[]
    for i,c in enumerate(trozos(ps)):
        w=os.path.join(TMP,f'{cod}-{nivel}-{i}-{hashlib.md5((voz+c).encode()).hexdigest()[:10]}.wav')  # el nombre lleva el hash del texto: un trozo solo se reutiliza si el texto no ha cambiado
        if not os.path.exists(w) and not tts(c,voz,P_NI if nivel=='n' else P_AD,w): return None
        wavs.append(w)
    wavs=iguala_ritmo(wavs,trozos(ps))
    sil=os.path.join(TMP,'sil.wav')
    if not os.path.exists(sil): subprocess.run(['ffmpeg','-v','error','-y','-f','lavfi','-i','anullsrc=r=24000:cl=mono','-t','0.7','-c:a','pcm_s16le',sil],check=True)
    lst=os.path.join(TMP,f'{cod}-{nivel}.txt'); open(lst,'w').write(''.join(f"file '{os.path.basename(w)}'\n"+("file 'sil.wav'\n" if j<len(wavs)-1 else '') for j,w in enumerate(wavs)))
    out=os.path.join(REPO,'audio',f'{cod}-{nivel}.mp3'); os.makedirs(os.path.dirname(out),exist_ok=True)
    subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',lst,'-ac','1','-b:a',kbps,out],check=True,cwd=TMP)
    return round(float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',out],capture_output=True,text=True).stdout))
def orden_voz(k):
    sec=seccion_de(k); idx=J('datos/indice.json'); ks=[x for c in idx['capitulos'] if c['sec']==sec for x in c['f']]
    return VOCES[ks.index(k)%10]
if __name__=='__main__':
    modo,arg=sys.argv[1],sys.argv[2]
    jobs=[]
    if modo=='fichas':
        ks=arg.split(',') if (',' in arg or '-' in arg and arg not in [c['id'] for c in J('datos/indice.json')['capitulos']]) else fichas_de(arg)
        for k in ks:
            T=J(f'datos/fichas-{seccion_de(k)}.json')[k]; A=J('datos/audio.json').get('fichas',{}).get(k,{}); v=A.get('voz_g') or orden_voz(k)
            for nv,voz,kb in (('n','Leda','48k'),('g',v,'48k'),('p',v,'32k')):
                if T.get(nv) and nv in os.environ.get('NIVELES','ngp'): jobs.append((k,nv,T[nv],voz,kb,None))
    else:
        D=J('datos/desarrollos.json'); TX={}
        for dk in arg.split(','):
            voz=VOCES[0]
            for sec in ('cosmos','prehistoria','antigua','media','moderna','contemporanea'):
                try: T=TX.setdefault(sec,J(f'datos/fichas-{sec}.json'))
                except Exception: continue
                own=[k for k,v in T.items() if 'd/'+dk in (v.get('p') or '')+(v.get('n') or '')]
                if own: voz=orden_voz(own[0]); break
            voz=J('datos/audio.json').get('fichas',{}).get(dk,{}).get('voz_d') or voz
            if 'd' in os.environ.get('DES_NIVELES','d,dg').split(','): jobs.append((dk,'d',D[dk]['h'],voz,'32k',D[dk]['t']))
            if D[dk].get('hg') and 'dg' in os.environ.get('DES_NIVELES','d,dg').split(','): jobs.append((dk,'dg',D[dk]['hg'],voz,'32k',D[dk]['t']))
    res={}
    def run(j):
        d=genera(*j)
        if d: res[(j[0],j[1])]=(d,j[3])
        print(f"{len(res)}/{len(jobs)}",j[0],j[1],'OK' if d else 'FALTA',flush=True)
    with ThreadPoolExecutor(int(os.environ.get('HILOS','4'))) as ex: list(ex.map(run,jobs))
    M=J('datos/audio.json'); F=M.setdefault('fichas',{})
    for (k,nv),(d,voz) in res.items(): F.setdefault(k,{})[nv]=d; F[k]['voz_'+nv]=voz
    json.dump(M,open(os.path.join(REPO,'datos','audio.json'),'w',encoding='utf-8'),ensure_ascii=False,indent=1)
    falta=[f'{j[0]}-{j[1]}' for j in jobs if (j[0],j[1]) not in res]
    print('FIN', len(res),'audios', '· FALTAN: '+','.join(falta) if falta else '· completo')
