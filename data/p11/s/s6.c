// P11_S6: Matches ref1 (different loop bounds)
#include <stdio.h>

void bubbleSort(int arr[], int n) {
  for (int i = 0; i <= n - 2; i++) {
    for (int j = 0; j <= n - i - 2; j++) {
      if (arr[j] > arr[j + 1]) {
        int temp = arr[j];
        arr[j] = arr[j + 1];
        arr[j + 1] = temp;
      }
    }
  }
}

int main() {
  int arr[] = {64, 34, 25, 12, 22, 11, 90};
  bubbleSort(arr, 7);
  for (int i = 0; i < 7; i++)
    printf("%d ", arr[i]);
  return 0;
}
