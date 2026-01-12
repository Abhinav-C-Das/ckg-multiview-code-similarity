// P2-S4: Separate comparison (matches ref1)
#include <stdio.h>
int getMax(int data[], int size) {
  int result = data[0];
  for (int j = 1; j < size; j++) {
    int current = data[j];
    if (current > result)
      result = current;
  }
  return result;
}
int main() {
  int arr[] = {12, 45, 23, 67, 34, 89, 21};
  printf("Max = %d\n", getMax(arr, 7));
  return 0;
}
