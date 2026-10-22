# and / or / not, plus truthiness of "" and 0.
username = "lan"
password = "secret123"
attempts = 2

has_name = username != ""
long_password = len(password) >= 8

if has_name and long_password:
    print("Credentials look valid")

if attempts >= 3 or not has_name:
    print("Locked")
else:
    print(f"{3 - attempts} attempt(s) left")

nickname = ""
if nickname:
    print(f"Hi, {nickname}")
else:
    print("Hi, stranger")

print(bool(""), bool("a"), bool(0), bool(5))
