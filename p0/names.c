#include<getopt.h>

void usage() {
    printf("C4.5 Dataset format. USAGE: \n");
    printf("[-c NAME]             - Add a continous variable. \n");
    printf("[-dn NAME | n]        - Add a discrete variable with integer which indicates how many values the attribute can take. \n");
    printf("[-dv NAME | v1,v2,v3] - Add a discrete variable with a list values the attribute can take. \n");
    printf("[-i NAME]             - Add a variable that will be ignored. \n");
}

int main(int argc, char** argv) {

  int c;

  opterr = 0;

  while ((c = getopt (argc, argv, "c:dn:dv:i:")) != -1)
    switch (c)
      {
      case 'c':
        aflag = 1;
        break;
      case 'dn':
        bflag = 1;
        break;
      case 'dv':
        cvalue = optarg;
        break;
      case 'i':
        if (optopt == 'c')
          fprintf (stderr, "Option -%c requires an argument.\n", optopt);
        else if (isprint (optopt))
          fprintf (stderr, "Unknown option `-%c'.\n", optopt);
        else
          fprintf (stderr,
                   "Unknown option character `\\x%x'.\n",
                   optopt);
        return 1;
      default:
        abort ();
      }

       printf ("aflag = %d, bflag = %d, cvalue = %s\n",
          aflag, bflag, cvalue);

  for (index = optind; index < argc; index++)
    printf ("Non-option argument %s\n", argv[index]);
  return 0;



}

