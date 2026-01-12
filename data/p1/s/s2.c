// P1 Student 2: Correct with = sum + arr[i] form (matches ref1)
#include <stdio.h>

int arraySum(int arr[], int n) {
  int sum = 0;
  for (int i = 0; i < n; i++) {
    sum = sum + arr[i]; // Explicit form instead of +=
  }
  return sum;
}

int main() {
  int arr[] = {5, 10, 15, 20, 25};
  printf("Sum = %d\n", arraySum(arr, 5));
  return 0;
}
