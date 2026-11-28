#!/usr/bin/env python3
"""Monta un número de «Bitácora del Almirante» (edición de adultos) a partir de sus textos en Markdown.

Uso: python3 herramientas/revista_almirante.py <carpeta de textos .md> <nº> <carpeta de la Grumete del mismo número>
  · Cada «## Sección · Título» es un artículo; la línea en cursiva siguiente es el subtítulo y el párrafo
    en negrita, la entrada. «### …» son ladillos; las citas «>» salen como citas destacadas.
  · Las ilustraciones y el glosario se toman de la edición Grumete del mismo número (FIGURAS de abajo).
  · Las efemérides «**D de mes de AAAA · Título.** texto *(Ficha: …)*» salen en rejilla con su enlace.
  · Deja biblioteca/almirante-NN/index.html; después hay que pasarle revista_paginas.py.
"""
import os, re, sys, json, shutil, subprocess, html

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src, num, gru = sys.argv[1], int(sys.argv[2]), os.path.abspath(sys.argv[3])
slug = f'almirante-{num:02d}'; dst = os.path.join(R, 'biblioteca', slug); os.makedirs(os.path.join(dst, 'img'), exist_ok=True)
G = open(os.path.join(gru, 'index.html'), encoding='utf-8').read()

# ---- ajustes de este número (nº 1, Pacífico) ----
NUMEROS = {
 1: dict(tema='Pacífico', fecha='Diciembre de 2026', alt='Portada de Bitácora del Almirante nº 1: Pacífico',
  carta=['Hace quinientos años, el océano más grande del planeta era un hueco en los mapas. Los barcos sabían cruzarlo en un sentido, pero no volver; los pilotos sabían a qué altura del mundo estaban, pero no cuánto habían avanzado; y en cada travesía morían de hambre y de escorbuto decenas de hombres.',
         'Este primer número de <b>Bitácora del Almirante</b> cuenta cómo se domó el Pacífico: la vuelta al mundo de Magallanes y Elcano, la ruta de vuelta que encontró un fraile guipuzcoano, el reloj que resolvió el problema de la longitud, los doscientos cincuenta años del galeón de Manila y la enfermera gallega que cruzó el océano cuidando a veintiséis niños. Además, un documento de la época, los mitos que conviene desmontar y dónde seguir leyendo.',
         'La misma historia, contada para los más jóvenes, está en <b>Bitácora del Grumete</b>, la revista hermana con Ammo.'],
  figuras={
   'magallanes': [('bit1-estrecho', 'El estrecho que hoy lleva el nombre de Magallanes: más de un mes de canales y fiordos, con las hogueras de los indígenas en la orilla. De ahí el nombre de Tierra del Fuego.', 2),
                  ('bit2-hambre', 'Noventa y ocho días sin tocar tierra: bizcocho podrido, cuero remojado, aserrín y ratas a medio ducado.', 5),
                  ('bit3-marianas', 'Las canoas de los chamorros rodean a las naves en Guam, el 6 de marzo de 1521.', 7)],
   'vuelta': [('bit9-mapa', 'Ida por el sur, con los alisios; vuelta por el norte, con los vientos del oeste y la corriente de Kuroshio: la ruta de Urdaneta.', 3),
              ('des-tornaviaje', 'Un galeón cruza el Pacífico Norte camino de Acapulco.', 6)],
   'ciencia': [('bit4-piloto', 'Un piloto mide la altura del Sol con el astrolabio: así se calculaba la latitud. La longitud era otra cosa.', 1),
               ('bit5-cronometro', 'El cronómetro marino, un reloj capaz de llevar durante meses la hora del puerto de salida.', 7)],
   'sociedad': [('bit6-galeon', 'Corte de un galeón: camarotes a popa, cañones, hamacas y una bodega repleta hasta el último rincón.', 3),
                ('bit7-fogon', 'El fogón, el único lugar del barco donde estaba permitido encender fuego.', 5)],
   'zendal': [('bit8-zendal', 'Isabel Zendal y los niños de la expedición, en una recreación: no se conserva ningún retrato suyo.', 3),
              ('des-balmis', 'La vacuna viajaba en el brazo de los niños, de dos en dos, cada diez días.', 6)],
   'curiosidades': [('bit10-trieste', 'El batiscafo Trieste en el fondo de la fosa de las Marianas, a casi once kilómetros de profundidad (1960).', 3)]},
  fichas={'la Segunda Guerra Mundial': 'con3-14', 'electricidad, teléfono, cine y aviones': 'con2-9',
          'la independencia de Estados Unidos': 'mod4-3', 'América entre 1789 y 1808': 'con-1789-am'},
  app={'«La primera vuelta al mundo»': 'mod1-1', '«Manila y el Galeón»': 'mod2-14', '«Cook y el Pacífico»': 'mod4-9',
       '«España entre 1789 y 1808»': 'con-1789-es'},
  ids={'Reportaje': 'magallanes', 'Historia': 'vuelta', 'Ciencia': 'ciencia', 'Sociedad': 'sociedad', 'Biografía': 'zendal',
       'El documento': 'documento', 'Mito o realidad': 'mitos', 'Para saber más': 'saber', 'Efemérides': 'efemerides',
       'Curiosidades': 'curiosidades'}),
}
N = NUMEROS[num]

