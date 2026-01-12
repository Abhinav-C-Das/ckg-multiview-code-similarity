// P11_S8: Matches ref2 (combined condition)
#include <stdio.h>

void bubbleSort(int arr[], int n) {
  int i = 0;
  int swapped = 1;
  while (i < n - 1 && swapped) {
    swapped = 0;
    for (int j = 0; j < n - i - 1; j++) {
      if (arr[j] > arr[j + 1]) {
        int temp = arr[j];
        arr[j] = arr[j + 1];
        arr[j + 1] = temp;
        swapped = 1;
      }
    }
    i++;
  }
}

int main() {
  int arr[] = {64, 34, 25, 12, 22, 11, 90};
  bubbleSort(arr, 7);
  for (int i = 0; i < 7; i++)
    printf("%d ", arr[i]);
  return 0;
}
