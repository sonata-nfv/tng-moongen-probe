<?php

$tid = $_GET["tid"];
$ingressip = $_GET["ingressip"];
$egressip = $_GET["egressip"];



$filename = '/home/ubuntu/uperf/workloads/'.$tid.'.json';

if (file_exists($filename)) {


echo "done";

$sock = socket_create(AF_INET, SOCK_DGRAM, SOL_UDP);

$msg = $ingressip.":".$egressip.":stop";

$len = strlen($msg);

socket_sendto($sock, $msg, $len, 0, '10.100.33.2', 33338);

socket_close($sock);


} else {
    echo "not done";
}



?>
