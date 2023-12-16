<?php
include dirname(__DIR__) .'/vendor/autoload.php';

$input = getopt("i:", [], $id);

use itbdw\Ip\IpLocation;

$ip = isset($_GET['ip']) ? $_GET['ip'] : $_SERVER['REMOTE_ADDR'];
$ip = trim(explode(',', $ip)[0]);
header('Content-Type: application/json;charset=utf-8');
header('Access-Control-Allow-Origin: *');
$response = array(
    'code' => 0,
    'data' => IpLocation::getLocation($ip)
);
if ($response['data']['error']) {
    $response['code'] = 400;
}
echo json_encode($response, JSON_UNESCAPED_UNICODE) . "\n";
