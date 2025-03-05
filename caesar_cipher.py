def encrypt_caesar(text: str, shift: int = 3) -> str:
    result = ''
    for char in text:
        if char.isalpha():
            base = ord('А') if char.isupper() else ord('а')
            if 'А' <= char <= 'я':
                result += chr((ord(char) - base + shift) % 32 + base)
            else:
                base = ord('A') if char.isupper() else ord('a')
                result += chr((ord(char) - base + shift) % 26 + base)
        else:
            result += char
    return result

def decrypt_caesar(text: str, shift: int = 3) -> str:
    return encrypt_caesar(text, -shift)
