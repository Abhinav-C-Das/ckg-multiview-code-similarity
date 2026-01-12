// P10: Prime Check - Ref1: Standard loop
#include <stdio.h>
int isPrime(int n) {
  if (n <= 1)
    return 0;
  for (int i = 2; i * i <= n; i++) {
    if (n % i == 0)
      return 0;
  }
  return 1;
}
int main() {
  printf("Is 17 prime? %d\n", isPrime(17));
  return 0;
}
