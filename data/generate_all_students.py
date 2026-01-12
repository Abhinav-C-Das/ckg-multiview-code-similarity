#!/usr/bin/env python3
"""
Generate all student variants for P12-P15
Creates complete dataset expansion
"""

import os

def create_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(content)

# P12 Students already created via previous script, but including for completeness
# P13 Binary Search Student Variants
p13_students = {
    "s1.c": """// P13_S1: Matches ref1 (iterative)
#include <stdio.h>

int search(int a[], int n, int x) {
    int l = 0, r = n - 1;
    while (l <= r) {
        int m = l + (r - l) / 2;
        if (a[m] == x) return m;
        if (a[m] < x) l = m + 1;
        else r = m - 1;
    }
    return -1;
}

int main() {
    int arr[] = {2, 5, 8, 12, 16, 23, 38, 45, 56, 67, 78};
    printf("Index: %d\\n", search(arr, 11, 23));
    return 0;
}""",
    "s2.c": """// P13_S2: Matches ref2 (recursive)
#include <stdio.h>

int searchRec(int arr[], int l, int r, int x) {
    if (l > r) return -1;
    int m = l + (r - l) / 2;
    if (arr[m] == x) return m;
    if (arr[m] < x) return searchRec(arr, m + 1, r, x);
    return searchRec(arr, l, m - 1, x);
}

int search(int arr[], int n, int x) {
    return searchRec(arr, 0, n - 1, x);
}

int main() {
    int arr[] = {2, 5, 8, 12, 16, 23, 38, 45, 56, 67, 78};
    printf("Index: %d\\n", search(arr, 11, 23));
    return 0;
}""",
    "s3.c": """// P13_S3: Matches ref1 (different mid calculation)
#include <stdio.h>

int search(int arr[], int n, int target) {
    int low = 0, high = n - 1;
    while (low <= high) {
        int mid = (low + high) / 2;
        if (arr[mid] == target) return mid;
        if (arr[mid] < target) low = mid + 1;
        else high = mid - 1;
    }
    return -1;
}

int main() {
    int arr[] = {2, 5, 8, 12, 16, 23, 38, 45, 56, 67, 78};
    printf("Index: %d\\n", search(arr, 11, 23));
    return 0;
}""",
    "s4.c": """// P13_S4: Matches ref1 (do-while variant)
#include <stdio.h>

int search(int arr[], int n, int x) {
    int left = 0, right = n - 1;
    if (left <= right) {
        do {
            int mid = left + (right - left) / 2;
            if (arr[mid] == x) return mid;
            if (arr[mid] < x) left = mid + 1;
            else right = mid - 1;
        } while (left <= right);
    }
    return -1;
}

int main() {
    int arr[] = {2, 5, 8, 12, 16, 23, 38, 45, 56, 67, 78};
    printf("Index: %d\\n", search(arr, 11, 23));
    return 0;
}""",
    "s5.c": """// P13_S5: Matches ref2 (tail recursive)
#include <stdio.h>

int bsearch(int a[], int l, int r, int x) {
    if (l > r) return -1;
    int mid = (l + r) / 2;
    if (a[mid] == x) return mid;
    return (a[mid] < x) ? bsearch(a, mid+1, r, x) : bsearch(a, l, mid-1, x);
}

int search(int a[], int n, int x) { return bsearch(a, 0, n-1, x); }

int main() {
    int arr[] = {2, 5, 8, 12, 16, 23, 38, 45, 56, 67, 78};
    printf("Index: %d\\n", search(arr, 11, 23));
    return 0;
}""",
    "s6.c": """// P13_S6: Matches ref1 (explicit checks)
#include <stdio.h>

int search(int arr[], int n, int target) {
    int start = 0, end = n - 1;
    while (start <= end) {
        int middle = start + (end - start) / 2;
        if (arr[middle] == target) {
            return middle;
        } else if (arr[middle] < target) {
            start = middle + 1;
        } else {
            end = middle - 1;
        }
    }
    return -1;
}

int main() {
    int arr[] = {2, 5, 8, 12, 16, 23, 38, 45, 56, 67, 78};
    printf("Index: %d\\n", search(arr, 11, 23));
    return 0;
}""",
    "s7.c": """// P13_S7: Matches ref1 (ternary variant)
#include <stdio.h>

int search(int arr[], int n, int x) {
    int l = 0, r = n - 1;
    while (l <= r) {
        int m = l + (r - l) / 2;
        if (arr[m] == x) return m;
        (arr[m] < x) ? (l = m + 1) : (r = m - 1);
    }
    return -1;
}

int main() {
    int arr[] = {2, 5, 8, 12, 16, 23, 38, 45, 56, 67, 78};
    printf("Index: %d\\n", search(arr, 11, 23));
    return 0;
}""",
    "s8.c": """// P13_S8: Matches ref2 (helper function)
#include <stdio.h>

int helper(int *a, int l, int r, int target) {
    if (l > r) return -1;
    int m = (l + r) >> 1;
    if (a[m] == target) return m;
    if (a[m] < target) return helper(a, m+1, r, target);
    return helper(a, l, m-1, target);
}

int search(int a[], int n, int x) { return helper(a, 0, n-1, x); }

int main() {
    int arr[] = {2, 5, 8, 12, 16, 23, 38, 45, 56, 67, 78};
    printf("Index: %d\\n", search(arr, 11, 23));
    return 0;
}"""
}

