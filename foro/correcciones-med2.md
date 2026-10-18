# Correcciones de datos · Edad Media, capítulo 2

Comprobadas con la web por el chat que monta (tarea programada, 18-oct-2026), sobre
`TEXTOS-LISTOS med2` (d786f23, rama `epocas-med2`). Aplicar ANTES de grabar voces de med2.
Si alguna voz ya está grabada, rehacer solo ese nivel (NIVELES=… en voces.py).
Señalar en el commit: CORRECCIONES med2 aplicadas.

| Ficha | Nivel | Cambio |
|---|---|---|
| med2-10 | p (biblio) | ERROR: no hay edición española de Al-Khalili titulada «La Casa de la Sabiduría»: ese es el título español del libro de Lyons. «Jim Al-Khalili, <i>La Casa de la Sabiduría (Pathfinders: The Golden Age of Arabic Science)</i> (2010)» → «Jim Al-Khalili, <i>Pathfinders. The Golden Age of Arabic Science</i> (2010)». (marcialpons.es, catálogos) |
| med2-10 | p (biblio) | El libro de Lyons sí tiene edición española (Turner, col. Noema, 2010). «Jonathan Lyons, <i>The House of Wisdom. How the Arabs Transformed Western Civilization</i> (2009)» → «Jonathan Lyons, <i>La Casa de la Sabiduría. Cuando la Ilustración llegaba de Oriente (The House of Wisdom)</i> (2009)». (marcialpons.es, ISBN 9788475069296) |
| med2-10 | p | ERROR: la lista que sigue tiene seis títulos. «Escribió en árabe al menos cinco obras:» → «Escribió en árabe al menos seis obras:». (el propio texto) |
| med2-10 | g | Si nació hacia 780 (p), en 825 tenía unos 45. «un sabio de unos cuarenta años» → «un sabio de unos cuarenta y cinco años». |
| med2-14 | p (biblio) | ERROR: la edición española (Península, 2022) se titula de otro modo. «Serhii Plokhy, <i>Las puertas de Europa. Historia de Ucrania</i> (2015)» → «Serhii Plokhy, <i>Las puertas de Europa. Pasado y presente de Ucrania</i> (2015)». (ISBN 9788411001038, planetadelibros) |
| med2-2 | g | El último emir fue el propio Abderramán III (emir 912-929), nieto de Abd Allah, como dice p. «Los venció en 928 el nieto del último emir, Abderramán III, que en 929 se proclamaría califa.» → «Los venció en 928 el emir Abderramán III, nieto de Abd Allah, que en 929 se proclamaría califa.» |
| med2-4 | p (biblio) | La edición española de Barbero (Ariel) se titula solo «Carlomagno»; «Un padre dell'Europa» es el subtítulo del original. «Alessandro Barbero, <i>Carlomagno. Un padre de Europa</i> (2000)» → «Alessandro Barbero, <i>Carlomagno (Carlo Magno. Un padre dell'Europa)</i> (2000)». (lecturalia, libraccio.it) |
| med2-5 | p | Spillings: 870-871 es la moneda más reciente y el peso es la suma de dos depósitos (40 + 27 kg). «el de Spillings, de hacia 870, pesa unos 67 kilos de plata» → «el de Spillings, escondido poco después de 870, reúne unos 67 kilos de plata». (Gotland Museum / Wikipedia «Spillings Hoard») |
| med2-6 | p | La fecha de Igbo-Ukwu hoy se discute (AMS de McIntosh: 1027-1180; Daraojimba et al. 2022: ss. X-XIII). «del siglo IX o X» → «que sus excavadores fecharon en el siglo IX o X (dataciones más recientes los llevan a los siglos X a XII)». |
| med2-6 | g | g contradice a p (Wari se vacía hacia el 1000, Tiwanaku decae «en las décadas siguientes»). «llegaron a su apogeo y se hundieron hacia el año 1000» → «llegaron a su apogeo y se hundieron entre los años 1000 y 1100». |
| med2-12 | p | Según la bibliografía que recoge Wikipedia, un análisis de carbono 14 de 2010 fechó el alma de roble a finales del siglo IX, lo que no encaja con la leyenda de Pelayo. «los análisis han confirmado que es roble, pero no su origen» → «es de roble, y un análisis de carbono 14 la fechó a finales del siglo IX, en tiempos de Alfonso III, lo que no encaja con esa leyenda». (Wikipedia «Victory Cross») |
| med2-13 | p | Se cuentan unas 500 granjas en el Asentamiento Oriental y unas 100 en el Occidental. «en unas quinientas granjas» → «en unas seiscientas granjas». (worldhistory.org) |
| med2-13 | p (biblio) | Título de la edición española (Siruela); las dos sagas son anónimas del siglo XIII y de fechas distintas. «Anónimo, <i>La saga de los groenlandeses y La saga de Erik el Rojo</i> (1250)» → «Anónimo, <i>Saga de los groenlandeses. Saga de Eirik el Rojo</i> (siglo XIII)». (siruela.com) |
| med2-15 | p | El lugar exacto de Talas no se conoce; se sitúa junto a Taraz, en la frontera. «junto al río <b>Talas</b>, en el actual Kazajistán» → «junto al río <b>Talas</b>, en la frontera de los actuales Kazajistán y Kirguistán». |
| med2-16 | p (biblio) | Coedès no tiene edición española (solo francés e inglés, *The Indianized States of Southeast Asia*, 1968). «George Coedès, <i>Los estados hinduizados de Indochina e Indonesia (Les États hindouisés d'Indochine et d'Indonésie)</i> (1948)» → «George Coedès, <i>Les États hindouisés d'Indochine et d'Indonésie</i> (1948)». (CiNii, Center for Khmer Studies) |
| med2-16 | p | Koh Ker está a ~85 km en línea recta y a ~120-127 por carretera. «a unos 90 kilómetros al noreste» → «a unos 90 kilómetros al noreste en línea recta». (Lonely Planet) |
| med2-18 | p | Evans et al. (Science, 2018): lluvia un 41-54 % menor, hasta un 70 % en los peores momentos. «llovió entre un 40 y un 50 por ciento menos de lo normal» → «llovió entre un 41 y un 54 por ciento menos que hoy, y en los peores momentos hasta un 70 por ciento menos». (Univ. Cambridge, 2018) |

