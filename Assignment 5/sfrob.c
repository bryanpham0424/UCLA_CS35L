#include <stdio.h>
#include <stdlib.h>

int frobcmp(char const* a, char const* b)
{
    while (*a != ' ' && *b != ' ')
    {
        if (*a == ' ') return -1;
        if (*b == ' ') return 1;

        char frobA = *a ^ 42;
        char frobB = *b ^ 42;

        if (frobA < frobB) return -1;
        if (frobA > frobB) return 1;

        a++;
        b++;
    }

    //if we finish the while loop w/o returning, then they're equal
    return 0;
}

int generalCmp(const void* a, const void* b)
{
    return frobcmp(*(const char**)a, *(const char**)b);
}

void checkForInputError()
{
    if (ferror(stdin) != 0)
    {
        fprintf(stderr, "Error reading input.");
        exit(1);
    }
}

void checkForOutputError()
{
    if (ferror(stdout) != 0)
    {
        fprintf(stderr, "Error writing output.");
        exit(1);
    }
}

int main(void)
{
    //the current word
    char* currentWord = (char*)malloc(sizeof(char));
    int currentLetterPosition = 0;

    //use a pointer to a pointer as an array of strings
    char** arrayOfWords = (char**)malloc(sizeof(char*));
    int currentWordPosition = 0;

    //get the current character from stdin
    char currentChar = getchar();

    checkForInputError();

    //check for leading spaces
    while (currentChar == ' ')
    {
        currentChar = getchar();
        checkForInputError();
    }

    //we also want to get the next one to check for extra spaces
    //or the end of the input
    char nextChar = getchar();

    checkForInputError();

    while (!feof(stdin))
    {
        int dontIncrementLetter = 0;

        currentWord[currentLetterPosition] = currentChar;

        char* wordWithMoreSpace = realloc(currentWord, (currentLetterPosition + 2) * sizeof(char));

        //error allocating memory
        if (wordWithMoreSpace == NULL)
        {
            free(currentWord);
            fprintf(stderr, "Error allocating memory.");
            exit(1);
        }
        else
        {
            currentWord = wordWithMoreSpace;
        }


        //if we've reached the end of the current word
        if (currentChar == ' ')
        {

            //add the current word to the array of words
            arrayOfWords[currentWordPosition] = currentWord;

            char** wordsWithMoreSpace = realloc(arrayOfWords, (currentWordPosition + 2) * sizeof(char*));

            //error allocating more memory
            if (wordsWithMoreSpace == NULL)
            {
                free(arrayOfWords);
                fprintf(stderr, "Error allocating more memory.");
                exit(1);
            }
            else
            {
                arrayOfWords = wordsWithMoreSpace;
                currentWordPosition++;

                //reset the currentWord
                currentLetterPosition = 0;
                dontIncrementLetter = 1;
                currentWord = NULL;
                currentWord = (char*)malloc(sizeof(char));
            }

            //treat multiple spaces like one
            if (nextChar == ' ')
            {
                while (nextChar == ' ')
                {
                    nextChar = getchar();
                    checkForInputError();
                }
            }
        }

        if (dontIncrementLetter == 0)
        {
            currentLetterPosition++;
        }

        currentChar = nextChar;

        nextChar = getchar();

        checkForInputError();
    }

    if (currentLetterPosition > 0 && currentWord[currentLetterPosition - 1] != ' ')
    {
        currentWord[currentLetterPosition] = currentChar;
        currentLetterPosition++;

        if (currentChar != ' ')
        {
            currentWord[currentLetterPosition] = ' ';
        }

        arrayOfWords[currentWordPosition] = currentWord;
        currentWordPosition++;
    }

    //function pointer to the general compare function
    int (*functionPtr) (const void*, const void*) = &generalCmp;

    //pass the function pointer as a parameter to qsort, and sort the words
    qsort(arrayOfWords, currentWordPosition, sizeof(char*), functionPtr);

    //output the words
    size_t i;
    for (i = 0; i < currentWordPosition; i++)
    {
        size_t j = 0;
        int alwaysTrue = 1;
        while (alwaysTrue == 1)
        {
            putchar(arrayOfWords[i][j]);
            checkForOutputError();
            if (arrayOfWords[i][j] == ' ')
            {
                break;
            }
            j++;
        }
    }

    //free all memory allocated
    size_t wordIndex;
    for (wordIndex = 0; wordIndex < currentWordPosition; wordIndex++)
    {
        free(arrayOfWords[wordIndex]);
    }

    free(arrayOfWords);
    return 0;
}





