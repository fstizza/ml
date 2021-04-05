#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <time.h>
#include "gauss_gen.h"
#include <getopt.h>

void diagonal(int n, int d, float c)
{
	n = n / 2;
	c = sqrt(c);

	for (int i = 0; i < n; i++)
	{
		gauss_gen(d, 1.0, c);
		printf("%s \n", "0");
	}
	for (int i = 0; i < n; i++)
	{
		gauss_gen(d, -1.0, c);
		printf("%s \n", "1");
	}
}

void extremos(int n, int d, float c)
{
	n = n / 2;
	for (int i = 0; i < n; i++)
	{
		gauss_gen(1, 1.0, c);
		gauss_gen(d - 1, 0.0, c);
		printf("%s \n", "0");
	}
	for (int i = 0; i < n; i++)
	{
		gauss_gen(1, -1.0, c);
		gauss_gen(d - 1, 0.0, c);
		printf("%s \n", "1");
	}
}

int inside_circle(float x, float y, float cx, float cy, float r)
{
	return sqrt(pow(x - cx, 2) + pow(y - cy, 2)) < pow(r, 2) ? 1 : 0;
}

int rho(float x, float y)
{
	float angle = atan2(y, x);
	float ro_i = angle / (4 * M_PI);
	float ro_f = (angle + M_PI) / (4 * M_PI);
	float d = sqrt(pow(x, 2) + pow(y, 2));

	return (ro_i < d && ro_f > d) ||
				   (ro_i + 0.5 < d && ro_f + 0.5 > d) ||
				   (ro_i + 1.0 < d && ro_f + 1.0 > d)
			   ? 1
			   : 0;
}

void espiral(int n)
{
	float cx = 0.0f, cy = 0.0f, r = 1.0f; // Origen y radio del circulo.
	n = n / 2;
	int i = 0, j = 0;
	while (i < n || j < n)
	{
		float x = random_float(-1, 1);
		float y = random_float(-1, 1);

		if (inside_circle(x, y, cx, cy, r))
		{
			if (rho(x, y) && i < n)
			{
				printf("%f, %f, %s\n", x, y, "0");
				i++;
			}
			else if (j < n)
			{
				printf("%f, %f, %s\n", x, y, "1");
				j++;
			}
		}
	}
}

int main(int argc, char **argv)
{
	// Default values.
	int n = 200, d = 2;
	float c = 0.75f;
	char m = 'a';

	srand(time(NULL));

	opterr = 0;
	int o;

	while ((o = getopt(argc, argv, "m:n:d:c:")) != -1)
	{
		switch (o)
		{
		case 'm':
			m = optarg[0];
			break;
		case 'n':
			n = atoi(optarg);
			break;
		case 'd':
			d = atoi(optarg);
			break;
		case 'c':
			c = atof(optarg);
			break;

		default:
			break;
		}
	}

	for (int index = optind; index < argc; index++)
		printf("Non-option argument %s\n", argv[index]);

	if(opterr){
		printf("USAGE: \n");
		return 1;
	}


	switch (m)
	{
	case 'a':
		diagonal(n, d, c * sqrt(d));
		break;

	case 'b':
		extremos(n, d, c);
		break;

	case 'c':
		espiral(n);
		break;

	default:
		printf("Invalid option.");
		return 1;
	}

	return 0;
}