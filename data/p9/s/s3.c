// P9-S3: GCD iterative with modulo direct (matches ref1)
#include <stdio.h>
int gcd(int a, int b) {
  while (b != 0) {
    int remainder = a % b;
    a = b;
    b = remainder;
  }
  return a;
}
int main() {
  printf("GCD(48,18) = %d\n", gcd(48, 18));
  return 0;
}
