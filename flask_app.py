from flask import Flask, render_template, redirect, session
import requests
from flask_wtf import FlaskForm
from wtforms import StringField

app = Flask(__name__)
app.debug = True
app.secret_key = 'bbbbbbbbbbbbbbbbbbbbbbbbbbbbbboooooooooooooooooooooooooooooooooooooooooooooooommmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmbbbbbbbbbbbbbbbbbbbbb'

API_KEY = '3641ab635b53178dbe56a8e894e40431'

class MistoForm(FlaskForm):
    mistovybrane = StringField()

@app.route('/')
def pocasi():
    try:
        misto = session['misto']
    except:
        return redirect('/misto')
    url = f'https://api.openweathermap.org/data/2.5/weather?q={misto}&appid={API_KEY}&lang=cz&units=metric'
    odpoved = requests.get(url).json()
    teplota = odpoved['main']['temp']
    podnebi = odpoved['weather'][0]['description']
    popis_pocasi = odpoved['weather'][0]['main']
    latitude = odpoved['coord']['lat']
    longitude = odpoved['coord']['lon']
    return render_template('index.html', odpoved=odpoved, teplota=teplota, podnebi=podnebi, misto=misto,popis_pocasi=popis_pocasi, latitude=latitude, longitude=longitude)

@app.route('/misto', methods=['GET', 'POST'])
def nastav_misto():
    form = MistoForm()
    nova_lokace = form.mistovybrane.data
    if form.validate_on_submit():
        session['misto'] = nova_lokace
        return redirect('/')
    return render_template('nastav_misto.html', form=form)

if __name__ == '__main__':
    app.run()
