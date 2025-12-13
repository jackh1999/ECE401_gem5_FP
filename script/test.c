#include <stdio.h>

int main() {
    // Simple arithmetic to exercise the pipeline
    volatile int a = 10;
    volatile int b = 20;
    volatile int c = a + b;
    
    printf("test from RV32I Pipeline! Result: %d\n", c);
    return 0;
}