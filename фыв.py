for i in range(1, 100):
    a = bin(i)[2:]
    if a.count('1') % 2 == 0:
        a += '00'
    else:
        a += '10'
    if int(a, 2) > 77:
        print(int(a, 2))
        break