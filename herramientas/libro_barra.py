#!/usr/bin/env python3
"""Barra de arriba de los libros: que nunca sea más ancha que la pantalla (móviles con letra grande).
Uso: python3 herramientas/libro_barra.py <carpeta del libro> [más…]
  En pantallas estrechas «‹ Biblioteca» se queda en «‹» y los botones, si no caben, se deslizan
  dentro de la barra en vez de empujar la página."""
import re, sys, os
CSS = ('/*BARRA-INI*/.barra{gap:8px}.barra>a{flex:none;white-space:nowrap}'
       '.bacc{min-width:0;flex-wrap:nowrap;overflow-x:auto;scrollbar-width:none}.bacc::-webkit-scrollbar{display:none}'
       '.bacc button{white-space:nowrap;flex:none}'
       '@media(max-width:480px){.barra{padding:8px 10px}.barra .bt{display:none}}/*BARRA-FIN*/')
for c in sys.argv[1:]:
    f = os.path.join(c.rstrip('/'), 'index.html'); p = open(f, encoding='utf-8').read()
    p = re.sub(r'/\*BARRA-INI\*/.*?/\*BARRA-FIN\*/', '', p, flags=re.S)
    i = p.index('</style>'); p = p[:i] + CSS + p[i:]
    for a, b in [('>‹ Biblioteca</a>', '>‹<span class="bt"> Biblioteca</span></a>'),
                 ('>☰ Índice</button>', '>☰<span class="bt"> Índice</span></button>'),
                 ('>≡ Seguido</button>', '>≡<span class="bt"> Seguido</span></button>'),
                 ('>📖 Páginas</button>', '>📖<span class="bt"> Páginas</span></button>'),
                 (".textContent=this.on?'≡ Seguido':'📖 Páginas'", ".innerHTML=this.on?'≡<span class=bt> Seguido</span>':'📖<span class=bt> Páginas</span>'")]:
        p = p.replace(a, b)
    open(f, 'w', encoding='utf-8').write(p); print(os.path.basename(c.rstrip('/')), 'ok')
