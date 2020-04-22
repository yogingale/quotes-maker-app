## Flask Starter

This project will be a starter project using Flask and creative-tim.com themes called:

[Get SH IT done](https://www.creative-tim.com/product/get-shit-done-kit)

[Paper Kit 2](https://www.creative-tim.com/product/paper-kit-2)

[Paper Dashboard 2](https://www.creative-tim.com/product/paper-dashboard-2)

This project will use flask-login, blueprints for a basic starter with a login and a landing page.  It will not use a database but this can be added later.

When you navigate to the index page: localhost:5000 if you are running a typical flask web server, if you are not logged in you will be redirected to the login page.  Once logged in you are navigated back to the index page.

From the index page, you are able to transition to another page, served from another blueprint.  Just a simple way to show navigating between blueprints and to make sure the static url resolution was working.


### Features

- Login required
- Role based access of routes
- Protected routes
- Simple navigation between pages
- Integration with Vue.js and axios (Paper Dashboard2)

#### Paper Dashboard 2
This template has Vue.js integrated into it and Axios for remote Ajax calls to the Flask server.  The Vue.js integration is a light integration at the Jinja template level.  It is meant to be a very light touch way to get the benefits of Vue.js while still leverage the more traditional Jinja template approach.


## Assumptions

  1) Python3 is installed

## Setup and Install
The flask_starter project uses a number of different python packages.  The best way to install everything is the following:

  1) cd to directory where you want to hold the project
  2) git clone https://github.com/youngsoul/flask_starter
  3) cd flask_start
  4) python3 -m venv venv
  5) source venv/bin/activate
  6) pip install -r requirements.txt

## Run

To start the server.
python main.py

## Themes

This project has three CreativeTim (www.creative-tim.com) themes that can be used.

In *config.py* there are three configuration parameters to set the theme:

**CONTENT_DIR**
This is the name of the content directory that will be in *templates* and *static*.

Changing the value of the CONTENT_DIR will automatically update the STATIC_PATH and TEMPLATES_DIR.

The current values are one of:

```python
    #CONTENT_DIR = 'get-shit-done-1.4.1'
    #CONTENT_DIR = 'pk2-free-v2'
    #CONTENT_DIR = 'paper-dashboard-2'
```

**STATIC_PATH**

**TEMPLATES_DIR**

STATIC_PATH is the relative path to the static files, for example, *static/pk2-free-v2*

TEMPLATES_DIR is the relative pat to the template files, for example, *templates/pk2-free-v2*

Changing these config properties will change the themes used by the application.


# Creative Tim Template Updates

## Html Updates

* where you see:

*href="assets/img/apple-icon.png"*


Change this to use the url_for, for the 'static' folder

*href="{{ url_for('static', filename='assets/img/apple-icon.png') }}*

or, notice the url method around the jinja url_for,

*... style="background-image: url( {{ url_for('static', filename='assets/img/cover_4.jpg', _external=True) }} )">*


## html_to_jinja.py

This script is a helper script to convert some of the urls, links, img srcs to using Flasks, url_for().  It might not get everything, but it convert a lot of hrefs to use the url_for static resources.

To use this script, open the html_to_jinja.py and look for the variable **tim_files** and change the path to the root of the html themed files.


## Users

This flask starter does not use a database, but the users are defined in *config.py*


## TODOs

    [] Finish remaining pages for Paper Dashboard 2
    [] Create an Admin page for Paper Dashboard 2
    [] Add logout to Paper Dashboard 2
    [] Add read data connections to Paper Dashboard 2

## Get SH IT Done Landing Page Screen Capture
![Get SH IT Done](./creative-tim/images/getshitdone.png)

## Paper Kit 2 Landing Page Screen Capture
![Paper Kit 2](./creative-tim/images/paperkit2.png)

## Paper Dashboard 2 Landing Page Screen Capture
![Paper Dashboard 2](./creative-tim/images/paperdashboard2.png)
