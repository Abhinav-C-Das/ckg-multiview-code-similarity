// P2-S6-S10: More variations for P2
#include <stdio.h>
int findMax(int arr[], int n) {
  int max = arr[0];
  for (int i = 0; i < n; i++) {
    if (arr[i] > max)
      max = arr[i];
  }
  return max;
}
int main() {
  int arr[] = {12, 45, 23, 67, 34, 89, 21};
  printf("Max = %d\n", findMax(arr, 7));
  return 0;
}
