// P5-S2: Two-pointer with temp (matches ref1)
#include <stdio.h>
void reverseArray(int a[], int n) {
  int i = 0, j = n - 1;
  while (i < j) {
    int temp = a[i];
    a[i] = a[j];
    a[j] = temp;
    i++;
    j--;
  }
}
int main() {
  int arr[] = {1, 2, 3, 4, 5};
  reverseArray(arr, 5);
  for (int k = 0; k < 5; k++)
    printf("%d ", arr[k]);
  return 0;
}
