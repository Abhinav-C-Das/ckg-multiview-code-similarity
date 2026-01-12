// P14_S6: Matches ref1 (do-while variant)
#include <stdio.h>

int sum(int m[][3], int r, int c) {
  int total = 0;
  int i = 0;
  do {
    int j = 0;
    do {
      total += m[i][j];
      j++;
    } while (j < c);
    i++;
  } while (i < r);
  return total;
}

int main() {
  int matrix[3][3] = {{1, 2, 3}, {4, 5, 6}, {7, 8, 9}};
  printf("Sum: %d\n", sum(matrix, 3, 3));
  return 0;
}
