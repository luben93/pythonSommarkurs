def mystery(m, n):
    if (m < n):
        return 1 + mystery(m + 1, n)
    return 5

print(mystery(2, 3))