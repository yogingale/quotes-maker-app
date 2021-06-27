## Quotes Maker AI


### Features

- Create quotes based on image and moods.
- Custom and Google Signup/Login added

### Deployment

Commit on master branch deploys the site on https://quotes-maker.com  
Commit on dev branch deploys the site on https://dev.quotes-maker.com  

### Backend
DB - Mongo  
Object recognition from image - Amazon Rekognition  
Hosting - Heroku  
Domain registration - GoDaddy  
CDN - Cloudflare  


### Setup locally

#### Prerequisite

Set env var `APP_STAGE` as local, dev or prod based on environment.

#### Steps
  1) git clone the repository
  2) python3 -m venv .venv
  3) source .venv/bin/activate
  4) pip install -r requirements.txt

### Run

To start the server run  
`python main.py`

### File structure
* main.py - Main file to start flask server
* services - Helper classes
* static - Static files (CSS, JS, etc)
* templates - HTML Jinja template

### Google signup token
Google signup tokens: https://console.developers.google.com/apis/credentials?pli=1