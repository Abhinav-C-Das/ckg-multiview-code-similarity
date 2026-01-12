// P14_S3: Matches ref1 (while loops)
#include <stdio.h>

int sum(int m[][3], int r, int c) {
  int total = 0;
  int i = 0;
  while (i < r) {
    int j = 0;
    while (j < c) {
      total += m[i][j];
      j++;
    }
    i++;
  }
  return total;
}

int main() {
  int matrix[3][3] = {{1, 2, 3}, {4, 5, 6}, {7, 8, 9}};
  printf("Sum: %d\n", sum(matrix, 3, 3));
  return 0;
}
