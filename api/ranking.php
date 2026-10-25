<?php
// Devuelve las fichas más vistas (o con más "me gusta"), para hacerte una idea
// de qué funciona mejor. No requiere código de usuario.
//
// GET api/ranking.php?tipo=vista&limite=20

header('Content-Type: application/json; charset=utf-8');
header('Access-Control-Allow-Origin: *');

$cfgFile = __DIR__ . '/config.php';
if (!file_exists($cfgFile)) {
    http_response_code(500);
    echo json_encode(['error' => 'Falta configurar la base de datos (config.php)']);
    exit;
}
$cfg = require $cfgFile;

$mysqli = @new mysqli($cfg['host'], $cfg['usuario'], $cfg['contrasena'], $cfg['basedatos']);
if ($mysqli->connect_errno) {
    http_response_code(500);
    echo json_encode(['error' => 'No se pudo conectar a la base de datos']);
    exit;
}
$mysqli->set_charset('utf8mb4');

$tipo = preg_replace('/[^a-zA-Z0-9_\-]/', '', (string) ($_GET['tipo'] ?? 'vista'));
$limite = max(1, min(100, (int) ($_GET['limite'] ?? 20)));

$stmt = $mysqli->prepare('SELECT ficha, COUNT(*) AS n FROM eventos WHERE tipo = ? GROUP BY ficha ORDER BY n DESC LIMIT ?');
$stmt->bind_param('si', $tipo, $limite);
$stmt->execute();
$res = $stmt->get_result();
$out = [];
while ($fila = $res->fetch_assoc()) {
    $out[] = ['ficha' => $fila['ficha'], 'n' => (int) $fila['n']];
}
echo json_encode($out);
