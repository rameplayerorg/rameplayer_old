<?php
//
// Copyright 2015 rameplayerorg
// Licensed under GPLv2, which you must read from the included LICENSE file.
//
// Main media player web client GUI.

header("Access-Control-Allow-Origin: *");

$config = parse_ini_file("/media/config/config.ini");
$slave_ip = $config['slave_ip'];
$slave_delay = $config['slave_delay'];
if("" == $slave_delay) {
	$slave_delay = 0;
}

$slave2_ip = $config['slave2_ip'];
$slave2_delay = $config['slave2_delay'];
if("" == $slave2_delay) {
        $slave2_delay = 0;
}



?>
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>RaMePlayer - prototype 1</title>
  <link rel="stylesheet" type="text/css" href="css/skel.css">

  <style type="text/css">
	body {
		font-family:Verdana,Geneva,Arial,Helvetica,sans-serif;
		font-size:10pt;
		background-color:#E0E0E0;
	}
	h1 {
		font-size:12pt;
	}
	#RaMePlayer_UI {
		width: 760px;
		margin-left: auto;
		margin-right: auto;
		margin-top: 5px;
		padding: 0;
	}
	#RaMeFace {
		width: 530px;
		height: 60px;
		margin: 0;
		padding: 65px 115px 65px 115px;
		background-image: url(images/mediaplayer_face.png);
		vertical-align: top;
		color: white;
	}
	#RaMeLeft {
		width: 20px;
		margin: 0;
		padding: 0;
		background-image: url(images/mediaplayer_left.png);
		background-repeat: repeat-y;
	}
	#RaMeContent {
		width: 680px;
		background-color: white;
		margin: 0;
		padding: 10px 20px 10px 20px;
		vertical-align: top;
	}
	#RaMeRight {
		width: 20px;
		margin: 0;
		padding: 0;
		background-image: url(images/mediaplayer_right.png);
		background-repeat: repeat-y;
	}
	#RaMeBottom {
		width: 760px;
		height: 20px;
		margin: 0;
		padding: 0;
		background-image: url(images/mediaplayer_bottom.png);
	}
	#RaMeInfo {
		width: 750px;
		height: 20px;
		margin: 0;
		padding: 5px;
		text-align: center;
	}
	#status {
		float: left;
		width: 215px;
		height: 60px;
		margin: 0;
		padding: 0;
	}
	#controls {
		float: left;
		width: 250px;
		height: 30px;
		margin: 10px 10px 10px 40px;
		padding: 0;
		text-align: center;
	}
	input[type="button"] {
		-moz-appearance: none;
		-webkit-appearance: none;
		-o-appearance: none;
		-ms-appearance: none;
		appearance: none;
		-moz-transition: background-color 0.2s ease-in-out;
		-webkit-transition: background-color 0.2s ease-in-out;
		-o-transition: background-color 0.2s ease-in-out;
		-ms-transition: background-color 0.2s ease-in-out;
		transition: background-color 0.2s ease-in-out;
		background: #666666;
		border-radius: 10px;
		border: 0;
		color: white;
		cursor: pointer;
		display: inline-block;
		padding: 0.80em 1em;
		text-align: center;
		text-decoration: none;
		font-size: 1em;
		font-weight: 600;
		min-width: 5em;
	}
		.greenbutton:hover {
			background-color: #339933;
		}
		.redbutton:hover {
			background-color: #993333;
		}
	.clicked {
		background: #0000FF;
		color: white;
	}
  </style>
  <script>

var xmlhttp_status;
var xmlhttp;
var xmlhttp_slave;
var xmlhttp_slave2;

var mediatype="";
var last_status="";

var slave_ip="<?php echo $slave_ip; ?>";
var slave_delay=<?php echo $slave_delay; ?>;

var slave2_ip="<?php echo $slave2_ip; ?>";
var slave2_delay=<?php echo $slave2_delay; ?>;


function slave_callback() {

        if (xmlhttp.readyState==4 && xmlhttp.status==200){
                //alert(xmlhttp.responseText);
	}
}

function doServerCall(url, cfunc, delay) {

	//alert(url);

	loadXMLDoc(url,cfunc);
	if("" != slave_ip){
		slave_url="http://"+slave_ip+"/"+url;
		setTimeout(function(){ loadXMLDoc_slave(slave_url, slave_callback); }, delay);
//		alert(slave_url);
	}
        if("" != slave2_ip){
                slave_url="http://"+slave2_ip+"/"+url;
                setTimeout(function(){ loadXMLDoc_slave2(slave2_url, slave_callback); }, delay);
//              alert(slave_url);
        }
}


function loadXMLDoc_slave(url,cfunc)
{
if (window.XMLHttpRequest)
  {// code for IE7+, Firefox, Chrome, Opera, Safari
  xmlhttp_slave=new XMLHttpRequest();
  }
else
  {// code for IE6, IE5
  xmlhttp_slave=new ActiveXObject("Microsoft.XMLHTTP");
  }

xmlhttp_slave.onreadystatechange=cfunc;
xmlhttp_slave.open("GET",url,true);
xmlhttp_slave.send();
}


