from flask import render_template, request, redirect, session, url_for

from app import app
from app.db import get_db


def attendance_count():
    db = get_db()
    res = db.execute('SELECT COUNT(name) FROM invitee WHERE attending = 1')
    return res.fetchone()[0]


def map_attend_value(value):
    if value == None:
        return "hasn't RSVP'd yet"
    elif value == 1:
        return "is attending"
    elif value == 0:
        return "is not attending"
    elif value == 2:
        return "is not sure yet"
    else:
        raise ValueError(f'Could not parse attendance value: {value}')


def attendance_list():
    db = get_db()
    res = db.execute('SELECT name, attending FROM invitee')
    return [
        {
            'name': i[0],
            'attending': map_attend_value(i[1]),
        } for i in list(res.fetchall())
    ]


def add_invitee(name, attending=None):
    db = get_db()
    try:
        db.execute(
            "INSERT INTO invitee (name, attending) VALUES (?, ?)",
            (name, attending)
        )
        db.commit()
    except db.IntegrityError:
        error = f"Invitee {name} is already listed."
        app.logger.error(error)


def get_invitee_rsvp(name):
    db = get_db()
    res = db.execute("SELECT attending FROM invitee WHERE name = ?", (name,))
    return res.fetchone()[0]


def update_rsvp(name):
    db = get_db()
    attending = get_invitee_rsvp(name)
    if attending is None:
        new_attending = True
    else:
        new_attending = (attending - 1) % 3
    # If this fails, something is truly wrong; so no try-catch
    db.execute(
        "UPDATE invitee SET attending = ? WHERE name = ?",
        (new_attending, name)
    )
    db.commit()


def archive_invitees():
    db = get_db()
    res = db.execute("SELECT name, attending FROM invitee")
    (invitee_names, _) = zip(*list(res.fetchall()))
    for name in invitee_names:
        try:
            db.execute(
                "INSERT INTO past_invitee (name) VALUES (?)",
                (name,)
            )
            db.commit()
        except db.IntegrityError:
            message = f"Invitee {name} already in past invitees."
            app.logger.debug(message)
    db.execute("DELETE FROM invitee")
    db.commit()


@app.route("/", methods=["GET"])
def index():
    count = attendance_count()
    invitees = attendance_list()
    return render_template("index.html", count=count, invitees=invitees, client_ip=request.remote_addr)


@app.route("/invite", methods=["GET","POST"])
def invite():
    add_invitee(request.form['name'])
    return redirect(url_for('index'))


@app.route("/rsvp", methods=["GET","POST"])
def rsvp():
    def extract_name_from_imd(immutablemultidict):
        return list(immutablemultidict.to_dict(flat=False).keys())[0]
    update_rsvp(extract_name_from_imd(request.form))
    return redirect(url_for('index'))


@app.route("/archive", methods=["GET", "POST"])
def archive():
    archive_invitees()
    return redirect(url_for('index'))
