#!/bin/bash

for i in 2 4 8 16 32
do
	cd ./diagonal_d${i}_c0.78_10000
	echo Running: $(pwd)
	./nb diagonal_d${i}_c0.78_10000 > ../nb/$i/diagonal.dt
	cd ../

	cd ./parallel_d${i}_c0.78_10000
	echo Running: $(pwd)
	./nb parallel_d${i}_c0.78_10000 > ../nb/$i/parallel.dt
	cd ../
done
