// P15_S3: Matches ref1 (for loop variant)
#include <ctype.h>
#include <stdio.h>
#include <string.h>


int check(char s[]) {
  int n = strlen(s);
  for (int i = 0; i < n / 2; i++) {
    if (tolower(s[i]) != tolower(s[n - 1 - i]))
      return 0;
  }
  return 1;
}

int main() {
  printf("%s\n", check("racecar") ? "Palindrome" : "Not palindrome");
  return 0;
}
