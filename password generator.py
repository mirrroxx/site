import random
import string


def generate_password():
    digits = ''.join(random.choices(string.digits, k=8))
    uppercase_letter = random.choice(string.ascii_uppercase)
    lowercase_letter = random.choice(string.ascii_lowercase)
    password = digits + uppercase_letter + lowercase_letter
    password_list = list(password)
    random.shuffle(password_list)
    password = ''.join(password_list)
    for i in range(len(password) - 2):
        if password[i] == password[i + 1] == password[i + 2]:
            password = password[:i + 2] + str((int(password[i + 2]) + 1) % 10) + password[i + 3:]
    return password