# P14 Matrix Sum Student Variants
p14_students = {
    "s1.c": """// P14_S1: Matches ref1 (row-major)
#include <stdio.h>

int sum(int m[][3], int r, int c) {
    int total = 0;
    for (int i = 0; i < r; i++)
        for (int j = 0; j < c; j++)
            total += m[i][j];
    return total;
}

int main() {
    int matrix[3][3] = {{1,2,3},{4,5,6},{7,8,9}};
    printf("Sum: %d\\n", sum(matrix, 3, 3));
    return 0;
}""",
    "s2.c": """// P14_S2: Matches ref2 (column-major)
#include <stdio.h>

int sum(int m[][3], int r, int c) {
    int total = 0;
    for (int j = 0; j < c; j++)
        for (int i = 0; i < r; i++)
            total += m[i][j];
    return total;
}

int main() {
    int matrix[3][3] = {{1,2,3},{4,5,6},{7,8,9}};
    printf("Sum: %d\\n", sum(matrix, 3, 3));
    return 0;
}""",
    "s3.c": """// P14_S3: Matches ref1 (while loops)
#include <stdio.h>

int sum(int m[][3], int r, int c) {
    int total = 0;
    int i = 0;
    while (i < r) {
        int j = 0;
        while (j < c) {
            total += m[i][j];
            j++;
        }
        i++;
    }
    return total;
}

int main() {
    int matrix[3][3] = {{1,2,3},{4,5,6},{7,8,9}};
    printf("Sum: %d\\n", sum(matrix, 3, 3));
    return 0;
}""",
    "s4.c": """// P14_S4: Matches ref1 (accumulator name variant)
#include <stdio.h>

int sum(int m[][3], int r, int c) {
    int result = 0;
    for (int x = 0; x < r; x++)
        for (int y = 0; y < c; y++)
            result += m[x][y];
    return result;
}

int main() {
    int matrix[3][3] = {{1,2,3},{4,5,6},{7,8,9}};
    printf("Sum: %d\\n", sum(matrix, 3, 3));
    return 0;
}""",
    "s5.c": """// P14_S5: Matches ref2 (pointer arithmetic)
#include <stdio.h>

int sum(int m[][3], int r, int c) {
    int total = 0;
    for (int col = 0; col < c; col++)
        for (int row = 0; row < r; row++)
            total += *(*(m + row) + col);
    return total;
}

int main() {
    int matrix[3][3] = {{1,2,3},{4,5,6},{7,8,9}};
    printf("Sum: %d\\n", sum(matrix, 3, 3));
    return 0;
}""",
    "s6.c": """// P14_S6: Matches ref1 (do-while variant)
#include <stdio.h>

int sum(int m[][3], int r, int c) {
    int total = 0;
    int i = 0;
    do {
        int j = 0;
        do {
            total += m[i][j];
            j++;
        } while (j < c);
        i++;
    } while (i < r);
    return total;
}

int main() {
    int matrix[3][3] = {{1,2,3},{4,5,6},{7,8,9}};
    printf("Sum: %d\\n", sum(matrix, 3, 3));
    return 0;
}""",
    "s7.c": """// P14_S7: Matches ref2 (column first with different bounds)
#include <stdio.h>

int sum(int m[][3], int r, int c) {
    int s = 0;
    for (int j = 0; j <= c-1; j++)
        for (int i = 0; i <= r-1; i++)
            s += m[i][j];
    return s;
}

int main() {
    int matrix[3][3] = {{1,2,3},{4,5,6},{7,8,9}};
    printf("Sum: %d\\n", sum(matrix, 3, 3));
    return 0;
}""",
    "s8.c": """// P14_S8: Matches ref1 (compact variant)
#include <stdio.h>

int sum(int m[][3], int r, int c) {
    int s = 0;
    for (int i = 0; i < r; i++) for (int j = 0; j < c; j++) s += m[i][j];
    return s;
}

int main() {
    int matrix[3][3] = {{1,2,3},{4,5,6},{7,8,9}};
    printf("Sum: %d\\n", sum(matrix, 3, 3));
    return 0;
}"""
}

