import time

def G(k, r, s, p, dynamic = False, found = []):
    if dynamic:
        if found[k][r] > 0:
            return found[k][r]
    if (k == 0 or r == 0):
        if dynamic:
            found[k][r]=0
        return 0
    elif (s[k] > r):
        number = G(k-1, r, s, p, dynamic, found)
        if dynamic:
            found[k][r] = number
        return number
    else:
        number1 = G(k-1, r, s, p, dynamic, found)
        number2 = G(k-1, r-s[k], s, p, dynamic, found) + p[k]
        if dynamic:
            found[k-1][r] = number1
            found[k-1][r-s[k]] = number2
        return max([number1, number2])

found = [[0 for i in range(10)] for j in range(10)]
s = [4, 5, 7, 3, 8, 6, 4, 8, 9, 0]
p = [2, 8, 6, 4, 7, 2, 5, 5, 11, 21]
num = G(9, 8, s, p, True, found)
print(num)
print(found)
