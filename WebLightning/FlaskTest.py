from flask import Flask, render_template, url_for
import LightningStuff as LS
import shapefile


app = Flask(__name__)

kml = 'http://www.zeus.iag.usp.br/linet/linet_0-15.kml'
lightnings = LS.crawler(kml)

# Abre os arquivos shapefile do BR
#fname2 = 'gadm/gadm36_BRA_2.shp'
fnameUF = 'Estados/BRUFE250GC_SIR.shp'

sfBr = shapefile.Reader(fnameUF)
states = sfBr.shapes()
SPS = states[24].points
list_of_lists = [list(elem) for elem in SPS]
print (list_of_lists[:])


@app.route('/')
def home():
    return render_template('LeafletMap.html', SP=list_of_lists, lightnings=lightnings)

if __name__ == '__main__':
    app.run(debug=True)

