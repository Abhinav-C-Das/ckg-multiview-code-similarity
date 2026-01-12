// P12_S5: Matches ref2 (index-based copy)
#include <stdio.h>
#include <string.h>

void reverse(char str[]) {
  int n = strlen(str);
  char copy[100];
  int j = 0;
  for (int i = n - 1; i >= 0; i--) {
    copy[j++] = str[i];
  }
  copy[n] = '\0';
  for (int i = 0; i < n; i++)
    str[i] = copy[i];
}

int main() {
  char str[] = "hello";
  reverse(str);
  printf("%s\n", str);
  return 0;
}
