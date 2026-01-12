// P5-S4: XOR swap (different strategy, matches ref1 conceptually)
#include <stdio.h>
void reverseArray(int arr[], int n) {
  int left = 0, right = n - 1;
  while (left < right) {
    // XOR swap without temp variable
    arr[left] = arr[left] ^ arr[right];
    arr[right] = arr[left] ^ arr[right];
    arr[left] = arr[left] ^ arr[right];
    left++;
    right--;
  }
}
int main() {
  int arr[] = {1, 2, 3, 4, 5};
  reverseArray(arr, 5);
  for (int i = 0; i < 5; i++)
    printf("%d ", arr[i]);
  return 0;
}
