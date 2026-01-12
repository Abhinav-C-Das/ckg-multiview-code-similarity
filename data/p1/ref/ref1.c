// Problem 1: Array Sum
// Reference 1: Correct iterative accumulation with +=
// Strategy: Accumulation pattern (CES: ACCUMULATIVE)

#include <stdio.h>

int arraySum(int arr[], int n) {
  int sum = 0;
  for (int i = 0; i < n; i++) {
    sum += arr[i]; // Accumulation: depends on previous value
  }
  return sum;
}

int main() {
  int arr[] = {5, 10, 15, 20, 25};
  int n = 5;
  printf("Sum = %d\n", arraySum(arr, n));
  return 0;
}
