// P8-S3: Fibonacci iterative with different swap (matches ref1)
#include <stdio.h>
int fibonacci(int n) {
  if (n <= 1)
    return n;
  int prev = 0, curr = 1;
  for (int i = 2; i <= n; i++) {
    int next = prev + curr;
    prev = curr;
    curr = next;
  }
  return curr;
}
int main() {
  printf("Fib(7) = %d\n", fibonacci(7));
  return 0;
}
