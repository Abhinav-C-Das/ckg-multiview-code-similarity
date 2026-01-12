// P5-S6: Decreasing loop (matches ref2)
#include <stdio.h>
void reverseArray(int arr[], int n) {
  for (int i = 0; i <= n / 2 - 1; i++) {
    int t = arr[i];
    arr[i] = arr[(n - 1) - i];
    arr[(n - 1) - i] = t;
  }
}
int main() {
  int arr[] = {1, 2, 3, 4, 5};
  reverseArray(arr, 5);
  for (int i = 0; i < 5; i++)
    printf("%d ", arr[i]);
  return 0;
}
