// P2-S2: Ternary operator (matches ref2)
#include <stdio.h>
int max(int arr[], int n) {
  int m = arr[0];
  for (int i = 1; i < n; i++)
    m = (arr[i] > m) ? arr[i] : m;
  return m;
}
int main() {
  int arr[] = {12, 45, 23, 67, 34, 89, 21};
  printf("Max = %d\n", max(arr, 7));
  return 0;
}
