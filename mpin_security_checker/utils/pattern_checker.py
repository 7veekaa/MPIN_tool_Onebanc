def get_pattern_type(mpin):
    famous_numbers = {'2020', '1947', '2000', '1999', '7777', '123456', '1515', '202020'}

    # Ensure string type
    mpin = str(mpin)

    # Sequential pattern check (forward or reverse)
    if mpin in "0123456789" or mpin in "9876543210":
        return "Sequential"

    # Repeated digits check
    if all(ch == mpin[0] for ch in mpin):
        return "Repeated Digits"

    # Keypad patterns (basic examples — can expand)
    if mpin in ["2580", "1478", "1593", "7531", "258025", "147852", "159357"]:
        return "Keypad Patterns"

    # Mirror/Symmetry (like 1221 or 123321)
    if mpin == mpin[::-1]:
        return "Mirror/Symmetry"

    # Alternating digits (abab or ababab)
    if len(mpin) >= 4 and all(mpin[i] == mpin[i % 2] for i in range(len(mpin))):
        return "Alternating"

    # Doublets (aabb or aabbcc)
    if (len(mpin) == 4 and mpin[:2] == mpin[0]*2 and mpin[2:] == mpin[2]*2) or \
       (len(mpin) == 6 and mpin[:2] == mpin[0]*2 and mpin[2:4] == mpin[2]*2 and mpin[4:] == mpin[4]*2):
        return "Doublets"

    # Famous / culturally known numbers
    if mpin in famous_numbers:
        return "Special/Other"

    # If no match
    return "Random"
