// P4-S4: While loop early return (matches ref1)
#include <stdio.h>
int linearSearch(int arr[], int n, int target) {
  int i = 0;
  while (i < n) {
    if (arr[i] == target)
      return i;
    i++;
  }
  return -1;
}
int main() {
  int arr[] = {10, 23, 45, 67, 89};
  printf("Index: %d\n", linearSearch(arr, 5, 45));
  return 0;
}
