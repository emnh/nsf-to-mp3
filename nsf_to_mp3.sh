#!/bin/bash
file=$1
songs=$(nosefart -i $file | fgrep "Number of Songs" | cut -f2 -d:)
echo $songs
out=output
mkdir -p $out
bname=$(basename $file | sed 's/\.nsf$//')
touch $out/$bname.txt
for i in `seq 1 $songs`; do
  wav="$out/${bname}_$i.wav"
  wine ~/Downloads/nsfplay/nsfplay.exe "$file" "$wav" "$i"
  #ffmpeg -i "$wav" "$out/${bname}_$i.mp3"
  ffmpeg -y -i "$wav" -c:a libopus -b:a 128k "$out/${bname}_$i.opus"
  echo file "'"${bname}_$i.mp3"'" >> $out/$bname.txt
done
#ffmpeg -f concat -i $out/$bname.txt -c copy "done"/$bname.mp3
