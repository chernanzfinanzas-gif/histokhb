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

## LAS QUE QUEDAN PARA GEMINI (17) — pedir SOLO estas

Veo no supo animarlas sin cambiar el dibujo. Todas las demás láminas ya tienen animación. Carlos las hace en su Gemini con la plantilla de arriba, una por conversación; al recibir cada vídeo se sube, se pasa `herramientas/igualar_lamina.py <código>` y se marca aquí con [x]. Hechas el 25-oct: ant4-20, ant5-1, con1-19, con3-17.

1. ✓ con4-0 · La Guerra Fría
2. ✓ con4-17 · 1968: juventud, música y protesta
3. ✓ con5-5 · Y mientras tanto…
4. ✓ des-malaspina · La expedición Malaspina (1789-1794)
5. ✓ des-mesiniense · Cuando el Mediterráneo era un desierto de sal
6. des-polvo-estrellas · Polvo de estrellas: de dónde viene cada átomo de tu cuerpo — REPETIR (la actual tiene un cangrejo)
7. des-rev1789 · 1789: el año que cambió Francia
8. des-scrovegni · La Capilla de los Scrovegni
9. des-terracota · Los guerreros de terracota
10. med3-11 · El Cid, entre la historia y el cantar
11. med3-17 · Cahokia, la ciudad del Misisipi
12. med4-13 · El final de los templarios
13. mod1-1 · La primera vuelta al mundo
14. mod1-16 · Japón en guerra y los primeros europeos
15. mod2-15 · Galileo
16. mod3-17 · Nueva Francia y los pueblos de los Grandes Lagos
17. mod4-16 · Junípero Serra y las misiones de California

## Prioridad

- [x] des-guiza (Gemini, 18-oct) · Cómo se construyó la Gran Pirámide

## Resto


### Edad Antigua
- [x] ant1-0 (Gemini, 25-oct) · Sumer y sus ciudades
- [x] ant1-11 (Veo, 25-oct) · Caral, la ciudad más antigua de América
- [x] ant1-12 (Veo, 25-oct) · China antes de las dinastías: Longshan y el «gran Yu»
- [x] ant1-13 (Veo, 25-oct) · El Argar, el primer Estado de la península
- [x] ant1-2 (Veo, 25-oct) · El valle del Indo
- [x] ant1-3 (Veo, 25-oct) · Y mientras tanto…
- [x] ant1-4 (Gemini, 25-oct) · Narmer y la unificación de Egipto
- [x] ant1-5 (Veo, 25-oct) · Gilgamesh, el primer héroe
- [x] ant1-6 (Veo, 25-oct) · Las tumbas reales de Ur
- [x] ant1-7 (Veo, 25-oct) · Enheduanna, la primera autora con nombre
- [x] ant1-9 (Veo, 25-oct) · Ebla y Mari, archivos de barro

### Cosmos y Tierra
- [x] arcaico-6 (Veo, 25-oct) · Los fósiles más antiguos: la búsqueda de la primera vida
- [x] mesozoico-8 (Veo, 25-oct) · Los primeros mamíferos, a la sombra de los dinosaurios
- [x] paleozoico-11 (Veo, 25-oct) · El bosque que se hizo carbón
- [x] proterozoico-5 (Veo, 25-oct) · La vida se hace múltiple
- [x] proterozoico-7 (Veo, 25-oct) · La capa de ozono: un filtro solar para el planeta

### Prehistoria
- [x] neolitico-19 (Veo, 25-oct) · Las megaaldeas de Ucrania
- [x] neolitico-6 (Veo, 25-oct) · Agriculturas de otros mundos
- [x] paleolitico-12 (Veo, 25-oct) · El poblamiento del planeta
- [x] paleolitico-14 (Gemini, 25-oct) · Las Venus paleolíticas

### Desarrollos
- [x] des-altamira (Gemini, 25-oct) · Altamira: la cueva que nadie creyó
- [x] des-antequera (Veo, 25-oct) · Antequera: Menga, Viera y El Romeral
- [x] des-argar (Veo, 25-oct) · La Bastida de Totana
- [x] des-bola-nieve (Veo, 25-oct) · La Tierra bola de nieve
- [x] des-mesiniense (Gemini, 26-oct) · Cuando el Mediterráneo era un desierto de sal
- [x] des-mohenjo (Gemini, 25-oct) · Un paseo por Mohenjo-Daro
- [ ] des-polvo-estrellas (REPETIR: el vídeo actual de Gemini pinta un cangrejo en la nebulosa; se deja puesto hasta tener uno mejor) · Polvo de estrellas: de dónde viene cada átomo de tu cuerpo
- [x] des-sistema-solar (Veo, 25-oct) · Cómo nace un sistema solar: del polvo a los planetas
- [x] des-stonehenge (Gemini, 25-oct) · Stonehenge: piedras traídas de muy lejos
- [x] des-ur (Veo, 25-oct) · Las tumbas reales de Ur

