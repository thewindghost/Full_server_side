import sqlite3

connection = sqlite3.connect('database.db')

curr = connection.cursor()

curr.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    email TEXT NOT NULL,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    number_phone TEXT NOT NULL,
    website_company TEXT NOT NULL,
    birth_year INTEGER NOT NULL,
    is_admin INTEGER DEFAULT 0,
    is_root INTEGER DEFAULT 0
)
''')

curr.execute('''
INSERT OR IGNORE INTO users (username, password, email, first_name, last_name, number_phone, website_company, birth_year, is_root) VALUES ("root", "root123", "root@codetoanbug.com", "Root", "User", "092316186", "coding.codetoanbug.com", 1980, 1)
''')

curr.execute('''
INSERT OR IGNORE INTO users (username, password, email, first_name, last_name, number_phone, website_company, birth_year, is_admin) VALUES ("admin", "admin123", "admin@codetoanbug.com", "Admin", "User", "098285213", "labs.codetoanbug.com", 1985, 1)
''')

curr.execute('''
INSERT OR IGNORE INTO users (username, password, email, first_name, last_name, number_phone, website_company, birth_year) VALUES ("guest", "guest123", "guest@codetoanbug.com", "Guest", "User", "095358553", "codetoanbug.com", 1990)
''')

connection.commit()
connection.close()
