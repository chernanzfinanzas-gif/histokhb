<?php
// Clasificación del «Viaje por la historia» (reto del día), por categoría: n (Niños), g (General), p (Profundo).
// Solo aparecen quienes han elegido un apodo; los códigos no se devuelven nunca.
//
// GET api/clasificacion.php[?codigo=XXXX]  ->  {"lista":{"g":[["apodo",puntos],...],...}, "yo":{"cat":"g","pos":3}}
//
// Cada móvil guarda en su copia de usuarios.datos un «marcador» {cat, pts, dia}: los puntos a la fecha de su último
// reto. Aquí se descuenta 1 punto por cada día sin jugar desde entonces (General y Profundo; en Niños nunca se resta).

header('Content-Type: application/json; charset=utf-8');
header('Access-Control-Allow-Origin: *');
header('Cache-Control: no-store');

$cfgFile = __DIR__ . '/config.php';
if (!file_exists($cfgFile)) { http_response_code(500); echo json_encode(['error' => 'Falta config.php']); exit; }
$cfg = require $cfgFile;
$mysqli = @new mysqli($cfg['host'], $cfg['usuario'], $cfg['contrasena'], $cfg['basedatos']);
if ($mysqli->connect_errno) { http_response_code(500); echo json_encode(['error' => 'Sin base de datos']); exit; }
$mysqli->set_charset('utf8mb4');

require __DIR__ . '/clasificacion_calc.php';

$filas = [];
$res = $mysqli->query("SELECT codigo, datos FROM usuarios");
while ($res && ($f = $res->fetch_assoc())) { $filas[] = [$f['codigo'], json_decode($f['datos'], true)]; }
$codigo = strtoupper(preg_replace('/[^A-Za-z0-9]/', '', (string) ($_GET['codigo'] ?? '')));
echo json_encode(clasificacion($filas, $codigo, date('Y-m-d')), JSON_UNESCAPED_UNICODE);
