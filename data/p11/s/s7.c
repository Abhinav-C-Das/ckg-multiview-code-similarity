// P11_S7: Matches ref1 (descending order variant)
#include <stdio.h>

void bubbleSort(int arr[], int n) {
  for (int i = n - 1; i > 0; i--) {
    for (int j = 0; j < i; j++) {
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
