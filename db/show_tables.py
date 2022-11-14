import sqlite3
import os

db_abs_path = os.path.dirname(os.path.realpath(__file__)) + '/quizwiz.db'

print("Options: (cards,all)")
table = input("Show table: ")

conn = sqlite3.connect(db_abs_path)
c = conn.cursor()


def show_cards():
    try:
        cards = c.execute("""SELECT
                                    c.question, c.answer
                                 FROM
                                    cards AS c                                 
        """)

        print("CARDS")
        print("#############")
        for row in cards:
            print("Question:", row[0]),
            print("Answer: ", row[1]),
            print("\n")
    except:
        print("Something went wrong, please run db_init.py to initialize the database.")
        conn.close()


if table == "cards":
    show_cards()
elif table == "all":
    show_cards()
else:
    print("This option does not exist.")

conn.close()
