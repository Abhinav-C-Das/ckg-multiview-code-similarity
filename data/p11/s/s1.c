// P11_S1: Matches ref1 (standard swap)
#include <stdio.h>

void sort(int a[], int size) {
  for (int x = 0; x < size - 1; x++) {
    for (int y = 0; y < size - x - 1; y++) {
      if (a[y] > a[y + 1]) {
        int t = a[y];
        a[y] = a[y + 1];
        a[y + 1] = t;
      }
    }
  }
}

int main() {
  int nums[] = {64, 34, 25, 12, 22, 11, 90};
  sort(nums, 7);
  for (int i = 0; i < 7; i++)
    printf("%d ", nums[i]);
  return 0;
}
