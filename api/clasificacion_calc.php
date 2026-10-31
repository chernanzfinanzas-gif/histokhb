<?php
// Cálculo de la clasificación, separado para poder probarlo sin base de datos.
// Cada usuario trae «marcadores» {n|g|p: {pts, dia}}: un viaje por nivel (o el antiguo «marcador» {cat, pts, dia}).
function viajero(string $cod): string { return 'Viajero ' . str_pad((string) (crc32('hk-viajero-' . $cod) % 10000), 4, '0', STR_PAD_LEFT); }
function clasificacion(array $filas, string $codigo, string $hoy): array {
    $lista = ['n' => [], 'g' => [], 'p' => []];
    foreach ($filas as [$cod, $d]) {
        if (!is_array($d) || !empty($d['solo'])) continue;          // «Solo compito conmigo»: no aparece
        $ms = $d['marcadores'] ?? null;
        if (!is_array($ms) && is_array($d['marcador'] ?? null)) $ms = [($d['marcador']['cat'] ?? '') => $d['marcador']];
        if (!is_array($ms)) continue;
        $ap = trim((string) ($d['apodo'] ?? ''));
        $ap = $ap === '' ? viajero($cod) : mb_substr(preg_replace('/\s+/u', ' ', strip_tags($ap)), 0, 20);
        foreach ($ms as $cat => $m) {
            if (!isset($lista[$cat]) || !is_array($m)) continue;
            $pts = max(0, (int) ($m['pts'] ?? 0)); $dia = (string) ($m['dia'] ?? '');
            if ($cat !== 'n' && preg_match('/^\d{4}-\d{2}-\d{2}$/', $dia) && $dia < $hoy) {
                // días completos sin jugar desde el último reto de ese nivel (hoy aún se puede jugar); como mucho 7: luego se congela
                $sin = (int) round((strtotime($hoy) - strtotime($dia)) / 86400) - 1;
                $pts = max(0, $pts - min(7, max(0, $sin)));
            }
            $lista[$cat][] = [$ap, $pts, $cod];
        }
    }
    // apodos repetidos entre personas distintas: al segundo se le añade su número de viajero
    $dueno = [];
    foreach ($lista as $cat => $l) foreach ($l as $e) { $k = mb_strtolower($e[0]); if (!isset($dueno[$k])) $dueno[$k] = $e[2]; }
    $yo = [];
    foreach ($lista as $cat => &$l) {
        foreach ($l as &$e) if ($dueno[mb_strtolower($e[0])] !== $e[2]) $e[0] .= ' · ' . substr(viajero($e[2]), 8);
        unset($e);
        usort($l, fn($a, $b) => $b[1] <=> $a[1] ?: strcmp($a[0], $b[0]));
        foreach ($l as $i => $e) if ($codigo !== '' && $e[2] === $codigo) $yo[$cat] = $i + 1;
        $l = array_map(fn($e) => [$e[0], $e[1]], array_slice($l, 0, 100));
    }
    unset($l);
    return ['lista' => $lista, 'yo' => (object) $yo, 'apodos' => array_keys($dueno)];
}
