# sqlalchemy-challenge

To begin, use Python and SQLAlchemy to do basic climate analysis and data exploration of your climate database. All of the following analysis should be completed using SQLAlchemy ORM queries, Pandas, and Matplotlib.


Use SQLAlchemy automap_base() to reflect your tables into classes and save a reference to those classes called Station and Measurement.

Precipitation Analysis

Using this date, retrieve the last 12 months of precipitation data by querying the 12 preceding months of data. Note you do not pass in the date as a variable to your query.


Station Analysis


Design a query to calculate the total number of stations in the dataset.


Design a query to find the most active stations (i.e. which stations have the most rows?)



Design a query to retrieve the last 12 months of temperature observation data (TOBS).


Filter by the station with the highest number of observations.


Query the last 12 months of temperature observation data for this station.


Plot the results as a histogram with bins=12.

