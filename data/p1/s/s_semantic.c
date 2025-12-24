#include <stdio.h>

int compute(int x, int y) {
    int z = x + y;          // def-use (x,y -> z)

    if (z > 10) {           // control predicate
        printf("%d\n", z);  // parameter -> output via z
        return z;           // parameter -> return (via def-use)
    }

    for (int i = 0; i < x; i++) {   // loop
        z += i;                     // def-use
    }

    return z;
}