function loadXMLDoc_slave2(url,cfunc)
{
if (window.XMLHttpRequest)
  {// code for IE7+, Firefox, Chrome, Opera, Safari
  xmlhttp_slave2=new XMLHttpRequest();
  }
else
  {// code for IE6, IE5
  xmlhttp_slave2=new ActiveXObject("Microsoft.XMLHTTP");
  }

xmlhttp_slave2.onreadystatechange=cfunc;
xmlhttp_slave2.open("GET",url,true);
xmlhttp_slave2.send();
}


function loadXMLDoc(url,cfunc)
{
if (window.XMLHttpRequest)
  {// code for IE7+, Firefox, Chrome, Opera, Safari
  xmlhttp=new XMLHttpRequest();
  }
else
  {// code for IE6, IE5
  xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
  }

xmlhttp.onreadystatechange=cfunc;
xmlhttp.open("GET",url,true);
xmlhttp.send();
//document.getElementById("myDiv").innerHTML=xmlhttp.responseText;
}


function getStatus()
{
if (window.XMLHttpRequest)
  {// code for IE7+, Firefox, Chrome, Opera, Safari
  xmlhttp_status=new XMLHttpRequest();
  }

xmlhttp_status.onreadystatechange=status_callback;
xmlhttp_status.open("GET","command.php?action=status",true);
xmlhttp_status.send();
}



function play_callback() {

	if (xmlhttp.readyState==4 && xmlhttp.status==200){
		response = xmlhttp.responseText;
		//alert(response);
		//document.getElementById("myDiv").innerHTML = response;
	}
}

function status_callback() {

        if (xmlhttp_status.readyState==4 && xmlhttp_status.status==200){
                response = xmlhttp_status.responseText;
                //alert(response);

		if(last_status != response) {
			if("playing" == response) {
	                	document.getElementById("myDiv").innerHTML = "Playing media";
			}

                        if("stopped" == response) {
                                document.getElementById("myDiv").innerHTML = "Media stopped";
                        }
                        if("paused" == response) {
                                document.getElementById("myDiv").innerHTML = "Media paused";
                        }


			last_status = response;
		}
        }
}



function play_video(filename){
	doServerCall('command.php?action=play&filename=/media/data/'+filename, play_callback, slave_delay )
}


function stop_video(){
 	document.getElementById("myDiv").innerHTML = "Stopping media";
	doServerCall('command.php?action=stop', play_callback, 0 );
}



function select_mediafile(mediafile, mediatype){
	document.getElementById("myDiv").innerHTML = "Selected:<br>" + mediafile;
	document.getElementById("selected_media").value = mediafile;
}


function play_button() {

	var mediafile = document.getElementById("selected_media").value;
	var mediafiletype = document.getElementById("selected_media_type").value;

	if(""==mediafile) {
		alert("Select mediafile first");
	}
	if("playing"==last_status){
		document.getElementById("myDiv").innerHTML = "Pausing media";
	}
	if("paused"==last_status){
                document.getElementById("myDiv").innerHTML = "Playing media";
        }

	play_video(mediafile);
}

setInterval(getStatus, 1000);


</script>
</head>

<body>
<table id="RaMePlayer_UI" width="760" height="800" border="0" cellpadding="0" cellspacing="0">
	<tr>
		<td colspan="3" id="RaMeFace">

<!-- ---------------- status text start ---------------- -->
		<div id="status">
<!-- ---------------- status text end ---------------- -->
			<div id="myDiv"></div>
		</div>
<!-- ---------------- control buttons start ---------------- -->
		<div id="controls">

			<input type="hidden" id="selected_media" value="">
			<input type="hidden" id="selected_media_type" value="">

			<input type="Button" id="btn_stop" onclick="stop_video()"   value="Stop" class="redbutton">
			<input type="Button" id="btn_play" onclick="play_button()"  value="Play" class="greenbutton">
		</div>
<!-- ---------------- control buttons end ---------------- -->
		</td>
	</tr>
	<tr>
		<td id="RaMeLeft">&nbsp;</td>
		<td id="RaMeContent">
<div class="container">
<div class="row">
<section class="12u">
<H1>Choose media file from USB-stick:</H1>
</section>
</div>
<div class="row">
<!-- ---------------- file list start ---------------- -->

<section class="6u">
<?php
$dir    = '/media/data';
$files1 = scandir($dir);

asort($files1);
$counter =1;

foreach( $files1 as $key=>$value){
	if(1==strlen($counter)) {
		$str_counter = "0".$counter.": ";
	} else {
		$str_counter = $counter.": ";
	}

	if("."==$value | ".."==$value | "background.jpg"==$value){
		continue;
	}
	if(strpos($value, ".mp4") || strpos($value, ".mp3") ){
		echo "<div onclick=\"select_mediafile('".$value."','video')\">". $str_counter.$value."</div>";
		$counter = $counter + 1;
	}
	if(25==$counter) {
		echo "</section><section class=\"6u\">";
	}
}
?>
</section>

<!-- ---------------- file list end ---------------- -->

</div>
</div>
		</td>
		<td id="RaMeRight">&nbsp;</td>
	</tr>
	<tr>
		<td colspan="3" id="RaMeBottom">&nbsp;</td>
	</tr>
	<tr>
<!-- ---------------- player info start ---------------- -->
		<td colspan="3" id="RaMeInfo">
		What ever additional info we need to display goes here...
		</td>
<!-- ---------------- player info end ---------------- -->
	</tr>
</table>

</body>
</html>
