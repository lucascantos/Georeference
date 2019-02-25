# RAIOS
from xml.dom import minidom
import urllib.request
import numpy as np

from matplotlib.patches import Polygon as Poli


def crawler(url):
    '''
    :param url: Caminho do url (KML). Por hora apenas funciona no formato do Morales
    :return: Numpy Array contendo as coordenadas lat/lon de cada raio
    '''
    file = urllib.request.urlopen(url)
    folder = minidom.parse(file).getElementsByTagName("coordinates")
    coordList = []
    for pm in folder:
        rawCoord = pm.firstChild.data
        coord = str(rawCoord).split(",")
        tempDict = {'longitude':coord[0], 'latitude':coord[1]}
        coordList.append(tempDict)
    #coordArray = np.array(coordList, dtype=float)
    return coordList


def shapePatch(shape, color):
    '''
    :param shape: Array de pontos de um Shape
    :param color: Cor de fundo do shape. Otimo pra separar Background de shape relevante
    :return: Plota direto no mapa o shape da regiao. Tambem plota mini regioes como ilhas e lagos sem ligacoes estranhas
    '''
    npoints = len(shape.points)  # total points
    nparts = len(shape.parts)  # total parts
    if nparts == 1:
        shp = shape.points
        poligon = Poli(shp, facecolor=color, edgecolor='black', linewidth=0.5)
        try:
            ax.add_patch(poligon)
        except:
            print("A prior map plot is required in order to plot this poligon")
    else:
        for ip in range(nparts):
            i0 = shape.parts[ip]
            if ip < nparts - 1:
                i1 = shape.parts[ip + 1] - 1
            else:
                i1 = npoints
            seg = shape.points[i0:i1 + 1]
            poligon = Poli(seg, facecolor=color, edgecolor='black', linewidth=0.5)
            try:
                ax.add_patch(poligon)
            except:
                print("A prior map plot is required in order to plot this poligon")

def bufferArea(raio):
    '''
    :param raio: Raio em metros da area de busca de outros raios proximos
    :return:
    '''
    r_d = raio / 110744 #converte raio em metros para graus (lat/lon)
    buffer_ratio = (r_d) * (1 - 0.99919687401213 + 1)  # Variavel que converte buffer em metros. Na verdade acho que converte Metros em numero aleatorio pro calculo do buffer
    return buffer_ratio

