#!/bin/bash

for i in 2 4 8 16 32
do
	echo Running: diagonal_d${i}_c0.78_10000
	./knn diagonal_d${i}_c0.78_10000/diagonal_d${i}_c0.78_10000 > knn_d${i}_1.dt

	echo Running: $(pwd) 
	./knn parallel_d${i}_c0.78_10000/parallel_d${i}_c0.78_10000 > knn_p${i}_1.dt
done
