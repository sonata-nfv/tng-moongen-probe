<?php
// required headers
header("Access-Control-Allow-Origin: *");
header("Content-Type: text/html; charset=UTF-8");
header("Access-Control-Allow-Methods: POST");
header("Access-Control-Max-Age: 3600");
header("Access-Control-Allow-Headers: Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With");

// get database connection
// include_once '../config/database.php';

// instantiate product object
// include_once '../objects/product.php';

// $database = new Database();
// $db = $database->getConnection();

// $product = new Product($db);

// get posted data

try {
$testvar = file_get_contents("php://input");
#$testvar = stream_get_contents(STDIN);
$varjson = json_decode($testvar, true);

file_put_contents('php://stderr', print_r("irthe to test", TRUE));
file_put_contents('php://stderr', print_r($testvar, TRUE));

if ($varjson["testType"]=="simple" || $varjson["testType"]=="rfc"){

$msg = $varjson["ingressIP"].":".$varjson["egressIP"].":".$varjson["testBandwidth"].":".$varjson["testTime"].":".$varjson["testID"].":".$varjson["moongenOutput"].":".$varjson["moongenInput"].":".$varjson["testType"];

$sock = socket_create(AF_INET, SOCK_DGRAM, SOL_UDP);

$len = strlen($msg);

socket_sendto($sock, $msg, $len, 0, '10.30.0.253', 33333);

$msg = $varjson["ingressIP"].":".$varjson["egressIP"].":start";

$len = strlen($msg);

socket_sendto($sock, $msg, $len, 0, '10.100.33.2', 33337);

socket_close($sock);

echo "test started";

}else{

echo "unknown testType";

}


} catch (Exception $e) {
    echo "failed";
}

?>
