// P1 Student 5: While loop accumulation (matches ref1)
#include <stdio.h>

int arraySum(int arr[], int n) {
  int sum = 0;
  int i = 0;
  while (i < n) {
    sum += arr[i];
    i++;
  }
  return sum;
}

int main() {
  int arr[] = {5, 10, 15, 20, 25};
  printf("Sum = %d\n", arraySum(arr, 5));
  return 0;
}
