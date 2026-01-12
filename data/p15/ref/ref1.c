// P15: Palindrome Check - Reference 1 (Two-pointer)
#include <ctype.h>
#include <stdio.h>
#include <string.h>


int isPalindrome(char str[]) {
  int left = 0;
  int right = strlen(str) - 1;

  while (left < right) {
    if (tolower(str[left]) != tolower(str[right])) {
      return 0;
    }
    left++;
    right--;
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
