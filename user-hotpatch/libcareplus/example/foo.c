// foo.c                                                                        
#include <stdio.h>
#include <time.h>

void print_hello(void)
{
    printf("Hello world!\n");
}

int main(void)
{
    while (1) {
        print_hello();
        sleep(1);
    }
}

