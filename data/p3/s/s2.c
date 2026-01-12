// P3-S2: Counter with += (matches ref2)
#include <stdio.h>
int countOccurrences(int arr[], int n, int target) {
  int cnt = 0;
  for (int i = 0; i < n; i++) {
    if (arr[i] == target)
      cnt += 1;
  }
  return cnt;
}
int main() {
  int arr[] = {5, 2, 5, 8, 5, 3};
  printf("Count: %d\n", countOccurrences(arr, 6, 5));
  return 0;
}
