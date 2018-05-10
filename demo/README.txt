To run this demo, you need to have Flask installed. Flask is web framework for Python. You can find installation instructions here:  http://flask.pocoo.org/docs/1.0/installation/


Once flask is installed, cd to the directory that this readme is in and then run these two commands:

export FLASK_APP=example.py
flask run


You can then go to the following pages in your browser:

- Attendance Sheets/Administrative part of the application: http://0.0.0.0:5000/static/landing.html

- Sign In: http://0.0.0.0:5000/static/signin.html

- Fingerprint Scan Success: http://0.0.0.0:5000/static/success.html

- Fingerprint Scan Error: http://0.0.0.0:5000/static/failure.html

We primarily used Safari when developing and testing these pages.


example.py is a mock server that our frontend makes HTTP requests to. example.py responds to HTTP requests with fake data. This demo server does not perform any business logic or communicate with a database. For student profiles, it only has data for Tanya Williams and Kelly Fink. Clicking on other students leads to Kelly. example.py responds with the same list of students for the class rosters, "Who's here?", and "All Students". In the attendance sheets part of the app, we use JavaScript to dynamically generate the HTML based on the responses from the server. With the exception of profile images, the content is not hard coded and is based off of the data from the serve. The frontend API calls should work with our server that is connected with the database, but we ran out of time to integrate it.

If you are interested in seeing what we did for our database and our work with the fingerprint scanner, visit our GitHub repository: https://github.com/benedictb/9.3best
