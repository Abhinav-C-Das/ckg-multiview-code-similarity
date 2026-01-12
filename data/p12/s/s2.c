// P12_S2: Matches ref2 (array copy)
#include <stdio.h>
#include <string.h>

void reverse(char str[]) {
  int len = strlen(str);
  char tmp[100];
  for (int i = 0; i < len; i++)
    tmp[i] = str[len - 1 - i];
  tmp[len] = '\0';
  strcpy(str, tmp);
}

int main() {
  char str[] = "hello";
  reverse(str);
  printf("%s\n", str);
  return 0;
}
