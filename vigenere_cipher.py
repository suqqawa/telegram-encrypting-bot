def encrypt_vigenere(text: str, key: str) -> str:
    result = ""
    key = key.upper()
    key_length = len(key)
    
    for i in range(len(text)):
        char = text[i]
        if char.isalpha():
            if 'А' <= char.upper() <= 'Я':
                base = ord('А') if char.isupper() else ord('а')
                key_shift = ord(key[i % key_length]) - ord('А')
                shifted = (ord(char) - base + key_shift) % 32 + base
                result += chr(shifted)
            else:
                base = ord('A') if char.isupper() else ord('a')
                key_shift = ord(key[i % key_length]) - ord('A')
                shifted = (ord(char) - base + key_shift) % 26 + base
                result += chr(shifted)
        else:
            result += char
    return result

def decrypt_vigenere(text: str, key: str) -> str:
    result = ""
    key = key.upper()
    key_length = len(key)
    
    for i in range(len(text)):
        char = text[i]
        if char.isalpha():
            if 'А' <= char.upper() <= 'Я':
                base = ord('А') if char.isupper() else ord('а')
                key_shift = ord(key[i % key_length]) - ord('А')
                shifted = (ord(char) - base - key_shift) % 32 + base
                result += chr(shifted)
            else:
                base = ord('A') if char.isupper() else ord('a')
                key_shift = ord(key[i % key_length]) - ord('A')
                shifted = (ord(char) - base - key_shift) % 26 + base
                result += chr(shifted)
        else:
            result += char
    return result
