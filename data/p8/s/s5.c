// P8-S5: Fibonacci with while loop (matches ref1)
#include <stdio.h>
int fibonacci(int n) {
  if (n <= 1)
    return n;
  int a = 0, b = 1;
  int i = 2;
  while (i <= n) {
    int temp = a + b;
    a = b;
    b = temp;
    i++;
  }
  return b;
}
int main() {
  printf("Fib(7) = %d\n", fibonacci(7));
  return 0;
}
