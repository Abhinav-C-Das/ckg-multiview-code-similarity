// P7: Factorial Recursive - Ref1: Standard recursion
#include <stdio.h>
int factorial(int n) {
  if (n <= 1)
    return 1;
  return n * factorial(n - 1); // CES: ACCUMULATIVE recursion
}
int main() {
  printf("5! = %d\n", factorial(5));
  return 0;
}
