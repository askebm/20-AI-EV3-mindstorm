#!/bin/bash
for level in ../levels/*; do
	echo $level >> results.txt
	{ time python bf.py $level ; } &>> results.txt
	echo $? >> results.txt
done
	
