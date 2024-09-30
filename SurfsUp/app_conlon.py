# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################

# Create engine using the `hawaii.sqlite` database file
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Declare a Base using `automap_base()`
Base = automap_base()

# Use the Base class to reflect the database tables
Base.prepare(autoload_with=engine)

# Assign the measurement class to a variable called `Measurement` and
# the station class to a variable called `Station`
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create a session
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )  

#Convert the query results from your precipitation analysis (i.e. retrieve only the last 12 months of data) to a dictionary using date as the key and prcp as the value.
#Return the JSON representation of your dictionary.

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

# Query the last 12 months of precipitation data
    results = session.query(Measurement.date, Measurement.prcp).filter(
        Measurement.date >= '2017-08-23'
    ).all()

# Convert the results to a dictionary
    precipitation_data = {date: prcp for date, prcp in results}
    
 # Close the session
    session.close()
    
    # Return the JSON representation of the dictionary
    return jsonify(precipitation_data)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    results = session.query(Station.station).all()
    stations_list = list(np.ravel(results))
    session.close()
    return jsonify(stations=stations_list)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    results = session.query(Measurement.tobs).filter(
        Measurement.station == 'USC00519281',
        Measurement.date >= '2017-08-23'
    ).all()
    tobs_list = list(np.ravel(results))
    session.close()
    return jsonify(temperature_observations=tobs_list)

@app.route("/api/v1.0/<start>")
def start(start):
    session = Session(engine)
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(
        Measurement.date >= start
    ).all()
    session.close()
    return jsonify(start=start, TMIN=results[0][0], TAVG=results[0][1], TMAX=results[0][2])

@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    session = Session(engine)
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(
        Measurement.date >= start,
        Measurement.date <= end
    ).all()
    session.close()
    return jsonify(start=start, end=end, TMIN=results[0][0], TAVG=results[0][1], TMAX=results[0][2])

if __name__ == "__main__":
    app.run(debug=True)