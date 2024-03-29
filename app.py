import os
from flask import Flask, render_template, request, flash, session, url_for, redirect
from util import db, disaster

from datetime import datetime, date, timedelta

app = Flask(__name__)
app.secret_key = "super secret key"

@app.route("/")
def home():
	if "logged_in" in session:
		data = db.get_donations(session["logged_in"])
		return render_template("home.html", title = "Home", heading = "Hello " + session["logged_in"] + "!", user = session["logged_in"], logged_in = True)
	return render_template("home.html", title = "Home", logged_in = False)

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
	display = current.strftime("%A, %b %d %Y")
	d = current.strftime("%Y-%m-%d")
	prev = prev.strftime("%Y-%m-%d")
	try:
		data = disaster.getDate(prev, current)
		for each in data:
			data[each].append(format(db.get_funding(each), '.2f'))
	except:
		flash("Sorry, an error has occurred while retrieving information.")
		return redirect(url_for("home"))
	return render_template("info.html", display = display, d = d, date = current, content = data, logged_in = status, title = "Today's Earthquakes", heading = "Today's Earthquakes")

# ================info================
@app.route("/search")
def load_info():
	status = "logged_in" in session
	date = request.args["date"].split('-')
	if (date == ['']):
		flash("Please enter a date.")
		return render_template("home.html", logged_in=status)
	endDate = datetime(int(date[0]), int(date[1]), int(date[2]))
	startDate = endDate - timedelta(1)
	date = endDate.strftime("%Y-%m-%d")
	display = endDate.strftime("%A, %b %d %Y")
	startDate = startDate.strftime("%Y-%m-%d")
	try:
		data = disaster.getDate(startDate, date)
		for each in data:
			data[each].append(format(db.get_funding(each), '.2f'))
	except:
		flash("Sorry, an error has occurred while retrieving information.")
		return redirect(url_for("home"))
	return render_template("info.html", title = "Earthquakes from " + display, heading = "Earthquakes from " + display, display = display, date = endDate, d = date, content = data, logged_in = status)

# ================donate================
@app.route("/donate")
def donate():
	status = "logged_in" in session
	if status:
		display = request.args["display"]
		date = request.args["date"]
		d = request.args["d"]
		place = request.args["place"]
		mag = request.args["mag"]
		return render_template("donate.html", title = "Donate", heading = "Donate", display = display, date = date, d = d, place = place, mag = mag, logged_in = status)
	else:
		flash ("Please login to donate")
		return render_template("login.html", title = "Login", heading = "Login")

@app.route("/donations")
def getDonations():
	status = "logged_in" in session
	if status:
		data = db.get_donations(session["logged_in"])
		return render_template("donations.html", title = "Donations", heading = "Donations", content = data, logged_in = status)
	else:
		flash ("Please login to view Watchlist")
		return render_template("login.html", title = "Login", heading = "Login")

@app.route("/change_donations", methods = ["GET", "POST"])
def change_donations():
	try:
		place = request.args["place"]
		mag = request.args["mag"]
		amt = request.args["amount"]
		db.add_donations(session["logged_in"], place, mag, amt)
	except:
		flash("failed to add location to database")
	date = request.args["d"]
	return redirect(url_for("load_info", date = date))

# ================partnerships================
@app.route("/partnerships")
def partnership():
	status = "logged_in" in session
	return render_template("/partnerships.html", title = "Our Partners", heading = "Our Partners", logged_in = status)

# ================my donations================
@app.route("/mydonations")
def mydonations():
	status = "logged_in" in session
	return render_template("/mydonations.html", title = "My Donations", heading = session["logged_in"] + "'s Donations", logged_in = status)

if __name__ == "__main__":
        app.debug = True
        app.run()
