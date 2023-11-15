import os
import os
import math
from cs50 import SQL
from datetime import datetime
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

db = SQL("sqlite:///tracker.db")

notes_list = db.execute("SELECT list_notes_id, position, note FROM list_notes WHERE notes_id = 1;")

for note in notes_list:
    print(note["list_notes_id"])

    

        session["track_name"] = request.form.get("track_name")
        session["event"] = request.form.get("event")
        session["date"] = request.form.get("date")
        session["bike"] = request.form.get("bike")
        session["general"] = request.form.get("general")

        session["tracks"] = db.execute("SELECT * FROM tracks WHERE track_name=?;", session["track_name"])
        session["link"] = session["tracks"][0]["map_url"]
        session["name"] = session["tracks"][0]["track_name"]
        # insert new note into databse
        db.execute("INSERT INTO notes (users_id, track_name, event, date, bike, general) VALUES (?, ?, ?, ?, ?, ?);", session["user_id"], session["track_name"], session["event"], session["date"], session["bike"], session["general"])

        # get the note id from last inserted note and store in session[]
        session["current_noteid"] = db.execute("SELECT notes_id FROM notes ORDER BY notes_id DESC LIMIT 1; ");

        # return note to template with session[] info and note list as none
        return render_template("createnote.html", link=session["link"], name = session["name"], event = session["event"], date = session["date"], bike = session["bike"], general = session["general"], notes_list = None)
    
    else:
        # get list_notes
        notes_list = db.execute("SELECT list_notes_id, position, note FROM list_notes WHERE notes_id = ?;", session["current_noteid"][0]["notes_id"])
        # render the template with session[] and note info
        return render_template("createnote.html", link=session["link"], name = session["name"], event = session["event"], date = session["date"], bike = session["bike"], general = session["general"], notes_list = notes_list)

