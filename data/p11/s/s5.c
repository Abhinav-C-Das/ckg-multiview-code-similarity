// P11_S5: Matches ref2 (different flag variable name)
#include <stdio.h>

void bubbleSort(int arr[], int n) {
  for (int i = 0; i < n - 1; i++) {
    int didSwap = 0;
    for (int j = 0; j < n - i - 1; j++) {
      if (arr[j] > arr[j + 1]) {
        int temp = arr[j];
        arr[j] = arr[j + 1];
        arr[j + 1] = temp;
        didSwap = 1;
      }
    }
    if (didSwap == 0)
      break;
  }
}

int main() {
  int arr[] = {64, 34, 25, 12, 22, 11, 90};
  bubbleSort(arr, 7);
  for (int i = 0; i < 7; i++)
    printf("%d ", arr[i]);
  return 0;
}
