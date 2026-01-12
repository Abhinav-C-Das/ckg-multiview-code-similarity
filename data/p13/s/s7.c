// P13_S7: Matches ref1 (ternary variant)
#include <stdio.h>

int search(int arr[], int n, int x) {
  int l = 0, r = n - 1;
  while (l <= r) {
    int m = l + (r - l) / 2;
    if (arr[m] == x)
      return m;
    (arr[m] < x) ? (l = m + 1) : (r = m - 1);
  }
  return -1;
}

int main() {
  int arr[] = {2, 5, 8, 12, 16, 23, 38, 45, 56, 67, 78};
  printf("Index: %d\n", search(arr, 11, 23));
  return 0;
}
