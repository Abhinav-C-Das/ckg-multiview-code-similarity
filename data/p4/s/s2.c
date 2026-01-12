// P4-S2: Early return with different vars (matches ref1)
#include <stdio.h>
int search(int a[], int n, int x) {
  for (int i = 0; i < n; i++) {
    if (a[i] == x)
      return i;
  }
  return -1;
}
int main() {
  int arr[] = {10, 23, 45, 67, 89};
  printf("Index: %d\n", search(arr, 5, 45));
  return 0;
}
