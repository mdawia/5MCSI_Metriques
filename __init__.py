from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen
import sqlite3
                                                                                                                                       
app = Flask(__name__)                                                                                                                  
                                                                                                                                       
@app.route('/')
def hello_world():
    return render_template('hello.html') #Commentaire


@app.route("/contact/")
def MaPremiereAPI():
    return "<h2>Ma page de contact</h2>"

from flask import Flask, render_template_string, render_template, jsonify
from flask import json
from datetime import datetime
from urllib.request import urlopen
import sqlite3

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('hello.html')  # Commentaire

@app.route("/contact/")
def MaPremiereAPI():
    return "<h2>Ma page de contact</h2>"

# Nouvelle route pour /tawarano/
@app.route('/tawarano/')
def meteo():
    response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')  # Timestamp brut
        temp_day_value = list_element.get('main', {}).get('temp') - 273.15  # Conversion de Kelvin à °C
        results.append({
            'Jour': datetime.utcfromtimestamp(dt_value).strftime('%Y-%m-%d %H:%M:%S'),  # Conversion Timestamp
            'temp': round(temp_day_value, 2)  # Arrondi à 2 décimales
        })
    return jsonify(results=results)

@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")


  
if __name__ == "__main__":
  app.run(debug=True)
