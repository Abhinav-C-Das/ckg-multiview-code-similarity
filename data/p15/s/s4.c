// P15_S4: Matches ref1 (pointer variant)
#include <ctype.h>
#include <stdio.h>
#include <string.h>


int check(char *s) {
  char *left = s, *right = s + strlen(s) - 1;
  while (left < right) {
    if (tolower(*left) != tolower(*right))
      return 0;
    left++;
    right--;
  }
  return 1;
}

int main() {
  printf("%s\n", check("racecar") ? "Palindrome" : "Not palindrome");
  return 0;
}
