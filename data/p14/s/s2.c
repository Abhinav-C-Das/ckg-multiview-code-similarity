// P14_S2: Matches ref2 (column-major)
#include <stdio.h>

int sum(int m[][3], int r, int c) {
  int total = 0;
  for (int j = 0; j < c; j++)
    for (int i = 0; i < r; i++)
      total += m[i][j];
  return total;
}

int main() {
  int matrix[3][3] = {{1, 2, 3}, {4, 5, 6}, {7, 8, 9}};
  printf("Sum: %d\n", sum(matrix, 3, 3));
  return 0;
}