def md2html(t):
    return subprocess.run(['pandoc', '-f', 'markdown-smart', '-t', 'html', '--wrap=none'], input=t, capture_output=True, text=True, check=True).stdout

texto = ''.join(open(os.path.join(src, f), encoding='utf-8').read() + '\n\n' for f in sorted(os.listdir(src)) if f.endswith('.md'))
texto = re.sub(r'^# .*\n', '', texto, flags=re.M)                       # título general del primer fichero
partes = re.split(r'^## ', texto, flags=re.M)[1:]

MESES = {'enero': 'ene', 'febrero': 'feb', 'marzo': 'mar', 'abril': 'abr', 'mayo': 'may', 'junio': 'jun', 'julio': 'jul',
         'agosto': 'ago', 'septiembre': 'sep', 'octubre': 'oct', 'noviembre': 'nov', 'diciembre': 'dic'}
arts, indice = [], []
for parte in partes:
    cab, cuerpo = parte.split('\n', 1)
    sec, tit = [x.strip() for x in cab.split('·', 1)] if '·' in cab else (cab.strip(), cab.strip())
    aid = N['ids'].get(sec, re.sub(r'\W+', '-', sec.lower()))
    sub = ''; m = re.match(r'\s*\*([^*].*?)\*\s*\n', cuerpo)
    if m: sub, cuerpo = m.group(1), cuerpo[m.end():]
    ent = ''; m = re.match(r'\s*\*\*(.+?)\*\*\s*\n', cuerpo, re.S)
    if m and sec not in ('Efemérides',): ent, cuerpo = m.group(1), cuerpo[m.end():]
    cuerpo = cuerpo.strip().rstrip('-').strip()
    if sec == 'Efemérides':
        filas = ''
        for m in re.finditer(r'\*\*(\d+) de (\w+) de (\d+) · (.+?)\.\*\*\s*(.+?)(?=\n\n|\Z)', cuerpo, re.S):
            d, mes, y, t, x = m.groups(); x = x.strip()
            f = re.search(r'\s*\*\(Ficha: (.+?)\.\)\*', x); enl = ''
            if f:
                x = x[:f.start()] + x[f.end():]; fid = N['fichas'].get(f.group(1))
                if fid: enl = f' <a class="fic" href="../../#/f/{fid}">Ver ficha →</a>'
            xh = md2html(x).strip()[3:-4]
            filas += f'<div class="d">{d} {MESES[mes]}<small>{y}</small></div><div class="t"><h3>{html.escape(t)}</h3><p>{xh}{enl}</p></div>'
        intro = md2html(cuerpo.split('**', 1)[0]).strip()
        intro = re.sub(r'\s*\(Las mismas fechas[^)]*\)', '', intro)
        cuerpo_h = intro + f'<div class="efe">{filas}</div>'
    elif sec == 'Curiosidades':
        cards = ''
        for i, m in enumerate(re.finditer(r'\*\*(.+?)\*\*\s*(.+?)(?=\n\n|\Z)', cuerpo, re.S)):
            cards += f'<div class="c{" az" if i % 3 == 1 else ""}"><h3>{html.escape(m.group(1).rstrip("."))}</h3>{md2html(m.group(2).strip())}</div>'
        cuerpo_h = f'<div class="cur">{cards}</div>'
    else:
        cuerpo_h = md2html(cuerpo)
    # citas y fuentes
    cuerpo_h = re.sub(r'<blockquote>\s*<p>(.*?)</p>\s*</blockquote>', r'<div class="cita">\1</div>', cuerpo_h, flags=re.S)
    cuerpo_h = re.sub(r'<hr\s*/?>\s*<p><em>(.*?)</em></p>', r'<p class="fuentes">\1</p>', cuerpo_h, flags=re.S)
    cuerpo_h = cuerpo_h.replace('<h3', '<h2').replace('</h3>', '</h2>') if sec not in ('Efemérides', 'Curiosidades') else cuerpo_h
    if sec == 'Mito o realidad':
        cuerpo_h = re.sub(r'<p><strong>(.*?)</strong>\s*<em>(.*?)\.?</em>\.?', r'<div class="mito"><h3>\1</h3><span class="ver">\2</span><p>', cuerpo_h)
        cuerpo_h = re.sub(r'(<div class="mito">.*?</p>)', r'\1</div>', cuerpo_h, flags=re.S)
    if sec == 'Para saber más':
        for k, fid in N['app'].items():
            cuerpo_h = cuerpo_h.replace('Ficha ' + k, f'<a href="../../#/f/{fid}">Ficha {k} →</a>')
        cuerpo_h = re.sub(r'<p><strong>(.*?)</strong></p>', r'<h2>\1</h2>', cuerpo_h)
    # ilustraciones: tras el párrafo n-ésimo del artículo
    figs = N['figuras'].get(aid, [])
    if figs:
        trozos = re.split(r'(?<=</p>)', cuerpo_h); cuenta = 0; out = ''
        pos = {n: (f, c) for f, c, n in figs}
        for tz in trozos:
            out += tz
            if tz.endswith('</p>'):
                cuenta += 1
                if cuenta in pos:
                    f, c = pos.pop(cuenta)
                    shutil.copy(os.path.join(gru, 'img', f + '.webp'), os.path.join(dst, 'img', f + '.webp'))
                    out += f'<figure><img src="img/{f}.webp" alt="" loading="lazy"><figcaption>{html.escape(c)}</figcaption></figure>'
        cuerpo_h = out
    a = f'<article id="{aid}"><div class="sec">{html.escape(sec)}</div><h1>{html.escape(tit)}</h1>'
    if sub: a += f'<p class="subt">{html.escape(sub)}</p>'
    if ent: a += f'<p class="ent">{html.escape(ent)}</p>'
    a += cuerpo_h + '<a class="arriba" href="#indice">↑ Índice</a></article>'
    arts.append(a); indice.append(f'<li><a href="#{aid}"><small>{html.escape(sec)}</small>{html.escape(tit)}</a></li>')

