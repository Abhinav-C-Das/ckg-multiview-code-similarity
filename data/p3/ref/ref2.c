// P3: Count Occurrences - Ref2: Compound operator
#include <stdio.h>
int countOccurrences(int arr[], int n, int target) {
  int count = 0;
  for (int i = 0; i < n; i++) {
    if (arr[i] == target)
      count += 1; // Explicit +=
  }
  return count;
}
int main() {
  int arr[] = {5, 2, 5, 8, 5, 3};
  printf("Count of 5: %d\n", countOccurrences(arr, 6, 5));
  return 0;
}
