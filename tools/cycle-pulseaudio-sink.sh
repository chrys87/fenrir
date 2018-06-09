#!/bin/bash

sinks=(`pacmd list-sinks | sed -n -e 's/\**[[:space:]]index:[[:space:]]\([[:digit:]]\)/\1/p'`)
sinks_count=${#sinks[@]}
active_sink_index=`pacmd list-sinks | sed -n -e 's/\*[[:space:]]index:[[:space:]]\([[:digit:]]\)/\1/p'`
newSink=${sinks[0]}
ord=0

while [ $ord -lt $sinks_count ];
do
	echo ${sinks[$ord]}
	if [ ${sinks[$ord]} -gt $active_sink_index ] ; then
		newSink=${sinks[$ord]}
		break
	fi
	let ord++
done

pactl list short sink-inputs|while read stream; do
	streamId=$(echo $stream|cut '-d ' -f1)
	echo "moving stream $streamId"
	pactl move-sink-input "$streamId" "$newSink"
done
pacmd set-default-sink "$newSink"

#https://unix.stackexchange.com/questions/65246/change-pulseaudio-input-output-from-shell
