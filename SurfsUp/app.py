# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy import inspect

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################

engine = create_engine('sqlite:///Resources/hawaii.sqlite')

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station


#################################################
# Flask Setup
#################################################

app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route('/')
def welcome():
    '''List all available api routes.'''
    return (
        f'Available Routes:<br/>'
        f'/api/v1.0/precipitation<br/>'
        f'/api/v1.0/stations<br/>'
        f'/api/v1.0/tobs<br/>'
        f'NOTE! Dates should be yyyy-mm-dd format<br/>'
        f'/api/v1.0/start_date<br/>'
        f'/api/v1.0/start_date/end_date<br/>'
    )


@app.route('/api/v1.0/precipitation')
def names():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    # Convert the query results from your precipitation analysis (i.e. retrieve only the last 12 months of data) to a dictionary using date as the key and prcp as the value.
    precipitation = session.query(measurement.date, measurement.prcp).filter(measurement.date >= '2016-08-23').order_by(measurement.date).all()
    
    session.close()

    # Convert list of tuples into normal list
    precipitation_dict = {}

    for date, value in precipitation:
        if date not in precipitation_dict:
            precipitation_dict[date] = []
        if value is not None:  # Exclude None values
            precipitation_dict[date].append(value)

    return jsonify(precipitation_dict)


@app.route('/api/v1.0/stations')
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    # Return a JSON list of stations from the dataset.
    station_data = session.query(station).all()

    session.close()

    station_dict = {}

    for item in station_data:
        station_dict[item.station] = [item.name, item.latitude, item.longitude, item.elevation]
        
    return jsonify(station_dict)

@app.route('/api/v1.0/tobs')
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    # Query the dates and temperature observations of the most-active station for the previous year of data.
    one_year_data = session.query(measurement.date, measurement.tobs).filter(measurement.date > '2016-08-23', measurement.station == 'USC00519281').order_by(measurement.date).all()

    session.close()

    one_year_dict = {}

    for item in one_year_data:
        one_year_dict[item.date] = item.tobs

    return jsonify(one_year_dict)

@app.route('/api/v1.0/<start>')
def start(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    # Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start
    early_date = session.query(func.min(measurement.date)).all()
    late_date = session.query(func.max(measurement.date)).all()

    if start < early_date[0][0] or start > late_date[0][0]:
        return("Date out of range")
    else:
        start_data = session.query(func.min(measurement.tobs),func.max(measurement.tobs),func.avg(measurement.tobs)) \
                .filter(measurement.date >= start).all()
    
    session.close()

    temperature_data = {
        'Minimum Temperature': start_data[0][0],
        'Maximum Temperature': start_data[0][1],
        'Average Temperature': start_data[0][2]
    }
    
    return(temperature_data)

@app.route('/api/v1.0/<start>/<end>')
def time_period(start, end):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    # Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start
    early_date = session.query(func.min(measurement.date)).all()
    late_date = session.query(func.max(measurement.date)).all()
    
    if start < early_date[0][0] or start > late_date[0][0]:
        return('Start date out of range')
    elif end < early_date[0][0] or end > late_date[0][0]:
        return('End date out of range')
    elif end < start:
        return('End date is before start date')
    else:
        period_data = session.query(func.min(measurement.tobs),func.max(measurement.tobs),func.avg(measurement.tobs)) \
                .filter(measurement.date >= start, measurement.date <= end).all()
    
    session.close()

    temperature_data = {
        'Minimum Temperature': period_data[0][0],
        'Maximum Temperature': period_data[0][1],
        'Average Temperature': period_data[0][2]
    }

    return(temperature_data)

if __name__ == '__main__':
    app.run(debug=True)