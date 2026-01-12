// P3-S4: Ternary increment (matches ref1)
#include <stdio.h>
int countOccurrences(int arr[], int n, int target) {
  int count = 0;
  for (int i = 0; i < n; i++) {
    count = (arr[i] == target) ? count + 1 : count;
  }
  return count;
}
int main() {
  int arr[] = {5, 2, 5, 8, 5, 3};
  printf("Count: %d\n", countOccurrences(arr, 6, 5));
  return 0;
}
