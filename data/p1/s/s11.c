// P1 Student 11: Correct with compound addition (matches ref1)
#include <stdio.h>

int calcSum(int values[], int count) {
  int total = 0;
  int idx = 0;
  while (idx < count) {
    total = total + values[idx]; // Explicit addition
    idx = idx + 1;
  }
  return total;
}

int main() {
  int values[] = {5, 10, 15, 20, 25};
  printf("Sum = %d\n", calcSum(values, 5));
  return 0;
}
