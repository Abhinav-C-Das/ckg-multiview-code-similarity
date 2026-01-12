// P11_S3: Matches ref1 (while loop variant)
#include <stdio.h>

void bubbleSort(int arr[], int n) {
  int i = 0;
  while (i < n - 1) {
    int j = 0;
    while (j < n - i - 1) {
      if (arr[j] > arr[j + 1]) {
        int temp = arr[j];
        arr[j] = arr[j + 1];
        arr[j + 1] = temp;
      }
      j++;
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
