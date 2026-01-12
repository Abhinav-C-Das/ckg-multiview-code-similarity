// P12: String Reversal - Reference 2 (Array copy approach)
#include <stdio.h>
#include <string.h>

void reverseString(char str[]) {
  int len = strlen(str);
  char temp[100];

  for (int i = 0; i < len; i++) {
    temp[i] = str[len - 1 - i];
  }
  temp[len] = '\0';

  for (int i = 0; i < len; i++) {
    str[i] = temp[i];
  }
}

int main() {
  char str[] = "hello";
  reverseString(str);
  printf("%s\n", str);
  return 0;
}
