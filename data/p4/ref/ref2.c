// P4: Linear Search - Ref2: Flag variable
#include <stdio.h>
int linearSearch(int arr[], int n, int target) {
  int found = -1;
  for (int i = 0; i < n; i++) {
    if (arr[i] == target)
      found = i; // No early exit
  }
  return found;
}
int main() {
  int arr[] = {10, 23, 45, 67, 89};
  printf("Index: %d\n", linearSearch(arr, 5, 45));
  return 0;
}
