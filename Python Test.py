#Mustafa Milad Ahmed, (C)group
import os
dict1 = {
    "username": "aliahmed",
    "password": "12345678",
    "name": "Ali Ahmed",
    "email": "ali@gmail.com"
}
attempts = 0
while attempts < 3:
    user = input("Enter username: ")
    pas = input("Enter pass: ")
    if user == dict1["username"] and pas == dict1["password"]:
        print("Login successful!")
        print(dict1)
        break
    else:
        attempts += 1
        print(f"Wrong credentials! Attempts left: {3 - attempts}")
if attempts == 3:
    dict1.clear()
    os.system('clear')
    print("Too many failed attempts. Dictionary emptied!")
    print(dict1)
