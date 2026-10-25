<?php
// Cuenta vistas (y, en el futuro, "me gusta") de forma anónima, sin código de usuario,
// para poder sacar un ranking de "lo más leído" / "lo que más gusta".
//
// POST api/evento.php   cuerpo: {"ficha":"ant3-2","tipo":"vista"}

header('Content-Type: application/json; charset=utf-8');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');
if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') { exit; }
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['error' => 'Método no permitido']);
    exit;
}

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

$mysqli->query("CREATE TABLE IF NOT EXISTS eventos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ficha VARCHAR(80) NOT NULL,
    tipo VARCHAR(20) NOT NULL,
    fecha DATETIME NOT NULL,
    KEY ficha_tipo (ficha, tipo)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4");

$body = json_decode(file_get_contents('php://input'), true);
$ficha = isset($body['ficha']) ? substr(preg_replace('/[^a-zA-Z0-9_\-]/', '', (string) $body['ficha']), 0, 80) : '';
$tipo  = isset($body['tipo']) ? substr(preg_replace('/[^a-zA-Z0-9_\-]/', '', (string) $body['tipo']), 0, 20) : '';
if ($ficha === '' || $tipo === '') {
    http_response_code(400);
    echo json_encode(['error' => 'Faltan datos']);
    exit;
}

$stmt = $mysqli->prepare('INSERT INTO eventos (ficha, tipo, fecha) VALUES (?, ?, NOW())');
$stmt->bind_param('ss', $ficha, $tipo);
$stmt->execute();
echo json_encode(['ok' => true]);
