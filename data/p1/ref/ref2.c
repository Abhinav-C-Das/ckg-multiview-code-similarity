// Problem 1: Array Sum
// Reference 2: Incorrect overwrite pattern (CES demonstration)
// Strategy: Recomputation - overwrites sum each iteration (CES: RECOMPUTED)

#include <stdio.h>

int arraySum(int arr[], int n) {
  int sum = 0;
  for (int i = 0; i < n; i++) {
    sum = arr[i]; // Overwrites - does NOT accumulate (BUGGY!)
  }
  return sum;
}

int main() {
  int arr[] = {5, 10, 15, 20, 25};
  int n = 5;
  printf("Sum = %d\n", arraySum(arr, n)); // Will print 25 (last element)
  return 0;
}
