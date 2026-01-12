// P3-S5: Explicit form count = count + 1 (matches ref2)
#include <stdio.h>
int count_target(int data[], int size, int val) {
  int result = 0;
  for (int j = 0; j < size; j++) {
    if (data[j] == val)
      result = result + 1;
  }
  return result;
}
int main() {
  int arr[] = {5, 2, 5, 8, 5, 3};
  printf("Count: %d\n", count_target(arr, 6, 5));
  return 0;
}
