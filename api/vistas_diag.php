<?php
// TEMPORAL (18-nov-2026): cuánta gente ha visto unos desarrollos. Solo números, ningún código ni apodo.
// «Vista» = el usuario pulsó «Ya la he visto» o escuchó el audio casi entero (hk_vistas).
// GET api/vistas_diag.php?fichas=des-estrella-tumba,des-alaska&desde=2026-11-14
header('Content-Type: application/json; charset=utf-8');
header('Cache-Control: no-store');
$cfgFile = __DIR__ . '/config.php';
if (!file_exists($cfgFile)) { http_response_code(500); echo json_encode(['error' => 'Falta config.php']); exit; }
$cfg = require $cfgFile;
$m = @new mysqli($cfg['host'], $cfg['usuario'], $cfg['contrasena'], $cfg['basedatos']);
if ($m->connect_errno) { http_response_code(500); echo json_encode(['error' => 'Sin base de datos']); exit; }
$m->set_charset('utf8mb4');
$fichas = array_values(array_filter(array_map(fn($x) => preg_replace('/[^a-z0-9\-]/', '', strtolower(trim($x))),
    explode(',', (string) ($_GET['fichas'] ?? '')))));
if (!$fichas || count($fichas) > 30) { echo json_encode(['error' => 'Pon ?fichas=a,b,c (máximo 30)']); exit; }
$desde = (string) ($_GET['desde'] ?? '');
if (!preg_match('/^\d{4}-\d{2}-\d{2}$/', $desde)) $desde = '2000-01-01';
$out = [];
foreach ($fichas as $f) $out[$f] = ['vista' => 0, 'vista_y_activo_desde' => 0, 'favorita' => 0, 'ultima_abierta' => 0];
$total = 0; $activos = 0;
$res = $m->query("SELECT datos, actualizado FROM usuarios WHERE codigo <> 'CIACTIONS'");
while ($r = $res->fetch_assoc()) {
    $d = json_decode($r['datos'], true);
    if (!is_array($d)) continue;
    $total++;
    $act = substr((string) $r['actualizado'], 0, 10) >= $desde;
    if ($act) $activos++;
    $v = is_array($d['vistas'] ?? null) ? $d['vistas'] : [];
    $fa = is_array($d['favs'] ?? null) ? $d['favs'] : [];
    $ul = (string) ($d['ultima'] ?? '');
    foreach ($fichas as $f) {
        if (in_array($f, $v, true)) { $out[$f]['vista']++; if ($act) $out[$f]['vista_y_activo_desde']++; }
        if (in_array($f, $fa, true)) $out[$f]['favorita']++;
        if ($ul === $f) $out[$f]['ultima_abierta']++;
    }
}
echo json_encode(['hora_servidor' => date('Y-m-d H:i:s'), 'usuarios' => $total, 'activos_desde' => [$desde => $activos],
    'fichas' => $out], JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE);
