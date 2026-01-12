// P15_S6: Matches ref1 (do-while variant)
#include <ctype.h>
#include <stdio.h>
#include <string.h>


int check(char s[]) {
  int l = 0, r = strlen(s) - 1;
  if (l < r) {
    do {
      if (tolower(s[l]) != tolower(s[r]))
        return 0;
      l++;
      r--;
    } while (l < r);
  }
  return 1;
}

int main() {
  printf("%s\n", check("racecar") ? "Palindrome" : "Not palindrome");
  return 0;
}
