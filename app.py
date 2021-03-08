from flask import Flask, render_template, jsonify,request
from main import stations, next_transports,next_line_station_direction
from station_file_1 import result1
from station_file_2 import result2
from station_file_3 import result3
from flask_cors import CORS
import sqlite3
from main import main, update_db, load_csv, create_schema, insert_csv_row
from apscheduler.schedulers.background import BackgroundScheduler
sched = BackgroundScheduler(daemon=True)
sched.add_job(main,'interval',seconds= 59)
sched.start()
app = Flask(__name__)


main()
@app.route('/')
def home():
    stations()
    return render_template('home.html',title='Welcome')

@app.route('/stations')
def entry_point():
    # jsonify(stations())
    # return render_template('./app.html')
    return render_template('Stations.html',title='Stations',
    blogs=result1)

@app.route('/next/<station>')
def demande(station):
    
    jsonify(next_transports(station))
    return render_template('next.html',title='Next',
    blogs1=result2)

# @app.route('/next/<line>/<station>/<direction>')
# def next_infos(line,station,direction):
#     return jsonify(next_line_station_direction(line,station,direction))

@app.route('/next', methods=['GET'])
def next_infos():

    args1 = request.args['Ligne']
    args2 = request.args['Station']
    args3 = request.args['Direction']
    (next_line_station_direction(args1,args2,args3))
    return render_template('next_line.html',title='Your Trip',blogs2=result3)



if __name__ == '__main__':
    app.run(host="127.0.0.1", port="5000", debug=True)
# @app.route('/next', methods=['GET'])
# def next_infos():

#     args1 = request.args['Ligne']
#     args2 = request.args['Station']
#     args3 = request.args['Direction']
#     jsonify(next_line_station_direction(args1,args2,args3))
#     return render_template('next_line.html',
#                         title='Your Trip',
#                         blogs1=result1)

