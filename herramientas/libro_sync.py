#!/usr/bin/env python3
"""Guarda con el código de usuario dónde va cada uno en el audiolibro de un libro de la Biblioteca.

Uso: python3 herramientas/libro_sync.py <carpeta del libro> [más carpetas…]
  Mete (o sustituye) un bloque <!--SYNC-INI-->…<!--SYNC-FIN--> antes de </body>.
  Usa el mismo servicio que el resto de la app (api/sync.php, por campos de primer nivel):
  cada libro guarda su propio campo «lib_<carpeta>» = {cap, pos, vel, t}, sin tocar lo demás.
  Sin código en el aparato, el libro funciona como antes (solo en ese aparato).
  Al abrir el libro o volver a él, si lo guardado con el código es más reciente, sigue desde ahí.
"""
import os, re, sys

JS = r'''<!--SYNC-INI--><script>
(function(){const CAMPO='lib___SLUG__',URL='../../api/sync.php?codigo=';
 const cod=()=>{try{return String(localStorage.getItem('hk_codigo')||'').replace(/[^A-Za-z0-9]/g,'')}catch(e){return''}};
 if(typeof LS==='undefined'||typeof P==='undefined')return;
 const set0=LS.set.bind(LS);let ult=0,pend=null;
 const datos=()=>({[CAMPO]:{cap:P.st.cap,pos:P.st.pos,vel:P.st.vel,t:P.st.t||0}});
 function sube(ya){const c=cod();if(!c||!P.st.cap)return;clearTimeout(pend);pend=null;ult=Date.now();
  const b=JSON.stringify(datos());
  if(ya&&navigator.sendBeacon){try{if(navigator.sendBeacon(URL+encodeURIComponent(c),new Blob([b],{type:'application/json'})))return}catch(e){}}
  fetch(URL+encodeURIComponent(c),{method:'POST',headers:{'Content-Type':'application/json'},body:b,keepalive:true}).catch(()=>{})}
 const firma=v=>JSON.stringify([v.cap,v.pos,v.vel]);let fir=firma(P.st);
 LS.set=function(v){const g=firma(v);if(g===fir){set0(v);return}fir=g;v.t=Date.now();set0(v);
  const f=Date.now()-ult;if(f>20000)sube();else if(!pend)pend=setTimeout(sube,20000-f)};
 function baja(){const c=cod();if(!c)return;fetch(URL+encodeURIComponent(c)).then(r=>r.json()).then(d=>{const r=d&&d[CAMPO];
  if(!r||!r.cap||(r.t||0)<=(P.st.t||0)||!au.paused)return;
  P.st.cap=r.cap;P.st.pos=Object.assign({},P.st.pos,r.pos||{});if(r.vel)P.st.vel=r.vel;P.st.t=r.t;fir=firma(P.st);set0(P.st);
  if(au.src&&!au.src.endsWith((P.c(r.cap)||{}).a||'#')){au.removeAttribute('src');au.load()}
  if(P.carga(r.cap)){au.currentTime=r.pos&&r.pos[r.cap]||0;$('mini').classList.add('on')}P.pinta()}).catch(()=>{})}
 au.addEventListener('pause',()=>sube());au.addEventListener('ended',()=>sube());
 document.addEventListener('visibilitychange',()=>{if(document.hidden)sube(true);else baja()});
 addEventListener('pagehide',()=>sube(true));
 baja();})();
</script><!--SYNC-FIN-->'''

for c in sys.argv[1:]:
    c = c.rstrip('/'); slug = os.path.basename(c); f = os.path.join(c, 'index.html')
    p = open(f, encoding='utf-8').read()
    if 'const P={st' not in p or 'const LS={' not in p:
        print(slug, ': no tiene el reproductor de audiolibro, lo salto'); continue
    js = JS.replace('__SLUG__', slug)
    if '<!--SYNC-INI-->' in p:
        p = re.sub(r'<!--SYNC-INI-->.*?<!--SYNC-FIN-->', lambda _: js, p, flags=re.S)
    else:
        i = p.rindex('</body>'); p = p[:i] + js + p[i:]
    open(f, 'w', encoding='utf-8').write(p)
    print(slug, ': guardado con código puesto')
