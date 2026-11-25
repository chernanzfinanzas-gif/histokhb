#!/usr/bin/env python3
"""Aplica un glosario a un visor de la Biblioteca de historiatotal.es.
- Subraya de puntos la primera aparición de cada término en cada capítulo (cada <h1> abre capítulo).
- Al tocar un término: ventanita con su explicación.
- Al mantener pulsada cualquier otra palabra: diccionario de la app (datos/dic/<letra>.json).
Uso: aplicar_glosario.py visor.html glosario.py   (se puede repetir: quita lo anterior antes)
"""
import sys, re, json, importlib.util
visor, fglos = sys.argv[1], sys.argv[2]
spec = importlib.util.spec_from_file_location('g', fglos); M = importlib.util.module_from_spec(spec); spec.loader.exec_module(M)
G, NOCAP = M.G, getattr(M, 'NOCAP', set())
s = open(visor, encoding='utf-8').read()
# quitar una aplicación anterior
s = re.sub(r'<!--GL-INI-->.*?<!--GL-FIN-->', '', s, flags=re.S)
s = re.sub(r'<span class="gl" data-g="\d+">([^<]*)</span>', r'\1', s)

FORMAS = []
for i, (gr, t, fs, d) in enumerate(G):
    for x in fs:
        FORMAS.append((x, i))
        if x[0].islower() and x not in NOCAP: FORMAS.append((x[0].upper() + x[1:], i))
for x in getattr(M, 'IGNORA', []): FORMAS.append((x, -1))
FORMAS.sort(key=lambda p: -len(p[0]))
FIDX = dict(FORMAS)
L = r'\wÁÉÍÓÚÜÑáéíóúüñʉ’\''
RX = re.compile(r'(?<![' + L + r'])(' + '|'.join(re.escape(x) for x, _ in FORMAS) + r')(?![' + L + r'])')
SALTA = ('h1', 'h2', 'h3', 'h4', 'a', 'button', 'script', 'style', 'title', 'head', 'textarea', 'select', 'svg')
CLASES_SALTA = ('barra', 'ent', 'num', 'desc', 'bacc')
cuenta = {}
ini = s.index('<body')
partes = re.split(r'(<[^>]+>)', s[ini:])
out = []; pila = []; usados = set()
for tok in partes:
    if tok.startswith('<'):
        m = re.match(r'<(/?)([a-zA-Z0-9]+)', tok)
        if m:
            cierra, nom = m.group(1), m.group(2).lower()
            if not cierra:
                if nom == 'h1': usados = set()
                cls = re.search(r'class="([^"]*)"', tok)
                salta = nom in SALTA or (cls and any(c in cls.group(1).split() for c in CLASES_SALTA))
                if salta and not tok.endswith('/>') and nom not in ('br', 'img', 'hr', 'input', 'meta', 'link'):
                    pila.append(nom)
                elif pila and nom == pila[-1] and not tok.endswith('/>'):
                    pila.append(nom)   # mismo elemento anidado dentro de uno que se salta
            elif pila and nom == pila[-1]:
                pila.pop()
        out.append(tok); continue
    if pila or not tok.strip():
        out.append(tok); continue
    def rep(m):
        i = FIDX[m.group(1)]
        if i < 0: return m.group(1)
        cuenta[i] = cuenta.get(i, 0) + 1
        if i in usados: return m.group(1)
        usados.add(i); return f'<span class="gl" data-g="{i}">{m.group(1)}</span>'
    out.append(RX.sub(rep, tok))
s = s[:ini] + ''.join(out)

