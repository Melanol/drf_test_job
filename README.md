This is a private API test job done with djangorestframework (admins only).

Installation:
- Create and activate a virtual environment for the project
- Install everything in requirements.txt in a Python environment
- Setup and run RabbitMQ and Celery (https://docs.celeryq.dev/en/stable/getting-started/first-steps-with-celery.html#first-steps)
- Create .env in drf_test_job/drf_test_job and put SECRET_KEY (for Django) and TOKEN (for the outer API). Do not use quotation marks.
- Run migrations with "python manage.py makemigrations notifications" and "python manage.py migrate"
- Create an admin with "python manage.py createsuperuser"
- Run the server with "python manage.py runserver"
- Log in as admin
- You can run commands in utilities/populate_db.py to test the server