# glosario de la Grumete: mismo bloque, y se marca la primera aparición de cada término por artículo
gl_ini = G.index('<!--GL-INI-->'); gl_fin = G.index('<!--GL-FIN-->') + len('<!--GL-FIN-->'); GLB = G[gl_ini:gl_fin]
i = GLB.index('const GL=') + len('const GL='); GL, _ = json.JSONDecoder().raw_decode(GLB, i)
def marca(a):
    for n, (t, *_r) in sorted(enumerate(GL), key=lambda x: -len(x[1][0])):
        m = re.search(r'(?<![\wáéíóúñ>])(' + re.escape(t) + r')(?![\wáéíóúñ])(?![^<]*>)', a)
        if m and not re.search(r'<(h1|h2|h3|a|figcaption)[^>]*>[^<]*$', a[:m.start()]):
            a = a[:m.start()] + f'<span class="gl" data-g="{n}">{m.group(1)}</span>' + a[m.end():]
    return a
arts = [marca(a) for a in arts]

estilo = re.search(r'<style>(.*?)</style>', G, re.S).group(1)
estilo = estilo.replace('--azul:#12324a', '--azul:#0f2236').replace('--oro:#b8860b', '--oro:#9c7a1c')
estilo = re.sub(r'\bFredoka\b', "'Playfair Display'", estilo).replace('Nunito,system-ui,sans-serif', "Lora,Georgia,serif")
estilo += ('\n.subt{font:italic 17px/1.4 Lora,Georgia,serif;color:#6b5a3e;margin:-6px 0 10px}'
           '.ent{font-weight:600}.fuentes{font-size:13px;color:#6b5a3e;border-top:1px solid #d9c6a0;padding-top:10px;margin-top:22px}'
           'article h2{font-size:21px}.carta{background:#fff;border:1px solid #e3d6bd;border-radius:6px;padding:16px 18px;margin:10px 0 18px}'
           '.carta h3{font:700 20px "Playfair Display",Georgia,serif;color:var(--azul);margin:0 0 6px}.carta p{margin:0 0 10px;font-size:16px;line-height:1.6}'
           '.mito{border-left:4px solid var(--oro);padding:2px 0 2px 14px;margin:16px 0}.mito h3{font:700 18px/1.3 "Playfair Display",Georgia,serif;color:var(--azul);margin:0}'
           '.mito .ver{display:inline-block;font:700 12px Lora,serif;letter-spacing:1.5px;text-transform:uppercase;color:#fff;background:var(--oro);padding:1px 8px;border-radius:3px;margin:4px 0}'
           '.mito p{margin:4px 0 0}.cur .c h3{font-size:17px}#saber ul{padding-left:20px}#saber li{margin:6px 0}#saber a{color:var(--azul);font-weight:700}'
           '.cita{font:italic 18px/1.55 Lora,Georgia,serif}body.libro .efe .t,body.libro .efe .d{break-inside:auto}')
