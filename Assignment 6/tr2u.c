#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>

void checkInputErr(ssize_t result)
{
  if (result == -1)
  {
    fprintf(stderr, "Error: character cannot be read in.");
    exit(1);
  }
}
void checkOutputErr(ssize_t result)
{
  if (result == -1)
  {
    fprintf(stderr, "Error: character cannot be written.");
    exit(1);
  }
}

void transliterate(char* from, char* to)
{
  // check that from and to are of equal lengths
  if (strlen(from) != strlen(to))
  {
    fprintf(stderr, "Error: Transliteration sets must be of the same length.");
    exit(1);
  }
  // check that from has no duplicates
  size_t length = strlen(from);
  for (size_t i=0; i<length; i++)
  {
    for (size_t j=i+1; j<length; j++)
    {
      if (from[i] == from[j])
        {
          fprintf(stderr, "Error: From set cannot contain duplicates.");
          exit(1);
        }
    }
  }    
  
  ssize_t c; 
  ssize_t d; 
  char inp[1]; 
  c = read(0, inp, 1);
  while (c != 0) 
  {
    checkInputErr(c);
    for (size_t i=0; i<length; ++i)
    {
      if (from[i] == (*inp)) 
      {
        (*inp) = (to[i]); 
        break;
      }
    }
    d = write(1, inp, 1);
    checkOutputErr(d);
    c = read(0, inp, 1);
  }
  return;
}

int main(int argc, char** argv)
{
  if (argc != 3)
  {
    fprintf(stderr, "Error: Please provide two sets of characters and input from standard input.");
    exit(1);
  }
  transliterate(argv[1], argv[2]);
  exit(0);
}
