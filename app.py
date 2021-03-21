from flask import Flask, jsonify

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

import numpy as np
import pandas as pd
import datetime as dt

# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Flask Routes

app = Flask(__name__)

@app.route("/")
def home():
    return(
        f"Home Page<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/2016-8-23<br/>"
        f"/api/v1.0/2016-1-1/2016-12-31"
    )

@app.route("/api/v1.0/precipitation")
def precip():
    # start session
    session = Session(engine)

    most_recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    #query_date = dt.date(2017,8,23) - dt.timedelta(days=365)
    query_date = dt.datetime.strptime(most_recent_date[0], '%Y-%m-%d').date() - dt.timedelta(days=365)

    # Perform a query to retrieve the data and precipitation scores
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= query_date).all()
    
    # close session
    session.close()

    # create data dictionary
    precip_data = []
    for date, prcp in results:
        precip_dict = {}
        precip_dict['date'] = date
        precip_dict['pcrp'] = prcp
        precip_data.append(precip_dict)

    return jsonify(precip_data)    

@app.route("/api/v1.0/stations")
def stations():
    # start session
    session = Session(engine)
    
    # query data
    results = session.query(Station.station).all()
    
    # close session
    session.close()
   
   # create data dictionary
    stations = []
    for station in results:
        stations.append(station[0])

    station_dict = {'stations': stations}

    return jsonify(station_dict)

@app.route("/api/v1.0/tobs")
def tobs():
    # start session
    session = Session(engine)

    # query data
    active_stations = session.query(Measurement.station, func.count(Measurement.station))\
    .group_by(Measurement.station)\
    .order_by(func.count(Measurement.station).desc()).all()

    most_active_station = active_stations[0][0]

    last_date = session.query(Measurement.date)\
    .filter(Measurement.station == most_active_station)\
    .order_by(Measurement.date.desc()).first()

    # set a query date to gather one year of data
    query_date = dt.datetime.strptime(last_date[0], '%Y-%m-%d').date() - dt.timedelta(days=365)

    # query measurement data to gather one year of temp data from most active station
    results = session.query(Measurement.date, Measurement.tobs)\
        .filter(Measurement.date >= query_date)\
        .filter(Measurement.station == most_active_station).all()

    # close session
    session.close()

    # create data dictionary
    temp_data = []
    for date, tobs in results:
        temp_dict = {}
        temp_dict['date'] = date
        temp_dict['tobs'] = tobs
        temp_data.append(temp_dict)
    
    return jsonify(temp_data)

@app.route("/api/v1.0/<start>")
def temps_start(start):
    # start session
    session = Session(engine)

    # query data
    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs))\
    .filter(Measurement.date >= start).all()

    # close session
    session.close()

    # create data dictionary
    temp_summary = []
    for min, max, avg in results:
        temp_dict = {}
        temp_dict['TMIN'] = min
        temp_dict['TMAX'] = max
        temp_dict['TAVG'] = avg
        temp_summary.append(temp_dict)

    return jsonify(temp_summary)

@app.route("/api/v1.0/<start>/<end>")
def temps_start_end(start, end):
    # start session
    session = Session(engine)

    # query data
    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs))\
    .filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    # close session
    session.close()

    # create data dictionary
    temp_summary = []
    for min, max, avg in results:
        temp_dict = {}
        temp_dict['TMIN'] = min
        temp_dict['TMAX'] = max
        temp_dict['TAVG'] = avg
        temp_summary.append(temp_dict)

    return jsonify(temp_summary)

if __name__ == "__main__":
    app.run(debug=True)