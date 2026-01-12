// P1 Student 10: Correct with different init (matches ref1)
#include <stdio.h>

int arraySum(int arr[], int n) {
  int sum = arr[0];             // Start with first element
  for (int i = 1; i < n; i++) { // Start from index 1
    sum += arr[i];
  }
  return sum;
}

int main() {
  int arr[] = {5, 10, 15, 20, 25};
  printf("Sum = %d\n", arraySum(arr, 5));
  return 0;
}
