#include "spiral.h"
#include "gauss_gen.h"
#include <stdio.h>
#include <math.h>

// Valor de la curva en al angulo dado.
#define RHO1(a) (float)(a / (4.0f * M_PI))
#define RHO2(a) (float)((a + M_PI) / (4.0f * M_PI))

int rho(float t, float d)
{
	if (
		(RHO1(t) <= d && d <= RHO2(t)) ||
		(RHO1(t) + 0.5 <= d && d < RHO2(t) + 0.5) ||
		(RHO1(t) + 1.0 < d && d <= RHO2(t) + 1.0))
		return 1;
	else
		return 0;
}

void spiral(int n)
{
	n = n / 2;
	int i = 0;
	while (i < n)
	{
		float x = random_float(-1, 1);
		float y = random_float(-1, 1);

		float t = atan2(y, x);
		float d = sqrt(pow(x, 2) + pow(y, 2));

		if (d > 1) continue;
		if (rho(t, d) && i < n)
		{
			printf("%f, %f, %s\n", x, y, "0");
			printf("%f, %f, %s\n", x * -1, y * -1, "1");
			i++;
		}
	}
}