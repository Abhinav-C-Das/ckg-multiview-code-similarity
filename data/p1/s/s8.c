// P1 Student 8: Do-while loop accumulation (matches ref1)
#include <stdio.h>

int arraySum(int arr[], int n) {
  if (n == 0)
    return 0;
  int sum = 0;
  int i = 0;
  do {
    sum += arr[i];
    i++;
  } while (i < n);
  return sum;
}

int main() {
  int arr[] = {5, 10, 15, 20, 25};
  printf("Sum = %d\n", arraySum(arr, 5));
  return 0;
}
