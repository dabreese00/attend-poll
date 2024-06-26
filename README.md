# Attendance poll

Features:

- Sign your name & RSVP
- See who is attending

How to develop:

- Clone the repo
- Install Flask in a virtualenv
- Run `flask --app attend-poll init-db`
- Run `flask --app attend-poll run --debug`
- Open browser and navigate to `http://127.0.0.1:5000`
- Play around, make changes, enjoy auto-reload.
- Reset the counter by running `python manage.py reset_db`

How to deploy:

Push to Dokku: `git push dokku main`

Requires:
- Dokku persistent storage directory created and mounted
- Dokku app configured with DATABASE variable pointing to persistent storage mount location

Reset the production database:

```
ssh dokku@dokku-host 'dokku run attend-poll "flask --app attend-poll init-db"'
```
