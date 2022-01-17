def encrypt(key, plaintext):
    ciphertext = ""
    incre = key % 26

    for c in plaintext:
        num = ord(c)

        if num >=65 and num <=90:
            num += incre
            if num > 90:
                num -= 26

        ciphertext += chr(num)

    return ciphertext


def decrypt(key, ciphertext):
    plaintext = ""
    decre = key % 26

    for c in ciphertext:
        num = ord(c)

        if num >= 65 and num <= 90:
            num -= decre
            if num < 65:
                num += 26

        plaintext += chr(num)
    return plaintext
