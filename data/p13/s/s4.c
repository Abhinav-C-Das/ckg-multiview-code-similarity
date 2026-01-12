// P13_S4: Matches ref1 (do-while variant)
#include <stdio.h>

int search(int arr[], int n, int x) {
  int left = 0, right = n - 1;
  if (left <= right) {
    do {
      int mid = left + (right - left) / 2;
      if (arr[mid] == x)
        return mid;
      if (arr[mid] < x)
        left = mid + 1;
      else
        right = mid - 1;
    } while (left <= right);
  }
  return -1;
}

int main() {
  int arr[] = {2, 5, 8, 12, 16, 23, 38, 45, 56, 67, 78};
  printf("Index: %d\n", search(arr, 11, 23));
  return 0;
}
