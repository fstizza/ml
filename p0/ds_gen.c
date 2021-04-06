#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include "gauss_gen.h"
#include "spiral.h"
#include <math.h>
#include <getopt.h>

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

	if (opterr)
	{
		printf("USAGE: \n");
		return 1;
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
		printf("Invalid option.");
		return 1;
	}

	return 0;
}