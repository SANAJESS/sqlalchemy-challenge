{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {},
   "outputs": [],
   "source": [
    "from flask import Flask, jsonify\n",
    "import sqlalchemy\n",
    "from sqlalchemy import create_engine, func\n",
    "from sqlalchemy.ext.automap import automap_base\n",
    "from sqlalchemy.orm import Session\n",
    "import datetime as dt\n",
    "import numpy as np\n",
    "import pandas as pd\n",
    "from datetime import timedelta"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "metadata": {},
   "outputs": [],
   "source": [
    "engine  = create_engine(\"sqlite:///Resources/hawaii.sqlite\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "metadata": {},
   "outputs": [],
   "source": [
    "Base = automap_base()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "metadata": {},
   "outputs": [],
   "source": [
    "Base.prepare(engine, reflect =True)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "metadata": {},
   "outputs": [],
   "source": [
    "Measurement = Base.classes.measurement\n",
    "Station = Base.classes.station\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "metadata": {},
   "outputs": [],
   "source": [
    "session = Session(engine)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "metadata": {},
   "outputs": [],
   "source": [
    "app = Flask(__name__)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 8,
   "metadata": {},
   "outputs": [],
   "source": [
    "@app.route(\"/\")\n",
    "def Home():\n",
    "    return (\n",
    "        f\"Available Routes:<br/>\"\n",
    "        f\"/api/v1.0/precipitation<br/>\"\n",
    "        f\"/api/v1.0/stations<br/>\"\n",
    "        f\"/api/v1.0/tobs<br/>\"\n",
    "        f\"/api/v1.0/temp/start/end\"\n",
    "    )\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 9,
   "metadata": {},
   "outputs": [],
   "source": [
    "@app.route(\"/api/v1.0/precipitation\")\n",
    "def percipitation():\n",
    "\n",
    "    session = Session(engine)\n",
    "    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first().date\n",
    "    last_date = dt.datetime.strptime(last_date, \"%Y-%m-%d\")\n",
    "    first_date = last_date - timedelta(days = 365)\n",
    "    prcp_results = (session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= first_date).order_by(Measurement.date).all())\n",
    "    return jsonify(prcp_results)\n",
    "\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 10,
   "metadata": {},
   "outputs": [],
   "source": [
    "@app.route(\"/api/v1.0/stations\")\n",
    "def stations():\n",
    "  session  = Session(engine)\n",
    "  stations_results = session.query(Station.station, Station.name).all()\n",
    "  return jsonify(stations_results)\n",
    "\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 11,
   "metadata": {},
   "outputs": [],
   "source": [
    "@app.route(\"/api/v1.0/tobs\")\n",
    "def tobs():\n",
    "    session = Session(engine)\n",
    "    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first().date\n",
    "    last_date = dt.datetime.strptime(last_date, \"%Y-%m-%d\")\n",
    "    first_date = last_date - timedelta(days = 365)\n",
    "    station_counts = (session.query(Measurement.station, func.count).filter(Measurement.station)).group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).all()\n",
    "    top_sation = (station_counts[0])\n",
    "    top_station = (top_station[0])\n",
    "    session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\\\n",
    "    filter(Measurement.station == top_station).all()\n",
    "    top_station_year_obs = session.query(Measurement.tobs).\\\n",
    "    filter(Measurement.station == top_station).filter(Measurement.date >= first_date).all()\n",
    "    return jsonify(top_station_year_obs)\n",
    "    \n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 13,
   "metadata": {},
   "outputs": [],
   "source": [
    "@app.route(\"/api/v1.0/temp/<start>\")\n",
    "@app.route(\"/api/v1.0/temp/<start>/<end>\")\n",
    "def start(start = None , end = None):\n",
    "    session = Session(engine)\n",
    "\n",
    "    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]\n",
    "    \n",
    "    if not end:\n",
    "        results = session.query(*sel).\\\n",
    "            filter(Measurement.date >= start).all()\n",
    "        temps = list(np.ravel(results))\n",
    "        return jsonify(temps)        \n",
    "\n",
    "    results = session.query(*sel).\\\n",
    "        filter(Measurement.date >= start).\\\n",
    "        filter(Measurement.date <= end).all()\n",
    "  \n",
    "    return jsonify(results)\n",
    "\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "if __name__ == \"__main__\":\n",
    " app.run()\n"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.8.5"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
