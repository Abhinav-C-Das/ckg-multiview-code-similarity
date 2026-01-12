// P8-S4: Fibonacci with array (matches ref1 conceptually)
#include <stdio.h>
int fibonacci(int n) {
  if (n <= 1)
    return n;
  int fib[100];
  fib[0] = 0;
  fib[1] = 1;
  for (int i = 2; i <= n; i++) {
    fib[i] = fib[i - 1] + fib[i - 2];
  }
  return fib[n];
}
int main() {
  printf("Fib(7) = %d\n", fibonacci(7));
  return 0;
}
