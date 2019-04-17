import os
from flask import Flask, render_template, request, redirect
import urllib.request
from flask import send_file
import sqlite3
from flask import g
import hashlib

salt = "TwinFuries"

app=Flask(__name__)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

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

#@app.route('/init_db')
#def init_db():
#    with app.app_context():
#        db = get_db()
#        with app.open_resource('schema.sql', mode='r') as f:
#            db.cursor().executescript(f.read())
#        db.commit()

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

@app.route('/submitChemicals', methods = ['GET', 'POST'])
def submitChemicals():
    if request.method == "POST":
        Sno = request.form["srNo"]
        Chem_Name = request.form["chemicalName"]
        Molecular_Formula = request.form["molecularFormula"]
        Stock_Available = request.form["stockAvailable"]
        snoFromDb = query_db('select Sno from CHEMICALS where Sno ="'+Sno+'"')
        #chemicalNameFromDb = query_db('select Chem_Name from CHEMICALS where Sno = " '+Sno+'"')
        #molecularFormulaFromDb = query_db('select Molecular_Formula from CHEMICALS where Sno = " '+Sno+'"')
        #message = chemicalNameFromDb," ",molecularFormulaFromDb
        if (snoFromDb):
            #if (chemicalNameFromDb[0][0] == Chem_Name and molecularFormulaFromDb[0][0] == Molecular_Formula):
            #    execute_db('update CHEMICALS set Stock_Available = "'+Stock_Available+'" where Sno = "'+Sno+'"')
            #    return redirect('/updateOptions')
            #else:
            message = "Serial Number already exists for a different chemical. Verify your input."
            return render_template('updateChemicals.html', confirm = message)
        else:
            execute_db('insert into CHEMICALS values("'+Sno+'","'+Chem_Name+'","'+Molecular_Formula+'","'+Stock_Available+'")')
            return redirect('/updateOptions')
        #return render_template('updateChemicals.html',confirm=message)
    return render_template('updateOptions.html')

@app.route('/updateChemicalStock', methods = ['GET', 'POST'])
def updateChemicalStock():
    if request.method == "POST":
        Sno = request.form["srNo"]
        #Chem_Name = request.form["chemicalName"]
        #Molecular_Formula = request.form["molecularFormula"]
        Stock_Available = request.form["stockAvailable"]
        snoFromDb = query_db('select Sno from CHEMICALS where Sno ="'+Sno+'"')
        #chemicalNameFromDb = query_db('select Chem_Name from CHEMICALS where Sno = " '+Sno+'"')
        #molecularFormulaFromDb = query_db('select Molecular_Formula from CHEMICALS where Sno = " '+Sno+'"')
        #message = chemicalNameFromDb," ",molecularFormulaFromDb
        if (snoFromDb):
            #if (chemicalNameFromDb[0][0] == Chem_Name and molecularFormulaFromDb[0][0] == Molecular_Formula):
            execute_db('update CHEMICALS set Stock_Available = "'+Stock_Available+'" where Sno = "'+Sno+'"')
            return redirect('/updateChemicalOptions')
            #else:
            #    message = "Serial Number already exists for a different chemical. Verify your input."
            #return render_template('updateChemicals.html', confirm = message)
        else:
            message = "Serial number does not exist. Please verify."
            #return redirect('/updateOptions')
        return render_template('updateChemicalStocks.html',confirm=message)
    return render_template('updateChemicalOptions.html')

@app.route('/submitGlassware', methods = ['GET', 'POST'])
def submitGlassware():
    if request.method == "POST":
        Sno = request.form["srNo"]
        Glass_Name = request.form["glasswareName"]
        Capacity = request.form["capacity"]
        Quantity_Available = request.form["stockAvailable"]
        execute_db('insert into GLASSWARE values("'+Sno+'","'+Glass_Name+'","'+Capacity+'","'+Quantity_Available+'")')
        return redirect('/updateOptions')
    return render_template('updateOptions.html')

@app.route('/submitInstruments', methods = ['GET', 'POST'])
def submitInstruments():
    if request.method == "POST":
        Sno = request.form["srNo"]
        Instrument_Name = request.form["instrumentName"]
        noOfUnits = request.form["noOfUnitsAvailable"]
        execute_db('insert into INSTRUMENT values("'+Sno+'","'+Instrument_Name+'","'+noOfUnits+'")')
        return redirect('/updateOptions')
    return render_template('updateOptions.html')

@app.route('/submitSuppliers', methods = ['GET', 'POST'])
def submitSuppliers():
    if request.method == "POST":
        supplierNumber = request.form["supplierNumber"]
        supplierName = request.form["supplierName"]
        supplierContactNumber = request.form["supplierContactNumber"]
        supplierAddress = request.form["supplierAddress"]
        companyName = request.form["companyName"]
        companyContactNumber = request.form["companyContactNumber"]
        execute_db('insert into SUPPLIER values("'+supplierNumber+'","'+supplierName+'","'+supplierContactNumber+'","'+companyName+'","'+supplierAddress+'","'+companyContactNumber+'")')
        return redirect('/updateOptions')
    return render_template('updateOptions.html')

@app.route('/db_add')
def adddata():
    pass

@app.route("/")
def home() : 
	return render_template("home.html")

@app.route("/chemicals")
def chemicals() : 
    c = get_db()
    cur = c.cursor()
    cur.execute("SELECT * from CHEMICALS")
    return render_template("chemicals.html", test = cur.fetchall())


@app.route("/glassware")
def glassware() : 
    c = get_db()
    cur = c.cursor()
    cur.execute("SELECT * from GLASSWARE")
    return render_template("glassware.html", test = cur.fetchall())

@app.route("/instruments")
def instruments() : 
    c = get_db()
    cur = c.cursor()
    cur.execute("SELECT * from INSTRUMENT")
    return render_template("instruments.html",test=cur.fetchall())

@app.route("/suppliers")
def suppliers() :
    c = get_db()
    cur = c.cursor()
    cur.execute("SELECT * from SUPPLIER")
    return render_template("suppliers.html", test=cur.fetchall())

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

@app.route("/updateChemicalOptions")
def updateChemicalOptions() : 
	return render_template("updateChemicalOptions.html")

@app.route("/updateChemicalStocks")
def updateChemicalStocks() : 
	return render_template("updateChemicalStocks.html")

if __name__ == "__main__":
	app.run(debug=True)