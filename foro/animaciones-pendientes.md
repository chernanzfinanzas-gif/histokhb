# Animaciones pendientes de mejorar con Gemini

Láminas que hoy solo tienen **movimiento de cámara** (Veo falló o no se intentó).
Se rehacen poco a poco con Gemini (≈3 vídeos por tramo de uso): una conversación nueva por vídeo,
adjuntando la lámina y un texto que prohíba añadir elementos. Si Gemini también falla, se queda la cámara.

## Plantilla del texto (la que funciona — 25-oct)

NO describir el dibujo (si se describe, Gemini genera una ilustración nueva). Solo decir qué se mueve y qué queda quieto:

```
Animate this illustration, not another one, as an 8-second video. Keep all elements exactly as they are — do not add, remove or change anything. Animate naturally: <qué se mueve>. <Edificios/objetos fijos> remain completely still. No camera movement, no zoom.
```

Al recibir un vídeo: se sube y se pasa `python3 herramientas/igualar_lamina.py <código>`. Si Gemini redibujó, la lámina pasa a ser el primer fotograma del vídeo (así imagen fija y vídeo coinciden). Carlos no tiene que revisar nada.

## Prioridad

- [x] des-guiza (Gemini, 18-oct) · Cómo se construyó la Gran Pirámide

## Resto


### Edad Antigua
- [x] ant1-0 (Gemini, 25-oct) · Sumer y sus ciudades
- [ ] ant1-11 · Caral, la ciudad más antigua de América
- [x] ant1-12 (Veo, 25-oct) · China antes de las dinastías: Longshan y el «gran Yu»
- [ ] ant1-13 · El Argar, el primer Estado de la península
- [ ] ant1-2 · El valle del Indo
- [ ] ant1-3 · Y mientras tanto…
- [x] ant1-4 (Gemini, 25-oct) · Narmer y la unificación de Egipto
- [ ] ant1-5 · Gilgamesh, el primer héroe
- [ ] ant1-6 · Las tumbas reales de Ur
- [ ] ant1-7 · Enheduanna, la primera autora con nombre
- [ ] ant1-9 · Ebla y Mari, archivos de barro

### Cosmos y Tierra
- [ ] arcaico-6 · Los fósiles más antiguos: la búsqueda de la primera vida
- [x] mesozoico-8 (Veo, 25-oct) · Los primeros mamíferos, a la sombra de los dinosaurios
- [ ] paleozoico-11 · El bosque que se hizo carbón
- [x] proterozoico-5 (Veo, 25-oct) · La vida se hace múltiple
- [x] proterozoico-7 (Veo, 25-oct) · La capa de ozono: un filtro solar para el planeta

### Prehistoria
- [ ] neolitico-19 · Las megaaldeas de Ucrania
- [x] neolitico-6 (Veo, 25-oct) · Agriculturas de otros mundos
- [x] paleolitico-12 (Veo, 25-oct) · El poblamiento del planeta
- [x] paleolitico-14 (Gemini, 25-oct) · Las Venus paleolíticas

### Desarrollos
- [x] des-altamira (Gemini, 25-oct) · Altamira: la cueva que nadie creyó
- [ ] des-antequera · Antequera: Menga, Viera y El Romeral
- [ ] des-argar · La Bastida de Totana
- [ ] des-bola-nieve · La Tierra bola de nieve
- [ ] des-mesiniense · Cuando el Mediterráneo era un desierto de sal
- [x] des-mohenjo (Gemini, 25-oct) · Un paseo por Mohenjo-Daro
- [ ] des-polvo-estrellas · Polvo de estrellas: de dónde viene cada átomo de tu cuerpo
- [ ] des-sistema-solar · Cómo nace un sistema solar: del polvo a los planetas
- [x] des-stonehenge (Gemini, 25-oct) · Stonehenge: piedras traídas de muy lejos
- [ ] des-ur · Las tumbas reales de Ur

