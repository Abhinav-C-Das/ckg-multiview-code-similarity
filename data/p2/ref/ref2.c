// Problem 2: Find Maximum in Array
// Reference 2: Alternative with ternary operator
// Strategy: Same max tracking but using ternary

#include <stdio.h>

int findMax(int arr[], int n) {
  int max = arr[0];
  for (int i = 1; i < n; i++) {
    max = (arr[i] > max) ? arr[i] : max; // Ternary operator
  }
  return max;
}

int main() {
  int arr[] = {12, 45, 23, 67, 34, 89, 21};
  printf("Max = %d\n", findMax(arr, 7));
  return 0;
}
