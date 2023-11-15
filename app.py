import os
import math
from cs50 import SQL
from datetime import datetime
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

# Configure application
app = Flask(__name__)
# Custom filter

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///tracker.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/", methods=["GET"])
@login_required
def index():
    tracks = db.execute("SELECT track_name FROM tracks ORDER BY track_name;")
    return render_template("index.html", tracks=tracks)


@app.route("/createnote", methods=["POST", "GET"])
@login_required
def createnote():
    if request.method =="POST":
    
        # checks
        if not request.form.get("event"):
            return apology("Insert event name", 403)

        if not request.form.get("track_name") or request.form.get("track_name") == "none":
            return apology("Select a track", 403)

        session["track_name"] = request.form.get("track_name")
        session["event"] = request.form.get("event")
        session["date"] = request.form.get("date")
        session["bike"] = request.form.get("bike")
        session["general"] = request.form.get("general")

        session["tracks"] = db.execute("SELECT * FROM tracks WHERE track_name=?;", session["track_name"])
        session["link"] = session["tracks"][0]["map_url"]
        session["name"] = session["tracks"][0]["track_name"]

        # insert new note into database
        db.execute("INSERT INTO notes (users_id, track_name, event, date, bike, general) VALUES (?, ?, ?, ?, ?, ?);", session["user_id"], session["track_name"], session["event"], session["date"], session["bike"], session["general"])

        # get the note id from last inserted note and store in session[]
        session["current_note_id"] = db.execute("SELECT notes_id FROM notes ORDER BY notes_id DESC LIMIT 1;");
        session["current_note_id"] = session["current_note_id"][0]["notes_id"]
        # return note to template with session[] info and note list as none
        return render_template("createnote.html", link=session["link"], name = session["name"], event = session["event"], date = session["date"], bike = session["bike"], general = session["general"], notes_list = None, note_id = session["current_note_id"])
    
    else:
        # get list_notes
        notes_list = db.execute("SELECT list_notes_id, position, note FROM list_notes WHERE notes_id = ?;", session["current_note_id"])
        # render the template with session[] and note info
        return render_template("createnote.html", link=session["link"], name = session["name"], event = session["event"], date = session["date"], bike = session["bike"], general = session["general"], notes_list = notes_list, note_id = session["current_note_id"])


@app.route("/add", methods=["POST"])
@login_required
def add():
    current_note_id = session["current_note_id"]
    # get new note
    position = request.form.get("position")
    note = request.form.get("newnote")
    # add new note to db
    db.execute("INSERT INTO list_notes (notes_id, position, note) VALUES (?, ?, ?);", current_note_id, position, note)
    # get all info and return to creatnote
    return redirect(url_for("createnote"))

@app.route("/edit/<toedit>", methods=["POST"])
@login_required
def edit(toedit):

    if toedit == "main":
        event = request.form.get("event")
        date = request.form.get("date")
        bike = request.form.get("bike")
        general_notes = request.form.get("general_notes")
        return render_template("edit.html", toedit = toedit, event = event, date = date, bike = bike, general_notes = general_notes)

    else:
        list_note_id = int(toedit)
        note_value = request.form.get(toedit)
        # add note position
        position_value = request.form.get(f"position_{toedit}")
        return render_template("edit.html", list_note_id = list_note_id, note_value = note_value, position_value = position_value)

@app.route("/editcomplete/<toedit>", methods=["POST"])
@login_required
def editcomplete(toedit):
    if toedit == "main":
        session["event"]= event = request.form.get("event")
        session["date"]= date = request.form.get("date")
        session["bike"]= bike = request.form.get("bike")
        session["general"]= general_notes = request.form.get("general_notes")

        db.execute("UPDATE notes SET event = ?, date = ?, bike = ?, general = ? WHERE notes_id = ?;", event, date, bike, general_notes, session["current_note_id"])
        return redirect(url_for("createnote"))
    else:
        # get the input 
        list_note_id = int(toedit)
        note_value = request.form.get(toedit)
        position_value = request.form.get(f"position_{toedit}")
        # update the note
        db.execute("UPDATE list_notes SET note = ?, position = ? WHERE list_notes_id = ?;", note_value, position_value, list_note_id )
        # return create note
        return redirect(url_for("createnote"))



@app.route("/delete/<list_notes_id>", methods=["POST"])
@login_required
def delete(list_notes_id):
    list_notes_id = int(list_notes_id)
    current_note = session["current_note_id"]
    # delete note from db
    db.execute("DELETE FROM list_notes WHERE list_notes_id = ?", list_notes_id)
    # get all info and return to creatnote
    return redirect(url_for("createnote"))


@app.route("/mynotes/")
@login_required
def mynotes():
    # get all data for user from notes
    all_notes = db.execute("SELECT * FROM notes WHERE users_id = ?;", session["user_id"])
    # link to view note
    return render_template("mynotes.html", all_notes = all_notes)


@app.route("/view/<int:note_id>", methods=["POST"])
def view(note_id):
        # get info from database
        note_info = db.execute("SELECT * FROM notes WHERE notes_id = ?;", note_id)
        # save to session
        session["current_note_id"] = note_id
        session["track_name"] = note_info[0]["track_name"]
        session["event"] = note_info[0]["event"]
        session["date"] = note_info[0]["date"]
        session["bike"] = note_info[0]["bike"]
        session["general"] = note_info[0]["general"]

        session["tracks"] = db.execute("SELECT * FROM tracks WHERE track_name=?;", session["track_name"])
        session["link"] = session["tracks"][0]["map_url"]
        session["name"] = session["tracks"][0]["track_name"]

        notes_list = db.execute("SELECT list_notes_id, position, note FROM list_notes WHERE notes_id = ?;", session["current_note_id"])
        return render_template("view.html", link=session["link"], name = session["name"], event = session["event"], date = session["date"], bike = session["bike"], general = session["general"], notes_list = notes_list, note_id = note_id)

@app.route("/deletenote/<int:note_id>", methods=["POST"])
def deletenote(note_id):
    db.execute("DELETE FROM list_notes WHERE notes_id = ?;", note_id )
    db.execute("DELETE FROM notes WHERE notes_id = ?;", note_id )
    return redirect(url_for("mynotes"))

@app.route("/success", methods=["POST"])
@login_required
def success():
    return render_template("success.html")

# login reg logout
@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        username = request.form.get("username")
        password = str(request.form.get("password"))
        confirmation = str(request.form.get("confirmation"))
        # check username submitted
        if not request.form.get("username"):
            return apology("Enter a Username, 403")
            check
        # check password submitted
        elif not request.form.get("password"):
            return apology("Enter a Password, 403")
        # check confirmation submitted
        elif confirmation == "":
            return apology("Confirm Password")
        # matching passwords
        elif password != confirmation:
            return apology("Password and Confirmation don't match, 403")
        # check user name not taken
        elif db.execute("SELECT username FROM users WHERE username = ?;", username):
            return apology("User already Exists, 403")
        else:
            # hash password
            hashed = generate_password_hash(password)
            # insert user
            db.execute("INSERT INTO users (username, hash) VALUES (?, ?);", username, hashed)
            return redirect("/")
    else:
        return render_template("register.html")
