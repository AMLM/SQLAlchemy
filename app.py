
# 1. import Flask
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
from flask import Flask, jsonify 

#Database setup and engine
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

#reflect an existing database using Base

Base = automap_base()
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
        f"precipitaton ~~ the latest on preceipitation data<br/>"
        f"<br/>"
        f"stations ~~ all the observation stations<br/>"
        f"<br/>"
        f"most_active_stations ~~ most active stations<br/>"
        f"<br/>"
        f"temperatures ~~ temperature observation from the most active station in the analysis for the last year<br/>"
        f"<br/>"
        

        )
# set the app.route decorator for the api precipitations route and define functions to return jsonify data

@app.route("precipitation")
def precipitation():

    session = Session(engine)

    most_current_date = str(most_current_date)[2:-3]
    year_from_current = str(eval(most_current_date[0:4])-1) + most_current_date[4:]

    last_12_prcp = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= year_from_current).filter(Measurement.date <= most_current_date).\
        order_by(Measurement.date).all()
    

    return jsonify (precipitation)

session.close()

@app.route("stations")
def stations():

    session = Session(engine)
    
    active_stations = session.query(Measurement.station, func.count(Measurement.tobs)).\
        group_by(Measurement.station).\
        order_by(func.count(Measurement.tobs).desc())

    return jsonify (precipitation)

session.close()

@app.route("most_active_stations")
def most_active_station():

    session = Session(engine)

    most_active_station = active_stations
    
    stats = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.station == most_active_station)

    return jsonify (precipitation)

session.close()

app.route("temperature")
def temperature():

    session = Session(engine)

    stats = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.station == most_active_station)

    return jsonify (precipitation)

session.close()

   
if __name__ == '__main__':
    app.run()
                     