// P1 Student 1: Correct accumulation with += (matches ref1)
#include <stdio.h>

int sum(int a[], int size) {
  int total = 0;
  for (int j = 0; j < size; j++) {
    total += a[j];
  }
  return total;
}

int main() {
  int numbers[] = {5, 10, 15, 20, 25};
  printf("Sum = %d\n", sum(numbers, 5));
  return 0;
}
