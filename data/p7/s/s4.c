// P7-S4: Recursive with explicit return statement (matches ref1)
#include <stdio.h>
int factorial(int n) {
  if (n <= 1) {
    return 1;
  } else {
    int temp = factorial(n - 1);
    return n * temp;
  }
}
int main() {
  printf("5! = %d\n", factorial(5));
  return 0;
}
