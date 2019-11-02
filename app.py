import os

from flask import Flask, render_template, request, flash, session, url_for, redirect

from util import db, coord, climate, ip, weather

app = Flask(__name__)

app.secret_key=os.getenv('SECRET_KEY', 'for dev')

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

# ================Watchlist================
@app.route("/watchlist")
def load_wl():
    status = "logged_in" in session
    if status:
        locations = db.get_watchlist(session["logged_in"])
        #print(locations)
        return render_template("watchlist.html", title = "Watchlist", heading = "Watchlist", watchlist = locations, logged_in=status)
    else:
        flash ("Please login to view Watchlist")
        return render_template("login.html", title = "Login", heading = "Login")

@app.route("/change_wl", methods = ["GET", "POST"])
def change_wl():
	try:
	    city = request.args["city"]
	    state = request.args["state"]
	    county = request.args["county"]
	    lat = request.args["lat"]
	    longi = request.args["long"]
	    if request.args["update"] == "Add to watchlist":
	        db.add_watchlist(session["logged_in"], city, county, state, lat, longi)
	    elif request.args["update"] == "Remove from watchlist":
	        db.remove_watchlist(session["logged_in"], city, county, state, lat, longi)
	except:
		flash("failed to add location to watchlist")
	page = request.args["page"]
	if page == "watchlist":
		return redirect(url_for("load_wl"))
	elif page == "info":
		return redirect(url_for("load_info", city = city, county = county, state = state, lat = lat, long = longi))
	else:
		location = request.args["search_location"]
		return redirect(url_for("load_results", search_location=location))

# ================search================
@app.route("/search")
def load_results():
    status = "logged_in" in session
    location = request.args["search_location"].strip()
    if (location == ""):
        flash ("Please enter a location")
        return render_template("search.html", title = "Try Again", heading = "Please Try Again", logged_in=status)
    result = coord.getOptions(location)
    if (len(result) < 1):
        flash ("No location found. Please try again.")
        return render_template("search.html", title = "Try Again", heading = "Please Try Again", logged_in=status)
    on_watchlist = {}
    if "logged_in" in session:
        for each in result:
            #print(each)
            on_watchlist[each[1]] = db.check_watchlist(session["logged_in"], each[0], each[1], each[2], str(each[4]), str(each[5]))
    #print(on_watchlist)
    return render_template("search.html", title = "Search Results", heading = "Search Results for \"" + location + "\"", result=result, on_watchlist=on_watchlist, logged_in=status, target=location)

# ================info================
@app.route("/info")
def load_info():
    status = "logged_in" in session
    # locations = db.get_watchlist(status)
    city = request.args["city"]
    county = request.args["county"]
    state = request.args["state"]
    lat = request.args["lat"]
    longi = request.args["long"]
    try:
        data = climate.getSearchInfo(city, county, state)
        weather_data = weather.get_info(lat, longi)
    except:
        flash("Sorry, an error has occurred while retriving information.")
        return redirect(url_for("home"))
    avg_temp = data[0]
    precip = data[1]
    on_watchlist = False
    if "logged_in" in session:
        on_watchlist = db.check_watchlist(session["logged_in"], city, county, state, lat, longi)
    return render_template("info.html", title = city + ", " + state, heading = city + ", " + state, logged_in = status, lat=lat, long=longi, city=city, state = state, county=county, tavg_data=avg_temp, on_watchlist=on_watchlist, prcp_data=precip, weather_data=weather_data)

# ================My Location================
@app.route("/current")
def load_current():
    status = "logged_in" in session
    location = ip.get_coord()
	# print(location)
    country = location['country_code']
    if country != "US":
        flash("'My location' feature is currently not supported for locations outside of the U.S.")
        return redirect(url_for("home"))
    state = location["region_code"]
    city = location['city']
    lat = location['latitude']
    longi = location['longitude']
    try:
        county = coord.getCounty(city, state)
        data = climate.getSearchInfo(city, county, state)
        weather_data = weather.get_info(lat, longi)
    except:
        flash("Sorry, an error has occurred while retriving information.")
        return redirect(url_for("home"))
    avg_temp = data[0]
    precip = data[1]
    on_watchlist = False
    if "logged_in" in session:
        on_watchlist = db.check_watchlist(session["logged_in"], city, county, state, lat, longi)
    return render_template("info.html", title = city + ", " + state, heading = city + ", " + state, logged_in = status, lat=lat, long=longi, city=city, state = state, county=county, tavg_data=avg_temp, on_watchlist=on_watchlist, prcp_data=precip, weather_data=weather_data)

if __name__ == "__main__":
        app.debug = True
        app.run()