### Edad Antigua · capítulo 2
- [x] ant2-0 (Veo, 25-oct) · Egipto: los Imperios Medio y Nuevo
- [x] ant2-1 (Veo, 25-oct) · Babilonia, Asiria y los hititas
- [x] ant2-2 (Veo, 25-oct) · El Egeo: minoicos y micénicos
- [x] ant2-3 (Veo, 25-oct) · India: los Vedas
- [x] ant2-4 (Veo, 25-oct) · China: la dinastía Shang
- [x] ant2-5 (Veo, 25-oct) · Y mientras tanto…
- [x] ant2-6 (Veo, 25-oct) · Hammurabi y su código
- [x] ant2-7 (Veo, 25-oct) · Hatshepsut, la mujer faraón
- [x] ant2-9 (Veo, 25-oct) · Tutankamón
- [x] ant2-10 (Gemini, 25-oct, redibujada) · Ramsés II y el primer tratado de paz
- [x] ant2-11 (Gemini, 18-oct) · La erupción de Thera
- [x] ant2-12 (Veo, 25-oct) · Troya, entre el mito y la historia
- [x] ant2-13 (Veo, 25-oct) · Kerma, el reino de Nubia
- [x] ant2-14 (Veo, 25-oct) · Fu Hao y los huesos oraculares
- [x] ant2-15 (Veo, 25-oct) · Las motillas de La Mancha
- [x] des-hattusa (Veo, 25-oct) · Hattusa, la capital de los hititas
- [x] des-tutankamon (Veo, 25-oct) · La tumba de Tutankamón
- [x] des-akrotiri (Veo, 25-oct) · Akrotiri, la Pompeya del Egeo
- [x] des-motilla (Veo, 25-oct) · La Motilla del Azuer

### Edad Antigua · capítulo 3
- [x] ant3-1 (Veo, 25-oct) · Egipto: decadencia y faraones extranjeros
- [x] ant3-2 (Veo, 25-oct) · Israel, Fenicia y el alfabeto
- [x] ant3-3 (Veo, 25-oct) · Asiria, Babilonia y el Imperio persa
- [x] ant3-4 (Veo, 25-oct) · Grecia: nace la polis
- [x] ant3-5 (Veo, 25-oct) · América: olmecas y Chavín
- [x] ant3-6 (Veo, 25-oct) · La Era Axial: Buda, Confucio y Lao-Tsé
- [x] ant3-7 (Veo, 25-oct) · China: los Zhou
- [x] ant3-8 (Veo, 25-oct) · La Iberia prerromana: Tartessos, iberos y celtíberos
- [x] ant3-9 (Veo, 25-oct) · Y mientras tanto…
- [x] ant3-10 (Veo, 25-oct) · El tesoro del Carambolo
- [x] ant3-11 (Veo, 25-oct) · Cancho Roano y Casas del Turuñuelo
- [x] ant3-12 (Veo, 25-oct) · Gadir y los fenicios en el Mediterráneo occidental
- [x] ant3-13 (Veo, 25-oct) · Asurbanipal y la biblioteca de Nínive
- [x] ant3-14 (Veo, 25-oct) · Nabucodonosor II y la Babilonia de la Puerta de Ishtar
- [x] ant3-15 (Veo, 25-oct) · Ciro el Grande
- [x] ant3-16 (Veo, 25-oct) · Homero y los primeros Juegos Olímpicos
- [x] ant3-17 (Veo, 25-oct) · Kush: los faraones negros
- [x] ant3-18 (Veo, 25-oct) · Los etruscos y la fundación de Roma
- [x] ant3-19 (Veo, 25-oct) · Los escitas, jinetes de las estepas
- [x] des-carambolo (Veo, 25-oct) · El tesoro del Carambolo
- [x] des-turunuelo (Veo, 25-oct) · Casas del Turuñuelo, el edificio enterrado
- [x] des-ninive (Veo, 25-oct) · La biblioteca de Asurbanipal
- [x] des-ishtar (Gemini) · La Puerta de Ishtar

### Edad Antigua · capítulo 4
- [x] ant4-0 (Gemini, 25-oct) · La Grecia clásica
- [x] ant4-1 (Veo, 25-oct) · Alejandro Magno y el helenismo
- [x] ant4-2 (Veo, 25-oct) · Roma: de la República al dominio del mundo
- [x] ant4-3 (Veo, 25-oct) · Hispania romana: conquista y romanización
- [x] ant4-5 (Veo, 25-oct) · China: Qin y Han
- [x] ant4-6 (Veo, 25-oct) · India: el Imperio Maurya
- [x] ant4-7 (Veo, 25-oct) · Y mientras tanto…
- [x] ant4-9 (Veo, 25-oct) · Pericles y la Acrópolis
- [x] ant4-10 (Veo, 25-oct) · Sócrates, Platón y Aristóteles
- [x] ant4-11 (Veo, 25-oct) · Aníbal y las guerras púnicas
- [x] ant4-12 (Veo, 25-oct) · Numancia
- [x] ant4-13 (Veo, 25-oct) · Viriato y los lusitanos
- [x] ant4-14 (Veo, 25-oct) · Julio César
- [x] ant4-15 (Veo, 25-oct) · Darío I y Persépolis
- [x] ant4-16 (Veo, 25-oct) · Qin Shi Huang y los guerreros de terracota
- [x] ant4-17 (Veo, 25-oct) · Ashoka
- [x] ant4-18 (Veo, 25-oct) · Las damas ibéricas: Elche, Baza y el Cerro de los Santos
- [x] ant4-20 (Gemini, 25-oct) · Paracas y Nazca
- [x] des-partenon (Veo, 25-oct) · El Partenón
- [x] des-numancia (Veo, 25-oct) · Numancia, el asedio
- [ ] des-terracota · Los guerreros de terracota
- [x] des-elche (Veo, 25-oct) · La Dama de Elche
- [x] des-persepolis (Veo, 25-oct) · Persépolis

