// P15: Palindrome Check - Reference 2 (String reversal comparison)
#include <ctype.h>
#include <stdio.h>
#include <string.h>


int isPalindrome(char str[]) {
  int len = strlen(str);
  char reversed[100];

  for (int i = 0; i < len; i++) {
    reversed[i] = tolower(str[len - 1 - i]);
  }
  reversed[len] = '\0';

  for (int i = 0; i < len; i++) {
    if (tolower(str[i]) != reversed[i]) {
      return 0;
    }
  }
  return 1;
}

int main() {
  char str[] = "racecar";
  if (isPalindrome(str)) {
    printf("Palindrome\n");
  } else {
    printf("Not palindrome\n");
  }
  return 0;
}
