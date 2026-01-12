// P15_S5: Matches ref2 (strcmp variant)
#include <ctype.h>
#include <stdio.h>
#include <string.h>


int check(char str[]) {
  int len = strlen(str);
  char rev[100], lower[100];
  for (int i = 0; i < len; i++) {
    lower[i] = tolower(str[i]);
    rev[i] = tolower(str[len - 1 - i]);
  }
  lower[len] = rev[len] = '\0';
  return strcmp(lower, rev) == 0;
}

int main() {
  printf("%s\n", check("racecar") ? "Palindrome" : "Not palindrome");
  return 0;
}
