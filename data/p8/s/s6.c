// P8-S6: Fibonacci recursive with explicit cases (matches ref2)
#include <stdio.h>
int fibonacci(int n) {
  if (n == 0)
    return 0;
  if (n == 1)
    return 1;
  return fibonacci(n - 1) + fibonacci(n - 2);
}
int main() {
  printf("Fib(7) = %d\n", fibonacci(7));
  return 0;
}
