// P5-S5: Pointer-based two-pointer (matches ref1)
#include <stdio.h>
void reverseArray(int *arr, int n) {
  int *start = arr;
  int *end = arr + n - 1;
  while (start < end) {
    int temp = *start;
    *start = *end;
    *end = temp;
    start++;
    end--;
  }
}
int main() {
  int arr[] = {1, 2, 3, 4, 5};
  reverseArray(arr, 5);
  for (int i = 0; i < 5; i++)
    printf("%d ", arr[i]);
  return 0;
}
