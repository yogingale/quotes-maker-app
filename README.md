## Caption Maker AI



### Features

- Login required
- Protected routes
- Simple navigation between pages


## Pre-requisite 


## Setup and Install

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
```

**STATIC_PATH**

**TEMPLATES_DIR**

STATIC_PATH is the relative path to the static files, for example, *static/pk2-free-v2*
