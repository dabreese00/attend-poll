from flask import render_template, request, redirect, session, url_for

from app import app
from app.db import get_db


def attendance_count():
    db = get_db()
    res = db.execute('SELECT COUNT(name) FROM invitee WHERE attending = 1')
    return res.fetchone()[0]


def attendance_list():
    db = get_db()
    res = db.execute('SELECT name, attending FROM invitee')
    return list(res.fetchall())


def add_attendance(name):
    db = get_db()
    try:
        db.execute(
            "INSERT INTO invitee (name, attending) VALUES (?, ?)",
            (name, True)
        )
        db.commit()
    except db.IntegrityError:
        error = f"Invitee {name} is already listed."
        app.logger.error(error)


@app.route("/", methods=["GET"])
def index():
    count = attendance_count()
    invitees = attendance_list()
    return render_template("index.html", count=count, invitees=invitees, client_ip=request.remote_addr)


@app.route("/attending", methods=["GET","POST"])
def hello():
    add_attendance(request.form['name'])
    return redirect(url_for('index'))