### Edad Antigua · capítulo 2
- [ ] ant2-0 · Egipto: los Imperios Medio y Nuevo
- [x] ant2-1 (Veo, 25-oct) · Babilonia, Asiria y los hititas
- [ ] ant2-2 · El Egeo: minoicos y micénicos
- [x] ant2-3 (Veo, 25-oct) · India: los Vedas
- [x] ant2-4 (Veo, 25-oct) · China: la dinastía Shang
- [ ] ant2-5 · Y mientras tanto…
- [ ] ant2-6 · Hammurabi y su código
- [ ] ant2-7 · Hatshepsut, la mujer faraón
- [ ] ant2-9 · Tutankamón
- [x] ant2-10 (Gemini, 25-oct, redibujada) · Ramsés II y el primer tratado de paz
- [x] ant2-11 (Gemini, 18-oct) · La erupción de Thera
- [ ] ant2-12 · Troya, entre el mito y la historia
- [ ] ant2-13 · Kerma, el reino de Nubia
- [ ] ant2-14 · Fu Hao y los huesos oraculares
- [ ] ant2-15 · Las motillas de La Mancha
- [ ] des-hattusa · Hattusa, la capital de los hititas
- [ ] des-tutankamon · La tumba de Tutankamón
- [ ] des-akrotiri · Akrotiri, la Pompeya del Egeo
- [ ] des-motilla · La Motilla del Azuer

### Edad Antigua · capítulo 3
- [x] ant3-1 (Veo, 25-oct) · Egipto: decadencia y faraones extranjeros
- [x] ant3-2 (Veo, 25-oct) · Israel, Fenicia y el alfabeto
- [ ] ant3-3 · Asiria, Babilonia y el Imperio persa
- [x] ant3-4 (Veo, 25-oct) · Grecia: nace la polis
- [x] ant3-5 (Veo, 25-oct) · América: olmecas y Chavín
- [x] ant3-6 (Veo, 25-oct) · La Era Axial: Buda, Confucio y Lao-Tsé
- [ ] ant3-7 · China: los Zhou
- [ ] ant3-8 · La Iberia prerromana: Tartessos, iberos y celtíberos
- [x] ant3-9 (Veo, 25-oct) · Y mientras tanto…
- [x] ant3-10 (Veo, 25-oct) · El tesoro del Carambolo
- [ ] ant3-11 · Cancho Roano y Casas del Turuñuelo
- [x] ant3-12 (Veo, 25-oct) · Gadir y los fenicios en el Mediterráneo occidental
- [ ] ant3-13 · Asurbanipal y la biblioteca de Nínive
- [x] ant3-14 (Veo, 25-oct) · Nabucodonosor II y la Babilonia de la Puerta de Ishtar
- [ ] ant3-15 · Ciro el Grande
- [x] ant3-16 (Veo, 25-oct) · Homero y los primeros Juegos Olímpicos
- [x] ant3-17 (Veo, 25-oct) · Kush: los faraones negros
- [ ] ant3-18 · Los etruscos y la fundación de Roma
- [ ] ant3-19 · Los escitas, jinetes de las estepas
- [x] des-carambolo (Veo, 25-oct) · El tesoro del Carambolo
- [ ] des-turunuelo · Casas del Turuñuelo, el edificio enterrado
- [ ] des-ninive · La biblioteca de Asurbanipal
- [ ] des-ishtar · La Puerta de Ishtar

### Edad Antigua · capítulo 4
- [x] ant4-0 (Gemini, 25-oct) · La Grecia clásica
- [x] ant4-1 (Veo, 25-oct) · Alejandro Magno y el helenismo
- [ ] ant4-2 · Roma: de la República al dominio del mundo
- [ ] ant4-3 · Hispania romana: conquista y romanización
- [ ] ant4-5 · China: Qin y Han
- [x] ant4-6 (Veo, 25-oct) · India: el Imperio Maurya
- [x] ant4-7 (Veo, 25-oct) · Y mientras tanto…
- [ ] ant4-9 · Pericles y la Acrópolis
- [ ] ant4-10 · Sócrates, Platón y Aristóteles
- [x] ant4-11 (Veo, 25-oct) · Aníbal y las guerras púnicas
- [ ] ant4-12 · Numancia
- [ ] ant4-13 · Viriato y los lusitanos
- [ ] ant4-14 · Julio César
- [x] ant4-15 (Veo, 25-oct) · Darío I y Persépolis
- [ ] ant4-16 · Qin Shi Huang y los guerreros de terracota
- [ ] ant4-17 · Ashoka
- [ ] ant4-18 · Las damas ibéricas: Elche, Baza y el Cerro de los Santos
- [ ] ant4-20 · Paracas y Nazca
- [ ] des-partenon · El Partenón
- [ ] des-numancia · Numancia, el asedio
- [ ] des-terracota · Los guerreros de terracota
- [ ] des-elche · La Dama de Elche
- [ ] des-persepolis · Persépolis

