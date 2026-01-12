// P12_S1: Matches ref1 (two-pointer)
#include <stdio.h>
#include <string.h>

void reverse(char s[]) {
  int i = 0, j = strlen(s) - 1;
  while (i < j) {
    char t = s[i];
    s[i] = s[j];
    s[j] = t;
    i++;
    j--;
  }
}

int main() {
  char str[] = "hello";
  reverse(str);
  printf("%s\n", str);
  return 0;
}
