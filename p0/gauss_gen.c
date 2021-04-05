#include<math.h>
#include<stdio.h>
#include<stdlib.h>
#include <time.h>
#include "gauss_gen.h"

float gauss(float x, float mu, float sg) {
    return (1 / (sqrt(2 * M_PI) * sg)) * exp((-1/(2 * pow(sg, 2))) * pow(x - mu, 2));
}

// Genera un numero aleatorio flotante en el rango dado.
float random_float(float a, float b) {
    float random = ((float) rand()) / (float) RAND_MAX;
    float diff = b - a;
    float r = random * diff;
    return a + r;
}

// Generamos N puntos con distribucion normal con centro MU y varianza SG.
void gauss_gen(int n, float mu, float sg) {
    
    float max_gauss = (1 / (sqrt(2 * M_PI) * sg));

    int i = 0;
    while(i < n){
        float x = random_float(mu - 5*sg, mu + 5*sg);
        float y = random_float(0, max_gauss);
        float fx = gauss(x, mu, sg);
        if(y < fx) {
            printf("%f, ",x);
            i++;   
        }
    }
}