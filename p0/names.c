#include <getopt.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define MAX_VAR_LENGTH 30
#define MAX_NUM_LENGTH 10
#define SEP ':'

void usage()
{
  printf("C4.5 Dataset format. USAGE: \n");
  printf("C=class1,class2      - Output classes, comma separated.\n");
  printf("[-c NAME]             - Add a continuous input. \n");
  printf("[-n NAME:n]           - Add a discrete input with integer which indicates how many values the attribute can take. \n");
  printf("[-v NAME:v1,v2,v3]    - Add a discrete input with a list values the attribute can take. \n");
  printf("[-i NAME]             - Add a input that will be ignored. \n");
}

int index_of(char c, char *str)
{
  for (unsigned short i = 1; i < strlen(str); i++)
    if (str[i - 1] == c)
      return i;

  return -1;
}

int main(int argc, char **argv)
{
  int c;
  opterr = 0;

  if (argc < 3 || argv[1] == NULL || strncmp(argv[1], "C=", 2))
  {
    printf("C=class1,class2,... argument is REQUIRED. \n");
    return -1;
  }

  printf("%s.\n", argv[1]);

  argc--;
  argv++;

  while ((c = getopt(argc, argv, "c:n:v:i:")) != -1)
    switch (c)
    {
    case 'c':
      printf("%s: continuous.\n", optarg);
      break;
    case 'n':
    {
      int idx = index_of(SEP, optarg);
      if (idx > 1)
      {
        char name[idx];
        char integer[MAX_NUM_LENGTH];
        strncpy(name, optarg, idx - 1);
        name[idx - 1] = '\0';
        strncpy(integer, optarg + idx, strlen(optarg));
        printf("%s: discrete %s.\n", name, integer);
      }
      else
      {
        printf("Invalid format.\n");
        abort();
      }
      break;
    }
    case 'v':
    {
      int idx = index_of(SEP, optarg);
      if (idx > 1)
      {
        char name[idx];
        strncpy(name, optarg, idx - 1);
        name[idx - 1] = '\0';
        printf("%s: discrete %s.\n", name, optarg + idx);
      }
      else
      {
        printf("Invalid format.\n");
        return -1;
      }
      break;
    }

    case 'i':
    {
      printf("%s: ignore.\n", optarg);
      break;
    }
    default:
      return -1;
    }

  for (int index = optind; index < argc; index++)
    printf("Non-option argument %s\n", argv[index]);

  if (opterr)
    return -1;

  return 0;
}
