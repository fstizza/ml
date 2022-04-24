#!/bin/bash

for i in 2 4 8 16 32
do

	echo Running: diagonal_d${i}_c0.78_10000
	python3 get_min_val.py diagonal_d${i}_c0.78_10000



	echo Running: $(pwd)
	python3 get_min_val.py parallel_d${i}_c0.78_10000

done
