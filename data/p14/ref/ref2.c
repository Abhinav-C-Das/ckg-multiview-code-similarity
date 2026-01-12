// P14: Matrix Sum - Reference 2 (Column-major traversal)
#include <stdio.h>

int matrixSum(int matrix[][3], int rows, int cols) {
  int sum = 0;
  for (int j = 0; j < cols; j++) {
    for (int i = 0; i < rows; i++) {
      sum += matrix[i][j];
    }
  }
  return sum;
}

int main() {
  int matrix[3][3] = {{1, 2, 3}, {4, 5, 6}, {7, 8, 9}};
  int result = matrixSum(matrix, 3, 3);
  printf("Sum: %d\n", result);
  return 0;
}