### Edad Media · capítulo 1
- [x] med1-0 (Veo, 25-oct) · La caída de Roma y los reinos bárbaros
- [x] med1-5 (Veo, 25-oct) · Suevos, vándalos y alanos: Hispania se rompe
- [x] med1-10 (Veo, 25-oct) · Clodoveo y los francos
- [x] med1-14 (Veo, 25-oct) · Teodorico y la Italia ostrogoda
- [x] med1-6 (Veo, 25-oct) · Justiniano, Teodora y Santa Sofía
- [x] med1-11 (Veo, 25-oct) · La peste de Justiniano
- [x] med1-3 (Veo, 25-oct) · La Iglesia, los monjes y el papado
- [x] med1-9 (Veo, 25-oct) · Los anglosajones y Sutton Hoo
- [x] med1-1 (Veo, 25-oct) · La Hispania visigoda: el reino de Toledo
- [x] med1-13 (Veo, 25-oct) · China: Sui y Tang
- [x] med1-7 (Veo, 25-oct) · Isidoro de Sevilla y las Etimologías
- [x] med1-12 (Veo, 25-oct) · Los mayas del Clásico: Palenque y Pakal
- [x] med1-8 (Veo, 25-oct) · El tesoro de Guarrazar
- [x] med1-4 (Veo, 25-oct) · Y mientras tanto…
- [x] des-ravena (Veo, 25-oct) · Los mosaicos de Rávena
- [x] des-santa-sofia (Veo, 25-oct) · Santa Sofía
- [x] des-guarrazar (Veo, 25-oct) · Las coronas de Guarrazar
- [x] des-sutton-hoo (Veo, 25-oct) · Sutton Hoo, el barco enterrado
- [x] des-palenque (Veo, 25-oct) · La tumba de Pakal

### Edad Antigua · capítulo 5
- [x] ant5-0 (Veo, 25-oct) · El Imperio romano
- [x] ant5-8 (Veo, 25-oct) · Augusto y la Pax Romana
- [x] ant5-1 (Gemini, 25-oct) · Egipto romano y cristiano
- [x] ant5-2 (Veo, 25-oct) · Judea, Jesús y el nacimiento del cristianismo
- [x] ant5-3 (Veo, 25-oct) · China: Han, Tres Reinos y división
- [x] ant5-12 (Veo, 25-oct) · Hispania en el Imperio: Mérida, Itálica y Las Médulas
- [x] ant5-19 (Veo, 25-oct) · Japón y Corea: Yamato y los Tres Reinos
- [x] ant5-15 (Veo, 25-oct) · Aksum
- [x] ant5-9 (Veo, 25-oct) · Pompeya y Herculano
- [x] ant5-11 (Veo, 25-oct) · El Coliseo y los gladiadores
- [x] ant5-10 (Veo, 25-oct) · Trajano y Adriano, emperadores de Hispania
- [x] ant5-14 (Veo, 25-oct) · Los moche y el Señor de Sipán
- [x] ant5-6 (Veo, 25-oct) · Mesoamérica: Teotihuacan y los mayas
- [x] ant5-5 (Veo, 25-oct) · Persia sasánida
- [x] ant5-13 (Veo, 25-oct) · Constantino y Constantinopla
- [x] ant5-4 (Veo, 25-oct) · India: el Imperio Gupta
- [x] ant5-16 (Veo, 25-oct) · Los visigodos y el fin del Imperio de Occidente
- [x] ant5-18 (Veo, 25-oct) · Hipatia de Alejandría
- [x] ant5-7 (Veo, 25-oct) · Y mientras tanto…
- [x] des-coliseo (Veo, 25-oct) · El Coliseo
- [x] des-medulas (Veo, 25-oct) · Las Médulas
- [x] des-pompeya (Gemini, 18-oct) · Pompeya, una ciudad detenida
- [x] des-sipan (Veo, 25-oct) · El Señor de Sipán
- [x] des-teotihuacan (Veo, 25-oct) · Teotihuacan

