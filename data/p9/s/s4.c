// P9-S4: GCD subtraction method (different algorithm)
#include <stdio.h>
int gcd(int a, int b) {
  while (a != b) {
    if (a > b)
      a = a - b;
    else
      b = b - a;
  }
  return a;
}
int main() {
  printf("GCD(48,18) = %d\n", gcd(48, 18));
  return 0;
}
