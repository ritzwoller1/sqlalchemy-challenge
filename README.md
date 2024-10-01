# sqlalchemy-challenge



Climate Analysis Notebook

sqlalchemy-challenge/SurfsUp/climate_analysis.ipynb

    This jupyter notebook aims to analyze weather conditions in Honolulu, Hawaii in preparation for a vacation.
    Analysis includes precipitation levels over a calander year using a date vs inches of rain chart, weather station activity is also included by analysing the activity for each station, then providing a frequency distribution comparing temperature and number of precipitation observations.

Climate App

sqlalchemy-challenge/SurfsUp/app.py

    This file creates the framework for a Flask API which privides the end user with various pieces of information as JSON objects.
    There are five routes in total:
        / - homepage, this presents the user with all possible routes and how to use them.
        /api/v1.0/precipitation - returns precipitation data from the previous year.
        /api/v1.0/stations - returns information about each station.
        /api/v1.0/tobs - returns temperature information of the most active station for the last year.
        /api/v1.0/start_date - returns minimum temperature, maximum temperature, and average temperature from the provided start date to the end of the data.
        /api/v1.0/start_date/end_date - eturns minimum temperature, maximum temperature, and average temperature from the provided start date to the provided end date.

Resources

sqlalchemy-challenge/SurfsUp/Resources/

    This directory contains files required for this analysis including a .sqlite file and two .csv files. The programs were written using the .sqlite file.