### Edad Media · capítulo 2
- [x] med2-0 (Veo, 25-oct) · Mahoma y la expansión del islam
- [x] med2-2 (Veo, 25-oct) · Al-Ándalus y el esplendor de Córdoba
- [x] med2-3 (Veo, 25-oct) · Covadonga y el reino de Asturias
- [x] med2-15 (Veo, 25-oct) · China Tang: esplendor y rebelión
- [x] med2-18 (Veo, 25-oct) · El colapso maya y Chichén Itzá
- [x] med2-17 (Veo, 25-oct) · Ghana, el país del oro
- [x] med2-4 (Veo, 25-oct) · Carlomagno y el Imperio carolingio
- [x] med2-1 (Veo, 25-oct) · La Edad de Oro del islam: Bagdad
- [x] med2-7 (Veo, 25-oct) · De Oviedo al Duero: de Alfonso II a Alfonso III
- [x] med2-12 (Veo, 25-oct) · El arte asturiano
- [x] med2-16 (Veo, 25-oct) · Angkor y el imperio jemer
- [x] med2-10 (Veo, 25-oct) · La Casa de la Sabiduría y al-Juarismi
- [x] med2-11 (Veo, 25-oct) · Santiago de Compostela y el nacimiento del Camino
- [x] med2-19 (Veo, 25-oct) · Fátima al-Fihri y la mezquita de al-Qarawiyyin
- [x] med2-14 (Veo, 25-oct) · La Rus de Kiev
- [x] med2-8 (Veo, 25-oct) · El reino de León y la Castilla de Fernán González
- [x] med2-9 (Veo, 25-oct) · Abderramán III y Medina Azahara
- [x] med2-6 (Veo, 25-oct) · Y mientras tanto…
- [x] des-mezquita (Veo, 25-oct) · La Mezquita de Córdoba
- [x] des-azahara (Veo, 25-oct) · Medina Azahara
- [x] des-naranco (Veo, 25-oct) · Santa María del Naranco
- [x] des-anse (Veo, 25-oct) · L'Anse aux Meadows

### Edad Media · capítulo 3
- [x] med3-9 (Veo, 25-oct) · El Japón de los samuráis
- [x] med3-4 (Veo, 25-oct) · Bizancio: esplendor y la Cuarta Cruzada
- [x] med3-8 (Veo, 25-oct) · China Song y la revolución de los inventos
- [x] med3-1 (Veo, 25-oct) · El Sacro Imperio y el Papado
- [x] med3-0 (Veo, 25-oct) · El feudalismo y el despegue de Europa
- [x] med3-13 (Veo, 25-oct) · El románico: de Jaca y Frómista al Pórtico de la Gloria
- [x] med3-20 (Veo, 25-oct) · Murasaki Shikibu y el Genji
- [x] med3-6 (Veo, 25-oct) · La Reconquista (II): de las taifas a Las Navas de Tolosa
- [x] med3-14 (Veo, 25-oct) · Almorávides y almohades
- [ ] med3-11 · El Cid, entre la historia y el cantar
- [ ] med3-17 · Cahokia, la ciudad del Misisipi
- [x] med3-2 (Veo, 25-oct) · Inglaterra y Francia: Hastings y la Carta Magna
- [x] med3-3 (Veo, 25-oct) · Las Cruzadas y el choque con el Islam
- [x] med3-15 (Veo, 25-oct) · Hildegarda de Bingen
- [x] med3-16 (Veo, 25-oct) · Angkor Wat
- [x] med3-18 (Veo, 25-oct) · Averroes y Maimónides
- [x] med3-12 (Veo, 25-oct) · La Escuela de Traductores de Toledo
- [x] med3-19 (Veo, 25-oct) · Leonor de Aquitania
- [x] med3-10 (Veo, 25-oct) · Y mientras tanto…
- [x] des-catedral-burgos (Veo, 25-oct) · La catedral de Burgos
- [x] des-giralda (Veo, 25-oct) · La Giralda
- [x] des-portico (Veo, 25-oct) · El Pórtico de la Gloria
- [x] des-angkor-wat (Veo, 25-oct) · Angkor Wat

### Edad Media · capítulo 4
- [x] med4-0 (Veo, 25-oct) · Gengis Kan y el Imperio Mongol
- [x] med4-2 (Veo, 25-oct) · África: Malí y Mansa Musa
- [x] med4-8 (Veo, 25-oct) · La Alhambra y el reino nazarí de Granada
- [x] med4-3 (Veo, 25-oct) · Los reinos del África negra
- [x] med4-1 (Veo, 25-oct) · El Islam después de los mongoles
- [x] med4-10 (Veo, 25-oct) · Gran Zimbabue
- [x] med4-5 (Veo, 25-oct) · Alfonso X el Sabio
- [x] med4-9 (Veo, 25-oct) · La Corona de Aragón en el Mediterráneo
- [x] med4-12 (Veo, 25-oct) · Dante, Giotto y el Trecento
- [x] med4-7 (Veo, 25-oct) · Kublai Kan y la China Yuan
- [x] med4-6 (Veo, 25-oct) · Marco Polo y el Libro de las maravillas
- [x] med4-11 (Veo, 25-oct) · Las invasiones mongolas de Japón
- [ ] med4-13 · El final de los templarios
- [x] med4-15 (Veo, 25-oct) · Los mexicas y la fundación de Tenochtitlan
- [x] med4-14 (Veo, 25-oct) · Ibn Battuta, el viajero de Tánger
- [x] des-cantigas (Veo, 25-oct) · Las Cantigas de Santa María
- [ ] des-scrovegni · La Capilla de los Scrovegni
- [x] des-tenochtitlan (Veo, 25-oct) · Tenochtitlan, la ciudad en el lago
- [x] des-zimbabue (Veo, 25-oct) · Gran Zimbabue

