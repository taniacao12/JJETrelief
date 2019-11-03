# JJETrelief

## Team
Tania Cao, Joyce Fang, Jody Sunray, Elaine Shi

## Project Overview
Send help. Get help.  
JJETrelief focuses on underrepresented communities affected by natural disasters all over the world. The website updates the status of these communities in real time and gives you the option to donate money if you wish. You may also customize what you wish to see based on the date.

### Launch Instructions
#### Install and run on localhost
1. Go to [root repository](https://github.com/puneetjohal/ShrimpCrackers/) and click "Clone or Download" button
2. Copy the ssh/https link and run `$ git clone <link>`
3. Make sure the latest version of Python (currently Python 3.7.1) is installed. If not, download it [here](https://www.python.org/downloads/).
4. Install virtualenv by running `$ pip install virtualenv`
   * Make a venv by running `$ python3 -m venv path_to_venv`
   * Activate it by running `$ . /path_to_venv/bin/activate`
   * Deactivate it by running `$ deactivate`
5. Move into the JJETrelief directory: `$ cd JJETrelief/`
6. **With your virtual environment activated**, download all of the app's dependencies by running
```
 (venv)$ pip install -r requirements.txt
```
7. Run `$ python app.py`
8. Launch the root route (http://127.0.0.1:5000/) in your browser to go to the login page.

#### API information
##### GeoJSON
*  [GeoJSON](https://earthquake.usgs.gov/earthquakes/feed/v1.0/geojson.php) is a format for encoding a variety of geographic data structures. A GeoJSON object may represent a geometry, a feature, or a collection of features.