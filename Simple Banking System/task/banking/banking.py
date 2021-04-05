import numpy as np
import random
import sqlite3

conn = sqlite3.connect('card.s3db')
c = conn.cursor()



loop = True
loop2 = True
cards = np.array([["Cardno","Pin","Balance"],[0,0,0]])

def print_menu():
    print("""1. Create an account
2. Log into account
0. Exit""")

def print_menu2():
    print("""1. Balance
2. Log out
0. Exit""")

def luhn_checksum(num):
    numlist = [int(n) for n in reversed(str(num))]
    for n in range(0, len(numlist), 2):
        if (numlist[n] * 2) > 9:
            numlist[n] = (numlist[n] * 2) - 9
        else:
            numlist[n] = numlist[n] * 2
    return (sum(numlist)*9) % 10

def create_card():
    global cards
    rando = random.randint(100000000,999999999)
    MII = 400000
    cardno = str(MII) + str(rando)
    cardno = cardno + str(luhn_checksum(cardno))
    pin = random.randint(1000,9999)
    balance = 0
    c.execute(" INSERT INTO card VALUES ((SELECT MAX(id) FROM card)+1, ?, ?, ?) ", (cardno, pin, balance))
    conn.commit()
    print("Your card has been created")
    print("Your card number:")
    print(cardno)
    print("Your card PIN:")
    print(pin)

def loggedin(x):
    global loop2
    global loop
    while loop2:
        print_menu2()
        choice = input()
        if choice == "1":
            c.execute("SELECT balance FROM card WHERE number = ?", (x,))
            fetch = c.fetchall()
            print("Balance:",fetch[0][0])
        elif choice == "2":
            print("You have successfully logged out!")
            loop2 = False
        elif choice == "0":
            loop2 = False
            loop = False
        else:
            print("Incorrect Input")

def login():
    cardinput = int(input("Enter your card number:"))
    c.execute("SELECT id FROM card WHERE number = ?", (cardinput,))
    exists = c.fetchone()
    if exists is not None:
        pinenter = input("Enter your PIN:")
        c.execute("SELECT pin FROM card WHERE number = ?", (cardinput,))
        fetch = c.fetchall()
        correctpin = fetch[0][0]
        if correctpin == pinenter:
            print("You have successfully logged in!")
            loggedin(cardinput)

        else:
            print("Wrong card number or PIN!")
    else:
        print("Wrong card number or PIN!")

while loop:
    print_menu()
    choice = input()
    if choice == "1":
        create_card()
    elif choice == "2":
        login()
    elif choice == "0":
        loop = False
    else:
        print("Incorrect Input")