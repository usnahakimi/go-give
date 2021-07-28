# Go-Give

# MVP:
* Register with first name, last name, email, location
* Signing in and out
* Being able to list an item with a description
* Being able to list an item with an image
* Being able to list an item with availability
* Being able to list an item with collection date
* Update a listing
* Delete a listing
* Message user with listed item
```
```
# Extra Features: 
* Add/change location
* Request to reserve item/items - automated messages e.g. ‘Is this still available?’
* Message the item lister
* Email confirmation when you sign up
* User ratings 
* Leave users feedback 
* Flash message about safety when collecting parcels
* Liking/saving an item
* Public profile page with all of your listed items, profile picture
* Search for items/keywords/users
* Search with filters (by location, size)
* Categories of items
* Browsing page
```
```
# Design:
* main.py and auth.py are views (the equivalent of Sinatra controllers)
* models.py contains all models for the project
* __init__.py is to create the app and set up database connection
```
```
# Setup:
* Install Python3
* Create a virtual environment python3 -m venv venv
* Activate the virtual environment . venv/bin/activate
* Install the dependencies pip3 install -e .
* Install chromedriver for feature testing sbase install chromedriver
* To create the database open python interpreter and put in following commands:
    * from go_give import db, create_app
    * db.create_all(app=create+app())
* Run the app
    * export FLASK_APP=go_give
    * flask run
```
```
# Running the tests:
* To run them all pytest
* To run the tests in a specific file, e.g. test_auth.py pytest ./tests/test_auth.py
```
```
# Dependency management:
* Add further dependencies to setup.py
* Then run this to install them pip3 install -e .