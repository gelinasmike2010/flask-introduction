import sqlite3

# connect to the database
with sqlite3.connect("sample.db") as connection:
    c = connection.cursor()
    c.execute("DROP TABLE posts")
    c.execute("CREATE TABLE posts(title TEXT, description TEXT)")
    c.execute("INSERT INTO posts VALUES("Good", "I\'m good.")")
    c.execute("INSERT INTO posts VALUES("Good", "I am good.")")
