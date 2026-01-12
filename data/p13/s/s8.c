// P13_S8: Matches ref2 (helper function)
#include <stdio.h>

int helper(int *a, int l, int r, int target) {
  if (l > r)
    return -1;
  int m = (l + r) >> 1;
  if (a[m] == target)
    return m;
  if (a[m] < target)
    return helper(a, m + 1, r, target);
  return helper(a, l, m - 1, target);
}

int search(int a[], int n, int x) { return helper(a, 0, n - 1, x); }

int main() {
  int arr[] = {2, 5, 8, 12, 16, 23, 38, 45, 56, 67, 78};
  printf("Index: %d\n", search(arr, 11, 23));
  return 0;
}