### Edad Media · capítulo 5
- [x] med5-2 (Veo, 25-oct) · La caída de Constantinopla y los otomanos
- [x] med5-1 (Veo, 25-oct) · La Guerra de los Cien Años
- [x] med5-0 (Veo, 25-oct) · La Peste Negra y la crisis del siglo XIV
- [x] med5-16 (Veo, 25-oct) · Christine de Pizan
- [x] med5-15 (Veo, 25-oct) · Los Ming y la Ciudad Prohibida
- [x] med5-8 (Veo, 25-oct) · Tamerlán, Samarcanda y la embajada de Clavijo
- [x] med5-14 (Veo, 25-oct) · El reino del Kongo
- [x] med5-7 (Veo, 25-oct) · Sefarad: de 1391 a la expulsión de 1492
- [x] med5-4 (Veo, 25-oct) · El Renacimiento y la imprenta
- [x] med5-17 (Veo, 25-oct) · Caspe y la Corona de Aragón en Nápoles
- [x] med5-9 (Veo, 25-oct) · Juana de Arco
- [x] med5-12 (Veo, 25-oct) · Los portugueses en la costa de África
- [x] med5-11 (Veo, 25-oct) · Brunelleschi y la cúpula de Florencia
- [x] med5-5 (Veo, 25-oct) · Los imperios de América: aztecas e incas
- [x] med5-13 (Veo, 25-oct) · Pachacútec y Machu Picchu
- [x] med5-3 (Veo, 25-oct) · El fin de la Reconquista: los Reyes Católicos
- [x] med5-6 (Veo, 25-oct) · Y mientras tanto…
- [x] des-ciudad-prohibida (Veo, 25-oct) · La Ciudad Prohibida
- [x] des-gutenberg (Veo, 25-oct) · La Biblia de Gutenberg
- [x] des-transito (Veo, 25-oct) · La sinagoga del Tránsito

### Edad Moderna · capítulo 1
- [x] mod1-0 (Veo, 25-oct) · Colón, los taínos y La Española
- [x] mod1-11 (Veo, 25-oct) · Las epidemias y el gran desplome de América
- [x] mod1-2 (Veo, 25-oct) · Portugal y el imperio de las especias
- [x] mod1-8 (Veo, 25-oct) · Leonardo, Miguel Ángel y Rafael
- [x] mod1-12 (Veo, 25-oct) · Los humanistas: Erasmo, Moro, Nebrija y Alcalá
- [x] mod1-14 (Veo, 25-oct) · Songhai y Tombuctú
- [x] mod1-15 (Veo, 25-oct) · Sevilla, la Casa de Contratación y la Carrera de Indias
- [x] mod1-3 (Veo, 25-oct) · El Imperio de Carlos V y Felipe II
- [x] mod1-13 (Veo, 25-oct) · Comuneros y Germanías
- [ ] mod1-1 · La primera vuelta al mundo
- [x] mod1-7 (Veo, 25-oct) · Montesinos, Las Casas y las Leyes Nuevas
- [x] mod1-9 (Veo, 25-oct) · Solimán el Magnífico y Hürrem
- [x] mod1-6 (Veo, 25-oct) · Cajamarca y el fin del Tahuantinsuyo
- [ ] mod1-16 · Japón en guerra y los primeros europeos
- [x] mod1-10 (Veo, 25-oct) · Potosí y la plata
- [x] mod1-4 (Veo, 25-oct) · Y mientras tanto…
- [x] des-potosi (Veo, 25-oct) · El Cerro Rico de Potosí
- [x] des-sevilla-indias (Veo, 25-oct) · Sevilla, puerto de Indias
- [x] des-suleymaniye (Veo, 25-oct) · La mezquita de Solimán

### Edad Moderna · capítulo 2
- [x] mod2-0 (Veo, 25-oct) · Lutero y la Reforma protestante
- [x] mod2-1 (Veo, 25-oct) · La Contrarreforma católica
- [x] mod2-7 (Veo, 25-oct) · Felipe II: Lepanto, Portugal y la Armada
- [x] mod2-17 (Veo, 25-oct) · Los moriscos: de las Alpujarras a la expulsión
- [x] mod2-8 (Veo, 25-oct) · Teresa de Jesús y Juan de la Cruz
- [x] mod2-20 (Veo, 25-oct) · La rebelión de los Países Bajos
- [x] mod2-11 (Veo, 25-oct) · Isabel I de Inglaterra y Shakespeare
- [x] mod2-3 (Veo, 25-oct) · Los imperios de la pólvora: otomanos y safávidas
- [x] mod2-12 (Veo, 25-oct) · Akbar, Nur Jahan y el Taj Mahal
- [x] mod2-14 (Veo, 25-oct) · Manila y el Galeón
- [x] mod2-16 (Veo, 25-oct) · Guamán Poma y el Inca Garcilaso
- [x] mod2-18 (Veo, 25-oct) · Matteo Ricci y el final de los Ming
- [x] mod2-13 (Veo, 25-oct) · Los Tokugawa y la embajada de Hasekura
- [x] mod2-9 (Veo, 25-oct) · Cervantes y el Quijote
- [x] mod2-19 (Veo, 25-oct) · La caza de brujas
- [x] mod2-5 (Veo, 25-oct) · El nacimiento de la ciencia moderna
- [ ] mod2-15 · Galileo
- [x] mod2-2 (Veo, 25-oct) · La Guerra de los Treinta Años
- [x] mod2-4 (Veo, 25-oct) · La decadencia de los Austrias
- [x] mod2-10 (Veo, 25-oct) · Velázquez y la pintura del Siglo de Oro
- [x] mod2-21 (Veo, 25-oct) · Njinga de Ndongo y Matamba
- [x] mod2-6 (Veo, 25-oct) · Y mientras tanto…
- [x] des-escorial (Veo, 25-oct) · El Escorial
- [x] des-globe (Veo, 25-oct) · El teatro del Globo
- [x] des-isfahan (Veo, 25-oct) · La plaza de Isfahán
- [x] des-taj-mahal (Veo, 25-oct) · El Taj Mahal

