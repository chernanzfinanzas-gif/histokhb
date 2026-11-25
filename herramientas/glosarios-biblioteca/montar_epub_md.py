# Regenera libro.md (fuente del EPUB) a partir de los capítulos y las notas actuales
import re
notas=open('novela-perro-sagrado-notas.md').read()
prologo=notas.split('## PRÓLOGO (borrador)')[1].split('## NOTAS FINALES')[0].strip()
notasf=notas.split('## NOTAS FINALES')[1].strip()
notasf=re.sub(r'### Glosario.*?(?=### Fuentes)','',notasf,flags=re.S)
notasf=re.sub(r'^### ','## ',notasf,flags=re.M)
out=['---\ntitle: El perro sagrado\nsubtitle: La llegada del caballo a las llanuras del bisonte\nauthor: Carlos Hernanz\nlang: es-ES\n---\n','# Prólogo\n\n'+prologo+'\n']
for i in range(1,21):
    L=open(f'novela-perro-sagrado-cap{i:02d}-v2.md').read().strip().split('\n')
    k=1; last=0
    while k<len(L) and (L[k].strip()=='' or L[k].strip().startswith('*')):
        if L[k].strip().startswith('*'):
            last=k; L[k]='<p class="ent"><em>'+L[k].strip().strip('*')+'</em></p>'
        k+=1
    L.insert(last+1,f'\n![](ilus_jpg/cap{i:02d}.jpg)\n')
    out.append('\n'.join(L)+'\n')
out.append('# Notas: historia e invención\n\n'+notasf+'\n')
open('libro.md','w').write('\n'.join(out))
