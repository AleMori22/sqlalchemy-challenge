# Import the dependencies.

from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func , inspect
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################


# reflect an existing database into a new model

engine = create_engine("sqlite:///Resources/hawaii.sqlite")


# reflect the tables

Base = automap_base()

Base.prepare(autoload_with=engine)


# Save references to each table

Station = Base.classes.station

Measurement = Base.classes.measurement

# Create our session (link) from Python to the DB

session = Session(engine)

#################################################
# Flask Setup
#################################################

app = Flask(__name__)

@app.route("/")
def homepage():
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end"

    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    
    last_date = dt.datetime(2017,8,23)
    
    first_date = dt.datetime(last_date.year - 1, last_date.month, last_date.day)
    
    year_data = session.query(Measurement.date, Measurement.prcp).filter(
        Measurement.date <= last_date,Measurement.date >= first_date).all()
    
    return(year_data)



@app.route("/api/v1.0/stations")
def stations():
    
    st = session.query(Measurement.station).group_by(Measurement.station).all()
    
    return jsonify(st)



@app.route("/api/v1.0/tobs")
def precipitation():
    
    last_date = dt.datetime(2017,8,23)
    
    first_date = dt.datetime(last_date.year - 1, last_date.month, last_date.day)
    
    tods = session.query(Measurement.date, Measurement.prcp).filter(
        Measurement.date <= last_date,Measurement.date >= first_date).all()
    
    return jsonify(tods)



@app.route("/api/v1.0/start")
def start():
    
    
    return()

@app.route("/api/v1.0/start/end")
def st_en():
    return()




#################################################
# Flask Routes
#################################################