### Edad Media · capítulo 1
- [ ] med1-0 · La caída de Roma y los reinos bárbaros
- [ ] med1-5 · Suevos, vándalos y alanos: Hispania se rompe
- [x] med1-10 (Veo, 25-oct) · Clodoveo y los francos
- [ ] med1-14 · Teodorico y la Italia ostrogoda
- [ ] med1-6 · Justiniano, Teodora y Santa Sofía
- [x] med1-11 (Veo, 25-oct) · La peste de Justiniano
- [ ] med1-3 · La Iglesia, los monjes y el papado
- [ ] med1-9 · Los anglosajones y Sutton Hoo
- [ ] med1-1 · La Hispania visigoda: el reino de Toledo
- [x] med1-13 (Veo, 25-oct) · China: Sui y Tang
- [ ] med1-7 · Isidoro de Sevilla y las Etimologías
- [ ] med1-12 · Los mayas del Clásico: Palenque y Pakal
- [ ] med1-8 · El tesoro de Guarrazar
- [ ] med1-4 · Y mientras tanto…
- [ ] des-ravena · Los mosaicos de Rávena
- [ ] des-santa-sofia · Santa Sofía
- [x] des-guarrazar (Veo, 25-oct) · Las coronas de Guarrazar
- [ ] des-sutton-hoo · Sutton Hoo, el barco enterrado
- [ ] des-palenque · La tumba de Pakal

### Edad Antigua · capítulo 5
- [ ] ant5-0 · El Imperio romano
- [ ] ant5-8 · Augusto y la Pax Romana
- [ ] ant5-1 · Egipto romano y cristiano
- [x] ant5-2 (Veo, 25-oct) · Judea, Jesús y el nacimiento del cristianismo
- [ ] ant5-3 · China: Han, Tres Reinos y división
- [x] ant5-12 (Veo, 25-oct) · Hispania en el Imperio: Mérida, Itálica y Las Médulas
- [ ] ant5-19 · Japón y Corea: Yamato y los Tres Reinos
- [ ] ant5-15 · Aksum
- [x] ant5-9 (Veo, 25-oct) · Pompeya y Herculano
- [ ] ant5-11 · El Coliseo y los gladiadores
- [ ] ant5-10 · Trajano y Adriano, emperadores de Hispania
- [ ] ant5-14 · Los moche y el Señor de Sipán
- [ ] ant5-6 · Mesoamérica: Teotihuacan y los mayas
- [ ] ant5-5 · Persia sasánida
- [x] ant5-13 (Veo, 25-oct) · Constantino y Constantinopla
- [ ] ant5-4 · India: el Imperio Gupta
- [ ] ant5-16 · Los visigodos y el fin del Imperio de Occidente
- [ ] ant5-18 · Hipatia de Alejandría
- [x] ant5-7 (Veo, 25-oct) · Y mientras tanto…
- [ ] des-coliseo · El Coliseo
- [ ] des-medulas · Las Médulas
- [x] des-pompeya (Gemini, 18-oct) · Pompeya, una ciudad detenida
- [ ] des-sipan · El Señor de Sipán
- [ ] des-teotihuacan · Teotihuacan

