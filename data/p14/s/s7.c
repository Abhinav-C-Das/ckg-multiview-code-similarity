// P14_S7: Matches ref2 (column first with different bounds)
#include <stdio.h>

int sum(int m[][3], int r, int c) {
  int s = 0;
  for (int j = 0; j <= c - 1; j++)
    for (int i = 0; i <= r - 1; i++)
      s += m[i][j];
  return s;
}

int main() {
  int matrix[3][3] = {{1, 2, 3}, {4, 5, 6}, {7, 8, 9}};
  printf("Sum: %d\n", sum(matrix, 3, 3));
  return 0;
}
