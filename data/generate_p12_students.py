#!/usr/bin/env python3
"""
Generate remaining P12-P15 student variants
Creates 8 student solutions for each problem
"""

import os

# P12 Student variants (String Reversal)
p12_students = [
    ("s1.c", """// P12_S1: Matches ref1 (two-pointer)
#include <stdio.h>
#include <string.h>

void reverse(char s[]) {
    int i = 0, j = strlen(s) - 1;
    while (i < j) {
        char t = s[i];
        s[i] = s[j];
        s[j] = t;
        i++; j--;
    }
}

int main() {
    char str[] = "hello";
    reverse(str);
    printf("%s\\n", str);
    return 0;
}"""),
    ("s2.c", """// P12_S2: Matches ref2 (array copy)
#include <stdio.h>
#include <string.h>

void reverse(char str[]) {
    int len = strlen(str);
    char tmp[100];
    for (int i = 0; i < len; i++) tmp[i] = str[len - 1 - i];
    tmp[len] = '\\0';
    strcpy(str, tmp);
}

int main() {
    char str[] = "hello";
    reverse(str);
    printf("%s\\n", str);
    return 0;
}"""),
    ("s3.c", """// P12_S3: Matches ref1 (for loop variant)
#include <stdio.h>
#include <string.h>

void reverse(char str[]) {
    int len = strlen(str);
    for (int i = 0; i < len/2; i++) {
        char temp = str[i];
        str[i] = str[len - 1 - i];
        str[len - 1 - i] = temp;
    }
}

int main() {
    char str[] = "hello";
    reverse(str);
    printf("%s\\n", str);
    return 0;
}"""),
    ("s4.c", """// P12_S4: Matches ref1 (pointer arithmetic)
#include <stdio.h>
#include <string.h>

void reverse(char *str) {
    char *start = str;
    char *end = str + strlen(str) - 1;
    while (start < end) {
        char temp = *start;
        *start++ = *end;
        *end-- = temp;
    }
}

int main() {
    char str[] = "hello";
    reverse(str);
    printf("%s\\n", str);
    return 0;
}"""),
    ("s5.c", """// P12_S5: Matches ref2 (index-based copy)
#include <stdio.h>
#include <string.h>

void reverse(char str[]) {
    int n = strlen(str);
    char copy[100];
    int j = 0;
    for (int i = n - 1; i >= 0; i--) {
        copy[j++] = str[i];
    }
    copy[n] = '\\0';
    for (int i = 0; i < n; i++) str[i] = copy[i];
}

int main() {
    char str[] = "hello";
    reverse(str);
    printf("%s\\n", str);
    return 0;
}"""),
    ("s6.c", """// P12_S6: Matches ref1 (do-while variant)
#include <stdio.h>
#include <string.h>

void reverse(char str[]) {
    int left = 0, right = strlen(str) - 1;
    if (left < right) {
        do {
            char t = str[left];
            str[left] = str[right];
            str[right] = t;
            left++; right--;
        } while (left < right);
    }
}

int main() {
    char str[] = "hello";
    reverse(str);
    printf("%s\\n", str);
    return 0;
}"""),
    ("s7.c", """// P12_S7: Matches ref2 (backward iteration)
#include <stdio.h>
#include <string.h>

void reverse(char str[]) {
    int len = strlen(str);
    char temp[100];
    int idx = 0;
    for (int i = len - 1; i >= 0; i--)  {
        temp[idx++] = str[i];
    }
    temp[len] = '\\0';
    strcpy(str, temp);
}

int main() {
    char str[] = "hello";
    reverse(str);
    printf("%s\\n", str);
    return 0;
}"""),
    ("s8.c", """// P12_S8: Matches ref1 (recursive approach converted to iterative)
#include <stdio.h>
#include <string.h>

void reverse(char str[]) {
    for (int i = 0, j = strlen(str) - 1; i < j; i++, j--) {
        char temp = str[i];
        str[i] = str[j];
        str[j] = temp;
    }
}

int main() {
    char str[] = "hello";
    reverse(str);
    printf("%s\\n", str);
    return 0;
}"""),
]

# Create P12 student files
base_path = "data/p12/s"
os.makedirs(base_path, exist_ok=True)
for filename, code in p12_students:
    with open(os.path.join(base_path, filename), 'w') as f:
        f.write(code)

print("✓ Created P12 student variants (8 files)")
