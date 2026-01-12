// P14_S4: Matches ref1 (accumulator name variant)
#include <stdio.h>

int sum(int m[][3], int r, int c) {
  int result = 0;
  for (int x = 0; x < r; x++)
    for (int y = 0; y < c; y++)
      result += m[x][y];
  return result;
}

int main() {
  int matrix[3][3] = {{1, 2, 3}, {4, 5, 6}, {7, 8, 9}};
  printf("Sum: %d\n", sum(matrix, 3, 3));
  return 0;
}
