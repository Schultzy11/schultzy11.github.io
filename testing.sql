CREATE TABLE notes(
    notes_id INTEGER PRIMARY KEY NOT NULL,
    users_id INTEGER NOT NULL,
    track_name TEXT NOT NULL ,
    event TEXT NOT NULL,
    date DATETIME NOT NULL,
    bike TEXT,
    general TEXT,
    FOREIGN KEY (users_id) REFERENCES users(id)
)


CREATE TABLE list_notes(
    list_notes_id INTEGER PRIMARY KEY NOT NULL,
    notes_id INTEGER NOT NULL,
    position TEXT,
    note TEXT,
    FOREIGN KEY (notes_id) REFERENCES notes(notes_id)
)


# add note base
db.execute("INSERT INTO notes (user_id, track_name, event, date, bike, general) VALUES (?, ?, ?, ?, ?, ?);", session, track_name, event, date, bike, general)


# get notes_list
#  add note lists
db.execute("INSERT INTO list_notes (note_id, position, note);", note_id, position, note)


"INSERT INTO Table
    ( users_id,
    track_name,
    event,
    date,
    bike,
    general,
)
    VALUES (
    ?
    ?
    ?
    ?
    ?
    ?
);", users_id, session["track_name"], session["event"], session["date"], session["bike"], session["general"]


CREATE TABLE shared(
    shared_notes_id INTEGER PRIMARY KEY NOT NULL,
    from_users_id INTEGER NOT NULL,
    to_users_id INTEGER NOT NULL,
    track_name TEXT NOT NULL ,
    event TEXT NOT NULL,
    date DATETIME NOT NULL,
    bike TEXT,
    general TEXT
)