int sum(int *x, int n) {
    int result = 0;
    for (int k = 0; k < n; k++) {
        result = result + x[k];
    }
    return result;
}
