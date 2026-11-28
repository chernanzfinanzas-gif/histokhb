#!/usr/bin/env python3
"""Reproductor de audiolibros: si el audio se corta por la conexión (pantalla apagada, cobertura),
vuelve a pedirlo y sigue en el mismo segundo, hasta 6 veces seguidas.
En ordenador, mientras suena, mantiene la pantalla encendida para que el equipo no se suspenda.
Uso: python3 herramientas/libro_reanuda.py <carpeta del libro> [más…]  (bloque <!--REANUDA-INI-->…)"""
import os, re, sys
JS = r'''<!--REANUDA-INI--><script>
(function(){if(typeof au==='undefined'||typeof P==='undefined')return;let n=0,sonando=false,t0=0;
 au.addEventListener('playing',()=>{sonando=true;n=0});au.addEventListener('pause',()=>{sonando=false});
 au.addEventListener('timeupdate',()=>{if(au.currentTime>0)t0=au.currentTime});
 function vuelve(){if(!sonando||n>=6||!au.currentSrc)return;n++;const s=au.currentSrc,t=t0;
  setTimeout(()=>{au.addEventListener('loadedmetadata',()=>{try{au.currentTime=t}catch(e){}au.play().catch(()=>{})},{once:true});au.src=s;au.load()},1200*n)}
 au.addEventListener('error',vuelve);
 // En ordenador, mientras suena, que no se suspenda (la web solo puede hacerlo manteniendo la pantalla encendida)
 const pc=matchMedia('(pointer:fine)').matches&&!('ontouchstart' in window);let wl=null;
 async function despierto(){if(!pc||!('wakeLock' in navigator)||wl||au.paused)return;try{wl=await navigator.wakeLock.request('screen');wl.addEventListener('release',()=>{wl=null})}catch(e){}}
 function duerme(){if(wl){wl.release().catch(()=>{});wl=null}}
 au.addEventListener('playing',despierto);au.addEventListener('pause',duerme);au.addEventListener('ended',()=>setTimeout(()=>{if(au.paused)duerme()},1500));
 document.addEventListener('visibilitychange',()=>{if(!document.hidden)despierto()});
 au.addEventListener('stalled',()=>{const t=au.currentTime;setTimeout(()=>{if(sonando&&au.currentTime===t&&au.readyState<3)vuelve()},8000)});
})();
</script><!--REANUDA-FIN-->'''
for c in sys.argv[1:]:
    f = os.path.join(c.rstrip('/'), 'index.html'); p = open(f, encoding='utf-8').read()
    if 'const P={st' not in p: print(c, ': sin reproductor'); continue
    p = re.sub(r'<!--REANUDA-INI-->.*?<!--REANUDA-FIN-->', '', p, flags=re.S)
    i = p.rindex('</body>'); p = p[:i] + JS + p[i:]
    open(f, 'w', encoding='utf-8').write(p); print(os.path.basename(c.rstrip('/')), ': reanudación puesta')
