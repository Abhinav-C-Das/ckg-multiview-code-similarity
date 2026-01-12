// P13_S6: Matches ref1 (explicit checks)
#include <stdio.h>

int search(int arr[], int n, int target) {
  int start = 0, end = n - 1;
  while (start <= end) {
    int middle = start + (end - start) / 2;
    if (arr[middle] == target) {
      return middle;
    } else if (arr[middle] < target) {
      start = middle + 1;
    } else {
      end = middle - 1;
    }
  }
  return -1;
}

int main() {
  int arr[] = {2, 5, 8, 12, 16, 23, 38, 45, 56, 67, 78};
  printf("Index: %d\n", search(arr, 11, 23));
  return 0;
}
