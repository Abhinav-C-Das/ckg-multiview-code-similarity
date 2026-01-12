// P1 Student 6: BUGGY - similar to ref2 with different var names
#include <stdio.h>

int getSum(int data[], int length) {
  int result = 0;
  for (int k = 0; k < length; k++) {
    result = data[k]; // WRONG: recomputation not accumulation
  }
  return result;
}

int main() {
  int data[] = {5, 10, 15, 20, 25};
  printf("Sum = %d\n", getSum(data, 5));
  return 0;
}
