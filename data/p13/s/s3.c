// P13_S3: Matches ref1 (different mid calculation)
#include <stdio.h>

int search(int arr[], int n, int target) {
  int low = 0, high = n - 1;
  while (low <= high) {
    int mid = (low + high) / 2;
    if (arr[mid] == target)
      return mid;
    if (arr[mid] < target)
      low = mid + 1;
    else
      high = mid - 1;
  }
  return -1;
}

int main() {
  int arr[] = {2, 5, 8, 12, 16, 23, 38, 45, 56, 67, 78};
  printf("Index: %d\n", search(arr, 11, 23));
  return 0;
}
