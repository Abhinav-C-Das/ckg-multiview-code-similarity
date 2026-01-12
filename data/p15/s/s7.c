// P15_S7: Matches ref2 (backward iteration)
#include <ctype.h>
#include <stdio.h>
#include <string.h>


int check(char str[]) {
  int n = strlen(str);
  char temp[100];
  for (int i = n - 1, j = 0; i >= 0; i--, j++)
    temp[j] = tolower(str[i]);
  temp[n] = '\0';
  for (int i = 0; i < n; i++)
    if (tolower(str[i]) != temp[i])
      return 0;
  return 1;
}

int main() {
  printf("%s\n", check("racecar") ? "Palindrome" : "Not palindrome");
  return 0;
}
