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
        if (snoFromDb):
            message = "Serial Number already exists for a different chemical. Verify your input."
            return render_template('updateChemicals.html', confirm = message)
        else:
            execute_db('insert into CHEMICALS values("'+Sno+'","'+Chem_Name+'","'+Molecular_Formula+'","'+Stock_Available+'")')
            return redirect('/updateOptions')
    return render_template('updateOptions.html')

@app.route('/updateChemicalStock', methods = ['GET', 'POST'])
def updateChemicalStock():
    if request.method == "POST":
        Sno = request.form["srNo"]
        Stock_Available = request.form["stockAvailable"]
        snoFromDb = query_db('select Sno from CHEMICALS where Sno ="'+Sno+'"')
        if (snoFromDb):
            execute_db('update CHEMICALS set Stock_Available = "'+Stock_Available+'" where Sno = "'+Sno+'"')
            return redirect('/updateChemicalOptions')
        else:
            message = "Serial number does not exist. Please verify."
        return render_template('updateChemicalStocks.html',confirm=message)
    return render_template('updateChemicalOptions.html')

@app.route('/updateInstrumentStock', methods = ['GET', 'POST'])
def updateInstrumentStock():
    if request.method == "POST":
        Sno = request.form["srNo"]
        Stock_Available = request.form["stockAvailable"]
        snoFromDb = query_db('select Sno from INSTRUMENT where Sno ="'+Sno+'"')
        if (snoFromDb):
            execute_db('update INSTRUMENT set Number_Of_Units_Present = "'+Stock_Available+'" where Sno = "'+Sno+'"')
            return redirect('/updateInstrumentOptions')
        else:
            message = "Serial number does not exist. Please verify."
        return render_template('updateInstrumentStocks.html',confirm=message)
    return render_template('updateChemicalOptions.html')

@app.route('/updateGlasswareStock', methods = ['GET', 'POST'])
def updateGlasswareStock():
    if request.method == "POST":
        Sno = request.form["srNo"]
        Stock_Available = request.form["stockAvailable"]
        snoFromDb = query_db('select Sno from GLASSWARE where Sno ="'+Sno+'"')
        if (snoFromDb):
            execute_db('update GLASSWARE set Quantiy_Available = "'+Stock_Available+'" where Sno = "'+Sno+'"')
            return redirect('/updateGlasswareOptions')
        else:
            message = "Serial number does not exist. Please verify."
        return render_template('updateGlasswareStocks.html',confirm=message)
    return render_template('updateGlasswareOptions.html')

@app.route('/updateSuppliersDetails', methods = ['GET', 'POST'])
def updateSuppliersDetails():
    if request.method == "POST":
        Sno = request.form["srNo"]
        supplierContactNumber = request.form["supplierContactNumber"]
        companyName = request.form["companyName"]
        supplierAddress = request.form["supplierAddress"]
        companyContactNumber = request.form["companyContactNumber"]
        snoFromDb = query_db('select Supplier_No from SUPPLIER where Supplier_No ="'+Sno+'"')
        if (snoFromDb):
            execute_db('update SUPPLIER set Supplier_Contact_No = "'+supplierContactNumber+'", Company_Name = "'+companyName+'", Supplier_Address = "'+supplierAddress+'", Company_Contact_No = "'+companyContactNumber+'" where Supplier_No = "'+Sno+'"')
            return redirect('/updateSuppliersOptions')
        else:
            message = "Serial number does not exist. Please verify."
        return render_template('updateSupplierDetails.html',confirm=message)
    return render_template('updateSupplierOptions.html')

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

@app.route('/orderChemical', methods = ['GET', 'POST'])
def orderChemical():
    if request.method == "POST":
        Sno = request.form["srNo"]
        chemicalName = request.form["chemicalName"]
        noOfPackets = request.form["noOfPackets"]
        suppliedBy = request.form["suppliedBy"]
        orderDate = request.form["orderDate"]
        deliveryDate = request.form["deliveryDate"]
        orderNumber = request.form["orderNumber"]
        pricePerStock = request.form["pricePerStock"]
        stockBought = request.form["stockBought"]
        totalPrice = request.form["totalPrice"]
        orderNumberFromDb = query_db('select Order_Number from CHEM_ORDER where Order_Number ="'+orderNumber+'"')
        chemicalNameFromDb = query_db('select Chem_Name from CHEMICALS where Chem_Name = "'+chemicalName+'"')
        suppliedByFromDb = query_db('select Supplier_No from SUPPLIER where Supplier_No = "'+suppliedBy+'"')
        if (orderNumberFromDb):
            message = "Order Number already exists for a different chemical. Verify your input."
            return render_template('orderChemicals.html', confirm = message)
        else:
            if(chemicalNameFromDb and suppliedByFromDb):
                execute_db('insert into CHEM_ORDER values("'+Sno+'","'+chemicalName+'","'+noOfPackets+'","'+suppliedBy+'","'+orderDate+'","'+deliveryDate+'","'+orderNumber+'","'+pricePerStock+'","'+totalPrice+'","'+stockBought+'")')
                return redirect('/orderChemicals')
            else:
                message = "Either Chemical Name or Supplier Number does not exist. Please Verify."
                return render_template('orderChemicals.html', confirm = message)
    return render_template('chemicals.html')

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

@app.route("/updateInstrumentStocks")
def updateInstrumentStocks() : 
	return render_template("updateInstrumentStocks.html")

@app.route("/updateInstrumentOptions")
def updateInstrumentOptions() : 
	return render_template("updateInstrumentoptions.html")

@app.route("/updateGlasswareOptions")
def updateGlasswareOptions() : 
	return render_template("updateGlasswareoptions.html")

@app.route("/updateGlasswareStocks")
def updateGlasswareStocks() : 
	return render_template("updateGlasswareStocks.html")

@app.route("/updateSuppliersOptions")
def updateSuppliersOptions() : 
	return render_template("updateSuppliersoptions.html")

@app.route("/updateSupplierDetails")
def updateSupplierDetails() : 
	return render_template("updateSupplierDetails.html")

@app.route("/orderChemicals")
def orderChemicals() : 
	return render_template("orderChemicals.html")

if __name__ == "__main__":
	app.run(debug=True)