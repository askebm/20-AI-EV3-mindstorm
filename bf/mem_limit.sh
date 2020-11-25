#!/bin/zsh
while sleep 1; do 
	pid=$(ps aur | grep python | awk '{print $2}') && \
	[[ 70 -lt $(ps aur | grep python | head -n1 | awk '{print $4}') ]] && kill $pid
done
