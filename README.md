# Attendance poll

Features:

- counts button clicks
- allows you to reset the counter via command line

How to use:

- Click the button if you're attending.
- Read the count of people attending.

How to develop:

- Clone the repo
- Install Flask in a virtualenv
- Run `flask --app attend-poll init-db`
- Run `flask --app attend-poll run --debug`
- Open browser and navigate to `http://127.0.0.1:5000`
- Play around, make changes, enjoy auto-reload.
- Reset the counter by running `python manage.py reset_db`

How to deploy:

- Clone the repo
- Push to Dokku
- Configure the DATABASE environment variable to "/app/storage/attend-poll.sqlite"
- In Dokku run `flask --app attend-poll init-db`
- Restart app
