# go-give

MVP:
Register with first name, last name, email, location
Signing in and out
Being able to list an item with a description/images/collection/avaIlability/date for collection
Update/delete listings
Message user who listed it

Extra Features: 
Add/change location
Request to reserve item/items - automated messages e.g. ‘Is this still available?’
Message the item lister
Email confirmation when you sign up
User ratings 
Leave users feedback 
Flash message about safety when collecting parcels
liking/saving an item
Public profile page with all of your listed items, profile picture
Search for items/keywords/users
Search with filters (by location, size)
Categories of items
Browsing page


Design:
posts.py and auth.py are views (the equivalent of Sinatra controllers)
post.py and user.py are models
db.py looks after creating the database connection

Setup:
Install Python3
Create a virtual environment python3 -m venv venv
Activate the virtual environment . venv/bin/activate
Install the dependencies pip3 install -e .
Install chromedriver for feature testing sbase install chromedriver
Create and migrate the database flask init-db
Run the app
export FLASK_APP=acebook
flask run

Running the tests:
To run them all pytest
To run the tests in a specific file, e.g. test_auth.py pytest ./tests/test_auth.py

Dependency management:
Add further dependencies to setup.py
Then run this to install them pip3 install -e .
