# OahuWeather
Weather analysis for Oahu Hawaii

# Description
The `weather_analysis.py` is a Flask application<br>
The process renders the index.html as the base router<br>
```
def welcome():
    return render_template('index.html')
```
In the `index.html`, we use the `{{url_for('<name of the function>')}}` to specify the url<br>
The route is decorated with the function:<br>
```
@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
```
The most complex route is `report` function where we specify a method to set the variables in the web form and pass it to python<br>
```
@app.route("/api/v1.0/report",methods = ['POST', 'GET'])
def report():
    if request.method == 'POST':
    start = request.form['start']
        end = request.form['end']
        return redirect(url_for('stats',start = start, end = end ))
    else 
        # set the variables
        start = request.args.get('start')
        end = request.args.get('end')
        return render_template('temperature.html')
```
The `stats` function checks if `end` is not specified then uses just the `start`<br>
otherwise both start and end are used. For this the function decorates two routes<br>
```
@app.route("/api/v1.0/stats/<start>/<end>")
@app.route("/api/v1.0/stats/<start>/")
def stats(start=None, end=None):
    # to avoid SQLite objects created in a thread can only be used in that same thread

```
also note the use of pointer in the function<br>
```
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]           

    if not end: 
        results = session.query(*sel).\
```



