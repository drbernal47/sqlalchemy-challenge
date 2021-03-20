import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import numpy as np
import datetime as dt

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the tables
Station = Base.classes.station
Measurement = Base.classes.measurement


#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query the database for measurement data
    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    # Convert the query results to a dictionary using date as the key and prcp as the value
    precip = []
    for date, prcp in results:
        precip_dict = {}
        precip_dict['date'] = date
        precip_dict['prcp'] = prcp
        precip.append(precip_dict)

    return jsonify(precip)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query the database for station data
    results = session.query(Station.name).all()

    session.close()

    # Convert list of tuples into normal list
    station_names = list(np.ravel(results))

    return jsonify(station_names)


@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Determine which station is the most active
    station_count = session.query(Measurement.station, func.count(Measurement.station)).\
        group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).all()
    station_id = station_count[0][0]

    # Determine the last date measured by that station & the date one year prior
    recent = session.query(Measurement.date).filter(Measurement.station == station_id).order_by(Measurement.date.desc()).first()
    recent_dt = dt.datetime.strptime(recent[0], '%Y-%m-%d')

    last_year_dt = dt.datetime(recent_dt.year - 1,recent_dt.month,recent_dt.day,0,0)

    # Query the date and temperature for that station for the last year
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == station_id).filter(Measurement.date > last_year_dt)

    session.close()

    # Convert the query results to a dictionary using date as the key and temp as the value
    temps = []
    for date, tobs in results:
        temp_dict = {}
        temp_dict['date'] = date
        temp_dict['tobs'] = tobs
        temps.append(temp_dict)

    return jsonify(temps)


@app.route("/api/v1.0/<start>")
def start_date(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query the temperature based on the given start-date
    TMIN = session.query(func.min(Measurement.tobs).filter(Measurement.date >= start))[0][0]
    TAVG = session.query(func.avg(Measurement.tobs).filter(Measurement.date >= start))[0][0]
    TMAX = session.query(func.max(Measurement.tobs).filter(Measurement.date >= start))[0][0]

    session.close()

    # Convert the data into a dictionary
    temp_dict = {}
    temp_dict['TMIN']=TMIN
    temp_dict['TAVG']=TAVG
    temp_dict['TMAX']=TMAX

    return jsonify(temp_dict)


@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start, end):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query the temperature based on the given start-date & end-date
    TMIN = session.query(func.min(Measurement.tobs).filter(Measurement.date >= start).filter(Measurement.date <= end))[0][0]
    TAVG = session.query(func.avg(Measurement.tobs).filter(Measurement.date >= start).filter(Measurement.date <= end))[0][0]
    TMAX = session.query(func.max(Measurement.tobs).filter(Measurement.date >= start).filter(Measurement.date <= end))[0][0]

    session.close()

    # Convert the data into a dictionary
    temp_dict = {}
    temp_dict['TMIN']=TMIN
    temp_dict['TAVG']=TAVG
    temp_dict['TMAX']=TMAX

    return jsonify(temp_dict)


@app.route("/")
def welcome():
    return (
        f"Welcome to the Hawaii Climate Data API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation"
        f"/api/v1.0/stations"
        f"/api/v1.0/tobs"
        f"/api/v1.0/<start>"
        f"/api/v1.0/<start>/<end>"
    )


if __name__ == "__main__":
    app.run(debug=True)
