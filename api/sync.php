<?php
// Guarda y recupera el progreso de un usuario (fichas vistas, reto, favoritos,
// preferencias de color/fuente/tamaño...) identificado solo por su código personal.
// No hay contraseñas ni datos personales: el código es la única clave.
//
// GET  api/sync.php?codigo=XXXXXXX        -> devuelve el JSON guardado (o {} si no hay nada aún)
// POST api/sync.php?codigo=XXXXXXX        -> guarda el JSON recibido en el cuerpo de la petición (lo sustituye entero)

header('Content-Type: application/json; charset=utf-8');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');
if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') { exit; }

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

// Crea la tabla sola la primera vez; no hace falta tocar phpMyAdmin.
$mysqli->query("CREATE TABLE IF NOT EXISTS usuarios (
    codigo VARCHAR(12) NOT NULL PRIMARY KEY,
    datos JSON NOT NULL,
    actualizado DATETIME NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4");

$codigo = $_GET['codigo'] ?? ($_POST['codigo'] ?? '');
$codigo = strtoupper(preg_replace('/[^A-Za-z0-9]/', '', (string) $codigo));
if ($codigo === '' || strlen($codigo) > 12) {
    http_response_code(400);
    echo json_encode(['error' => 'Código no válido']);
    exit;
}

if ($_SERVER['REQUEST_METHOD'] === 'GET') {
    $stmt = $mysqli->prepare('SELECT datos FROM usuarios WHERE codigo = ?');
    $stmt->bind_param('s', $codigo);
    $stmt->execute();
    $fila = $stmt->get_result()->fetch_assoc();
    echo $fila ? $fila['datos'] : '{}';
    exit;
}

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $cuerpo = file_get_contents('php://input');
    $json = json_decode($cuerpo, true);
    if (!is_array($json)) {
        http_response_code(400);
        echo json_encode(['error' => 'JSON no válido']);
        exit;
    }
    // Límite de tamaño sencillo para evitar abusos (200 KB sobra de sobra para esto).
    if (strlen($cuerpo) > 200000) {
        http_response_code(413);
        echo json_encode(['error' => 'Demasiados datos']);
        exit;
    }
    $datos = json_encode($json, JSON_UNESCAPED_UNICODE);
    $stmt = $mysqli->prepare('INSERT INTO usuarios (codigo, datos, actualizado) VALUES (?, ?, NOW())
        ON DUPLICATE KEY UPDATE datos = VALUES(datos), actualizado = NOW()');
    $stmt->bind_param('ss', $codigo, $datos);
    $stmt->execute();
    echo json_encode(['ok' => true]);
    exit;
}

http_response_code(405);
echo json_encode(['error' => 'Método no permitido']);
