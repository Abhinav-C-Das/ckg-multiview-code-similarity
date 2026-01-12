// P10-S5: Prime with flag variable (matches ref2)
#include <stdio.h>
int isPrime(int n) {
  if (n <= 1)
    return 0;
  int prime = 1;
  for (int i = 2; i < n; i++) {
    if (n % i == 0) {
      prime = 0;
      break;
    }
  }
  return prime;
}
int main() {
  printf("Is 17 prime? %d\n", isPrime(17));
  return 0;
}
