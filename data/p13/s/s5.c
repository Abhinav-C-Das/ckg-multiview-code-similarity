// P13_S5: Matches ref2 (tail recursive)
#include <stdio.h>

int bsearch(int a[], int l, int r, int x) {
  if (l > r)
    return -1;
  int mid = (l + r) / 2;
  if (a[mid] == x)
    return mid;
  return (a[mid] < x) ? bsearch(a, mid + 1, r, x) : bsearch(a, l, mid - 1, x);
}

int search(int a[], int n, int x) { return bsearch(a, 0, n - 1, x); }

int main() {
  int arr[] = {2, 5, 8, 12, 16, 23, 38, 45, 56, 67, 78};
  printf("Index: %d\n", search(arr, 11, 23));
  return 0;
}
