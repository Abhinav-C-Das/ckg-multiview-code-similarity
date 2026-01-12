// P10-S6: Prime while loop (matches ref1)
#include <stdio.h>
int isPrime(int n) {
  if (n <= 1)
    return 0;
  int i = 2;
  while (i * i <= n) {
    if (n % i == 0)
      return 0;
    i++;
  }
  return 1;
}
int main() {
  printf("Is 17 prime? %d\n", isPrime(17));
  return 0;
}
