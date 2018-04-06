from flask import Flask,jsonify
from sqlalchemy import create_engine,func
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
Base = automap_base()
import numpy as np

engine = create_engine("sqlite:///hawaii.sqlite")
Base.prepare(engine,reflect = True)
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(bind = engine)

app = Flask(__name__)
@app.route("/")
def welcome():
    return(
        f"Available Routes: <br/>"
        f"/api/v1.0/precipitation -- dates and temperature observations from the last year<br/>"
        f"/api/v1.0/stations -- list of stations<br/>"
        f"/api/v1.0/tobs -- list of Temperature Observations for the previous year <br/>"
        f"/api/v1.0/<start> -- Minimum temperature, average temperature, max temperature<br/>"
        f"/api/v1.0/<start>/<end> -- Min temperature, average temperature, max temperature of this period")

@app.route("/api/v1.0/precipitation")
def dtemp():
    temps = session.query(Measurement.date,Measurement.tobs).all()
    date_temp = []
    for temp in temps:
        dic = {}
        dic["date"]= temp[0]
        dic["tobs"]= temp[1]
        date_temp.append(dic)
    return jsonify(date_temp)

@app.route("/api/v1.0/stations")
def stations():
    stations = session.query(Station.station,Station.name).all()
    s = []
    for station in stations:
        dic = {}
        dic["station"]=station[0]
        dic["name"]=station[1]
        s.append(dic)
    return jsonify(s)

@app.route("/api/v1.0/tobs")
def tobs():
    tobss = session.query(Measurement.date,Measurement.tobs).filter(Measurement.date.like("%17")).all()
    l = []
    for tob in tobss:
        dic = {}
        dic["date"]=tob[0]
        dic["tobs"]=tob[1]
        l.append(dic)
    return jsonify(l)

@app.route("/api/v1.0/<start>")
def start_date(start):
    temperature = session.query(func.max(Measurement.tobs),func.min(Measurement.tobs),func.avg(Measurement.tobs)).filter(Measurement.date >= start).all()
    t_list = list(np.ravel(temperature))
    tempp = [
        {"Minimum temperature": t_list[1]},
        {"Maximum temperature": t_list[0]},
        {"Average temperature": t_list[2]}]
    return jsonify(tempp)

@app.route("/api/v1.0/<start>/<end>")
def dates(start,end):
    temperatures = session.query(func.max(Measurement.tobs),func.min(Measurement.tobs),func.avg(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date<= end).all()
    t = list(np.ravel(temperatures))
    te = [
        {"Maximum temperature":t[0]},
        {"Minimum temperature":t[1]},
        {"Average temperature":t[2]}
    ]
    return jsonify(te)
    

if __name__ == "__main__":
    app.run(debug=True)