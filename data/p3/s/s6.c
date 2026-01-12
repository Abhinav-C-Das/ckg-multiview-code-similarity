// P3-S6: Do-while variant (matches ref1)
#include <stdio.h>
int countOccurrences(int arr[], int n, int target) {
  if (n == 0)
    return 0;
  int count = 0;
  int i = 0;
  do {
    if (arr[i] == target)
      count++;
    i++;
  } while (i < n);
  return count;
}
int main() {
  int arr[] = {5, 2, 5, 8, 5, 3};
  printf("Count: %d\n", countOccurrences(arr, 6, 5));
  return 0;
}
