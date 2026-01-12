// P1 Student 9: Recursive with helper (matches ref3)
#include <stdio.h>

int sumHelper(int arr[], int n, int index) {
  if (index == n) {
    return 0;
  }
  return arr[index] + sumHelper(arr, n, index + 1);
}

int arraySum(int arr[], int n) { return sumHelper(arr, n, 0); }

int main() {
  int arr[] = {5, 10, 15, 20, 25};
  printf("Sum = %d\n", arraySum(arr, 5));
  return 0;
}
