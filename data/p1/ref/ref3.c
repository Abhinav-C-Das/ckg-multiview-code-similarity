// Problem 1: Array Sum
// Reference 3: Recursive accumulation
// Strategy: Recursive with tail accumulation (CES: ACCUMULATIVE in recursion)

#include <stdio.h>

int arraySum(int arr[], int n) {
  if (n == 0) {
    return 0;
  }
  return arr[n - 1] + arraySum(arr, n - 1); // Recursive accumulation
}

int main() {
  int arr[] = {5, 10, 15, 20, 25};
  int n = 5;
  printf("Sum = %d\n", arraySum(arr, n));
  return 0;
}
