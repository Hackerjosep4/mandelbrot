<?php
header('Content-Type: application/json');

$imgDir = __DIR__ . '/img';
$result = [];
$totalMb = 0;
$total = 0;

if (is_dir($imgDir)) {
    foreach (scandir($imgDir) as $entry) {
        if ($entry === '.' || $entry === '..') continue;
        $path = $imgDir . '/' . $entry;
        if (is_dir($path)) {
            $count = count(glob($path . '/*.png'));
            $result[$entry] = $count;
            $total += $count;
            if ($entry !== 'julia') {
                $totalMb += $count;
            }
        }
    }
}

$result['total-mb'] = $totalMb;
$result['total'] = $total;

echo json_encode($result);