#!/usr/bin/env python3
"""Modo «pasar páginas» para las revistas de la Biblioteca (Bitácora), como en los libros.

Uso: python3 herramientas/revista_paginas.py biblioteca/bitacora-01 [biblioteca/bitacora-02 …]
  Mantiene el diseño de la revista y le añade:
  · botones A− A+ y 📖/≡ en la barra (letra y modo páginas / lectura seguida),
  · páginas que ocupan el alto que queda libre en la pantalla (entre la barra y el pie),
    a dos páginas en pantallas anchas apaisadas, recalculadas al girar o cambiar la letra,
  · pasar página tocando a izquierda/derecha, deslizando, con las esquinas o con las flechas,
  · pie con el artículo y el número de página; el índice salta a la página del artículo,
  · recuerda la página y comparte con los libros la preferencia de modo y de letra.
  Se puede volver a pasar sobre una revista ya preparada (sustituye el bloque).
"""
import os, re, sys

CSS = r'''<!--PAG-INI--><style>
#lector{font-size:var(--fs,17px)}
.bpag{background:#ffffff26;border:0;color:#fff;font:600 13px Fredoka,Nunito,sans-serif;padding:4px 9px;border-radius:12px;cursor:pointer;margin-left:6px}
.barra .desc{display:flex;align-items:center;flex-wrap:nowrap;white-space:nowrap}
.barra>a{white-space:nowrap}
@media(max-width:480px){.barra{padding:8px 10px}.barra .bt{display:none}.barra .desc a{margin-left:8px}.bpag{padding:4px 7px;margin-left:4px}}
.dobla,#pie{display:none}
body.libro{overflow:hidden;height:100vh;height:100dvh}
body.libro #lector{position:fixed;left:0;right:0;top:var(--bt,46px);bottom:34px;max-width:none;margin:0;padding:0;overflow:hidden}
body.libro .hojas{height:100%;column-width:var(--pw);column-gap:var(--gap);column-fill:auto;padding:16px calc(var(--gap)/2) 0;box-sizing:border-box}
body.libro.doble .hojas{column-rule:1px solid #e3d6bd}
body.libro figure img,body.libro .fin img{max-height:calc(var(--ph) * .55);width:auto;max-width:100%;margin-left:auto;margin-right:auto}
body.libro .port img{max-height:calc(var(--ph) - 60px);margin:0 auto}
body.libro figure{margin:14px 0}
body.libro figure,body.libro .cita,body.libro .cifras div,body.libro .caja,body.libro .linea div,body.libro .bienv,body.libro .efe .t,body.libro .cur .c,body.libro .ind li{break-inside:avoid}
body.libro h1,body.libro h2,body.libro h3,body.libro .sec{break-after:avoid}
body.libro article,body.libro section.ind,body.libro footer.fin{break-before:column;border-top:0;margin-top:0;padding-top:0}
body.libro #pie{display:flex;justify-content:space-between;align-items:center;gap:10px;position:fixed;left:0;right:0;bottom:0;height:34px;padding:0 max(40px,env(safe-area-inset-left,0px));font:12px Nunito,sans-serif;color:#8a7350;background:var(--papel)}
body.libro #pCap{overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
body.libro .dobla{display:block;position:fixed;z-index:4;width:34px;height:34px;border:0;padding:0;cursor:pointer;background:none;-webkit-tap-highlight-color:transparent}
body.libro .dobla::before,body.libro .dobla::after{content:"";position:absolute;inset:0}
body.libro .dobla.sig{right:0;bottom:0}
body.libro .dobla.sig::after{background:var(--tinta);clip-path:polygon(100% 0,100% 100%,0 100%);opacity:.12}
body.libro .dobla.sig::before{background:linear-gradient(to top left,color-mix(in srgb,var(--papel) 74%,var(--tinta)) 48%,color-mix(in srgb,var(--papel) 94%,var(--tinta)) 100%);clip-path:polygon(0 0,100% 0,0 100%);filter:drop-shadow(-1.5px -1.5px 2px rgba(0,0,0,.3))}
body.libro .dobla.ant{left:0;top:var(--bt,46px)}
body.libro .dobla.ant::after{background:var(--tinta);clip-path:polygon(0 0,100% 0,0 100%);opacity:.12}
body.libro .dobla.ant::before{background:linear-gradient(to bottom right,color-mix(in srgb,var(--papel) 74%,var(--tinta)) 48%,color-mix(in srgb,var(--papel) 94%,var(--tinta)) 100%);clip-path:polygon(100% 0,100% 100%,0 100%);filter:drop-shadow(1.5px 1.5px 2px rgba(0,0,0,.3))}
body.libro .dobla[hidden]{display:none}
</style><!--PAG-FIN-->'''

