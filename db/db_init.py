import sqlite3
import os

db_abs_path = os.path.dirname(os.path.realpath(__file__)) + '/quizwiz.db'
conn = sqlite3.connect(db_abs_path)
c = conn.cursor()

c.execute("DROP TABLE IF EXISTS cards")

c.execute("""CREATE TABLE cards(
                    id              INTEGER PRIMARY KEY AUTOINCREMENT,
                    question        TEXT NOT NULL,
                    answer          TEXT NOT NULL
)""")


cards = [
    ("CH4", "methane"),
    ("C2H6", "ethane"),
    ("C3H8", "propane"),
    ("C4H10", "butane")
]
c.executemany("INSERT INTO cards (question,answer) VALUES (?,?)", cards)


conn.commit()
conn.close()

print("Database is created and initialized.")
print("You can see the tables with the show_tables.py script.")
