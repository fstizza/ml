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

	float diff = r2 - r1;

	return BW(r1, d, r2) || BW(r1 + 2 * diff, d, r2 + 2 * diff) || BW(r1 + 4 * diff, d, r2 + 4 * diff);
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
				printf("%f, %f, %s\n", x, y, "0");
				i++;
			}
		}
		else
		{
			if (i >= n / 2)
			{
				printf("%f, %f, %s\n", x, y, "1");
				i++;
			}
		}
	}
}
