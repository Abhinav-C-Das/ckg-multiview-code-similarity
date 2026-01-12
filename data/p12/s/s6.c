// P12_S6: Matches ref1 (do-while variant)
#include <stdio.h>
#include <string.h>

void reverse(char str[]) {
  int left = 0, right = strlen(str) - 1;
  if (left < right) {
    do {
      char t = str[left];
      str[left] = str[right];
      str[right] = t;
      left++;
      right--;
    } while (left < right);
  }
}

int main() {
  char str[] = "hello";
  reverse(str);
  printf("%s\n", str);
  return 0;
}
