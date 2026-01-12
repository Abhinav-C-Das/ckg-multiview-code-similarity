// P14_S5: Matches ref2 (pointer arithmetic)
#include <stdio.h>

int sum(int m[][3], int r, int c) {
  int total = 0;
  for (int col = 0; col < c; col++)
    for (int row = 0; row < r; row++)
      total += *(*(m + row) + col);
  return total;
}

int main() {
  int matrix[3][3] = {{1, 2, 3}, {4, 5, 6}, {7, 8, 9}};
  printf("Sum: %d\n", sum(matrix, 3, 3));
  return 0;
}
