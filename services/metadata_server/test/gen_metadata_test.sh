#!/bin/bash
#
# Copyright 2015 rameplayerorg
# Licensed under GPLv2, which you must read from the included LICENSE file.
#
#
# NOTES:
#
# We would more likely want to use ffprobe, but it didn't seem to be
# available as ready-made package for Raspbian for now.
#
# After looking around info about avprobe, it looks like it doesn't
# support listing chapters. This is not immediately needed but probably
# needs to be resolved in the future.
#
# Here are some ideas to resolve that:
# A) Find ffprobe package, or compile from sources.
#    After that one can use -show_chapter parameter with it.
# B) Save metadata (including chapters) as ffmetadata with ffmpeg:
#      ffmpeg -i filename -f ffmetadata meta_out.txt
#    Then make script which parses that output and writes out JSON.
#


METADATA_PATH=/tmp/media_metadata
MEDIA_PATH=/media/data

COMBO_ARRAY_FILE=$METADATA_PATH/toc.json
COMBO_ARRAY_JSON_ELEM='"toc"'


AVPROBE=`which avprobe`
if [ ! -x $AVPROBE ]; then
	echo "Error: Can't find avprobe"
	exit
fi

mkdir -p $METADATA_PATH
if [ ! -d $METADATA_PATH -o ! -w $METADATA_PATH ]; then
	echo "Error: Can't write to $METADATA_PATH"
	exit
fi

# remove potential previous version of combo array file first
rm "$COMBO_ARRAY_FILE"

# start of json doc & array to combo array file
echo "{ $COMBO_ARRAY_JSON_ELEM: [" >> $COMBO_ARRAY_FILE

iter=0
for f in $MEDIA_PATH/*; do
	if [ ! -r "$f" ]; then
		echo "Warning - can't read: $f";
	fi

	# print first json array delimiter (except on first entry)
	if [ "$iter" -gt 0 ]; then
		echo "," >> $COMBO_ARRAY_FILE
	fi
	iter=$(($iter+1))

	# save file specific metadata
	METADATA_FILE="$METADATA_PATH/$(basename "$f").json"
	$AVPROBE -show_format -of json "$f" > "$METADATA_FILE"
	# copy contents also to the combo array file
	cat "$METADATA_FILE" >> $COMBO_ARRAY_FILE
done

# end of json array & doc to combo array file
echo ']}' >> $COMBO_ARRAY_FILE
