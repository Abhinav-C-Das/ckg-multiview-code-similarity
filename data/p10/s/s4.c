// P10-S4: Prime with explicit 2 check (matches ref1)
#include <stdio.h>
int isPrime(int n) {
  if (n <= 1)
    return 0;
  if (n == 2)
    return 1;
  if (n % 2 == 0)
    return 0;
  for (int i = 3; i * i <= n; i += 2) {
    if (n % i == 0)
      return 0;
  }
  return 1;
}
int main() {
  printf("Is 17 prime? %d\n", isPrime(17));
  return 0;
}