JS = r'''<!--PAGJS-INI--><button class="dobla ant" id="dAnt" aria-label="Página anterior" onclick="R.ir(R.n-1,true)"></button><button class="dobla sig" id="dSig" aria-label="Página siguiente" onclick="R.ir(R.n+1,true)"></button>
<div id="pie"><span id="pCap"></span><span id="pNum"></span></div><script>
const R=(function(){const $=i=>document.getElementById(i),L=$('lector'),K='hk_rev___SLUG__';
const g=(k,d)=>{try{const v=localStorage.getItem(k);return v===null?d:v}catch(e){return d}},s=(k,v)=>{try{localStorage.setItem(k,v)}catch(e){}};
const R={on:false,n:0,pw:0,fs:+g('hk_libro_letra',17)||17,
 medir(){document.documentElement.style.setProperty('--bt',document.querySelector('.barra').offsetHeight+'px');
  const gap=32,W=innerWidth,N=W>=900&&W>innerHeight?2:1,w=Math.min(W,N*(680+gap));L.style.width=w+'px';L.style.left=((W-w)/2)+'px';
  document.body.classList.toggle('doble',N===2);const d=document.documentElement.style;d.setProperty('--pw',(w/N-gap)+'px');d.setProperty('--gap',gap+'px');d.setProperty('--ph',L.clientHeight+'px');this.pw=w},
 total(){return Math.max(1,Math.round(L.scrollWidth/this.pw))},
 ir(n,suave){const t=this.total();this.n=Math.max(0,Math.min(t-1,n));L.scrollTo({left:this.n*this.pw,behavior:suave?'smooth':'auto'});this.pie();s(K,this.n)},
 pagDe(el){return Math.floor((el.getBoundingClientRect().left+L.scrollLeft+4)/this.pw)},
 primer(){const x0=this.n*this.pw;return[...document.querySelectorAll('#hojas p,#hojas h1,#hojas h2,#hojas figure')].find(e=>e.getBoundingClientRect().left+L.scrollLeft>=x0-2)},
 pie(){$('pNum').textContent=(this.n+1)+' / '+this.total();$('dAnt').hidden=this.n<=0;$('dSig').hidden=this.n>=this.total()-1;let t='';
  document.querySelectorAll('#hojas article,#hojas section.ind').forEach(a=>{const x=(a.firstElementChild||a).getBoundingClientRect().left+L.scrollLeft;if(x<this.n*this.pw+this.pw-4){const h=a.querySelector('h1,h2');t=h?h.textContent:''}});$('pCap').textContent=t},
 rehacer(){if(!this.on)return;const r=this.primer();this.medir();requestAnimationFrame(()=>{if(r)this.ir(this.pagDe(r));else this.pie()})},
 modo(v){const r=this.on?this.primer():null;this.on=v===undefined?!this.on:v;if(!this.on){L.style.width=L.style.left=''}document.body.classList.toggle('libro',this.on);
  $('bModo').innerHTML=this.on?'≡<span class=bt> Seguido</span>':'📖<span class=bt> Páginas</span>';s('hk_libro_modo',this.on?'1':'0');
  if(this.on){document.querySelectorAll('#hojas img[loading]').forEach(i=>i.loading='eager');this.medir();requestAnimationFrame(()=>this.ir(+g(K,0)||0))}else if(r)r.scrollIntoView()},
 letra(d){const T=[15,17,19,21,23,26];let i=T.indexOf(this.fs);if(i<0)i=1;i=Math.max(0,Math.min(T.length-1,i+d));this.fs=T[i];
  const r=this.on?this.primer():null;document.documentElement.style.setProperty('--fs',this.fs+'px');s('hk_libro_letra',this.fs);
  if(this.on)requestAnimationFrame(()=>{this.medir();requestAnimationFrame(()=>{if(r)this.ir(this.pagDe(r));else this.pie()})})}};
document.documentElement.style.setProperty('--fs',R.fs+'px');
L.addEventListener('click',e=>{if(!R.on||e.target.closest('a,button,.gl,.dicw'))return;if(getSelection&&String(getSelection()).length)return;R.ir(R.n+(e.clientX/innerWidth>=0.4?1:-1),true)});
let tx=null,ty=null;L.addEventListener('touchstart',e=>{tx=e.touches[0].clientX;ty=e.touches[0].clientY},{passive:true});
L.addEventListener('touchend',e=>{if(!R.on||tx===null)return;const dx=e.changedTouches[0].clientX-tx,dy=e.changedTouches[0].clientY-ty;if(Math.abs(dx)>45&&Math.abs(dx)>Math.abs(dy))R.ir(R.n+(dx<0?1:-1),true);tx=null},{passive:true});
document.addEventListener('keydown',e=>{if(!R.on)return;if(e.key==='ArrowRight'||e.key===' '){e.preventDefault();R.ir(R.n+1,true)}if(e.key==='ArrowLeft')R.ir(R.n-1,true)});
document.addEventListener('click',e=>{const a=e.target.closest('a[href^="#"]');if(!a||!R.on)return;const t=document.getElementById(a.getAttribute('href').slice(1));if(!t)return;e.preventDefault();R.ir(R.pagDe(t),true)});
let pend=null;const otra=()=>{clearTimeout(pend);pend=setTimeout(()=>R.rehacer(),150)};
addEventListener('resize',otra);addEventListener('load',otra);document.querySelectorAll('#hojas img').forEach(i=>i.addEventListener('load',otra));
if(document.fonts&&document.fonts.ready)document.fonts.ready.then(otra);
R.modo(g('hk_libro_modo','1')==='1');return R})();
</script><!--PAGJS-FIN-->'''

