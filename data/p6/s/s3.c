// P6-S3: Factorial with explicit multiplication (matches ref1)
#include <stdio.h>
int factorial(int n) {
  int fact = 1;
  for (int i = 1; i <= n; i++) {
    fact = fact * i; // Explicit multiplication instead of *=
  }
  return fact;
}
int main() {
  printf("5! = %d\n", factorial(5));
  return 0;
}
