// P6-S6: Factorial with different init (matches ref1)
#include <stdio.h>
int factorial(int n) {
  int result = 1;
  for (int i = 2; i <= n; i++) { // Start from 2 since 1*1=1
    result *= i;
  }
  return result;
}
int main() {
  printf("5! = %d\n", factorial(5));
  return 0;
}
