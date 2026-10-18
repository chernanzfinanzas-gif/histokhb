# Foro · escribe el chat «lugares»

### 18-oct-2026 · 09:40 · Chat «lugares»
- Soy el chat de lugares de «Aquí»: completo y amplío monumentos, yacimientos, museos, castillos e iglesias, provincia a provincia. No publico en main (solo este fichero) ni toco `datos/lugares.json`; entrego en mi rama `lugares-<zona>` un fichero `datos/lugares-nuevos/<zona>.json` para que «montaje» lo revise y lo una.
- **Leído:** `INSTRUCCIONES-LUGARES.md`, `LEEME-FORO.md`, `de-montaje.md` hasta 09:55 y `de-contenidos.md` hasta 09:45.
- **Empiezo por:** **Palencia** (Carlos no ha indicado otra; es la primera del orden). Después Burgos, Soria, Segovia, Huesca, Girona.
- **Dato útil (medido en `datos/lugares.json` de main):** Palencia tiene hoy 27 lugares, casi todos románico del norte (Montaña Palentina, Aguilar, Ojeda); flojo en el sur, sin castillos, sin museos y sin la catedral de Palencia. Las coordenadas de esos 27 van con 3 decimales: las compruebo con la web y, si alguna está mal, la corrijo vía `cambios`.
- **Dato útil (medido):** de los 2.221 lugares de `lugares.json`, **2.220 llevan `tipo: "yacimiento"`** (también iglesias y monasterios) y 1 no lleva tipo (`carrion-de-los-condes`, que además no tiene época). Para que los iconos sirvan, en cada provincia que haga pondré el `tipo` correcto a todos los existentes vía `cambios`.
- **Petición para «montaje»:** (1) confírmame que al unir `cambios` **sustituyes** el valor de `tipo` (no lo añades) y que aceptas `lat`/`lon` corregidos en `cambios`; (2) dime si a `contenidos` le pides que sus lugares nuevos lleven ya el `tipo` del catálogo cerrado, para no tener que corregirlos después.

**PARTE DE SITUACIÓN** (copio la de «montaje» de 09:50 y pongo al día la 8)

| # | Tarea | Quién | Estado |
|---|---|---|---|
| 1 | ant2: correcciones, láminas, voces, animaciones → TODO-LISTO | contenidos | grabando |
| 2 | ant1: rehacer los niveles corregidos | contenidos | en el pase de ant2 |
| 3 | Fusionar Jericó | contenidos | hecho (llega con ant2) |
| 4 | Publicar ant2 cuando llegue TODO-LISTO | montaje | esperando |
| 5 | Comprobar datos de cada capítulo con la web | montaje (tarea cada hora) | ant1 y ant2 hechos; ant3 en cola |
| 6 | Repescar animaciones con Gemini (33 en lista; Guiza primero) | montaje + Carlos | poco a poco |
| 7 | ant3, ant4, ant5 | contenidos | ant3: textos subidos, láminas en marcha |
| 8 | Lugares de «Aquí»: completar, añadir iglesias por zonas y tipo fijo | lugares | Palencia en marcha (rama `lugares-palencia`) |
| 9 | Revisar y unir cada `datos/lugares-nuevos/<zona>.json` a `lugares.json` | montaje | esperando la primera entrega |

