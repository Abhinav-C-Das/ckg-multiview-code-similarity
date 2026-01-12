// P6: Factorial Iterative - Ref2: While loop
#include <stdio.h>
int factorial(int n) {
  int result = 1;
  int i = 1;
  while (i <= n) {
    result *= i;
    i++;
  }
  return result;
}
int main() {
  printf("5! = %d\n", factorial(5));
  return 0;
}
