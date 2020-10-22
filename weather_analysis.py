import datetime as dt
import numpy as np
import pandas as pd

# Add sqlalchemy dependencies
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# Add flask dependencies
from flask import Flask, jsonify, render_template, request, redirect, url_for

# example: engine = create_engine('sqlite:///C:\\path\\to\\foo.db')
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the database into classes
Base.prepare(engine, reflect=True)

# Create reference to the classes
Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

# Set up Flask application
app = Flask(__name__)

# set the token for debug mode
import secrets
token = secrets.token_urlsafe(16)
print(token)
app.config['SECRET_KEY'] = token
app.config['ENV']= 'development'

# define routes
@app.route("/")
def welcome():
    return render_template('index.html')
# Add precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    precipitation = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= prev_year).all()
    precip = {date: prcp for date, prcp in precipitation}
    return jsonify(precip)

# Add stations route
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    results = session.query(Station.station).all()
    # unravel the results into a one-dimensional array
    stations = list(np.ravel(results))
    return jsonify(stations=stations)

# Add temperature observations
@app.route("/api/v1.0/tobs")
def temp_monthly():
    session = Session(engine)
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
    filter(Measurement.station == 'USC00519281').\
    filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

# Summary statistics report
@app.route("/api/v1.0/report",methods = ['POST', 'GET'])
def report():
    if request.method == 'POST':
        start = request.form['start']
        end = request.form['end']
        return redirect(url_for('stats',start = start, end = end ))
    else:
        start = request.args.get('start')
        end = request.args.get('end')
        return render_template('temperature.html')

@app.route("/api/v1.0/stats/<start>/<end>")
@app.route("/api/v1.0/stats/<start>/")
def stats(start=None, end=None):
    # to avoid SQLite objects created in a thread can only be used in that same thread
    # we re-create the session variable locally in the function
    session = Session(engine)
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]           

    if not end: 
        results = session.query(*sel).\
        filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps)

    results = session.query(*sel).\
    filter(Measurement.date >= start).\
    filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

from flask_debugtoolbar import DebugToolbarExtension

if __name__ == '__main__':
    app.run(debug=True)
    toolbar = DebugToolbarExtension(app)