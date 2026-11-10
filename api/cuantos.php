<?php
// Cuántos códigos hay guardados (solo números, ningún código ni dato de nadie).
// Cada aparato que entra en la app recibe un código; se guarda aquí la primera vez que hace algo
// (ver una ficha, jugar al reto, hacer inglés...). GET api/cuantos.php
header('Content-Type: application/json; charset=utf-8');
header('Cache-Control: no-store');
$cfgFile = __DIR__ . '/config.php';
if (!file_exists($cfgFile)) { http_response_code(500); echo json_encode(['error' => 'Falta config.php']); exit; }
$cfg = require $cfgFile;
$m = @new mysqli($cfg['host'], $cfg['usuario'], $cfg['contrasena'], $cfg['basedatos']);
if ($m->connect_errno) { http_response_code(500); echo json_encode(['error' => 'Sin base de datos']); exit; }
$m->set_charset('utf8mb4');
$n = fn($sql) => (int)($m->query($sql)->fetch_row()[0] ?? 0);
echo json_encode([
  'codigos' => $n("SELECT COUNT(*) FROM usuarios WHERE codigo <> 'CIACTIONS'"),
  'activos_7_dias' => $n("SELECT COUNT(*) FROM usuarios WHERE codigo <> 'CIACTIONS' AND actualizado >= NOW() - INTERVAL 7 DAY"),
  'activos_30_dias' => $n("SELECT COUNT(*) FROM usuarios WHERE codigo <> 'CIACTIONS' AND actualizado >= NOW() - INTERVAL 30 DAY"),
  'con_ingles' => $n("SELECT COUNT(*) FROM usuarios WHERE JSON_LENGTH(JSON_EXTRACT(datos, '$.ingles.p')) > 0"),
  'hoy' => $n("SELECT COUNT(*) FROM usuarios WHERE codigo <> 'CIACTIONS' AND DATE(actualizado) = CURDATE()"),
], JSON_PRETTY_PRINT);
