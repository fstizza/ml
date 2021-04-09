#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include "gauss_gen.h"
#include "spiral.h"
#include <math.h>
#include <getopt.h>
#include <ctype.h>

int is_float(char *s)
{
	int len;
	float ignore;
	int ret = sscanf(s, "%f %n", &ignore, &len);
	return ret == 1 && !s[len];
}

int is_int(char *s)
{
	int len;
	int ignore;
	int ret = sscanf(s, "%d %n", &ignore, &len);
	return ret == 1 && !s[len];
}

void usage()
{
	printf("USAGE: \n");
	printf("[-h] print this help.\n");
	printf("[-m a|b|c] set generator mode, a: diagonal, b: corners, c: spiral.\n");
	printf("[-n SIZE] set output size.\n");
	printf("[-d INPUTS] set input size.\n");
	printf("[-c DEV] set deviation.\n");
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

	while ((o = getopt(argc, argv, "phm:n:d:c:")) != -1)
	{
		switch (o)
		{

		case 'm':
			if (strlen(optarg) != 1 || !isalpha(optarg[0]))
			{
				printf("Argument error: -m requires only an alphabetic character.\n");
				return -1;
			}
			m = optarg[0];
			break;
		case 'n':
			if (!is_int(optarg))
			{
				printf("Argument type error: integer is expected. \n");
				return -1;
			}
			n = atoi(optarg);
			break;
		case 'd':
			if (!is_int(optarg))
			{
				printf("Argument type error: integer is expected. \n");
				return -1;
			}
			d = atoi(optarg);
			break;
		case 'c':
			if (!is_float(optarg))
			{
				printf("Argument type error: floating point is expected. \n");
				return -1;
			}
			c = atof(optarg);
			break;
		case 'h':
			usage();
			return 0;
		
		case 'p':
			break;

		default:
			printf("Argument error: -%c is not a valid option.\n", optopt);
			return -1;
			break;
		}
	}

	switch (m)
	{
	case 'a':
		diagonal(n, d, c * sqrt(d));
		break;

	case 'b':
		corners(n, d, c);
		break;

	case 'c':
		spiral(n);
		break;

	default:
		printf("Error: %c is not a valid dataset generator mode.\n", m);
		return 1;
	}

	return 0;
}