### Edad Moderna · capítulo 3
- [x] mod3-0 (Veo, 25-oct) · Luis XIV y el absolutismo
- [x] mod3-1 (Veo, 25-oct) · Inglaterra: parlamento y revolución
- [x] mod3-2 (Veo, 25-oct) · La República Holandesa y su Siglo de Oro
- [x] mod3-8 (Veo, 25-oct) · Sor Juana Inés de la Cruz
- [x] mod3-13 (Veo, 25-oct) · El Japón de Edo
- [x] mod3-12 (Veo, 25-oct) · Kangxi y la China de los Qing
- [x] mod3-10 (Veo, 25-oct) · Pedro el Grande
- [x] mod3-11 (Veo, 25-oct) · Viena, 1683
- [x] mod3-9 (Veo, 25-oct) · Las misiones de los guaraníes
- [x] mod3-14 (Veo, 25-oct) · Piratas, corsarios y Cartagena de Indias
- [x] mod3-5 (Veo, 25-oct) · El comercio atlántico y la esclavitud
- [ ] mod3-17 · Nueva Francia y los pueblos de los Grandes Lagos
- [x] mod3-18 (Veo, 25-oct) · Maria Sibylla Merian, la pintora de las orugas
- [x] mod3-7 (Veo, 25-oct) · Carlos II y la Guerra de Sucesión
- [x] mod3-15 (Veo, 25-oct) · Bach, Händel y la música barroca
- [x] mod3-4 (Veo, 25-oct) · La América colonial: virreinatos y plata
- [x] mod3-3 (Veo, 25-oct) · Los grandes imperios de Asia: mogoles y safávidas
- [x] mod3-6 (Veo, 25-oct) · Y mientras tanto…
- [x] des-cartagena-indias (Veo, 25-oct) · Las murallas de Cartagena de Indias
- [x] des-misiones-guaranies (Veo, 25-oct) · Las ruinas de San Ignacio Miní
- [x] des-ronda-noche (Veo, 25-oct) · La ronda de noche

