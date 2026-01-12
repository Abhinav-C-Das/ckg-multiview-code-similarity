// P1 Student 3: BUGGY - overwrites sum (matches ref2)
#include <stdio.h>

int arraySum(int arr[], int n) {
  int sum = 0;
  for (int i = 0; i < n; i++) {
    sum = arr[i]; // WRONG: overwrites instead of accumulating
  }
  return sum;
}

int main() {
  int arr[] = {5, 10, 15, 20, 25};
  printf("Sum = %d\n", arraySum(arr, 5));
  return 0;
}
