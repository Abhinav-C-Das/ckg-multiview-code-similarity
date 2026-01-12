// P3-S1: matches ref1
#include <stdio.h>
int count(int a[], int n, int x) {
  int c = 0;
  for (int i = 0; i < n; i++)
    if (a[i] == x)
      c++;
  return c;
}
int main() {
  int a[] = {5, 2, 5, 8, 5, 3};
  printf("%d\n", count(a, 6, 5));
  return 0;
}
