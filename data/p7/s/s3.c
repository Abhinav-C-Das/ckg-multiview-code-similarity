// P7-S3: Recursive with ternary (matches ref1)
#include <stdio.h>
int factorial(int n) { return (n <= 1) ? 1 : n * factorial(n - 1); }
int main() {
  printf("5! = %d\n", factorial(5));
  return 0;
}
