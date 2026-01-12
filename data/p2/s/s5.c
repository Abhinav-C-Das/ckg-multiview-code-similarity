// P2-S5: Nested ternary (matches ref2)
#include <stdio.h>
int maximum(int a[], int n) {
  int max = a[0];
  int i = 1;
  while (i < n) {
    max = a[i] > max ? a[i] : max;
    i++;
  }
  return max;
}
int main() {
  int arr[] = {12, 45, 23, 67, 34, 89, 21};
  printf("Max = %d\n", maximum(arr, 7));
  return 0;
}
