# Hello!
This API assumes you have Django >5.0 installed and ready.
# Running
To run the server, navigate to the `events` directory, and enter the following commands in order: 

 1. `python manage.py makemigrations`
 2. `python manage.py migrate`
 3. `python manage.py runserver`

The server will begin running at http://localhost:8000/.
##  API Requests
The following API endpoints are available:

 1. `/venues/` -> create a venue. Requires POST.
 2. `/venues/{id}/` -> get a venue. Requires GET.
 3. `/events/{id}/artists/` -> get all the artists performing at an event. Requires GET.

## Sample Data
Note that sample data was created automatically when you made the migrations. The API endpoints requiring an ID value can be given the value `1` and this will show the sample data.

## Testing
Some unit tests have been included. You can run these by running the command `python manage.py test api`.
