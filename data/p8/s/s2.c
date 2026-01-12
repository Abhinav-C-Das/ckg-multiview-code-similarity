// P8-S2: Fibonacci recursive (matches ref2)
#include <stdio.h>
int fibonacci(int n) {
  if (n <= 1)
    return n;
  return fibonacci(n - 1) + fibonacci(n - 2);
}
int main() {
  printf("Fib(7) = %d\n", fibonacci(7));
  return 0;
}
