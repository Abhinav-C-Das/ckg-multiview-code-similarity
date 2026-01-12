// P9: GCD Euclidean - Ref2: Recursive
#include <stdio.h>
int gcd(int a, int b) {
  if (b == 0)
    return a;
  return gcd(b, a % b);
}
int main() {
  printf("GCD(48,18) = %d\n", gcd(48, 18));
  return 0;
}
