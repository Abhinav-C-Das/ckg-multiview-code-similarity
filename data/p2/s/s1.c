// P2-S1: Conditional max (matches ref1)
#include <stdio.h>
int findMax(int a[], int n) {
  int maximum = a[0];
  for (int i = 1; i < n; i++) {
    if (a[i] > maximum)
      maximum = a[i];
  }
  return maximum;
}
int main() {
  int arr[] = {12, 45, 23, 67, 34, 89, 21};
  printf("Max = %d\n", findMax(arr, 7));
  return 0;
}
