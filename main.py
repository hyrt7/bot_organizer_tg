a = input()
maxi = []
for i in range(9999, 1001, -1):
    b = []
    b.append(int(str(i)[0]) + int(str(i)[1]))
    b.append(int(str(i)[1]) + int(str(i)[2]))
    b.append(int(str(i)[2]) + int(str(i)[3]))
    b.sort()
    c = str(b[1]) + str(b[2])
    if c == a:
        maxi.append(i)

print(max(maxi))