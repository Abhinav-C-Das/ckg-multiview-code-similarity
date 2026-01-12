// P13_S1: Matches ref1 (iterative)
#include <stdio.h>

int search(int a[], int n, int x) {
  int l = 0, r = n - 1;
  while (l <= r) {
    int m = l + (r - l) / 2;
    if (a[m] == x)
      return m;
    if (a[m] < x)
      l = m + 1;
    else
      r = m - 1;
  }
  return -1;
}

int main() {
  int arr[] = {2, 5, 8, 12, 16, 23, 38, 45, 56, 67, 78};
  printf("Index: %d\n", search(arr, 11, 23));
  return 0;
}