### Edad Media · capítulo 2
- [ ] med2-0 · Mahoma y la expansión del islam
- [ ] med2-2 · Al-Ándalus y el esplendor de Córdoba
- [x] med2-3 (Veo, 25-oct) · Covadonga y el reino de Asturias
- [ ] med2-15 · China Tang: esplendor y rebelión
- [ ] med2-18 · El colapso maya y Chichén Itzá
- [ ] med2-17 · Ghana, el país del oro
- [ ] med2-4 · Carlomagno y el Imperio carolingio
- [x] med2-1 (Veo, 25-oct) · La Edad de Oro del islam: Bagdad
- [ ] med2-7 · De Oviedo al Duero: de Alfonso II a Alfonso III
- [ ] med2-12 · El arte asturiano
- [x] med2-16 (Veo, 25-oct) · Angkor y el imperio jemer
- [ ] med2-10 · La Casa de la Sabiduría y al-Juarismi
- [ ] med2-11 · Santiago de Compostela y el nacimiento del Camino
- [ ] med2-19 · Fátima al-Fihri y la mezquita de al-Qarawiyyin
- [x] med2-14 (Veo, 25-oct) · La Rus de Kiev
- [ ] med2-8 · El reino de León y la Castilla de Fernán González
- [ ] med2-9 · Abderramán III y Medina Azahara
- [ ] med2-6 · Y mientras tanto…
- [x] des-mezquita (Veo, 25-oct) · La Mezquita de Córdoba
- [ ] des-azahara · Medina Azahara
- [ ] des-naranco · Santa María del Naranco
- [x] des-anse (Veo, 25-oct) · L'Anse aux Meadows

### Edad Media · capítulo 3
- [ ] med3-9 · El Japón de los samuráis
- [ ] med3-4 · Bizancio: esplendor y la Cuarta Cruzada
- [x] med3-8 (Veo, 25-oct) · China Song y la revolución de los inventos
- [ ] med3-1 · El Sacro Imperio y el Papado
- [x] med3-0 (Veo, 25-oct) · El feudalismo y el despegue de Europa
- [ ] med3-13 · El románico: de Jaca y Frómista al Pórtico de la Gloria
- [ ] med3-20 · Murasaki Shikibu y el Genji
- [ ] med3-6 · La Reconquista (II): de las taifas a Las Navas de Tolosa
- [ ] med3-14 · Almorávides y almohades
- [ ] med3-11 · El Cid, entre la historia y el cantar
- [ ] med3-17 · Cahokia, la ciudad del Misisipi
- [ ] med3-2 · Inglaterra y Francia: Hastings y la Carta Magna
- [ ] med3-3 · Las Cruzadas y el choque con el Islam
- [ ] med3-15 · Hildegarda de Bingen
- [x] med3-16 (Veo, 25-oct) · Angkor Wat
- [ ] med3-18 · Averroes y Maimónides
- [ ] med3-12 · La Escuela de Traductores de Toledo
- [x] med3-19 (Veo, 25-oct) · Leonor de Aquitania
- [ ] med3-10 · Y mientras tanto…
- [ ] des-catedral-burgos · La catedral de Burgos
- [ ] des-giralda · La Giralda
- [ ] des-portico · El Pórtico de la Gloria
- [ ] des-angkor-wat · Angkor Wat

### Edad Media · capítulo 4
- [x] med4-0 (Veo, 25-oct) · Gengis Kan y el Imperio Mongol
- [x] med4-2 (Veo, 25-oct) · África: Malí y Mansa Musa
- [ ] med4-8 · La Alhambra y el reino nazarí de Granada
- [x] med4-3 (Veo, 25-oct) · Los reinos del África negra
- [ ] med4-1 · El Islam después de los mongoles
- [ ] med4-10 · Gran Zimbabue
- [ ] med4-5 · Alfonso X el Sabio
- [x] med4-9 (Veo, 25-oct) · La Corona de Aragón en el Mediterráneo
- [ ] med4-12 · Dante, Giotto y el Trecento
- [x] med4-7 (Veo, 25-oct) · Kublai Kan y la China Yuan
- [ ] med4-6 · Marco Polo y el Libro de las maravillas
- [ ] med4-11 · Las invasiones mongolas de Japón
- [ ] med4-13 · El final de los templarios
- [ ] med4-15 · Los mexicas y la fundación de Tenochtitlan
- [ ] med4-14 · Ibn Battuta, el viajero de Tánger
- [ ] des-cantigas · Las Cantigas de Santa María
- [ ] des-scrovegni · La Capilla de los Scrovegni
- [x] des-tenochtitlan (Veo, 25-oct) · Tenochtitlan, la ciudad en el lago
- [ ] des-zimbabue · Gran Zimbabue

