# Import the dependencies.

from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.dates as mdates
import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func , inspect
from flask import Flask, jsonify , abort

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
        f"/api/v1.0/start/<start><br/>"
        f"/api/v1.0/st_en/<start>/<end>"

    )


#################################################
# Flask Routes
#################################################

@app.route("/api/v1.0/precipitation")
def precipitation():
    
    session = Session(engine)

    last_date = dt.datetime(2017,8,23)
    
    first_date = dt.datetime(last_date.year - 1, last_date.month, last_date.day)
    
    year_data = session.query(Measurement.date, Measurement.prcp).filter(
        Measurement.date <= last_date,Measurement.date >= first_date).all()
    
    for_data = {date: prcp for date, prcp in year_data}
    
    session.close()

    return(for_data)



@app.route("/api/v1.0/stations")
def stations():
    
    session = Session(engine)

    st = session.query(
         Measurement.station).group_by(
              Measurement.station
              ).all()
    
    for_st = [station for (station,) in st]
    
    session.close()

    return jsonify(for_st)



@app.route("/api/v1.0/tobs")
def temperature():

    session = Session(engine)
    
    last_date = dt.datetime(2017,8,23)
    
    first_date = dt.datetime(last_date.year - 1, last_date.month, last_date.day)
    
    M_A_S = session.query(
         Measurement.station).group_by(
             Measurement.station).order_by(
                  func.count(Measurement.station).desc()
                  ).first()

    tods = session.query(
         Measurement.date,Measurement.tobs).filter(
              Measurement.station == M_A_S).filter(
                   Measurement.date <= last_date , Measurement.date >= first_date
                   ).all()
    
    For_tods = [{"date": date, "temperature": tobs} for date, tobs in tods]

    session.close()
    
    return jsonify(For_tods)



@app.route("/api/v1.0/start/<start>")
def start(start):

    session = Session(engine)

    try:
        
        start_date = dt.datetime.strptime(start, '%Y-%m-%d')  
    
    except ValueError:
        
        abort(400, description="Invalid date format. Please use YYYY-MM-DD format.")
    
    start_date = dt.datetime(start)

    if start_date > dt.datetime(2017, 8, 23) or start_date < dt.datetime(2010, 1, 1):
        
        abort(400, description="Date out of range. Please provide a date between 2010-01-01 and 2017-08-23.")

    MX = session.query(
             Measurement.tobs).filter(
                  Measurement.date >= start_date).order_by(
                       Measurement.tobs.desc()[0]
                       ).first()
        
    MN = session.query(
             Measurement.tobs).filter(
                  Measurement.date >= start_date).order_by(
                       Measurement.tobs.asc()[0]
                       ).first()
        
    AVG = session.query(
             func.avg(Measurement.tobs)).filter(
                  Measurement.date >= start_date)
            
    session.close()
    
    return jsonify({"max_temp": float(MX), "min_temp": float(MN), "avg_temp": float(AVG)})



@app.route("/api/v1.0/st_en/<start>/<end>")
def st_en(start , end):

    session = Session(engine)

    try:
        
        start_date = dt.datetime.strptime(start, '%Y-%m-%d')  
        
        last_date = dt.datetime.strptime(end, '%Y-%m-%d') 
    
    except ValueError:
        abort(400, description="Invalid date format. Please use YYYY-MM-DD format.")

    if start_date > last_date:
        abort(400, description="Start date cannot be after end date.")

    if last_date > dt.datetime(2017, 8, 23) or start_date < dt.datetime(2010, 1, 1):
        abort(400, description="Dates out of range. Please provide dates between 2010-01-01 and 2017-08-23.")

    start_date = start
    
    last_date = end

    MX = session.query(
             Measurement.tobs).filter(
                  Measurement.date <= last_date , Measurement.date >= start_date).order_by(
                       Measurement.tobs.desc()[0]
                       ).first()
        
    MN = session.query(
             Measurement.tobs).filter(
                  Measurement.date <= last_date , Measurement.date >= start_date).order_by(
                       Measurement.tobs.asc()[0]
                       ).first()
        
    AVG = session.query(
             func.avg(Measurement.tobs)).filter(
                  Measurement.date <= last_date , Measurement.date >= start_date
                  ).scalar()
            
    session.close()
    
    return jsonify({"max_temp": float(MX), "min_temp": float(MN), "avg_temp": float(AVG)})

if __name__ == "__main__":
    app.run(debug=True)
