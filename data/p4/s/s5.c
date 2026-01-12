// P4-S5: Full traversal with flag (matches ref2)
#include <stdio.h>
int findIndex(int data[], int size, int key) {
  int position = -1;
  for (int j = 0; j < size; j++) {
    if (data[j] == key)
      position = j;
  }
  return position;
}
int main() {
  int arr[] = {10, 23, 45, 67, 89};
  printf("Index: %d\n", findIndex(arr, 5, 45));
  return 0;
}
