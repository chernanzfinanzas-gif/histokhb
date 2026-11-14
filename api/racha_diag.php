<?php
// TEMPORAL (14-nov-2026): diagnóstico de la racha del reto para un apodo. Se quita en cuanto se resuelva.
// Solo devuelve fechas del reto; nunca el código del usuario.
// GET api/racha_diag.php?apodo=bruja
header('Content-Type: application/json; charset=utf-8');
header('Cache-Control: no-store');
$cfgFile = __DIR__ . '/config.php';
if (!file_exists($cfgFile)) { http_response_code(500); echo json_encode(['error' => 'Falta config.php']); exit; }
$cfg = require $cfgFile;
$m = @new mysqli($cfg['host'], $cfg['usuario'], $cfg['contrasena'], $cfg['basedatos']);
if ($m->connect_errno) { http_response_code(500); echo json_encode(['error' => 'Sin base de datos']); exit; }
$m->set_charset('utf8mb4');
$ap = mb_strtolower(trim((string) ($_GET['apodo'] ?? '')));
if ($ap === '') { echo json_encode(['error' => 'Falta ?apodo=']); exit; }
$res = $m->query("SELECT datos, actualizado FROM usuarios WHERE codigo <> 'CIACTIONS'");
$out = [];
$i = 0;
while ($f = $res->fetch_assoc()) {
    $d = json_decode($f['datos'], true);
    if (!is_array($d)) continue;
    $a = mb_strtolower(trim((string) ($d['apodo'] ?? '')));
    if ($a === '' || mb_strpos($a, $ap) === false) continue;
    $r = is_array($d['reto'] ?? null) ? $d['reto'] : [];
    $dias = [];
    foreach (($r['d'] ?? []) as $k => $v) if ($k >= '2026-10-20') $dias[$k] = $v;
    ksort($dias);
    $w = [];
    foreach (($r['w'] ?? []) as $c => $l) if (is_array($l)) { $x = array_filter($l, fn($k) => $k >= '2026-10-20', ARRAY_FILTER_USE_KEY); ksort($x); $w[$c] = $x; }
    $out[] = ['usuario' => ++$i, 'apodo' => $d['apodo'], 'ultima_sincronizacion' => $f['actualizado'],
              'dias_reto' => $dias, 'por_nivel' => $w, 'mejor_racha' => $r['best'] ?? null,
              'marcadores' => $d['marcadores'] ?? null];
}
echo json_encode(['hora_servidor' => date('Y-m-d H:i:s'), 'coincidencias' => $out], JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE);
