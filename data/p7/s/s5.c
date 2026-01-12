// P7-S5: Recursive with different comparison (matches ref2)
#include <stdio.h>
int factorial(int n) {
  if (n < 2)
    return 1;
  return n * factorial(n - 1);
}
int main() {
  printf("5! = %d\n", factorial(5));
  return 0;
}
