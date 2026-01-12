// P1 Student 12: Backward iteration accumulation (matches ref1)
#include <stdio.h>

int arraySum(int arr[], int n) {
  int sum = 0;
  for (int i = n - 1; i >= 0; i--) { // Backward iteration
    sum += arr[i];
  }
  return sum;
}

int main() {
  int arr[] = {5, 10, 15, 20, 25};
  printf("Sum = %d\n", arraySum(arr, 5));
  return 0;
}
