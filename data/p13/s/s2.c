// P13_S2: Matches ref2 (recursive)
#include <stdio.h>

int searchRec(int arr[], int l, int r, int x) {
  if (l > r)
    return -1;
  int m = l + (r - l) / 2;
  if (arr[m] == x)
    return m;
  if (arr[m] < x)
    return searchRec(arr, m + 1, r, x);
  return searchRec(arr, l, m - 1, x);
}

int search(int arr[], int n, int x) { return searchRec(arr, 0, n - 1, x); }

int main() {
  int arr[] = {2, 5, 8, 12, 16, 23, 38, 45, 56, 67, 78};
  printf("Index: %d\n", search(arr, 11, 23));
  return 0;
}
