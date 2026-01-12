// P12_S7: Matches ref2 (backward iteration)
#include <stdio.h>
#include <string.h>

void reverse(char str[]) {
  int len = strlen(str);
  char temp[100];
  int idx = 0;
  for (int i = len - 1; i >= 0; i--) {
    temp[idx++] = str[i];
  }
  temp[len] = '\0';
  strcpy(str, temp);
}

int main() {
  char str[] = "hello";
  reverse(str);
  printf("%s\n", str);
  return 0;
}