### Edad Media · capítulo 5
- [x] med5-2 (Veo, 25-oct) · La caída de Constantinopla y los otomanos
- [ ] med5-1 · La Guerra de los Cien Años
- [x] med5-0 (Veo, 25-oct) · La Peste Negra y la crisis del siglo XIV
- [ ] med5-16 · Christine de Pizan
- [ ] med5-15 · Los Ming y la Ciudad Prohibida
- [ ] med5-8 · Tamerlán, Samarcanda y la embajada de Clavijo
- [ ] med5-14 · El reino del Kongo
- [ ] med5-7 · Sefarad: de 1391 a la expulsión de 1492
- [ ] med5-4 · El Renacimiento y la imprenta
- [ ] med5-17 · Caspe y la Corona de Aragón en Nápoles
- [ ] med5-9 · Juana de Arco
- [x] med5-12 (Veo, 25-oct) · Los portugueses en la costa de África
- [ ] med5-11 · Brunelleschi y la cúpula de Florencia
- [x] med5-5 (Veo, 25-oct) · Los imperios de América: aztecas e incas
- [ ] med5-13 · Pachacútec y Machu Picchu
- [ ] med5-3 · El fin de la Reconquista: los Reyes Católicos
- [ ] med5-6 · Y mientras tanto…
- [ ] des-ciudad-prohibida · La Ciudad Prohibida
- [ ] des-gutenberg · La Biblia de Gutenberg
- [ ] des-transito · La sinagoga del Tránsito

### Edad Moderna · capítulo 1
- [ ] mod1-0 · Colón, los taínos y La Española
- [ ] mod1-11 · Las epidemias y el gran desplome de América
- [x] mod1-2 (Veo, 25-oct) · Portugal y el imperio de las especias
- [ ] mod1-8 · Leonardo, Miguel Ángel y Rafael
- [ ] mod1-12 · Los humanistas: Erasmo, Moro, Nebrija y Alcalá
- [ ] mod1-14 · Songhai y Tombuctú
- [x] mod1-15 (Veo, 25-oct) · Sevilla, la Casa de Contratación y la Carrera de Indias
- [ ] mod1-3 · El Imperio de Carlos V y Felipe II
- [ ] mod1-13 · Comuneros y Germanías
- [ ] mod1-1 · La primera vuelta al mundo
- [ ] mod1-7 · Montesinos, Las Casas y las Leyes Nuevas
- [ ] mod1-9 · Solimán el Magnífico y Hürrem
- [x] mod1-6 (Veo, 25-oct) · Cajamarca y el fin del Tahuantinsuyo
- [ ] mod1-16 · Japón en guerra y los primeros europeos
- [ ] mod1-10 · Potosí y la plata
- [ ] mod1-4 · Y mientras tanto…
- [x] des-potosi (Veo, 25-oct) · El Cerro Rico de Potosí
- [ ] des-sevilla-indias · Sevilla, puerto de Indias
- [ ] des-suleymaniye · La mezquita de Solimán

