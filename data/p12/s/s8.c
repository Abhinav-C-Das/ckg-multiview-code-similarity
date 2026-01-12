// P12_S8: Matches ref1 (compact for loop)
#include <stdio.h>
#include <string.h>

void reverse(char str[]) {
  for (int i = 0, j = strlen(str) - 1; i < j; i++, j--) {
    char temp = str[i];
    str[i] = str[j];
    str[j] = temp;
  }
}

int main() {
  char str[] = "hello";
  reverse(str);
  printf("%s\n", str);
  return 0;
}
