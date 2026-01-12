// P14_S1: Matches ref1 (row-major)
#include <stdio.h>

int sum(int m[][3], int r, int c) {
  int total = 0;
  for (int i = 0; i < r; i++)
    for (int j = 0; j < c; j++)
      total += m[i][j];
  return total;
}

int main() {
  int matrix[3][3] = {{1, 2, 3}, {4, 5, 6}, {7, 8, 9}};
  printf("Sum: %d\n", sum(matrix, 3, 3));
  return 0;
}
