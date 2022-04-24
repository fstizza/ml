#!/bin/bash

for i in 2 4 8 16 32 ; do
	cd ./diagonal_d${i}_c0.78_10000
	echo Running diagonal d${i}.
	for i in 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 ; do
		cd 250_${i}
		echo Running: $(pwd)
		../../../bp diagonal_d${i}_c0.78_10000 &
		cd ../		
	done 
	cd ../
done


