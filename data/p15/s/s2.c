// P15_S2: Matches ref2 (reversal)
#include <ctype.h>
#include <stdio.h>
#include <string.h>


int check(char str[]) {
  int len = strlen(str);
  char rev[100];
  for (int i = 0; i < len; i++)
    rev[i] = tolower(str[len - 1 - i]);
  rev[len] = '\0';
  for (int i = 0; i < len; i++)
    if (tolower(str[i]) != rev[i])
      return 0;
  return 1;
}

int main() {
  printf("%s\n", check("racecar") ? "Palindrome" : "Not palindrome");
  return 0;
}
