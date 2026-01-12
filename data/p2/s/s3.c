// P2-S3: While loop variant (matches ref1)
#include <stdio.h>
int findMax(int arr[], int n) {
  int max = arr[0];
  int i = 1;
  while (i < n) {
    if (arr[i] > max)
      max = arr[i];
    i++;
  }
  return max;
}
int main() {
  int arr[] = {12, 45, 23, 67, 34, 89, 21};
  printf("Max = %d\n", findMax(arr, 7));
  return 0;
}
