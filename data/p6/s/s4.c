// P6-S4: Factorial backward loop (matches ref1)
#include <stdio.h>
int factorial(int n) {
  int result = 1;
  for (int i = n; i >= 1; i--) {
    result *= i; // Backward multiplication
  }
  return result;
}
int main() {
  printf("5! = %d\n", factorial(5));
  return 0;
}
