from random import randint
import sqlite3


class Bank:
    def __init__(self):
        self.logged_in = False
        self.conn = sqlite3.connect('card.s3db')
        self.cur = self.conn.cursor()
        self.create_table()
        self.menu()

    def create_table(self):
        sql_create_card_table = """CREATE TABLE IF NOT EXISTS card (id INTEGER, number TEXT,
        pin TEXT, balance INTEGER DEFAULT 0); """
        self.cur.execute(sql_create_card_table)
        self.conn.commit()

    def create_card(self, id_, number, pin, balance):
        sql_insert_card = """INSERT INTO card (id, number, pin, balance) VALUES (?, ?, ?, ?); """
        data_tuple = (id_, number, pin, balance)
        self.cur.execute(sql_insert_card, data_tuple)
        self.conn.commit()

    def gen_id(self):
        query = """SELECT id FROM card ORDER BY id DESC LIMIT 1;"""
        self.cur.execute(query)
        records = self.cur.fetchall()
        try:
            return records[0][0] + 1
        except IndexError:
            return 1

    def read_card(self, card, pin):
        query = """SELECT number, pin FROM card WHERE number = ? AND pin = ?"""
        data_tuple = (card, pin)
        self.cur.execute(query, data_tuple)
        rows = self.cur.fetchone()
        return rows

    def check_card(self, card):
        query = """SELECT count(number) FROM card WHERE number = ?"""
        data_tuple = (card,)
        self.cur.execute(query, data_tuple)
        rows = self.cur.fetchone()
        return rows[0] == 1

    def menu(self):
        while not self.logged_in:
            print('1. Create an account\n2. Log into account\n0. Exit')
            choice = input()
            if choice == '1':
                self.create()
            elif choice == '2':
                self.login()
            elif choice == '0':
                print('\nBye!')
                self.cur.close()
                self.conn.close()
                quit()

    def account_menu(self, card):
        while self.logged_in:
            print('1. Balance\n2. Add income\n3. Do transfer\n4. Close account\n5. Log out\n0. Exit')
            choice = input()
            if choice == '1':
                print('\nBalance: ', self.check_balance(card))
            elif choice == '2':
                print('\nEnter income:')
                income = input()
                self.add_income(card, income)
            elif choice == '3':
                self.transfer_check(card)
            elif choice == '4':
                self.close_account(card)
                print('The account has been closed!')
            elif choice == '5':
                self.logged_in = False
                print('\nYou have successfully logged out!\n')
            elif choice == '0':
                print('\nBye!')
                self.cur.close()
                self.conn.close()
                quit()

    def create(self):
        print()
        id_ = self.gen_id()
        card = self.luhn_alg()
        pin = str.zfill(str(randint(0000, 9999)), 4)
        self.create_card(id_, card, pin, 0)
        print(f'Your card has been created\nYour card number:\n{card}\nYour card PIN:\n{pin}\n')

    def login(self):
        print('\nEnter your card number:')
        card = input()
        print('Enter your PIN:')
        pin = input()
        cards = self.read_card(card, pin)
        if cards:
            print('\nYou have successfully logged in!\n')
            self.logged_in = True
            self.account_menu(card)
        else:
            print('\nWrong card number or Pin!\n')

    def luhn_alg(self):
        card = '400000' + str.zfill(str(randint(000000000, 999999999)), 9)
        card_check = [int(i) for i in card]
        for index, _ in enumerate(card_check):
            if index % 2 == 0:
                card_check[index] *= 2
            if card_check[index] > 9:
                card_check[index] -= 9
        check_sum = str((10 - sum(card_check) % 10) % 10)
        card += check_sum
        return card

    def luhn_checksum(self, card):
        def digits_of(n):
            return [int(d) for d in str(n)]
        digits = digits_of(card)
        odd_digits = digits[-1::-2]
        even_digits = digits[-2::-2]
        checksum = 0
        checksum += sum(odd_digits)
        for d in even_digits:
            checksum += sum(digits_of(d * 2))
        return checksum % 10

    def is_luhn_valid(self, card):
        return self.luhn_checksum(card) == 0

    def check_balance(self, card):
        query = """SELECT balance FROM card WHERE number = ?"""
        data_tuple = (card,)
        self.cur.execute(query, data_tuple)
        rows = self.cur.fetchone()
        return rows[0]

    def add_income(self, card, income):
        query = """UPDATE card SET balance = balance + ? WHERE number = ?"""
        data_tuple = (income, card)
        self.cur.execute(query, data_tuple)
        self.conn.commit()
        print("Income was added!\n")

    def close_account(self, card):
        query = """DELETE FROM card WHERE number = ?"""
        data_tuple = (card,)
        self.cur.execute(query, data_tuple)
        self.conn.commit()

    def transfer(self, card, payee, amount):
        query1 = """UPDATE card SET balance = balance - ? WHERE number = ?"""
        query2 = """UPDATE card SET balance = balance + ? WHERE number = ?"""
        data_tuple1 = (amount,card)
        data_tuple2 = (amount,payee)
        self.cur.execute(query1, data_tuple1)
        self.conn.commit()
        self.cur.execute(query2, data_tuple2)
        self.conn.commit()
        print("Success!")

    def transfer_check(self, card):
        print("\nTransfer")
        print("Enter card number:")
        payee = input()
        if card == payee:
            print("You can't transfer money to the same account!")
        elif not self.is_luhn_valid(payee):
            print("Probably you made a mistake in the card number. Please try again!")
        elif not self.check_card(payee):
            print("Such a card does not exist.")
        else:
            print("Enter how much money you want to transfer:")
            amount = input()
            if int(amount) > int(self.check_balance(card)):
                print("Not enough money!")
            else:
                self.transfer(card, payee, amount)


if __name__ == '__main__':
    stage_3 = Bank()
