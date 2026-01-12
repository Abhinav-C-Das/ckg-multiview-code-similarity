// P12_S4: Matches ref1 (pointer arithmetic)
#include <stdio.h>
#include <string.h>

void reverse(char *str) {
  char *start = str;
  char *end = str + strlen(str) - 1;
  while (start < end) {
    char temp = *start;
    *start++ = *end;
    *end-- = temp;
  }
}

int main() {
  char str[] = "hello";
  reverse(str);
  printf("%s\n", str);
  return 0;
}
