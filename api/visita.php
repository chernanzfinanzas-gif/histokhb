<?php
// Cuenta aperturas por día: qué ficha, desarrollo, sincronía o sitio se abrió y qué día. Nada del usuario.
// POST api/visita.php  {"k":"d:des-estrella-tumba"}
header('Content-Type: application/json; charset=utf-8');
header('Cache-Control: no-store');
if ($_SERVER['REQUEST_METHOD'] !== 'POST') { http_response_code(405); echo '{}'; exit; }
$cfgFile = __DIR__ . '/config.php';
if (!file_exists($cfgFile)) { http_response_code(500); echo json_encode(['error' => 'Falta config.php']); exit; }
$cfg = require $cfgFile;
$m = @new mysqli($cfg['host'], $cfg['usuario'], $cfg['contrasena'], $cfg['basedatos']);
if ($m->connect_errno) { http_response_code(500); echo json_encode(['error' => 'Sin base de datos']); exit; }
$m->set_charset('utf8mb4');
$b = json_decode(file_get_contents('php://input'), true);
$k = is_array($b) ? trim(preg_replace('/[\x00-\x1F\x7F"\'<>\\\\]/u', '', (string) ($b['k'] ?? ''))) : '';
if (!preg_match('/^[fdslv]:.+/u', $k) || mb_strlen($k) > 150) { http_response_code(400); echo json_encode(['error' => 'Dato no válido']); exit; }
$m->query("CREATE TABLE IF NOT EXISTS visitas (
    ficha VARCHAR(160) NOT NULL,
    dia DATE NOT NULL,
    n INT NOT NULL DEFAULT 0,
    PRIMARY KEY (ficha, dia)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4");
$st = $m->prepare('INSERT INTO visitas (ficha, dia, n) VALUES (?, CURDATE(), 1) ON DUPLICATE KEY UPDATE n = n + 1');
$st->bind_param('s', $k);
$st->execute();
echo '{"ok":true}';
