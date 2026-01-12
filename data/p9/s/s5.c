// P9-S5: GCD recursive ternary (matches ref2)
#include <stdio.h>
int gcd(int a, int b) { return (b == 0) ? a : gcd(b, a % b); }
int main() {
  printf("GCD(48,18) = %d\n", gcd(48, 18));
  return 0;
}
