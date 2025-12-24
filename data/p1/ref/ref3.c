int sum(int *a, int n) {
    int s = 0;
    for (int i = 0; i < n; i++) {
        s = 0;
        for (int j = 0; j <= i; j++) {
            s += a[j];
        }
    }
    return s;
}
