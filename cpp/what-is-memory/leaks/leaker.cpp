#include <stdio.h>
#include <stdlib.h>

#include <cstdio>

int main(void) {
    char *p = (char *)malloc(12);
    printf("%ld",sizeof(p));
    p = 0;  // the leak is here
    printf("Hello, leak!\n");
    return 0;
}
