// P3-S3: While loop counter (matches ref1)
#include <stdio.h>
int countOccurrences(int arr[], int n, int target) {
  int count = 0;
  int i = 0;
  while (i < n) {
    if (arr[i] == target)
      count++;
    i++;
  }
  return count;
}
int main() {
  int arr[] = {5, 2, 5, 8, 5, 3};
  printf("Count: %d\n", countOccurrences(arr, 6, 5));
  return 0;
}
