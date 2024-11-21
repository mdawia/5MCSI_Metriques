from flask import Flask, render_template, jsonify
import requests
import matplotlib.pyplot as plt
import io
import base64
from datetime import datetime
import json

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('hello.html')  # Page d'accueil

# Route pour afficher les commits
@app.route('/commits/')
def commits():
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

# Route pour afficher les données météo (exemple)
@app.route('/tawarano/')
def meteo():
    url = 'https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx'
    response = requests.get(url)
    json_content = response.json()

    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')  # Timestamp brut
        temp_day_value = list_element.get('main', {}).get('temp') - 273.15  # Conversion de Kelvin à °C
        results.append({
            'Jour': datetime.utcfromtimestamp(dt_value).strftime('%Y-%m-%d %H:%M:%S'),  # Conversion Timestamp
            'temp': round(temp_day_value, 2)  # Arrondi à 2 décimales
        })

    return jsonify(results=results)

# Route pour afficher un autre graphique ou rapport
@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")

# Route pour afficher un histogramme des températures
@app.route('/histogramme/')
def histogramme():
    url = 'https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx'
    response = requests.get(url)
    json_content = response.json()

    results = []
    for list_element in json_content.get('list', []):
        dt_value = datetime.utcfromtimestamp(list_element.get('dt')).strftime('%Y-%m-%d %H:%M:%S')  # Format de la date
        temp_day_value = list_element.get('main', {}).get('temp') - 273.15  # Kelvin à °C
        results.append({'Jour': dt_value, 'temp': round(temp_day_value, 2)})

    return render_template('histogramme.html', results=results)

# Route pour afficher la page de contact
@app.route("/contact/")
def contact():
    return render_template("contact.html")

# Lancer l'application Flask
if __name__ == "__main__":
    app.run(debug=True)
