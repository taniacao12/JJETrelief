import sqlite3
import os

DIR = os.path.dirname(__file__) or '.'
DIR += '/../'

DB_FILE = DIR + "data/watchlist.db"

# ==================== Init ====================
def create_tables():
    """Creates tables for users' account info and watchlist."""
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    command = "CREATE TABLE user_info (username TEXT, password TEXT)"
    c.execute(command)

    command = "CREATE TABLE donations (username TEXT, place TEXT, mag INT, donation FLOAT)"
    c.execute(command)

    db.commit() #save changes
    db.close()  #close database

# create_tables()

# ==================== User Authentication ====================
#login / register routes
def add_user(username, password):
    """Insert the credentials for newly registered users into the database."""
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("INSERT INTO user_info VALUES(?, ?)", (username, password))
    db.commit() #save changes
    db.close()  #close database

def auth_user(username, password):
    """Authenticate user attempting to log in."""
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    for each in c.execute("SELECT user_info.username, user_info.password FROM user_info"):
        if(each[0] == username and each[1] == password):
            db.close()
            return True
    db.close()
    return False

def user_exist(username):
    """Check if a username has already been taken when registering."""
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    for each in c.execute("SELECT user_info.username FROM user_info"):
        if(each[0] == username):
            db.close()
            return True
    db.close()
    return False

# ==================== Watchlist ====================
def check_donations(user, place, mag, amt):
    """Check to see if the user already has the city in the watchlist."""
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    for each in c.execute("SELECT * FROM watchlist WHERE username =? ", (user,)):
        if(each[1] == place and each[2] == mag and each[3] == amt):
            print("already in wl")
            db.close()
            return True

    db.close()
    return False

def add_donations(user, place, mag, amt):
    """Insert a new watchlist city into the db for a user's watchlist."""
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    if (not check_watchlist(user, place, mag, amt)):
        c.execute("INSERT INTO watchlist VALUES(?, ?, ?, ?)", (user, place, mag, amt))

    db.commit()
    db.close()

def get_donations(user):
    """Get all the watchlist city for the user."""
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    data = []
    for each in c.execute("SELECT * FROM watchlist WHERE username =?", (user,)):
        # print (each)
        temp = []
        for i in range (1,len(each)):
            temp.append(each[i])
        data.append(temp)

    db.close()
    return data

# create_tables()
# add_watchlist("joyce","gz",30,20)
# add_watchlist("joyce","gz",20,30)
# add_watchlist("joyce","gz",20,30)
# add_watchlist("puneet","ny",10,10)
# add_watchlist("joyce","tx",30,30)
# remove_watchlist("joyce", "gz",30,20)
# print(get_watchlist("joyce"))