- [x] mod4-0 (Veo, 25-oct) · Newton y la razón universal
- [x] mod4-2 (Veo, 25-oct) · La España de los primeros Borbones
- [x] mod4-1 (Veo, 25-oct) · Los filósofos de la Ilustración
- [x] mod4-7 (Veo, 25-oct) · Las expediciones científicas españolas
- [x] mod4-12 (Veo, 25-oct) · Las mujeres de la Ilustración
- [x] mod4-15 (Veo, 25-oct) · Qianlong y el comercio de Cantón
- [x] mod4-18 (Veo, 25-oct) · El terremoto de Lisboa de 1755
- [x] mod4-10 (Veo, 25-oct) · Federico el Grande y la Guerra de los Siete Años
- [x] mod4-4 (Veo, 25-oct) · Catalina la Grande y la Europa oriental
- [x] mod4-6 (Veo, 25-oct) · Carlos III y el Madrid ilustrado
- [x] mod4-14 (Veo, 25-oct) · Plassey y la Compañía de las Indias
- [x] mod4-11 (Veo, 25-oct) · Empieza la Revolución Industrial
- [x] mod4-13 (Veo, 25-oct) · Mozart y el Clasicismo
- [ ] mod4-16 · Junípero Serra y las misiones de California
- [x] mod4-3 (Veo, 25-oct) · La independencia de Estados Unidos
- [x] mod4-17 (Veo, 25-oct) · Olaudah Equiano y los primeros abolicionistas
- [x] mod4-8 (Veo, 25-oct) · Túpac Amaru II y las rebeliones de 1780
- [x] mod4-5 (Veo, 25-oct) · Y mientras tanto…
- [x] des-edificio-prado (Veo, 25-oct) · El edificio de Villanueva
- [x] des-mision-carmelo (Veo, 25-oct) · La misión de Carmel
- [x] des-sanssouci (Veo, 25-oct) · Sanssouci
- [x] con-1789-0 (Veo, 25-oct) · El mundo entre 1789 y 1808: la era de las revoluciones
- [x] con-1789-es (Veo, 25-oct) · España entre 1789 y 1808: de Carlos IV a la crisis de la monarquía
- [x] con-1789-eu (Veo, 25-oct) · Europa entre 1789 y 1808: la Revolución francesa y Napoleón
- [x] con-1789-am (Veo, 25-oct) · América entre 1789 y 1808: Haití, Estados Unidos y los imperios ibéricos
- [x] con-1789-om (Veo, 25-oct) · Oriente Medio y el norte de África entre 1789 y 1808: Napoleón en Egipto
- [ ] des-rev1789 · 1789: el año que cambió Francia
- [x] des-terror (Veo, 25-oct) · El Terror (1793-1794)
- [x] des-napoleon (Veo, 25-oct) · Napoleón: del Consulado al Imperio (1799-1808)
- [x] des-egipto (Veo, 25-oct) · La expedición a Egipto y el nacimiento de la egiptología (1798-1801)
- [x] des-trafalgar (Veo, 25-oct) · Trafalgar (1805)
- [x] des-haiti (Veo, 25-oct) · La revolución de Haití (1791-1804)
- [x] des-luisiana (Veo, 25-oct) · La compra de Luisiana y el viaje de Lewis y Clark (1803-1806)
- [x] des-humboldt (Veo, 25-oct) · El viaje de Humboldt por América (1799-1804)
- [x] des-malaspina (Gemini, 26-oct) · La expedición Malaspina (1789-1794)
- [x] des-balmis (Veo, 25-oct) · La Real Expedición Filantrópica de la Vacuna (1803-1806)
- [x] con-1808-0 (Veo, 25-oct) · El mundo entre 1808 y 1830: imperios que caen, naciones que nacen y máquinas de vapor
- [x] con-1808-es (Veo, 25-oct) · España entre 1808 y 1830: de la guerra de la Independencia a la Década Ominosa
- [x] con-1808-eu (Veo, 25-oct) · Europa entre 1808 y 1830: de Napoleón a la Restauración
- [x] con-1808-am (Veo, 25-oct) · América entre 1808 y 1830: las independencias
- [x] con-1808-om (Veo, 25-oct) · Oriente Medio y el norte de África entre 1808 y 1830: reformas desde arriba y presión de Europa
- [x] con-1808-as (Veo, 25-oct) · Asia y Oceanía entre 1808 y 1830: imperios cerrados, compañías comerciales y un volcán que enfrió el mundo
- [x] des-cadiz (Veo, 25-oct) · Las Cortes de Cádiz y la Constitución de 1812
- [x] des-trienio (Veo, 25-oct) · Riego y el Trienio Liberal (1820-1823)
- [x] des-rusia1812 (Veo, 25-oct) · La campaña de Rusia (1812)
- [x] des-bolivar (Veo, 25-oct) · Simón Bolívar y la Gran Colombia (1810-1830)
- [x] des-sanmartin (Veo, 25-oct) · San Martín y el cruce de los Andes (1812-1822)
- [x] des-mexico (Veo, 25-oct) · México: de Hidalgo a Iturbide (1810-1824)
- [x] des-guerraind (Veo, 25-oct) · La guerra de la Independencia: Bailén, los Sitios y la guerrilla (1808-1814)
- [x] des-grecia (Veo, 25-oct) · La guerra de independencia griega (1821-1830)
- [x] des-te-opio (Veo, 25-oct) · El té, el opio y el viaje secreto de las plantas de té (1757-1860)

