from flask import Flask, render_template, jsonify,request
from main import stations, next_transports,next_line_station_direction,Ligne,ligne_search
from flask_cors import CORS
import sqlite3
from main import main, update_db, load_csv, create_schema, insert_csv_row
from apscheduler.schedulers.background import BackgroundScheduler
sched = BackgroundScheduler(daemon=True)
sched.add_job(main,'interval',seconds= 59)
sched.start()
app = Flask(__name__)
CORS(app)
main()

@app.route('/')
def home():
    stations()
    return render_template('home.html',title='Welcome')


@app.route('/stations')
def entry_point():
    return jsonify(stations())
 
   
@app.route('/next/<station>')
def demande(station):
    """ This function searches for the next trains to come
    at a set station no matter the line nor destination.
    Parameters : town, station (ex: Montpellier, BELEVEDERE)
    Returns : json data
    Example : http://127.0.0.1:5000/Montpellier/stations/BELVEDERE
    [ [ [ "10", "BELVEDERE", "AIGUELONGUE", "Montpellier" ],
    [ "20:06:10", "20:36:10", "19:50:13" ] ], ...
    [ [ "15", "BELVEDERE", "SABINES", "Montpellier" ],
    [ "20:21:47", "20:50:51" ] ] ]
    """
    return jsonify(next_transports(station))

@app.route('/line')
def ligne_list():
    """ This function searches for every train stops
    for a set town.
    Parameter : town (ex: Montpellier)
    Returns : json data
    Example : http://127.0.0.1:5000/Montpellier/stations
    [ "A. BROUSSONET", "A. L. JUSSIEU", "AGROPOLIS", ...,
    "ZI MARBRERIE", "ZONE ARTISANALE", "ZOO" ]
    """
    return jsonify(Ligne())    

@app.route('/line/<ligne>')
def demande_ligne(ligne):
    """ This function searches for the next trains to come
    at a set station considering a specific line and destination.
    Parameters : town, station, destination (ex: Montpellier, COMEDIE, SABINES)
    Returns : json data
    Example :
    http://127.0.0.1:5000/Montpellier/next?line=2&station=COMEDIE&destination=SABINES
    [ [ "2", "COMEDIE", "SABINES", "19:46:09", "Montpellier" ],
    [ "2", "COMEDIE", "SABINES", "19:58:21", "Montpellier" ] ]
    """ 
    return jsonify(ligne_search(ligne))

@app.route('/next', methods=['GET'])
def next_infos():

    args1 = request.args['Ligne']
    args2 = request.args['Station']
    args3 = request.args['Direction']
    return jsonify(next_line_station_direction(args1,args2,args3))
    


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000", debug=True)


