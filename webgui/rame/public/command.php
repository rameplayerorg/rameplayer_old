<?php 
//
// Copyright 2015 rameplayerorg
// Licensed under GPLv2, which you must read from the included LICENSE file.
//
// php socket gateway

if(!($sock = socket_create(AF_UNIX, SOCK_STREAM, 0)))
{
	$errorcode = socket_last_error();
    $errormsg = socket_strerror($errorcode);

    die("Couldn't create socket: [$errorcode] $errormsg \n");
}

#echo "Socket created \n";

//Connect socket to remote server
if(!socket_connect($sock , '/tmp/rameplayer' , 80))
{
	$errorcode = socket_last_error();
    $errormsg = socket_strerror($errorcode);

    die("Could not connect: [$errorcode] $errormsg \n");
}

#echo "Connection established \n";

$action = $_GET["action"];
$filename = $_GET["filename"];

$message = "ramecmd_".$action." ".$filename;

//Send the message to the server
if( ! socket_send ( $sock , $message , strlen($message) , 0))
{
	$errorcode = socket_last_error();
    $errormsg = socket_strerror($errorcode);

    die("Could not send data: [$errorcode] $errormsg \n");
}

#echo "Message send successfully \n";
if("status" == $action) {
	$result = socket_read ( $sock, 100);
	echo $result;
}
?>
