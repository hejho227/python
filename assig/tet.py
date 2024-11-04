file = open("tet.txt", 'r')
for pesel in file:
    pesel = pesel.strip()
    PESEL_LENGTH = 11
    PESEL_WEIGHT = (1, 3, 7, 9, 1, 3, 7, 9, 1, 3)
    checksum = 0
    for i in range(PESEL_LENGTH - 1):
        checksum += PESEL_WEIGHT[i] * int(pesel[i])
    checksum = (10 - (checksum % 10)) % 10
    if checksum == int(pesel[10]):
        print("Verification: Pass")
    else:
        print("Verification: Fail")
