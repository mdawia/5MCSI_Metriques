from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
import requests
import matplotlib.pyplot as plt
import io
import base64
from datetime import datetime
from urllib.request import urlopen
import sqlite3

                                                                                                                                       
app = Flask(__name__)                                                                                                                  
                                                                                                                                       
@app.route('/')
def hello_world():
    return render_template('hello.html') #Commentaire


@app.route('/commits/')
def commits():
    # Récupérer les commits via l'API GitHub
    url = 'https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits'
    response = requests.get(url)
    commits_data = response.json()

    # Dictionnaire pour compter les commits par minute
    commit_minutes = {}

    for commit in commits_data:
        commit_date = commit['commit']['author']['date']
        commit_time = commit_date.split('T')[1]  # Extraire l'heure (HH:MM:SSZ)
        commit_minute = commit_time[:5]  # Prendre les 5 premiers caractères (HH:MM)

        if commit_minute in commit_minutes:
            commit_minutes[commit_minute] += 1
        else:
            commit_minutes[commit_minute] = 1

    # Créer le graphique
    minutes = list(commit_minutes.keys())
    commit_counts = list(commit_minutes.values())

    fig, ax = plt.subplots()
    ax.bar(minutes, commit_counts)

    ax.set_xlabel('Minute')
    ax.set_ylabel('Nombre de Commits')
    ax.set_title('Commits par Minute')

    # Sauvegarder le graphique dans un objet image et le convertir en base64
    img = io.BytesIO()
    fig.savefig(img, format='png')
    img.seek(0)
    img_base64 = base64.b64encode(img.getvalue()).decode('utf8')

    return render_template('commits.html', img_base64=img_base64)


from flask import Flask, render_template_string, render_template, jsonify
from flask import json
from datetime import datetime
from urllib.request import urlopen
import sqlite3

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('hello.html')  # Commentaire



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

@app.route('/histogramme/')
def histogramme():
    # Récupérer les données de l'API
    response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = datetime.utcfromtimestamp(list_element.get('dt')).strftime('%Y-%m-%d %H:%M:%S')  # Format de la date
        temp_day_value = list_element.get('main', {}).get('temp') - 273.15  # Kelvin à °C
        results.append({'Jour': dt_value, 'temp': round(temp_day_value, 2)})

    # Rendre la page HTML avec les données
    return render_template('histogramme.html', results=results)

@app.route("/contact/")
def contact():
    return render_template("contact.html")




  
if __name__ == "__main__":
  app.run(debug=True)
