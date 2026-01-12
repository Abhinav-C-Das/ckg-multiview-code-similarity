// P9-S6: GCD iterative inline swap (matches ref1)
#include <stdio.h>
int gcd(int a, int b) {
  int temp;
  while (b) {
    temp = b;
    b = a % b;
    a = temp;
  }
  return a;
}
int main() {
  printf("GCD(48,18) = %d\n", gcd(48, 18));
  return 0;
}
