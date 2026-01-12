// P7: Factorial Recursive - Ref2: Explicit base case
#include <stdio.h>
int factorial(int n) {
  if (n == 0)
    return 1;
  if (n == 1)
    return 1;
  return n * factorial(n - 1);
}
int main() {
  printf("5! = %d\n", factorial(5));
  return 0;
}
