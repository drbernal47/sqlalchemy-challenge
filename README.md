# sqlalchemy-challenge
This repo contains an assignment related to SQLAlchemy.

In this assignment, we were asked to analyze data from a climate database (precipitation & temperature in Hawaii).

First I used an engine to access the SQL database from a jupyter notebook using SQLAlchemy. Several queries were constructed in the session, allowing me to explore precipitation data over the past 12 months. Later I did an analysis of temperature data on the most active stations (stations with more measurements).

These one-time analyses were then replicated in a Flask app, allowing for any changes to the database to be reflected in the analysis using an API. The same functionality of exploring precipitation data was created as one route of the app API, and the temperature functionality was modified to be able to examine whichever station becomes the most active over time.
