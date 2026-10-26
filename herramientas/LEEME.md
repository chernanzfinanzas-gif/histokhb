# Herramientas de voz y láminas animadas

Requisitos: `pip install google-auth requests pillow`, `ffmpeg`, y la variable
`GOOGLE_APPLICATION_CREDENTIALS` con la ruta del .json de la cuenta de servicio
(fuera del repositorio; nunca se sube). El dominio `*.googleapis.com` ya está permitido.

- `voces.py fichas <capítulo|códigos>` y `voces.py des <códigos>`: audios y `datos/audio.json`.
- `animar.py <capítulo|códigos>`: láminas animadas con Veo Lite y hoja de revisión.
- `animar.py --camara <códigos>`: movimiento de cámara para las que Veo estropee.

Las voces se hacen con los textos DEFINITIVOS: si un texto que se lee cambia, rehacer su audio.
`herramientas/_tmp/` es temporal y no se sube.

## Diccionario («mantén pulsada una palabra»)
- Base: `herramientas/diccionario_base.json` → `palabras` (g: significado general ≤120 caracteres, en castellano muy llano; h: sentido histórico ≤160, solo si aporta), `alias` (lema mal sacado → palabra) y `descartes`.
- `python3 herramientas/diccionario.py` genera `datos/dic/<letra>.json` (se ejecuta solo en cada publicación) y escribe `herramientas/diccionario_pendientes.json` con las palabras de las fichas que aún no tienen definición (si está instalado `wordfreq`).
- **Al cerrar cada tanda de fichas nuevas**: ejecutarlo, definir las pendientes con ese criterio (Carlos prefiere de más que de menos: hay lectores con poco vocabulario; solo se descartan las que sabe un niño de 10 años) y añadirlas a `palabras`.

## Esta semana, hace un tiempo
- `herramientas/semana.py` genera `datos/semana.json` desde `herramientas/semana_revisados.json` + las fechas exactas de fichas nuevas (se ejecuta solo al publicar). Las nuevas salen con la frase donde aparece la fecha: escribirlas completas y con sujeto («El 26 de octubre de 1909, Ahn Jung-geun…»).

## Novedades automáticas (`novedades.py`)
Se ejecuta sola en cada publicación y rellena `datos/novedades.json`; después el propio workflow guarda en el repo ese fichero y `novedades_huellas.json` (commit «Novedades automáticas»).
- **Contenido**: compara fichas, desarrollos y fichas de la Sincronía con la huella anterior. Lo que no existía → «✨ Nueva»; lo que crece de verdad (≥15 % y ≥300 caracteres) → «➕ Ampliada». Las correcciones pequeñas no se anuncian.
- **Mejoras de la app**: cada línea de la descripción de un commit que empiece por `NOVEDAD:` se anuncia tal cual como «🛠️ En la app». Escríbela para el lector, corta y en castellano llano.
- Como el workflow añade un commit a `main`, antes de publicar otra vez hay que hacer `git pull --rebase origin main`.

## Audios y vídeos (`medios.py`) — desde el 26-oct-2026 NO van en el repositorio
Los `.mp3` de `audio/` y los `.mp4` de `img/vivas/` están en `.gitignore`. Viven en el hosting y, como copia, en el PC de Carlos (`Historia Universal\Multimedia`, que se pone al día con «Actualizar copia (1 clic).bat»). `datos/medios.json` guarda la huella (bytes y md5) de cada uno.
- **Después de grabar voces o animar** (voces.py, animar.py…): `python3 herramientas/medios.py subir <rutas>` (sin rutas: todos los que haya). Los deja en la rama `buzon-medios`. **Súbelos ANTES de publicar en main** el `datos/audio.json` que los menciona.
- El workflow los recoge, los copia al hosting, apunta su huella en `datos/medios.json` y vacía el buzón.
- Una sesión nueva NO tiene los audios ni los vídeos antiguos. Si hay que retocar uno (p. ej. igualar_lamina.py), se trae del PC de Carlos con el puente o se vuelve a generar.