GLJ = json.dumps([[t, d, gr] for gr, t, fs, d in G], ensure_ascii=False)
GLF = json.dumps({x.lower(): i for x, i in FORMAS if ' ' not in x and i >= 0}, ensure_ascii=False)
bloque = '''<!--GL-INI--><style>
.gl{text-decoration:underline dotted;text-decoration-color:color-mix(in srgb,currentColor 55%,transparent);text-decoration-thickness:1.5px;text-underline-offset:3px;cursor:pointer}
.dicw{position:fixed;left:50%;transform:translateX(-50%);bottom:calc(58px + env(safe-area-inset-bottom,0px));z-index:9000;width:min(560px,calc(100% - 24px));background:var(--papel,#fbf7ef);color:var(--tinta,#2a2622);border:1.5px solid var(--glc,#8a5a2b);border-radius:14px;box-shadow:0 8px 28px #0005;padding:11px 14px 12px;font-family:Nunito,system-ui,sans-serif;text-align:left}
.dicw.hide{display:none}.dicw .dh{display:flex;align-items:baseline;gap:8px}
.dicw .dp{font:600 19px Georgia,'EB Garamond',serif;flex:1}
.dicw .dx{border:0;background:none;font-size:24px;line-height:1;color:inherit;opacity:.6;padding:0 2px;cursor:pointer}
.dicw .dl{margin:5px 0 0;font-size:15px;line-height:1.45;text-indent:0;text-align:left!important;hyphens:none}
.dicw .dl b{display:block;font-size:11px;letter-spacing:1px;text-transform:uppercase;color:var(--glc,#8a5a2b)}
.dicw .dr{display:inline-block;margin-top:7px;font-size:13px;color:var(--glc,#8a5a2b)}
</style><div id="dicw" class="dicw hide"></div><script>
(function(){const GL=%GL%,GLF=%GLF%;const DIC={};let dicT=null,dicUlt='';const W=()=>document.getElementById('dicw');
const esc=t=>String(t).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const cierra=()=>{W().classList.add('hide');dicUlt=''};window.dicCierra=cierra;
const pinta=h=>{const w=W();w.innerHTML=h;w.classList.remove('hide')};
const cab=t=>`<div class="dh"><div class="dp">${esc(t)}</div><button class="dx" onclick="dicCierra()" aria-label="Cerrar">×</button></div>`;
const gl=i=>{const g=GL[i];pinta(cab(g[0])+`<p class="dl"><b>${esc(g[2])}</b>${esc(g[1])}</p>`)};
const letra=w=>{const c=w[0];return c==='ñ'?'ñ':c.normalize('NFD')[0]};
async function carga(l){if(!(l in DIC)){try{const r=await fetch('../../datos/dic/'+encodeURIComponent(l)+'.json');DIC[l]=r.ok?await r.json():{f:{},d:{}}}catch(e){DIC[l]={f:{},d:{}}}}return DIC[l]}
async function busca(w){const a=await carga(letra(w));const l=a.d[w]?w:(a.f[w]||w);const b=letra(l)===letra(w)?a:await carga(letra(l));return b.d[l]?{l,e:b.d[l]}:null}
async function dic(pal,mayus){const w=pal.toLowerCase();if(w in GLF)return gl(GLF[w]);const r=await busca(w);const rw=r?r.l:w;
 const ext=mayus?`<a class="dr" href="https://es.wikipedia.org/wiki/${encodeURIComponent(pal)}" target="_blank" rel="noopener">Más sobre «${esc(pal)}» en Wikipedia ↗</a>`:`<a class="dr" href="https://dle.rae.es/${encodeURIComponent(rw)}" target="_blank" rel="noopener">Buscar «${esc(rw)}» en el diccionario de la RAE ↗</a>`;
 let h=cab(r&&!mayus?r.l:pal);if(r){const e=r.e;if(e[1])h+=`<p class="dl"><b>En historia</b>${esc(e[1])}</p>`;h+=`<p class="dl">${e[1]?'<b>Significado general</b>':''}${esc(e[0])}</p>`}else h+=`<p class="dl">No está en el diccionario de Historia Total.</p>`;pinta(h+ext)}
document.addEventListener('click',e=>{const g=e.target.closest('.gl');if(g){e.preventDefault();e.stopPropagation();gl(+g.dataset.g)}},true);
document.addEventListener('selectionchange',()=>{clearTimeout(dicT);dicT=setTimeout(()=>{const s=getSelection();if(!s||s.isCollapsed)return;
 const n=s.anchorNode&&(s.anchorNode.nodeType===1?s.anchorNode:s.anchorNode.parentElement);if(!n||n.closest('.dicw,.barra,button,a'))return;
 const pal=s.toString().trim().replace(/^[«"“'(¿¡—]+|[»"”').,;:!?…—]+$/g,'');if(!/^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ]{2,30}$/.test(pal)||pal===dicUlt)return;
 dicUlt=pal;const pre=(s.anchorNode.textContent||'').slice(0,s.anchorOffset).trim();dic(pal,pal[0]!==pal[0].toLowerCase()&&pre!==''&&!/[.!?»—]$/.test(pre))},450)});
document.addEventListener('pointerdown',e=>{const w=W();if(w&&!w.classList.contains('hide')&&!w.contains(e.target)&&!e.target.closest('.gl'))cierra()},true);
})();</script><!--GL-FIN-->'''.replace('%GL%', GLJ).replace('%GLF%', GLF)
s = s.replace('</body>', bloque + '</body>', 1)
open(visor, 'w', encoding='utf-8').write(s)
sin = [G[i][1] for i in range(len(G)) if i not in cuenta]
print(f'{visor}: {sum(1 for _ in re.finditer(chr(60)+"span class=.gl.", s))} marcas; términos que no aparecen: {sin}')