- [x] con1-8 (Veo, 25-oct) · 
- [x] con1-10 (Veo, 25-oct) · 
- [x] con1-18 (Veo, 25-oct) · 
- [x] con1-9 (Veo, 25-oct) · 
- [x] con1-14 (Veo, 25-oct) · 
- [x] con1-19 (Gemini, 25-oct) · 
- [x] con1-11 (Veo, 25-oct) · 
- [x] con1-4 (Veo, 25-oct) · 
- [x] con1-15 (Veo, 25-oct) · 
- [x] con1-13 (Veo, 25-oct) · 
- [x] con1-17 (Veo, 25-oct) · 
- [x] con1-20 (Veo, 25-oct) · 
- [x] con1-16 (Veo, 25-oct) · 
- [x] con1-21 (Veo, 25-oct) · 
- [x] con1-7 (Veo, 25-oct) · 
- [x] des-cruz-roja (Veo, 25-oct) · La Cruz Roja de Ginebra
- [x] des-galapagos (Veo, 25-oct) · Las islas Galápagos
- [x] des-suez (Veo, 25-oct) · El canal de Suez
- [x] con2-1 (Veo, 25-oct) · 
- [x] con2-12 (Veo, 25-oct) · 
- [x] con2-0 (Veo, 25-oct) · 
- [x] con2-9 (Veo, 25-oct) · 
- [x] con2-10 (Veo, 25-oct) · 
- [x] con2-4 (Veo, 25-oct) · 
- [x] con2-3 (Veo, 25-oct) · 
- [x] con2-7 (Veo, 25-oct) · 
- [x] con2-5 (Veo, 25-oct) · 
- [x] con2-16 (Veo, 25-oct) · 
- [x] con2-2 (Veo, 25-oct) · 
- [x] con2-14 (Veo, 25-oct) · 
- [x] con2-17 (Veo, 25-oct) · 
- [x] con2-13 (Veo, 25-oct) · 
- [x] con2-15 (Veo, 25-oct) · 
- [x] con2-8 (Veo, 25-oct) · 
- [x] con2-18 (Veo, 25-oct) · 
- [x] con2-6 (Veo, 25-oct) · 
- [x] des-ellis-island (Veo, 25-oct) · Ellis Island
- [x] des-sagrada-familia (Veo, 25-oct) · La Sagrada Família
- [x] des-transiberiano (Veo, 25-oct) · El Transiberiano
- [x] con3-0 (Veo, 25-oct) · 
- [x] con3-10 (Veo, 25-oct) · 
- [x] con3-8 (Veo, 25-oct) · 
- [x] con3-1 (Veo, 25-oct) · 
- [x] con3-18 (Veo, 25-oct) · 
- [x] con3-9 (Veo, 25-oct) · 
- [x] con3-12 (Veo, 25-oct) · 
- [x] con3-4 (Veo, 25-oct) · 
- [x] con3-19 (Veo, 25-oct) · 
- [x] con3-2 (Veo, 25-oct) · 
- [x] con3-3 (Veo, 25-oct) · 
- [x] con3-13 (Veo, 25-oct) · 
- [x] con3-16 (Veo, 25-oct) · 
- [x] con3-17 (Gemini, 25-oct) · 
- [x] con3-14 (Veo, 25-oct) · 
- [x] con3-5 (Veo, 25-oct) · 
- [x] con3-15 (Veo, 25-oct) · 
- [x] con3-6 (Veo, 25-oct) · 
- [x] con3-7 (Veo, 25-oct) · 
- [x] des-auschwitz (Veo, 25-oct) · Auschwitz-Birkenau
- [x] des-guernica (Veo, 25-oct) · El Guernica
- [x] des-verdun (Veo, 25-oct) · Verdún
- [x] con4-0 (Gemini, 26-oct) · 
- [x] con4-10 (Veo, 25-oct) · 
- [x] con4-16 (Veo, 25-oct) · 
- [x] con4-4 (Veo, 25-oct) · 
- [x] con4-11 (Veo, 25-oct) · 
- [x] con4-5 (Veo, 25-oct) · 
- [x] con4-1 (Veo, 25-oct) · 
- [x] con4-2 (Veo, 25-oct) · 
- [x] con4-12 (Veo, 25-oct) · 
- [x] con4-15 (Veo, 25-oct) · 
- [x] con4-14 (Veo, 25-oct) · 
- [x] con4-17 (Gemini, 26-oct) · 
- [x] con4-3 (Veo, 25-oct) · 
- [x] con4-7 (Veo, 25-oct) · 
- [x] con4-13 (Veo, 25-oct) · 
- [x] con4-6 (Veo, 25-oct) · 
- [x] con4-19 (Veo, 25-oct) · 
- [x] con4-8 (Veo, 25-oct) · 
- [x] con4-9 (Veo, 25-oct) · 
- [x] des-chernobil (Veo, 25-oct) · Chernóbil
- [x] des-congreso-1978 (Veo, 25-oct) · El Congreso y la Constitución de 1978
- [x] des-onu (Veo, 25-oct) · La sede de la ONU en Nueva York
- [x] des-robben-island (Veo, 25-oct) · Robben Island
- [x] con5-7 (Veo, 25-oct) · 
- [x] con5-10 (Veo, 25-oct) · 
- [x] con5-8 (Veo, 25-oct) · 
- [x] con5-9 (Veo, 25-oct) · 
- [x] con5-1 (Veo, 25-oct) · 
- [x] con5-11 (Veo, 25-oct) · 
- [x] con5-12 (Veo, 25-oct) · 
- [x] con5-2 (Veo, 25-oct) · 
- [x] con5-16 (Veo, 25-oct) · 
- [x] con5-13 (Veo, 25-oct) · 
- [x] con5-15 (Veo, 25-oct) · 
- [x] con5-4 (Veo, 25-oct) · 
- [x] con5-14 (Veo, 25-oct) · 
- [x] con5-18 (Veo, 25-oct) · 
- [x] con5-3 (Veo, 25-oct) · 
- [x] con5-6 (Veo, 25-oct) · 
- [x] con5-5 (Gemini, 26-oct) · 
- [x] des-atocha-11m (Veo, 25-oct) · El memorial del 11-M en Atocha
- [x] des-cern (Veo, 25-oct) · El CERN y el bosón de Higgs
- [x] des-memorial-11s (Veo, 25-oct) · El Memorial del 11-S
- [x] des-srebrenica (Veo, 25-oct) · El memorial de Srebrenica-Potočari

## Hechos con Gemini

- [x] ant1-1 (Gemini Flash, 18-oct) · Egipto: el Imperio Antiguo y las pirámides
- [x] paleolitico-13 (Gemini Flash, 18-oct) · El arte de las cavernas
- [x] des-ishtar (Gemini Flash, 18-oct) · La puerta de Ishtar

- [x] ant1-8 (al final con Veo; el de Gemini también salió bien) · Sargón de Acad, el primer imperio
- [x] des-caral · Caral: una ciudad sin guerra (recortado a 5 s en ida y vuelta: Gemini arrastró el zigurat del vídeo anterior)