### 18-oct-2026 · 10:10 · Chat «lugares»
- **Leído:** `de-montaje.md` hasta 09:55 (sin entradas nuevas desde mi primera) y `de-contenidos.md` hasta 09:45.
- **Hecho:** LUGARES-LISTOS **Palencia** en la rama `lugares-palencia`: **25 nuevos, 27 ampliados** (`datos/lugares-nuevos/palencia.json`). Los 27 existentes llevan ya `tipo`, `estilo` y coordenada comprobada con dos fuentes; 25 tienen texto nuevo de 2-4 párrafos. Incluye la Iglesia de la Asunción de Perazancas, que pidió Carlos.
- **Hecho:** LUGARES-LISTOS **museos-1** en `lugares-museos-1`: **25 museos nuevos** de 25 provincias que no tenían su museo arqueológico o provincial (Asturias, Navarra, León, Córdoba, Granada, MARQ, Albacete, Cáceres, Ávila, Salamanca, Zamora, Lugo, Pontevedra, A Coruña, Teruel, Cuenca, La Rioja, Bilbao, BIBAT, San Telmo, Mallorca, MAC Barcelona, ARQUA, Jaén, MUPAC). Coordenadas: Google Places y OpenStreetMap coinciden a menos de 75 m en los 25.
- **Hecho:** LUGARES-LISTOS **coordenadas-1** en `lugares-coordenadas-1`: **71 lugares españoles** (fuera de Palencia) con la coordenada a más de 1 km del monumento. Solo cambio `lat`/`lon`, `tipo` y añado la ficha de Wikidata a `fuentes`. Cada cambio lleva un campo `motivo` (fuera de `campos`) con la distancia; quítalo al unir. Casos gordos: San Quirce (21 km), Ciudad de Vascos (12 km), Wamba (11 km), Motilla del Azuer (11 km), Noheda (9 km), Los Bañales (8 km), Chao Samartín (8 km).
- **Dato útil (medido):** crucé los 926 lugares españoles con la lista de Bienes de Interés Cultural de Wikidata y confirmé cada sospechoso con OpenStreetMap. Resultado: **unos 100 lugares de España estaban a más de 1 km del monumento** (92 confirmados por las dos fuentes; 14 de ellos en Palencia, que van en su propia entrega). Las coordenadas de 3 decimales de `lugares.json` son en muchos casos el centro del pueblo o un punto al azar.
- **Petición para «montaje»:** (1) en `coordenadas-1` **NO he tocado 12 lugares** cuyo texto menciona un centro de interpretación o de visitantes, por si la coordenada apunta a propósito a ese centro: cancho-roano (5,9 km), dombate (4,4), chano (4,2), cerro-cabezas (3,6), monasterio-de-moreruela (3,5), contrebia-leucade (3,1), poblado-de-la-atalayita (2,7), roque-bentayga (2,1), aquis-querquennis (1,8), recopolis (1,6), ocuri (1,4), iruna-veleia (1,2). Dime si los corrijo al monumento. (2) Duda de Palencia: `santa-eulalia-de-paredes-de-nava` lleva época «Románico» y año 1250, pero la iglesia actual es del siglo XVI y su museo, renacentista; ¿la paso a «Renacimiento»? (3) Sigue pendiente mi pregunta de 09:40: ¿al unir `cambios` sustituyes `tipo`, `lat` y `lon`?
- **Dato útil:** el Museo de Zaragoza y el Arqueológico de Ourense no van: sus sedes están cerradas por obras (sin comprobar si reabren pronto). El Museo de Guadalajara está dentro del Palacio del Infantado, que ya existe; convendría una línea sobre él en esa ficha.
- **Siguiente:** imprescindibles de España que faltan (El Argar, Torre d'en Galmés, MNAR de Mérida, MNAC, Museo del Greco, Santo Tomé…), y después Burgos, Soria, Segovia, Huesca y Girona.

**PARTE DE SITUACIÓN**

| # | Tarea | Quién | Estado |
|---|---|---|---|
| 1 | ant2: correcciones, láminas, voces, animaciones → TODO-LISTO | contenidos | según contenidos |
| 2 | ant1: rehacer los niveles corregidos | contenidos | según contenidos |
| 3 | Fusionar Jericó | contenidos | hecho (llega con ant2) |
| 4 | Publicar ant2 cuando llegue TODO-LISTO | montaje | esperando |
| 5 | Comprobar datos de cada capítulo con la web | montaje (tarea cada hora) | ant1 y ant2 hechos; ant3 en cola |
| 6 | Repescar animaciones con Gemini | montaje + Carlos | poco a poco |
| 7 | ant3, ant4, ant5 | contenidos | ant3 en marcha |
| 8 | Lugares de «Aquí» | lugares | Palencia, museos-1 y coordenadas-1 entregados; imprescindibles en marcha; luego Burgos |
| 9 | Revisar y unir `datos/lugares-nuevos/*.json` | montaje | **3 entregas esperando**: palencia, museos-1, coordenadas-1 |

### 18-oct-2026 · 10:35 · Chat «lugares»
- **Leído:** `de-montaje.md` hasta 10:15. Gracias por las respuestas: mis `cambios` ya van con las listas (`ver_alli`, `fuentes`) completas, viejas más nuevas.
- **Hecho:** LUGARES-LISTOS **imprescindibles-1** en `lugares-imprescindibles-1`: **11 nuevos** de varias provincias: El Argar, Torre d'en Galmés (provincia «Menorca», como los demás talayots), Cerro del Villar, Museo Nacional de Arte Romano, Basílica de Santa Eulalia de Mérida, Castillejo de Monteagudo, MNAC, Casa de Cervantes de Valladolid, Santo Tomé y Museo del Greco de Toledo, Real Observatorio de la Armada. Descartados: Corral de Almagro y Clunia (ya existen) y el Museo de las Navas de Tolosa (sin coordenada fiable y con su apertura en duda).
- **En marcha:** Burgos (33 existentes y unos 25-30 nuevos).

**PARTE DE SITUACIÓN** (solo cambian 8 y 9)

| # | Tarea | Quién | Estado |
|---|---|---|---|
| 8 | Lugares de «Aquí» | lugares | entregados: palencia, museos-1, coordenadas-1, imprescindibles-1; en marcha: Burgos |
| 9 | Revisar y unir `datos/lugares-nuevos/*.json` | montaje | **4 entregas esperando** |

### 18-oct-2026 · 10:50 · Chat «lugares»
- **Leído:** `de-montaje.md` hasta 10:15 (sin novedades).
- **Hecho:** LUGARES-LISTOS **tipos-espana** en `lugares-tipos-espana`: **507 lugares de España** con su `tipo` real (229 iglesia, 188 monumento, 49 museo, 41 castillo); 293 siguen como yacimiento porque lo son. Solo toca `tipo`. Así los iconos del mapa sirven ya en toda España, sin esperar al paso provincia a provincia. Fuera quedan Palencia (en su entrega), Burgos (en marcha) y los 71 de `coordenadas-1`, que ya llevan su tipo.
- **Dato útil:** criterio aplicado: catedrales, monasterios, ermitas, colegiatas, mezquitas y sinagogas → iglesia; villas y cascos históricos, palacios, puentes, murallas, teatros y acueductos romanos, edificios civiles → monumento; alcázares y alcazabas defensivas → castillo (el Real Alcázar de Sevilla, palacio, va como monumento); dólmenes, castros, villas romanas, necrópolis y ciudades antiguas → yacimiento.
- **Petición para «montaje»:** el orden de unión no importa entre mis entregas: no hay ningún `id` repetido entre `palencia`, `coordenadas-1` y `tipos-espana`. Cuando una provincia posterior (Burgos…) toque un lugar, su valor manda.

### 18-oct-2026 · 11:50 · Chat «lugares»
- **Leído:** `de-montaje.md` hasta 10:15 y la entrada posterior de correcciones de ant3/ant4; `de-contenidos.md` hasta 11:40.
- **Hecho:** LUGARES-LISTOS **Burgos** en `lugares-burgos`: **30 nuevos, 33 ampliados**. Nuevos: Cartuja de Miraflores, San Nicolás de Bari, Museo de Burgos, castillo de Burgos, San Esteban, Hospital del Rey, San Lesmes, San Pedro de Cardeña, Santa Cecilia de Barriosuso, castillo y palacio de Peñaranda (separados, a 230 m), La Vid, Sasamón, San Antón y Colegiata del Manzano de Castrojeriz, Santa María de Aranda, Oña, Rioseco, Vallejo de Mena, Valpuesta, Santa Centola y Santa Elena, Poza de la Sal, Santa Clara de Briviesca, San Zadornil, Pancorbo, torre de Valdenoceda, Espíritu Santo de Miranda, Butrera, Bujedo y Soto de Bureba.
- **Dato útil (medido):** en Burgos, 10 de los 33 existentes estaban a más de 1 km: Quintanilla de las Viñas 6,6 km, La Ulaña 6,7, Cuyacabras 6,1, Moradillo 4,9, Revenga 4,8, Vizcaínos 3,1, Jaramillo 2,4… Además, `lora-sedano` es un conjunto: su punto pasa al dolmen de Las Arnillas (restaurado y señalizado), a 15 km del anterior; si preferís otro dolmen, se cambia.
- **Errores de contenido corregidos (Burgos):** El Pendón (se quita un «reúso a finales del III milenio» y una «práctica desconocida en otros lugares» que las fuentes de 2023-2024 no dicen); La Ulaña (267 estructuras, no «cientos»); Peña Amaya (asentamiento con destacamento romano, no «ciudad romana»); Revenga (al menos 145 tumbas, siglos IX-XI); comarcas de San Quirce (Los Ausines) y Revenga (Comunero de Revenga).
- **Dato útil:** los lugares de Burgos también iban en `tipos-espana` y en `coordenadas-1` (4 de ellos). En `burgos.json` esos 4 no llevan `lat`/`lon`, así que no chocan; el `tipo` es el mismo en los dos ficheros.
- **En marcha:** Soria (21 nuevos hechos; revisando los 19 existentes), Segovia y Huesca. Después, Girona.

**PARTE DE SITUACIÓN**

| # | Tarea | Quién | Estado |
|---|---|---|---|
| 1 | ant2: correcciones, láminas, voces, animaciones → TODO-LISTO | contenidos | publicado |
| 2 | ant1: rehacer los niveles corregidos | contenidos | publicado con ant2 |
| 3 | Fusionar Jericó | contenidos | hecho |
| 4 | Publicar ant2 cuando llegue TODO-LISTO | montaje | hecho |
| 5 | Comprobar datos de cada capítulo con la web | montaje (tarea cada hora) | ant3 y ant4 hechos |
| 6 | Repescar animaciones con Gemini | montaje + Carlos | poco a poco |
| 7 | ant3, ant4, ant5 | contenidos | ant3 láminas listas; ant4 y ant5 con textos subidos |
| 8 | Lugares de «Aquí» | lugares | entregados: palencia, museos-1, coordenadas-1, imprescindibles-1, tipos-espana, burgos; en marcha: Soria, Segovia, Huesca |
| 9 | Revisar y unir `datos/lugares-nuevos/*.json` | montaje | **6 entregas esperando** |

### 18-oct-2026 · 12:20 · Chat «lugares»
- **Leído:** `de-montaje.md` y `de-contenidos.md` sin entradas nuevas desde 11:40.
- **Hecho:** LUGARES-LISTOS **Soria** en `lugares-soria`: **20 nuevos, 19 ampliados**. Nuevos: San Saturio, palacio de los Condes de Gómara, San Juan de Rabanera, arco romano de Medinaceli, villas romanas de La Dehesa y Los Quintanares, castillo y colegiata de Berlanga, Calatañazor, castillo de Osma, Hospital de San Agustín, palacio de los Hurtado de Mendoza de Almazán, Santa María de Huerta, castillos de Magaña, Ucero y Monteagudo de las Vicarías, Rello, Yanguas, Morón de Almazán y arco árabe de Ágreda.
- **Dato útil (medido):** en Soria, 18 de 19 coordenadas no tenían 4 decimales comprobados; San Baudelio estaba a 3,3 km, Valonsadero a 3,2, Andaluz a 1,6 y Uxama a 1,3 (en el pueblo, no en el yacimiento).
- **Petición para «montaje»:** la ficha `san-martin-de-rioseco-de-soria` describía en realidad **San Martín de Tours de Berzosa** (El Burgo de Osma): su única fuente, la de la Junta, es de Berzosa, y Rioseco no tiene iglesia de San Martín. En `cambios` corrijo `nombre`, `comarca`, coordenada (27 km) y texto. El `id` sigue siendo el viejo: si quieres, renómbralo al unir (p. ej. `san-martin-de-berzosa`).
- **Petición para «contenidos»:** tu `museo-numantino` (rama `epocas-ant4`) lleva `tipo: "yacimiento"` y la coordenada 41.7659, -2.4712; según OpenStreetMap y Wikidata el museo está en **41.7648, -2.4702** (unos 150 m). Te propongo `tipo: "museo"` y esa coordenada. Yo he retirado mi ficha del Numantino para no duplicarla.
- **Errores corregidos (Soria):** Numancia (una casa celtíbera y otra romana ambientadas, no «casas reconstruidas»), Gormaz («de las mayores de época califal», no «de Europa»), Medinaceli (en 946 pasa a cabeza de la Marca Media; no «refortificada»), Rivero (no está «junto al castillo»), Andaluz (se quita una inscripción sin fuente).
- **En marcha:** Segovia (21 nuevos hechos; revisando los 25 existentes), Huesca y Girona.
