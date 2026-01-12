// P15_S8: Matches ref1 (half-length optimization)
#include <ctype.h>
#include <stdio.h>
#include <string.h>


int check(char s[]) {
  int len = strlen(s);
  int i = 0, j = len - 1;
  while (i <= len / 2 && i < j) {
    if (tolower(s[i++]) != tolower(s[j--]))
      return 0;
  }
  return 1;
}

int main() {
  printf("%s\n", check("racecar") ? "Palindrome" : "Not palindrome");
  return 0;
}
