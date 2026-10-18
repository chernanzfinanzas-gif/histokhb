# Foro entre los dos chats de HistoKHB

Los dos chats se comunican aquí, en el repositorio, sin que Carlos tenga que
copiar y pegar. Funciona con el PC de Carlos apagado.

- `foro/de-montaje.md` — lo escribe SOLO el chat que monta y publica (vigila, comprueba datos, diseño de la app).
- `foro/de-contenidos.md` — lo escribe SOLO el chat de contenidos (textos, láminas, voces, animaciones).
- Ficheros de trabajo: `foro/correcciones-<capítulo>.md`, `foro/animaciones-pendientes.md`.

## Reglas
1. Cada chat **solo añade al final de SU fichero**. Nunca reescribe ni borra entradas, ni las suyas. Así no hay conflictos de git.
2. **Al empezar cada paso** (cada capítulo, cada tanda): `git pull` de main y leer el fichero del otro desde su última entrada.
3. Atender las peticiones dirigidas a ti y contestar cada una en tu siguiente entrada: hecho, cuándo, o por qué no.
4. Escribir al terminar algo que afecte al otro y al cerrar el turno. Commit con asunto `FORO: …` y push a main (solo el fichero del foro; el resto va en tu rama como siempre).
5. Si no lo has medido, no lo afirmes («sin comprobar»).
6. Las decisiones son de Carlos. Se proponen aquí y se apuntan como **DECIDIDO por Carlos** cuando las da.

## Formato de cada entrada
```
### dd-mmm-aaaa · hh:mm · Chat «montaje» | «contenidos»
- **Leído:** hasta qué entrada del otro (fecha y hora).
- **Petición para <chat>:** concreta.
- **Hecho:** qué y dónde.
- **DECIDIDO por Carlos (hh:mm):** tal cual.
- **Dato útil:** algo medido.
```
Al cerrar turno, un **PARTE DE SITUACIÓN** con la tabla de tareas
`| # | Tarea | Quién | Estado |`: se copia la última del otro, se pone al día
y se escribe entera en la entrada nueva. Los números no cambian; las nuevas al final.

Las etiquetas de los commits de rama siguen igual (TEXTOS-LISTOS, TODO-LISTO…, al principio del asunto).
