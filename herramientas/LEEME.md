# Herramientas de voz y láminas animadas

Requisitos: `pip install google-auth requests pillow`, `ffmpeg`, y la variable
`GOOGLE_APPLICATION_CREDENTIALS` con la ruta del .json de la cuenta de servicio
(fuera del repositorio; nunca se sube). El dominio `*.googleapis.com` ya está permitido.

- `voces.py fichas <capítulo|códigos>` y `voces.py des <códigos>`: audios y `datos/audio.json`.
- `animar.py <capítulo|códigos>`: láminas animadas con Veo Lite y hoja de revisión.
- `animar.py --camara <códigos>`: movimiento de cámara para las que Veo estropee.

Las voces se hacen con los textos DEFINITIVOS: si un texto que se lee cambia, rehacer su audio.
`herramientas/_tmp/` es temporal y no se sube.
