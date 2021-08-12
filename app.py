from datetime import date
from flask import Flask, jsonify
from sqlalchemy import create_engine,func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
import datetime as dt
import pandas as pd

# Create an app, being sure to pass __name__
app = Flask(__name__)
#for 

# Define what to do when a user hits the index route
@app.route("/")
def home():
    print("Server received request for 'Home' page...")
   
    return (
        f"<center><h1><font color = green>Welcome to the Climate API!<br></h1><hr><br>"
        f"<h2>Available Routes:<br></h2>"
        f'<h3><a href="/api/v1.0/precipitation">/api/v1.0/precipitation</a><br>'
        f'<a href="/api/v1.0/stations">/api/v1.0/stations</a><br>'
        f'<a href="/api/v1.0/tobs">/api/v1.0/tobs</a><br>'
        f'/api/v1.0/startdate<br>'
        f'/api/v1.0/start/end</h3>')


# Define what to do when a user hits the /precipitation route
@app.route("/api/v1.0/precipitation")
def prcp():
    print("Server received request for 'Precipitation' page...")
    #Establish connection with database
    engine = create_engine("sqlite:///Resources/hawaii.sqlite")

    Base = automap_base()
    Base.prepare(engine, reflect=True)
    Measure = Base.classes.measurement

    session = Session(engine)

    data = session.query(Measure.date,Measure.prcp).all()
    query_dates = session.query(Measure.date).all()
    query_prcp = session.query(Measure.prcp).all()
    ##prcp_dict = data.__dict__
    #data_list = []
    prcp_dict = {}

    prcp_dict = dict(data)   

    session.close()
    return jsonify(prcp_dict)

@app.route("/api/v1.0/stations")
def station():
    print("Server received request for 'Stations' page...")
    engine = create_engine("sqlite:///Resources/hawaii.sqlite")

    Base = automap_base()
    Base.prepare(engine, reflect=True)
    Station = Base.classes.station

    session = Session(engine) 

    data = session.query(Station.station,Station.name).all()
    stat_dict = {}

    stat_dict = dict(data)

    session.close()

    return jsonify(stat_dict)

    #return "Welcome to 'Stations' page!"

# Define what to do when a user hits the /tobs route
@app.route("/api/v1.0/tobs")
def tobs():
    print("Server received request for 'Tobs' page...")
    engine = create_engine("sqlite:///Resources/hawaii.sqlite")

    Base = automap_base()
    Base.prepare(engine, reflect=True)
    Measure = Base.classes.measurement

    session = Session(engine) 

    st_query_date = dt.date(2017,8,18) - dt.timedelta(days = 365)

    active_station_dets = session.query(Measure.date,Measure.tobs).\
    filter(Measure.station == 'USC00519281').filter(Measure.date > st_query_date).all()

    active_stat_dict = dict(active_station_dets )
    session.close()
    
    return jsonify(active_stat_dict)
    #return "Welcome to 'Tobs' page!"

@app.route("/api/v1.0/startdate/<startdate>")
def start(startdate):
    print("Server received request for 'StartDate' page...")
    engine = create_engine("sqlite:///Resources/hawaii.sqlite")

    Base = automap_base()
    Base.prepare(engine, reflect=True)
    Measure = Base.classes.measurement

    session = Session(engine) 


    st = [Measure.date, 
        func.max(Measure.tobs), 
        func.min(Measure.tobs), 
        func.avg(Measure.tobs)]
    date_summary = session.query(*st).\
        filter(Measure.date >= startdate).group_by(Measure.date).all()

    date_dict = {}
    df = pd.DataFrame(date_summary,columns=['Date','Max Temp','Main Temp', 'Avg Temp'])
    df.set_index('Date')
    #df.T
    date_dict = df.to_dict(orient='index')

    session.close()
    return jsonify(date_dict)
    
    #return "Welcome to 'Start' page!"


@app.route("/api/v1.0/start/end/<startdate>/<enddate>")
def startend(startdate,enddate):
    print("Server received request for 'StartDate' page...")
    engine = create_engine("sqlite:///Resources/hawaii.sqlite")

    Base = automap_base()
    Base.prepare(engine, reflect=True)
    Measure = Base.classes.measurement

    session = Session(engine) 

    st = [Measure.date, 
       func.max(Measure.tobs), 
       func.min(Measure.tobs), 
       func.avg(Measure.tobs)]
    date_summary = session.query(*st).\
    filter(Measure.date >= startdate).filter(Measure.date <= enddate).group_by(Measure.date).all()

    date_dict = {}
    df = pd.DataFrame(date_summary,columns=['Date','Max Temp','Main Temp', 'Avg Temp'])
    df.set_index('Date')
    #df.T
    date_dict = df.to_dict(orient='index')

    session.close()
    
    return jsonify(date_dict)
    #return "Welcome to 'StartEnd' page!"

if __name__ == "__main__":
    app.run(debug=True)