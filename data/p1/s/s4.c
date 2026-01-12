// P1 Student 4: Recursive accumulation (matches ref3)
#include <stdio.h>

int sumArray(int arr[], int index) {
  if (index < 0) {
    return 0;
  }
  return arr[index] + sumArray(arr, index - 1);
}

int main() {
  int arr[] = {5, 10, 15, 20, 25};
  printf("Sum = %d\n", sumArray(arr, 4));
  return 0;
}
