# DjangoScraper

# Dependencies
Django-3.2.5    #
asgiref-3.4.1
sqlparse-0.4.1

# version check
python3 -m django --version

#Install django admin
sudo apt install python3-django

#Create the project 
django-admin startproject scraperX

# check the development server --run inside top level scraperX
python3 manage.py runserver

#Create scraper module
python3 manage.py startapp scraper

#create database 
python3 manage.py migrate

# Create models of scraper
python3 manage.py makemigrations scraper

#  Create sql
python3 manage.py sqlmigrate scraper 0001

# Applying changes 
python3 manage.py migrate

# Create super user
python3 manage.py createsuperuser
#username: admin
#password: admin123
#email: admin@scraperX.com

#run the development server
python3 manage.py runserver

# if sqlite3 is not present in ubuntu 20.04 install with apt
sudo apt install sqlite3


# installation steps
1. Install dpendencies with pip3 in ubutu use pip in windows
pip3 install -r requirements.txt

2. make migrations should be run inside base Property Analyzer directory
pytohn3 manage.py makemigrations

3.Run the server in the Property Analyzer directory(top Level)
python3 manage.py runserver

Note: If you are using ubuntu you can run the ./install.sh inside root property Analyser directory