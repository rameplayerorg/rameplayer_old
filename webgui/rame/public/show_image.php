<?php
//
// Copyright 2015 rameplayerorg
// Licensed under GPLv2, which you must read from the included LICENSE file.
//
// Shows's image 
$filename = $_GET["filename"];

echo exec('/home/pi/show_image.sh /media/data/'.$filename);

echo "Displaying image: ".$filename;
exec('sudo /home/pi/lcdi2c -i -b 1 -x 0 -y 0 "Displaying image"');
?>
