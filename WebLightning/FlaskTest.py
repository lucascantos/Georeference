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
print (sfBr)
states = sfBr.shapes()
SPS = states[24].points
SPFix = []
for i in SPS:
    x = list([i[1],i[0]])
    SPFix.append(x)



@app.route('/')
def home():
    return render_template('LeafletMap.html', SP=SPFix, lightnings=lightnings)

if __name__ == '__main__':
    app.run(debug=True)

