<?php

$tid = $_GET["tid"];
$ingressip = $_GET["ingressip"];
$egressip = $_GET["egressip"];



$filename = '/home/localadmin/MoonGen/'.$tid.'.json';

if (file_exists($filename)) {


$myfile = fopen($filename, "r") or die("not done:0:0:0");
// Output one line until end-of-filea

$json="";
while(!feof($myfile)) {
  $json = $json . fgets($myfile);
}
fclose($myfile);

$jsonIterator = new RecursiveIteratorIterator(
    new RecursiveArrayIterator(json_decode($json, TRUE)),
    RecursiveIteratorIterator::SELF_FIRST);

$sum_latency = 0;
$num_latency = 0;
$prevlatency = 0;

$sum_rx = 0;
$sum_tx = 0;


$flaggertxrx = 0;

foreach ($jsonIterator as $key => $val) {
    if(is_array($val)) {
        #echo "$key:\n\n\n";
	if ($key=="PktStatsRx"){
		if ($key!="0"){
			$flaggertxrx = 1;
		}
	}else if ($key=="PktStatsTx"){
		$flaggertxrx = 2;
	}
    } else {
        #echo "$key => $val\n";
        if ($key=="Latency"){
		$sum_latency = $sum_latency + $val;
		$prevlatency = $val;
	}
	if ($key=="NumberOfPackets"){
		$num_latency = $num_latency + (1*$val);
		$sum_latency = $sum_latency + ($val*$prevlatency)-$prevlatency;
	}
	if ($key=="TotalPackets"){
		if ($flaggertxrx==1){
			$sum_rx = $sum_rx + $val;
		}
		if ($flaggertxrx==2){
			$sum_tx = $sum_tx + $val;
		}
	}

    }
}

$avglatency = $sum_latency/$num_latency;
$avglatency = explode(".", $avglatency)[0];
if ($avglatency==""){
	$avglatency=0;
}

#echo $avglatency."\n";
#echo "TX: ". $sum_tx . " - RX: " . $sum_rx;

echo "done:".$avglatency.":".$sum_tx.":".$sum_rx;

$sock = socket_create(AF_INET, SOCK_DGRAM, SOL_UDP);

$msg = $ingressip.":".$egressip.":stop";

$len = strlen($msg);

socket_sendto($sock, $msg, $len, 0, '10.100.33.2', 33337);

socket_close($sock);


} else {
    echo "not done:0:0:0";
}



?>
