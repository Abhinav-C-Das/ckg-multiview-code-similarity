// P6-S5: Factorial with do-while (matches ref2)
#include <stdio.h>
int factorial(int n) {
  if (n == 0)
    return 1;
  int result = 1;
  int i = 1;
  do {
    result *= i;
    i++;
  } while (i <= n);
  return result;
}
int main() {
  printf("5! = %d\n", factorial(5));
  return 0;
}
