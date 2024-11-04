import time
PESEL_WEIGHT = (1, 3, 7, 9, 1, 3, 7, 9, 1, 3)
PESEL_LENGTH = 11
MONTH = [1, 2, 3, 5, 7, 8, 10, 12]
# Months in which max no. of days is not 30 days


start = time.time()

# counters
total = correct = male = female = 0
invalid_length = invalid_digit = invalid_date = invalid_checksum = 0

file = open("1e6.dat", 'r')

# main processing loop
for pesel in file:
    pesel = pesel.strip()
    total += 1
# check if right lenght
    if len(pesel) != 11:
        invalid_length += 1
        continue
# check if is a digit
    if not pesel.isdigit():
        invalid_digit += 1
        continue
    yy = int(pesel[:2])
    m1 = int(pesel[2:3])
    m2 = int(pesel[3:4])
    dd = int(pesel[4:6])
    nnn = int(pesel[6:9])
    x = int(pesel[9:10])
    c = int(pesel[10:11])
# calculate month
    if m1 % 2 == 0:
        month = m2
    else:
        month = 10 + m2
# check month
    if month == 0 or month > 12:
        invalid_date += 1
        continue
# check day
    if dd == 0 or dd > 31:
        invalid_date += 1
        continue
    elif month not in MONTH:
        if dd > 30:
            invalid_date += 1
            continue
    elif month == 2:
        # february in years divisable by 4
        if yy % 4 == 0:
            if dd > 29:
                invalid_date += 1
                continue
        else:
            # february in years not divisable by 4
            if dd > 28:
                invalid_date += 1
                continue
# check checksum
    checksum = 0
    for i in range(PESEL_LENGTH - 1):
        checksum += PESEL_WEIGHT[i] * int(pesel[i])
    checksum = (10 - (checksum % 10)) % 10
    if checksum != c:
        invalid_checksum += 1
        continue

    correct += 1
# male or female
    if x % 2 == 0:
        female += 1
    else:
        male += 1

file.close()
# show results
print(total, correct, female, male)
print(invalid_length, invalid_digit, invalid_date, invalid_checksum)
print("Runtime [s]= ", time.time()-start)
