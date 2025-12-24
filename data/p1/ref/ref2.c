int sum(int *arr, int len) {
    int total = 0;
    int i = 0;
    while (i < len) {
        total = total + arr[i];
        i++;
    }
    return total;
}