fuentes = '<link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400;0,600;0,700;1,400&family=Playfair+Display:wght@700;800&display=swap" rel="stylesheet">'
tit = f'Bitácora del Almirante nº {num} · {N["tema"]}'
pagina = f'''<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{tit}</title>
<meta name="description" content="La revista de Historia Total para adultos: {N["tema"]}."><meta property="og:title" content="{tit}"><meta property="og:image" content="https://historiatotal.es/biblioteca/{slug}/img/portada.webp">
{fuentes}<style>{estilo}</style></head><body>
<div class="barra"><a href="../../#/biblioteca">‹<span class="bt"> Biblioteca</span></a><span>ALMIRANTE · nº {num}</span><span class="desc"><a href="{slug}.epub" download onclick="cuenta('epub')">EPUB ⬇</a> <a href="{slug}.pdf" download onclick="cuenta('pdf')">PDF ⬇</a></span></div>
<main><header class="port"><img src="img/portada.webp" alt="{N["alt"]}"></header><section id="indice" class="ind"><div class="carta"><h3>Carta del almirante</h3>{"".join(f"<p>{p}</p>" for p in N["carta"])}</div><h2 class="it">En este número</h2><ol>{"".join(indice)}</ol></section>
{"".join(arts)}
<footer class="fin"><h2>Hasta el próximo número</h2><p><b>Bitácora del Almirante</b> es la revista de Historia Total para adultos. Cada quince días, un viaje distinto por la historia, también en versión para jóvenes en <b>Bitácora del Grumete</b>.</p><p><a class="btn" href="../../#/biblioteca">Volver a la Biblioteca</a></p></footer></main>
<script>function cuenta(q){{try{{if(navigator.webdriver||!/historiatotal\\.es$/.test(location.hostname))return;fetch('../../api/visita.php',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{k:'b:{slug}-'+q}}),keepalive:true}}).catch(()=>{{}})}}catch(e){{}}}}cuenta('web');</script>
{GLB}
</body></html>'''
open(os.path.join(dst, 'index.html'), 'w', encoding='utf-8').write(pagina)
print(slug, ':', len(arts), 'artículos,', len(re.sub('<[^>]+>', ' ', pagina).split()), 'palabras en la página,',
      pagina.count('class="gl"'), 'términos del glosario,', pagina.count('<figure>'), 'ilustraciones')
