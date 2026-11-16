<?php
// Guarda y recupera el progreso de un usuario (fichas vistas, reto, favoritos,
// preferencias de color/fuente/tamaño...) identificado solo por su código personal.
// No hay contraseñas ni datos personales: el código es la única clave.
//
// GET  api/sync.php?codigo=XXXXXXX        -> devuelve el JSON guardado (o {} si no hay nada aún)
// POST api/sync.php?codigo=XXXXXXX        -> junta (y en «reto», además, junta los días)
//                                            junta el JSON recibido con lo guardado, POR CAMPOS DE PRIMER NIVEL:
//                                            los campos que llegan sustituyen a los guardados y el resto se conserva
//                                            (desde 15-nov-2026: así Viajes puede enviar solo {"cuadernos":…} sin borrar vistas, reto…)

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

function retoJunta($a, $b) {
    $o = array_merge($a, $b);
    $o['d'] = array_merge(is_array($a['d'] ?? null) ? $a['d'] : [], is_array($b['d'] ?? null) ? $b['d'] : []);
    foreach (['v', 'w'] as $t) {
        if (!isset($a[$t]) && !isset($b[$t])) continue;
        $o[$t] = [];
        foreach (['n', 'g', 'p'] as $c) {
            $x = is_array($a[$t][$c] ?? null) ? $a[$t][$c] : [];
            $y = is_array($b[$t][$c] ?? null) ? $b[$t][$c] : [];
            $o[$t][$c] = (object) array_merge($x, $y);   // claves de fecha: se conservan tal cual
        }
    }
    $o['best'] = max((int) ($a['best'] ?? 0), (int) ($b['best'] ?? 0));
    if ($o['d'] === []) $o['d'] = new stdClass();
    return $o;
}

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $cuerpo = file_get_contents('php://input');
    $json = json_decode($cuerpo, true);
    // tiene que ser un objeto {campo: valor}, no una lista
    if (!is_array($json) || ($json !== [] && array_keys($json) === range(0, count($json) - 1))) {
        http_response_code(400);
        echo json_encode(['error' => 'JSON no válido']);
        exit;
    }
    // Límite de tamaño sencillo para evitar abusos (600 KB: desde nov-2026 guarda también los textos en inglés,
    // ~110 KB al año de un alumno constante). Se mira lo recibido y, más abajo, el resultado ya juntado.
    $LIMITE = 600000;
    if (strlen($cuerpo) > $LIMITE) {
        http_response_code(413);
        echo json_encode(['error' => 'Demasiados datos']);
        exit;
    }
    // Leer lo guardado bloqueando la fila, para que dos envíos a la vez (web y Viajes) no se pisen.
    $mysqli->begin_transaction();
    $stmt = $mysqli->prepare('SELECT datos FROM usuarios WHERE codigo = ? FOR UPDATE');
    $stmt->bind_param('s', $codigo);
    $stmt->execute();
    $fila = $stmt->get_result()->fetch_assoc();
    $guardado = $fila ? json_decode($fila['datos'], true) : [];
    if (!is_array($guardado)) { $guardado = []; }
    // «reto»: se JUNTAN los días en vez de sustituirlos (igual que retoJunta() en la web), para que si
    // dos aparatos usan el mismo código, el que no jugó un día no borre ese día al enviar sus datos (16-nov-2026)
    if (isset($json['reto']) && is_array($json['reto']) && isset($guardado['reto']) && is_array($guardado['reto'])) {
        $json['reto'] = retoJunta($guardado['reto'], $json['reto']);
    }
    foreach ($json as $campo => $valor) { $guardado[$campo] = $valor; }   // solo los campos que llegan
    if (isset($guardado['reto']['d']) && $guardado['reto']['d'] === []) { $guardado['reto']['d'] = new stdClass(); }
    $datos = json_encode((object) $guardado, JSON_UNESCAPED_UNICODE);
    if (strlen($datos) > $LIMITE) {
        $mysqli->rollback();
        http_response_code(413);
        echo json_encode(['error' => 'Demasiados datos']);
        exit;
    }
    $stmt = $mysqli->prepare('INSERT INTO usuarios (codigo, datos, actualizado) VALUES (?, ?, NOW())
        ON DUPLICATE KEY UPDATE datos = VALUES(datos), actualizado = NOW()');
    $stmt->bind_param('ss', $codigo, $datos);
    $stmt->execute();
    $mysqli->commit();
    echo json_encode(['ok' => true]);
    exit;
}

http_response_code(405);
echo json_encode(['error' => 'Método no permitido']);
