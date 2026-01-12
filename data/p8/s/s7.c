// P8-S7: Fibonacci with XOR swap (matches ref1)
#include <stdio.h>
int fibonacci(int n) {
  if (n <= 1)
    return n;
  int a = 0, b = 1;
  for (int i = 2; i <= n; i++) {
    b = a + b;
    a = b - a; // Clever swap without temp
  }
  return b;
}
int main() {
  printf("Fib(7) = %d\n", fibonacci(7));
  return 0;
}
