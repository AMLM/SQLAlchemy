
# 1. import Flask
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt,
from flask import Flask, jsonify, 

#Database setup and engine
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

#reflect an existing database using Base

Base= automap_base()
Base.prepare(engine, reflect=True)

#Save the reflections of each table
Measurement = Base.classes.measurement
Station = Base.classes.station

#Init the session
session = Session(bind=engine)


# 2. Create an app using Flask, being sure to pass __name__
app = Flask(__name__)



# 3. Set up the app.route decorator for the base'/'
@app.route("/")
def home():
    return (
        f"Welcome to Surf's Up!: Hawai'i Climate API<br/>"
        f"<br/>"
        f"Available APIs at this site:<br/>"
        f"<br/>"
        f"/api/v1.0/stations ~~~~~ a list of observation stations<br/>"
        f"<br/>"
        f"/api/v1.0/precipitaton ~~ the latest on preceipitation data<br/>"
        f"<br/>"
        f"/api/v1.0/temperature ~~ the latest year on temperature data<br/>"
        f"<br/>"
        f"/api/v1.0/datesearch/2015-05-30  ~~ Tmperature observation statistics on specific dates<br/>"
        )
# set the app.route decorator for the api precipitations route and define functions to return jsonify data

@app.route("/api/v1.0/precipitation")
def precipitation():

    session = Session(engine)
#Calculate precipitation for the last year
    prev_year = dt.date(2017,8,23) - dt.timedelta(days=365)
    last_12_prcp = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= prev_year).\
        order_by(Measurement.date.asc()).all()

    session.close()

# create a dictionary to store the pprcp pairs and return the jsonify dictionary
    prcp_pairs = []
    for date, prcp in last_12_prcp:
        dict_row = {}
        dict_row["date"] = date
        dict_row["prcp"] = prcp
        prcp_pairs.append(dict_row)
        return jsonify(prcp_pairs)

# set the app.route decorator for api stations route, define functions and return jsonified data.

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    stations_all = session.query(Station.station, Station.name).\
                           group_by(Station.station).all()


    session.close()

    list_stations = list(np.ravel(stations_all))
    return jsonify(list_stations)

# set the app.route decorator for api tobs route, define functions and return jsonified data.

@app.route("/api/v1.0/tobs")

def temp_monthly():

    session = Session(engine)
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    temperature = session.query(Measurement.date, Measurement.tobs).\
                          filter_by(Measurement.date >= prev_year).\
                          order_by(Measurement.date.asc()).all()

    session.close()

    return jsonify(temperature)

    #Set the app.route decorator for the start and end dates
    
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")

def stats(start=None, end=None):
    session = Session(engine)
    
    #stats
    
    if end is None:
        aggregates = func.min(Measurement.tobs).label("Min_Temp"),\
                     func.avg(Measurement.tobs).label("Avg_Temp"),\
                     func.max(Measurement.tobs).label("Max_Temp")

        temp_data = session.query(*aggregates).filter(Measurement.date >= start).all()

        list_temp = []

        for data in temp_data:

            dict_temp = {}
            dict_temp["minimum temperature"] = data.Min_Temp
            dict_temp["average temperature"] = data.Avg_Temp
            dict_temp["maximum temperature"] = data.Max_Temp
            list_temp.append(dict_temp)
        return jsonify(list_temp)

    else:

        aggregates = func.min(Measurement.tobs).label("Min_Temp"),\
                    func.avg(Measurement.tobs).label("Avg_Temp"),\
                    func.max(Measurement.tobs).label("Max_Temp")
        temp_data = session.query(*aggregates).\
                    filter(Measurement.date >= start).\
                    filter(Measurement.date <= end).all()

        list_temp = []
                     

        for data in temp_data:

            dict_temp = {}
            dict_temp["minimum temperature"] = data.Min_Temp
            dict_temp["average temperature"] = data.Avg_Temp
            dict_temp["maximum temperature"] = data.Max_Temp
            list_temp.append(dict_temp)

        session.close()
        return jsonify(list_temp)

if __name__ == '__main__':
    app.run()
                     