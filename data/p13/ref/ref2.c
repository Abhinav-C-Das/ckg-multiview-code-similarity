// P13: Binary Search - Reference 2 (Recursive)
#include <stdio.h>

int binarySearchRecursive(int arr[], int left, int right, int target) {
  if (left > right) {
    return -1;
  }

  int mid = left + (right - left) / 2;

  if (arr[mid] == target) {
    return mid;
  }
  if (arr[mid] < target) {
    return binarySearchRecursive(arr, mid + 1, right, target);
  }
  return binarySearchRecursive(arr, left, mid - 1, target);
}

int binarySearch(int arr[], int n, int target) {
  return binarySearchRecursive(arr, 0, n - 1, target);
}

int main() {
  int arr[] = {2, 5, 8, 12, 16, 23, 38, 45, 56, 67, 78};
  int n = 11;
  int target = 23;

  int result = binarySearch(arr, n, target);
  printf("Index: %d\n", result);
  return 0;
}