### Edad Moderna · capítulo 2
- [ ] mod2-0 · Lutero y la Reforma protestante
- [ ] mod2-1 · La Contrarreforma católica
- [ ] mod2-7 · Felipe II: Lepanto, Portugal y la Armada
- [ ] mod2-17 · Los moriscos: de las Alpujarras a la expulsión
- [x] mod2-8 (Veo, 25-oct) · Teresa de Jesús y Juan de la Cruz
- [ ] mod2-20 · La rebelión de los Países Bajos
- [x] mod2-11 (Veo, 25-oct) · Isabel I de Inglaterra y Shakespeare
- [x] mod2-3 (Veo, 25-oct) · Los imperios de la pólvora: otomanos y safávidas
- [ ] mod2-12 · Akbar, Nur Jahan y el Taj Mahal
- [x] mod2-14 (Veo, 25-oct) · Manila y el Galeón
- [ ] mod2-16 · Guamán Poma y el Inca Garcilaso
- [ ] mod2-18 · Matteo Ricci y el final de los Ming
- [ ] mod2-13 · Los Tokugawa y la embajada de Hasekura
- [ ] mod2-9 · Cervantes y el Quijote
- [ ] mod2-19 · La caza de brujas
- [ ] mod2-5 · El nacimiento de la ciencia moderna
- [ ] mod2-15 · Galileo
- [ ] mod2-2 · La Guerra de los Treinta Años
- [ ] mod2-4 · La decadencia de los Austrias
- [ ] mod2-10 · Velázquez y la pintura del Siglo de Oro
- [ ] mod2-21 · Njinga de Ndongo y Matamba
- [x] mod2-6 (Veo, 25-oct) · Y mientras tanto…
- [ ] des-escorial · El Escorial
- [ ] des-globe · El teatro del Globo
- [ ] des-isfahan · La plaza de Isfahán
- [ ] des-taj-mahal · El Taj Mahal

### Edad Moderna · capítulo 3
- [ ] mod3-0 · Luis XIV y el absolutismo
- [ ] mod3-1 · Inglaterra: parlamento y revolución
- [x] mod3-2 (Veo, 25-oct) · La República Holandesa y su Siglo de Oro
- [ ] mod3-8 · Sor Juana Inés de la Cruz
- [ ] mod3-13 · El Japón de Edo
- [ ] mod3-12 · Kangxi y la China de los Qing
- [ ] mod3-10 · Pedro el Grande
- [ ] mod3-11 · Viena, 1683
- [ ] mod3-9 · Las misiones de los guaraníes
- [x] mod3-14 (Veo, 25-oct) · Piratas, corsarios y Cartagena de Indias
- [ ] mod3-5 · El comercio atlántico y la esclavitud
- [ ] mod3-17 · Nueva Francia y los pueblos de los Grandes Lagos
- [x] mod3-18 (Veo, 25-oct) · Maria Sibylla Merian, la pintora de las orugas
- [ ] mod3-7 · Carlos II y la Guerra de Sucesión
- [ ] mod3-15 · Bach, Händel y la música barroca
- [ ] mod3-4 · La América colonial: virreinatos y plata
- [ ] mod3-3 · Los grandes imperios de Asia: mogoles y safávidas
- [ ] mod3-6 · Y mientras tanto…
- [ ] des-cartagena-indias · Las murallas de Cartagena de Indias
- [ ] des-misiones-guaranies · Las ruinas de San Ignacio Miní
- [x] des-ronda-noche (Veo, 25-oct) · La ronda de noche

