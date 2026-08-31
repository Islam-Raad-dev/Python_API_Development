from argon2 import PasswordHasher

ph = PasswordHasher()

def Hash(password: str):
    salt = "b_x1bdx80+x1dxdxcaMxd4x81x06qxc7R"
    password_with_salt = salt + password
    return ph.hash(password_with_salt)

