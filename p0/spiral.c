#include "spiral.h"
#include "gauss_gen.h"
#include <stdio.h>
#include <math.h>

// Valor de la curva en al angulo dado.
#define RHO1(a) (float)(a / (4.0f * M_PI))
#define RHO2(a) (float)((a + M_PI) / (4.0f * M_PI))

#define BW(a, b, c) (a < b && b < c)

int rho(float t, float d)
{
	float r1 = RHO1(t);
	float r2 = RHO2(t);

	// Chequeamos que este en el primer periodo de las curvas.
	if(BW(r1, d, r2)) return 1;	
	float offset = (r2 - r1)*2;
	
	// Luego son todas paralelas con distancia offset.
	r1 += offset;
	r2 += offset;

	if(BW(r1, d, r2)) return 1;

	r1 += offset;
	r2 += offset;

	if(BW(r1, d, r2)) return 1;

	return 0;
}

void spiral(int n)
{
	int i = 0;
	while (i < n)
	{
		float x = random_float(-1, 1);
		float y = random_float(-1, 1);

		float t = atan2(y, x);
		float d = sqrt(pow(x, 2) + pow(y, 2));

		if (d > 1)
			continue;
		if (rho(t, d))
		{
			if (i < n / 2)
			{
				printf("%f,%f,%s\n", x, y, "0");
				i++;
			}
		}
		else
		{
			if (i >= n / 2)
			{
				printf("%f,%f,%s\n", x, y, "1");
				i++;
			}
		}
	}
}