- [ ] mod4-0 · Newton y la razón universal
- [x] mod4-2 (Veo, 25-oct) · La España de los primeros Borbones
- [ ] mod4-1 · Los filósofos de la Ilustración
- [x] mod4-7 (Veo, 25-oct) · Las expediciones científicas españolas
- [ ] mod4-12 · Las mujeres de la Ilustración
- [ ] mod4-15 · Qianlong y el comercio de Cantón
- [ ] mod4-18 · El terremoto de Lisboa de 1755
- [ ] mod4-10 · Federico el Grande y la Guerra de los Siete Años
- [ ] mod4-4 · Catalina la Grande y la Europa oriental
- [ ] mod4-6 · Carlos III y el Madrid ilustrado
- [ ] mod4-14 · Plassey y la Compañía de las Indias
- [x] mod4-11 (Veo, 25-oct) · Empieza la Revolución Industrial
- [ ] mod4-13 · Mozart y el Clasicismo
- [ ] mod4-16 · Junípero Serra y las misiones de California
- [ ] mod4-3 · La independencia de Estados Unidos
- [ ] mod4-17 · Olaudah Equiano y los primeros abolicionistas
- [ ] mod4-8 · Túpac Amaru II y las rebeliones de 1780
- [x] mod4-5 (Veo, 25-oct) · Y mientras tanto…
- [ ] des-edificio-prado · El edificio de Villanueva
- [ ] des-mision-carmelo · La misión de Carmel
- [ ] des-sanssouci · Sanssouci
- [x] con-1789-0 (Veo, 25-oct) · El mundo entre 1789 y 1808: la era de las revoluciones
- [x] con-1789-es (Veo, 25-oct) · España entre 1789 y 1808: de Carlos IV a la crisis de la monarquía
- [ ] con-1789-eu · Europa entre 1789 y 1808: la Revolución francesa y Napoleón
- [x] con-1789-am (Veo, 25-oct) · América entre 1789 y 1808: Haití, Estados Unidos y los imperios ibéricos
- [ ] con-1789-om · Oriente Medio y el norte de África entre 1789 y 1808: Napoleón en Egipto
- [ ] des-rev1789 · 1789: el año que cambió Francia
- [ ] des-terror · El Terror (1793-1794)
- [x] des-napoleon (Veo, 25-oct) · Napoleón: del Consulado al Imperio (1799-1808)
- [ ] des-egipto · La expedición a Egipto y el nacimiento de la egiptología (1798-1801)
- [x] des-trafalgar (Veo, 25-oct) · Trafalgar (1805)
- [ ] des-haiti · La revolución de Haití (1791-1804)
- [x] des-luisiana (Veo, 25-oct) · La compra de Luisiana y el viaje de Lewis y Clark (1803-1806)
- [x] des-humboldt (Veo, 25-oct) · El viaje de Humboldt por América (1799-1804)
- [ ] des-malaspina · La expedición Malaspina (1789-1794)
- [ ] des-balmis · La Real Expedición Filantrópica de la Vacuna (1803-1806)
- [x] con-1808-0 (Veo, 25-oct) · El mundo entre 1808 y 1830: imperios que caen, naciones que nacen y máquinas de vapor
- [x] con-1808-es (Veo, 25-oct) · España entre 1808 y 1830: de la guerra de la Independencia a la Década Ominosa
- [ ] con-1808-eu · Europa entre 1808 y 1830: de Napoleón a la Restauración
- [ ] con-1808-am · América entre 1808 y 1830: las independencias
- [x] con-1808-om (Veo, 25-oct) · Oriente Medio y el norte de África entre 1808 y 1830: reformas desde arriba y presión de Europa
- [x] con-1808-as (Veo, 25-oct) · Asia y Oceanía entre 1808 y 1830: imperios cerrados, compañías comerciales y un volcán que enfrió el mundo
- [ ] des-cadiz · Las Cortes de Cádiz y la Constitución de 1812
- [ ] des-trienio · Riego y el Trienio Liberal (1820-1823)
- [x] des-rusia1812 (Veo, 25-oct) · La campaña de Rusia (1812)
- [x] des-bolivar (Veo, 25-oct) · Simón Bolívar y la Gran Colombia (1810-1830)
- [x] des-sanmartin (Veo, 25-oct) · San Martín y el cruce de los Andes (1812-1822)
- [x] des-mexico (Veo, 25-oct) · México: de Hidalgo a Iturbide (1810-1824)
- [x] des-guerraind (Veo, 25-oct) · La guerra de la Independencia: Bailén, los Sitios y la guerrilla (1808-1814)
- [x] des-grecia (Veo, 25-oct) · La guerra de independencia griega (1821-1830)
- [ ] des-te-opio · El té, el opio y el viaje secreto de las plantas de té (1757-1860)