# P15 Palindrome Check Student Variants
p15_students = {
    "s1.c": """// P15_S1: Matches ref1 (two-pointer)
#include <stdio.h>
#include <string.h>
#include <ctype.h>

int check(char s[]) {
    int l = 0, r = strlen(s) - 1;
    while (l < r) {
        if (tolower(s[l]) != tolower(s[r])) return 0;
        l++; r--;
    }
    return 1;
}

int main() {
    printf("%s\\n", check("racecar") ? "Palindrome" : "Not palindrome");
    return 0;
}""",
    "s2.c": """// P15_S2: Matches ref2 (reversal)
#include <stdio.h>
#include <string.h>
#include <ctype.h>

int check(char str[]) {
    int len = strlen(str);
    char rev[100];
    for (int i = 0; i < len; i++) rev[i] = tolower(str[len-1-i]);
    rev[len] = '\\0';
    for (int i = 0; i < len; i++)
        if (tolower(str[i]) != rev[i]) return 0;
    return 1;
}

int main() {
    printf("%s\\n", check("racecar") ? "Palindrome" : "Not palindrome");
    return 0;
}""",
    "s3.c": """// P15_S3: Matches ref1 (for loop variant)
#include <stdio.h>
#include <string.h>
#include <ctype.h>

int check(char s[]) {
    int n = strlen(s);
    for (int i = 0; i < n/2; i++) {
        if (tolower(s[i]) != tolower(s[n-1-i])) return 0;
    }
    return 1;
}

int main() {
    printf("%s\\n", check("racecar") ? "Palindrome" : "Not palindrome");
    return 0;
}""",
    "s4.c": """// P15_S4: Matches ref1 (pointer variant)
#include <stdio.h>
#include <string.h>
#include <ctype.h>

int check(char *s) {
    char *left = s, *right = s + strlen(s) - 1;
    while (left < right) {
        if (tolower(*left) != tolower(*right)) return 0;
        left++; right--;
    }
    return 1;
}

int main() {
    printf("%s\\n", check("racecar") ? "Palindrome" : "Not palindrome");
    return 0;
}""",
    "s5.c": """// P15_S5: Matches ref2 (strcmp variant)
#include <stdio.h>
#include <string.h>
#include <ctype.h>

int check(char str[]) {
    int len = strlen(str);
    char rev[100], lower[100];
    for (int i = 0; i < len; i++) {
        lower[i] = tolower(str[i]);
        rev[i] = tolower(str[len-1-i]);
    }
    lower[len] = rev[len] = '\\0';
    return strcmp(lower, rev) == 0;
}

int main() {
    printf("%s\\n", check("racecar") ? "Palindrome" : "Not palindrome");
    return 0;
}""",
    "s6.c": """// P15_S6: Matches ref1 (do-while variant)
#include <stdio.h>
#include <string.h>
#include <ctype.h>

int check(char s[]) {
    int l = 0, r = strlen(s) - 1;
    if (l < r) {
        do {
            if (tolower(s[l]) != tolower(s[r])) return 0;
            l++; r--;
        } while (l < r);
    }
    return 1;
}

int main() {
    printf("%s\\n", check("racecar") ? "Palindrome" : "Not palindrome");
    return 0;
}""",
    "s7.c": """// P15_S7: Matches ref2 (backward iteration)
#include <stdio.h>
#include <string.h>
#include <ctype.h>

int check(char str[]) {
    int n = strlen(str);
    char temp[100];
    for (int i = n-1, j = 0; i >= 0; i--, j++) temp[j] = tolower(str[i]);
    temp[n] = '\\0';
    for (int i = 0; i < n; i++)
        if (tolower(str[i]) != temp[i]) return 0;
    return 1;
}

int main() {
    printf("%s\\n", check("racecar") ? "Palindrome" : "Not palindrome");
    return 0;
}""",
    "s8.c": """// P15_S8: Matches ref1 (half-length optimization)
#include <stdio.h>
#include <string.h>
#include <ctype.h>

int check(char s[]) {
    int len = strlen(s);
    int i = 0, j = len - 1;
    while (i <= len/2 && i < j) {
        if (tolower(s[i++]) != tolower(s[j--])) return 0;
    }
    return 1;
}

int main() {
    printf("%s\\n", check("racecar") ? "Palindrome" : "Not palindrome");
    return 0;
}"""
}

# Create all files
problems = [
    ("p13", p13_students),
    ("p14", p14_students),
    ("p15", p15_students)
]

for problem, students in problems:
    for filename, code in students.items():
        path = f"data/{problem}/s/{filename}"
        create_file(path, code)
    print(f"✓ Created {problem} student variants (8 files)")

print("\n✅ Dataset expansion complete!")
print("📊 New totals:")
print("  - Problems: 15 (was 10)")
print("  - Students: 100 (was 60)")
print("  - References: 30 (was 23)")
print("  - Total files: 130 C programs")
