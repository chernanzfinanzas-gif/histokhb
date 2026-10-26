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
