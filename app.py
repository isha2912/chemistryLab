import os
from flask import Flask, render_template, request, redirect
import urllib.request
from flask import send_file
import sqlite3
from flask import g
import hashlib

app=Flask(__name__)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
salt = "TwinFuries"

DATABASE = os.path.join(APP_ROOT,'database/database.db')

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        #db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))

@app.route('/init_db')
def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def execute_db(query):
    cur = get_db()
    cur.execute(query)
    cur.commit()
    cur.close()

@app.route("/")
def home() : 
	return render_template("home.html")

@app.route("/chemicals")
def chemicals() : 
	return render_template("chemicals.html")


@app.route("/glassware")
def glassware() : 
	return render_template("glassware.html")

@app.route("/instruments")
def instruments() : 
	return render_template("instruments.html")

@app.route("/suppliers")
def suppliers() : 
	return render_template("suppliers.html")

@app.route("/login")
def login() : 
	return render_template("login.html")

@app.route("/updateOptions")
def updateOptions() : 
	return render_template("updateOptions.html")

@app.route("/updateChemicals")
def updateChemicals() : 
	return render_template("updateChemicals.html")

@app.route("/updateGlassware")
def updateGlassware() : 
	return render_template("updateGlassware.html")

@app.route("/updateInstruments")
def updateInstruments() : 
	return render_template("updateInstruments.html")

@app.route("/updateSuppliers")
def updateSuppliers() : 
	return render_template("updateSuppliers.html")

if __name__ == "__main__":
	app.run(debug=True)