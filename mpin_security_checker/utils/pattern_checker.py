def get_pattern_type(mpin):
    famous_numbers = {'2020', '1947', '2000', '1999', '7777', '123456', '1515', '202020'}


    mpin = str(mpin)


    if mpin in "0123456789" or mpin in "9876543210":
        return "Sequential"


    if all(ch == mpin[0] for ch in mpin):
        return "Repeated Digits"

    if mpin in ["2580", "1478", "1593", "7531", "258025", "147852", "159357"]:
        return "Keypad Patterns"

    if mpin == mpin[::-1]:
        return "Mirror/Symmetry"

    if len(mpin) >= 4 and all(mpin[i] == mpin[i % 2] for i in range(len(mpin))):
        return "Alternating"

    if (len(mpin) == 4 and mpin[:2] == mpin[0]*2 and mpin[2:] == mpin[2]*2) or \
       (len(mpin) == 6 and mpin[:2] == mpin[0]*2 and mpin[2:4] == mpin[2]*2 and mpin[4:] == mpin[4]*2):
        return "Doublets"


    if mpin in famous_numbers:
        return "Special/Other"


    return "Random"
