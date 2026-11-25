<?php
// Sirve los ficheros de una revista o libro de la Biblioteca antes de su fecha de salida,
// solo a quien tiene la vista previa abierta (api/prev.php). Después de la fecha, el .htaccess
// de cada carpeta deja de mandar aquí y los ficheros se sirven directamente.
ini_set('session.gc_maxlifetime', '2592000');
session_set_cookie_params(['lifetime' => 2592000, 'path' => '/', 'secure' => true, 'httponly' => true, 'samesite' => 'Lax']);
session_start();
header('Cache-Control: private, no-store');
if (empty($_SESSION['hkprev'])) { http_response_code(403); header('Content-Type: text/plain; charset=utf-8'); echo "Todavía no se ha publicado. Sale pronto en la Biblioteca de Historia Total."; exit; }
$base = realpath(__DIR__ . '/../biblioteca');
$f = (string)($_GET['f'] ?? '');
if ($f === '' || substr($f, -1) === '/') $f .= 'index.html';
$ruta = realpath($base . '/' . $f);
if ($ruta === false || strpos($ruta, $base . DIRECTORY_SEPARATOR) !== 0 || !is_file($ruta) || basename($ruta)[0] === '.') { http_response_code(404); exit; }
$tipos = ['html' => 'text/html; charset=utf-8', 'webp' => 'image/webp', 'jpg' => 'image/jpeg', 'png' => 'image/png', 'mp3' => 'audio/mpeg', 'pdf' => 'application/pdf', 'epub' => 'application/epub+zip', 'json' => 'application/json', 'css' => 'text/css', 'js' => 'text/javascript'];
$ext = strtolower(pathinfo($ruta, PATHINFO_EXTENSION));
header('Content-Type: ' . ($tipos[$ext] ?? 'application/octet-stream'));
header('Accept-Ranges: bytes');
$tam = filesize($ruta); $ini = 0; $fin = $tam - 1;
if (isset($_SERVER['HTTP_RANGE']) && preg_match('/bytes=(\d*)-(\d*)/', $_SERVER['HTTP_RANGE'], $m)) {
  if ($m[1] === '' && $m[2] !== '') { $ini = max(0, $tam - (int)$m[2]); } else { $ini = (int)$m[1]; if ($m[2] !== '') $fin = min($fin, (int)$m[2]); }
  if ($ini > $fin || $ini >= $tam) { http_response_code(416); header("Content-Range: bytes */$tam"); exit; }
  http_response_code(206); header("Content-Range: bytes $ini-$fin/$tam");
}
header('Content-Length: ' . ($fin - $ini + 1));
$fp = fopen($ruta, 'rb'); fseek($fp, $ini); $q = $fin - $ini + 1;
while ($q > 0 && !feof($fp)) { $b = fread($fp, min(65536, $q)); echo $b; $q -= strlen($b); flush(); }
fclose($fp);