## Desarrollos

| Desarrollo | Cambio |
|---|---|
| des-angkor | Bibliografía: no hay edición española con ese título, y la obra se escribió después de 1297. «Zhou Daguan, Relación de las costumbres de Camboya (Zhenla fengtu ji) (1297)» → «Zhou Daguan, <i>A Record of Cambodia. The Land and Its People (Zhenla fengtu ji)</i> (hacia 1297-1312; trad. Peter Harris, Silkworm Books, 2007)». Igual en med3-16. |
| des-anse | El origen por las medusas es solo una de las explicaciones (la Canadian Encyclopedia da «L'Anse à la Médée»). «viene seguramente del francés L'Anse aux Méduses, «la cala de las medusas», que los pescadores fueron deformando» → «viene probablemente de un nombre francés anterior, L'Anse à la Médée o, según otros, L'Anse aux Méduses, «la cala de las medusas», que los pescadores fueron deformando». |
| des-anse | Los pueblos árticos ya martilleaban hierro meteórico; Parks Canada habla de la primera fundición conocida. «Fue la primera vez que alguien trabajó el hierro en América.» → «Es la primera fundición de hierro conocida en América.» |
| des-naranco | Los lunes la visita es gratuita y sin guía; el resto de días, guiada y de pago (3 €). «Se visitan con guía, con entrada, y conviene consultar el horario» → «Se visitan con guía y entrada de pago (los lunes, gratis y sin guía), y conviene consultar el horario». |

**Fuera del capítulo (sincronía, para quien la lleve):** `sinc-det-med.json` (Xuanzong) da la rebelión de An Lushan como 755-762; lo habitual, y lo que dice med2-15, es 755-763. `sinc-eventos.json` (751) dice «el papel chino pasa al mundo islámico», que med2-15 llama con razón leyenda → «Batalla de Talas: los abasíes vencen a los Tang».

Sin cambios (comprobado): fechas de la expansión islámica, Bagdad (30-VII-762), Covadonga y reyes asturianos, Roncesvalles, Verdún, vikingos (Lindisfarne, Sevilla 844, París 845, Oseberg, Gokstad), Medina Azahara (112 ha, mezquita de 941, museo de 2009, UNESCO 2018), Teodomiro (estudio de *Antiquity* 2024), cruces de 808 y 908, Kuitems 2021, Rus de Kiev, Tang (censos de 754 y 764, edicto de 845, Sutra del Diamante de 868), Angkor (Sdok Kak Thom, barays, Koh Ker UNESCO 2023, lidar 2012/2015), Ghana (al-Bakri 1068), mayas (Copán, lidar 2018, cenote), Fez (859, Chaouni 2012-2016), Mezquita de Córdoba (ampliaciones, horario gratuito 8:30-9:30), y el resto de la bibliografía.
