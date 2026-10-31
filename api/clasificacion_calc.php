<?php
// Cálculo de la clasificación, separado para poder probarlo sin base de datos.
function clasificacion(array $filas, string $codigo, string $hoy): array {
    $lista = ['n' => [], 'g' => [], 'p' => []];
    $mio = null;
    foreach ($filas as [$cod, $d]) {
        if (!is_array($d)) continue;
        $ap = trim((string) ($d['apodo'] ?? ''));
        $m = $d['marcador'] ?? null;
        if (!is_array($m) || !isset($lista[$m['cat'] ?? ''])) continue;
        // sin apodo: «Viajero 4821», número fijo sacado del código que no permite adivinarlo
        if ($ap === '') $ap = 'Viajero ' . str_pad((string) (crc32('hk-viajero-' . $cod) % 10000), 4, '0', STR_PAD_LEFT);
        $cat = $m['cat']; $pts = max(0, (int) ($m['pts'] ?? 0));
        $dia = (string) ($m['dia'] ?? '');
        if ($cat !== 'n' && preg_match('/^\d{4}-\d{2}-\d{2}$/', $dia) && $dia < $hoy) {
            // días completos sin jugar después del último reto (hoy aún se puede jugar: no cuenta)
            $sin = (int) ((strtotime($hoy) - strtotime($dia)) / 86400) - 1;
            $pts = max(0, $pts - max(0, $sin));
        }
        $ap = mb_substr(preg_replace('/\s+/u', ' ', strip_tags($ap)), 0, 20);
        $lista[$cat][] = [$ap, $pts, $cod];
    }
    // apodos repetidos (por si dos móviles lo guardaron a la vez): al segundo se le añade su número de viajero
    $vistos = [];
    foreach ($lista as &$l0) foreach ($l0 as &$e0) {
        $k = mb_strtolower($e0[0]);
        if (isset($vistos[$k]) && $vistos[$k] !== $e0[2]) $e0[0] .= ' · ' . str_pad((string) (crc32('hk-viajero-' . $e0[2]) % 10000), 4, '0', STR_PAD_LEFT);
        else $vistos[$k] = $e0[2];
    }
    unset($l0, $e0);
    $yo = null;
    foreach ($lista as $cat => &$l) {
        usort($l, fn($a, $b) => $b[1] <=> $a[1] ?: strcmp($a[0], $b[0]));
        foreach ($l as $i => $e) if ($codigo !== '' && $e[2] === $codigo) $yo = ['cat' => $cat, 'pos' => $i + 1];
        $l = array_map(fn($e) => [$e[0], $e[1]], array_slice($l, 0, 100));
    }
    // ¿está libre un apodo? (?apodo=…)  — para avisar al elegirlo
    return ['lista' => $lista, 'yo' => $yo, 'apodos' => array_keys($vistos)];
}
