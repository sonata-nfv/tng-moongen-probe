<?php
// required headers
header("Access-Control-Allow-Origin: *");
header("Content-Type: text/html; charset=UTF-8");
header("Access-Control-Allow-Methods: POST");
header("Access-Control-Max-Age: 3600");
header("Access-Control-Allow-Headers: Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With");


try {
$testvar = file_get_contents("php://input");
#$testvar = stream_get_contents(STDIN);
$varjson = json_decode($testvar, true);

file_put_contents('php://stderr', print_r("irthe to test", TRUE));
file_put_contents('php://stderr', print_r($testvar, TRUE));

if ($varjson["testType"]=="simple" || $varjson["testType"]=="rfc"){

$msg = $varjson["ingressIP"].":".$varjson["egressIP"].":".$varjson["testBandwidth"].":".$varjson["testTime"].":".$varjson["testID"].":".$varjson["placeholder1"].":".$varjson["placeholder2"].":".$varjson["testType"];

$sock = socket_create(AF_INET, SOCK_DGRAM, SOL_UDP);

$len = strlen($msg);

socket_sendto($sock, $msg, $len, 0, '172.16.1.18', 33333);

$msg = $varjson["ingressIP"].":".$varjson["egressIP"].":start";

$len = strlen($msg);

socket_sendto($sock, $msg, $len, 0, '10.100.33.2', 33338);

socket_close($sock);

echo "test started";

}else{

echo "unknown testType";

}


} catch (Exception $e) {
    echo "failed";
}

?>