BOTONES = ('<button class="bpag" onclick="R.letra(-1)" aria-label="Letra más pequeña">A−</button>'
           '<button class="bpag" onclick="R.letra(1)" aria-label="Letra más grande">A+</button>'
           '<button class="bpag" id="bModo" onclick="R.modo()" aria-label="Cambiar modo de lectura">≡<span class=bt> Seguido</span></button>')

for c in sys.argv[1:]:
    c = c.rstrip('/'); slug = os.path.basename(c); f = os.path.join(c, 'index.html')
    p = open(f, encoding='utf-8').read()
    p = re.sub(r'<!--PAG-INI-->.*?<!--PAG-FIN-->', '', p, flags=re.S)
    p = re.sub(r'<!--PAGJS-INI-->.*?<!--PAGJS-FIN-->', '', p, flags=re.S)
    p = re.sub(r'<button class="bpag".*?</button>(?=<button class="bpag"|<a |</span>)', '', p)
    if '</head>' in p: p = p.replace('</head>', CSS + '</head>', 1)
    else: p = p.replace('<body', CSS + '<body', 1)          # (la nº 2 no cierra el head)
    if '<main id="lector">' not in p:
        assert p.count('<main>') == 1 and p.count('</main>') == 1, slug + ': no encuentro <main>'
        p = p.replace('<main>', '<main id="lector"><div class="hojas" id="hojas">').replace('</main>', '</div></main>')
    p = p.replace('>‹ Biblioteca</a>', '>‹<span class="bt"> Biblioteca</span></a>', 1)
    m = re.search(r'<span class="desc">', p); assert m, slug + ': no encuentro la zona de descargas'
    p = p[:m.end()] + BOTONES + p[m.end():]
    i = p.rindex('</body>') if '</body>' in p else len(p)
    p = p[:i] + JS.replace('__SLUG__', slug) + p[i:]
    open(f, 'w', encoding='utf-8').write(p)
    print(slug, ': modo páginas puesto')
