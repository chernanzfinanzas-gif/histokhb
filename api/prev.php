<?php
// Vista previa de la Biblioteca: el código del autor puede ver revistas y libros antes de su fecha.
// Solo se guarda una huella bcrypt (lenta) del código; el acceso queda en la sesión del servidor.
ini_set('session.gc_maxlifetime', '2592000');
session_set_cookie_params(['lifetime' => 2592000, 'path' => '/', 'secure' => true, 'httponly' => true, 'samesite' => 'Lax']);
session_start();
header('Content-Type: application/json; charset=utf-8');
header('Cache-Control: private, no-store');
$huella = '$2y$12$dnQ1BaVLLNeTnDYKwfYgFeMOSFqTpfTgoMc4xBnsadQDmBLSEvH82';
$c = strtoupper(preg_replace('/[^A-Za-z0-9]/', '', (string)($_POST['codigo'] ?? $_GET['codigo'] ?? '')));
$ok = $c !== '' && strlen($c) <= 12 && password_verify($c, $huella);
if ($ok) { $_SESSION['hkprev'] = 1; session_regenerate_id(true); } else { unset($_SESSION['hkprev']); }
echo json_encode(['ok' => $ok]);
