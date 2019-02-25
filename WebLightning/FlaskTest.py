from flask import Flask, render_template, url_for
import LightningStuff as LS
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('Mapa.html', lightnings=lightnings)

kml = 'http://www.zeus.iag.usp.br/linet/linet_0-15.kml'
lightnings = LS.crawler(kml)
print (lightnings)


if __name__ == '__main__':
    app.run(debug=True)

