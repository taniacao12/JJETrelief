# JJETrelief

## Team
Tania Cao, Joyce Fang, Jody Sunray, Elaine Shi

## Inspiration
We noticed that only a certain few news stories grab the attention of the general population. Natural disasters are only one example of those stories that go unheard. With temperatures on the rise and a rapidly changing climate, we should be paying more attention to natural disasters.
 
JJETrelief focuses on underrepresented communities affected by natural disasters all over the world. The website updates the status of these communities in real time and gives you the option to donate money if you wish. You may also customize what you wish to see based on the date.

## How we built it
We started off learning the basics: setting up the repository, learning the basic commands/syntax of different languages, navigating the documentation of those languages, and having a long brainstorming session. Once we had our idea, we put together a site map and component map to help guide us through the project. Joyce and Jody focused on the front-end portion, while Tania and Elaine worked on the back-end.

## What we learned
It was the first time doing a hackathon for most of our team. It was also most of our first time using Github and the command prompt.

We improved our coding skills, and got a taste of Bootstrap and SQLite. Though many of us had difficulties with the programming aspect, we all found our own way to contribute to the final product.

We learned how to use Github and how to set up a virtual environment. We went through the process of creating a dynamic website. Under the time pressure, we learned to efficiently collaborate with each other and make use of each individual's strengths.

## Launch Instructions
### Install and run on localhost
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

### API information
#### GeoJSON
*  [GeoJSON](https://earthquake.usgs.gov/earthquakes/feed/v1.0/geojson.php) is a format for encoding a variety of geographic data structures. A GeoJSON object may represent a geometry, a feature, or a collection of features.