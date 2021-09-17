// bar.c                                                                                   
#include <stdio.h>
#include <time.h>

void print_hello(void)
{
    printf("Hello world %s!\n", "being patched");
}

int main(void)
{
    while (1) {
        print_hello();
        sleep(1);
    }
}

