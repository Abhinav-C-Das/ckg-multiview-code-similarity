// P6: Factorial Iterative - Ref1: Standard loop
#include <stdio.h>
int factorial(int n) {
  int result = 1;
  for (int i = 1; i <= n; i++) {
    result *= i; // CES: ACCUMULATIVE (multiplication)
  }
  return result;
}
int main() {
  printf("5! = %d\n", factorial(5));
  return 0;
}