- [ ] con1-8 · 
- [x] con1-10 (Veo, 25-oct) · 
- [ ] con1-18 · 
- [ ] con1-9 · 
- [x] con1-14 (Veo, 25-oct) · 
- [ ] con1-19 · 
- [x] con1-11 (Veo, 25-oct) · 
- [ ] con1-4 · 
- [ ] con1-15 · 
- [ ] con1-13 · 
- [ ] con1-17 · 
- [ ] con1-20 · 
- [ ] con1-16 · 
- [ ] con1-21 · 
- [ ] con1-7 · 
- [ ] des-cruz-roja · La Cruz Roja de Ginebra
- [x] des-galapagos (Veo, 25-oct) · Las islas Galápagos
- [x] des-suez (Veo, 25-oct) · El canal de Suez
- [ ] con2-1 · 
- [ ] con2-12 · 
- [x] con2-0 (Veo, 25-oct) · 
- [ ] con2-9 · 
- [ ] con2-10 · 
- [ ] con2-4 · 
- [ ] con2-3 · 
- [x] con2-7 (Veo, 25-oct) · 
- [ ] con2-5 · 
- [ ] con2-16 · 
- [ ] con2-2 · 
- [ ] con2-14 · 
- [x] con2-17 (Veo, 25-oct) · 
- [x] con2-13 (Veo, 25-oct) · 
- [x] con2-15 (Veo, 25-oct) · 
- [ ] con2-8 · 
- [x] con2-18 (Veo, 25-oct) · 
- [ ] con2-6 · 
- [ ] des-ellis-island · Ellis Island
- [ ] des-sagrada-familia · La Sagrada Família
- [x] des-transiberiano (Veo, 25-oct) · El Transiberiano
- [ ] con3-0 · 
- [ ] con3-10 · 
- [ ] con3-8 · 
- [ ] con3-1 · 
- [ ] con3-18 · 
- [ ] con3-9 · 
- [ ] con3-12 · 
- [ ] con3-4 · 
- [ ] con3-19 · 
- [ ] con3-2 · 
- [ ] con3-3 · 
- [ ] con3-13 · 
- [ ] con3-16 · 
- [ ] con3-17 · 
- [ ] con3-14 · 
- [ ] con3-5 · 
- [ ] con3-15 · 
- [ ] con3-6 · 
- [ ] con3-7 · 
- [ ] des-auschwitz · Auschwitz-Birkenau
- [ ] des-guernica · El Guernica
- [ ] des-verdun · Verdún
- [ ] con4-0 · 
- [ ] con4-10 · 
- [ ] con4-16 · 
- [ ] con4-4 · 
- [x] con4-11 (Veo, 25-oct) · 
- [x] con4-5 (Veo, 25-oct) · 
- [ ] con4-1 · 
- [ ] con4-2 · 
- [x] con4-12 (Veo, 25-oct) · 
- [ ] con4-15 · 
- [ ] con4-14 · 
- [ ] con4-17 · 
- [ ] con4-3 · 
- [ ] con4-7 · 
- [ ] con4-13 · 
- [ ] con4-6 · 
- [x] con4-19 (Veo, 25-oct) · 
- [x] con4-8 (Veo, 25-oct) · 
- [ ] con4-9 · 
- [ ] des-chernobil · Chernóbil
- [ ] des-congreso-1978 · El Congreso y la Constitución de 1978
- [x] des-onu (Veo, 25-oct) · La sede de la ONU en Nueva York
- [ ] des-robben-island · Robben Island
- [ ] con5-7 · 
- [ ] con5-10 · 
- [ ] con5-8 · 
- [x] con5-9 (Veo, 25-oct) · 
- [ ] con5-1 · 
- [ ] con5-11 · 
- [ ] con5-12 · 
- [ ] con5-2 · 
- [ ] con5-16 · 
- [ ] con5-13 · 
- [x] con5-15 (Veo, 25-oct) · 
- [x] con5-4 (Veo, 25-oct) · 
- [ ] con5-14 · 
- [ ] con5-18 · 
- [ ] con5-3 · 
- [ ] con5-6 · 
- [ ] con5-5 · 
- [ ] des-atocha-11m · El memorial del 11-M en Atocha
- [ ] des-cern · El CERN y el bosón de Higgs
- [ ] des-memorial-11s · El Memorial del 11-S
- [ ] des-srebrenica · El memorial de Srebrenica-Potočari

## Hechos con Gemini

- [x] ant1-1 (Gemini Flash, 18-oct) · Egipto: el Imperio Antiguo y las pirámides
- [x] paleolitico-13 (Gemini Flash, 18-oct) · El arte de las cavernas
- [x] des-ishtar (Gemini Flash, 18-oct) · La puerta de Ishtar

- [x] ant1-8 (al final con Veo; el de Gemini también salió bien) · Sargón de Acad, el primer imperio
- [x] des-caral · Caral: una ciudad sin guerra (recortado a 5 s en ida y vuelta: Gemini arrastró el zigurat del vídeo anterior)
