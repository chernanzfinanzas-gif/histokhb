<?php
// Aperturas de fichas, desarrollos, sincronías y sitios (las anota api/visita.php). Solo números.
// GET api/ranking.php                         -> las más abiertas (?limite=20, ?desde=AAAA-MM-DD, ?tipo=f|d|s|l)
// GET api/ranking.php?fichas=d:des-alaska,d:des-ayanz  -> esas, día a día
header('Content-Type: application/json; charset=utf-8');
header('Cache-Control: no-store');
header('Access-Control-Allow-Origin: *');
$cfgFile = __DIR__ . '/config.php';
if (!file_exists($cfgFile)) { http_response_code(500); echo json_encode(['error' => 'Falta config.php']); exit; }
$cfg = require $cfgFile;
$m = @new mysqli($cfg['host'], $cfg['usuario'], $cfg['contrasena'], $cfg['basedatos']);
if ($m->connect_errno) { http_response_code(500); echo json_encode(['error' => 'Sin base de datos']); exit; }
$m->set_charset('utf8mb4');
$hay = $m->query("SHOW TABLES LIKE 'visitas'");
if (!$hay || !$hay->num_rows) { echo json_encode(['aviso' => 'Aún no hay visitas anotadas']); exit; }
$desde = (string) ($_GET['desde'] ?? '');
if (!preg_match('/^\d{4}-\d{2}-\d{2}$/', $desde)) $desde = '2000-01-01';
$desdeE = $m->real_escape_string($desde);
$fichas = array_values(array_filter(array_map('trim', explode(',', (string) ($_GET['fichas'] ?? '')))));
if ($fichas) {
    $out = [];
    foreach (array_slice($fichas, 0, 30) as $f) {
        $fe = $m->real_escape_string($f);
        $res = $m->query("SELECT dia, n FROM visitas WHERE ficha = '$fe' AND dia >= '$desdeE' ORDER BY dia");
        $dias = []; $t = 0;
        while ($r = $res->fetch_assoc()) { $dias[$r['dia']] = (int) $r['n']; $t += (int) $r['n']; }
        $out[$f] = ['total' => $t, 'por_dia' => $dias];
    }
    echo json_encode($out, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE);
    exit;
}
$limite = max(1, min(200, (int) ($_GET['limite'] ?? 20)));
$tipo = preg_replace('/[^fdsl]/', '', (string) ($_GET['tipo'] ?? ''));
$filtro = $tipo !== '' ? " AND ficha LIKE '" . $tipo[0] . ":%'" : '';
$res = $m->query("SELECT ficha, SUM(n) AS n FROM visitas WHERE dia >= '$desdeE'$filtro GROUP BY ficha ORDER BY n DESC LIMIT $limite");
$out = [];
while ($r = $res->fetch_assoc()) $out[] = ['ficha' => $r['ficha'], 'n' => (int) $r['n']];
echo json_encode($out, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE);
