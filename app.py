import os
from flask import Flask, render_template, request, flash, session, url_for, redirect
from util import db, disaster

from datetime import datetime, date, timedelta

app = Flask(__name__)

@app.route("/")
def home():
	if "logged_in" in session:
		data = db.get_watchlist(session["logged_in"])
		return render_template("home.html", title = "Home", heading = "Hello " + session["logged_in"] + "!", user = session["logged_in"], logged_in = True)
	return render_template("home.html", title = "Home", heading = "Hello Guest!", logged_in = False)

# ================Accounts================
@app.route("/auth", methods = ["GET", "POST"])
def auth():
	return_page = "home"

	for each in request.form:
		if request.form[each] == "Login":
			return_page = each

	given_user = request.form["username"]
	given_pwd = request.form["password"]
	if db.auth_user(given_user, given_pwd):
		session["logged_in"] = given_user
		return redirect(url_for(return_page))
	else:
		flash("Username or password is incorrect")
		return redirect(url_for("login"))

@app.route("/login", methods = ["GET", "POST"])
def login():
    return render_template("login.html", title = "Login", heading = "Login")

#Sends the user to the register.html to register a new account
@app.route("/register")
def register():
	return render_template("register.html", title = "Register", heading = "Register")

#Attempts to add the user to the database
@app.route("/adduser")
def add_user():
    if(not request.args["user"].strip() or not request.args["password"] or not request.args["confirm_password"]):
            flash("Please fill in all fields")
            return redirect(url_for("register"))

    if(db.user_exist(request.args["user"])):
            flash("User already exists")
            return redirect(url_for("register"))

    if(request.args["password"] != request.args["confirm_password"]):
            flash("Passwords don't match")
            return redirect(url_for("register"))

    db.add_user(request.args["user"], request.args["password"])
    session["logged_in"] = request.args["user"]
    return redirect(url_for("home"))

#Logs the user out and removes session
#returns to the page the user was on previously
@app.route("/logout")
def logout():
	if session.get("logged_in"):
		session.pop("logged_in")
	return redirect(url_for("home"))

@app.route("/current")
def load_current():
	status = "logged_in" in session
	current = date.today()
	prev = current - timedelta(1)
	try:
		data = disaster.getDate(prev, current)
	except:
		flash("Sorry, an error has occurred while retriving information.")
		return redirect(url_for("home"))
	return render_template("info.html", content = data, logged_in = status, title = "Today")

# ================info================
@app.route("/search")
def load_info():
	status = "logged_in" in session
	month = int(request.args["month"])
	day = int(request.args["day"])
	year = int(request.args["year"])
	endDate = datetime(year, month, day)
	startDate = endDate - timedelta(1)
	try:
		data = disaster.getDate(startDate, endDate)
	except:
		flash("Sorry, an error has occurred while retriving information.")
		return redirect(url_for("home"))
	return render_template("info.html", content = data, logged_in = status)

# ================donate================
@app.route("/donate")
def donate():
	return render_template("donate.html", title = "Donate", heading = "Donate")

if __name__ == "__main__":
        app.debug = True
        app.run()
