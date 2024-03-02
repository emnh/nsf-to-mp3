#!/bin/bash
file=$1
songs=$(nosefart -i $file | fgrep "Number of Songs" | cut -f2 -d:)
echo $songs
out=output
mkdir -p $out cmds
bname=$(basename $file | sed 's/\.nsf$//')
touch $out/$bname.txt
for i in `seq 1 $songs`; do
  wav="$out/${bname}_$i.wav"
  echo wine ~/Downloads/nsfplay/nsfplay.exe \"$file\" \"$wav\" \"$i\" >> cmds/nsfplay_commands.txt
  echo ffmpeg -y -i \"$wav\" -c:a libopus -b:a 128k \"$out/${bname}_$i.opus\" >> cmds/ffmpeg_commands.txt
  #ffmpeg -i "$wav" "$out/${bname}_$i.mp3"
  #echo file "'"${bname}_$i.mp3"'" >> $out/$bname.txt
done
#ffmpeg -f concat -i $out/$bname.txt -c copy "done"/$bname.mp3

# Run this first
# time ( for file in *.nsf; do ~/data/devel/nsf-to-mp3/nsf_to_mp3.sh $file; done )
# Run this after
# N=12; time ( ( cat cmds/nsfplay_commands.txt | parallel -j $N eval ) && ( cat cmds/ffmpeg_commands.txt| parallel -j $N eval ) )
