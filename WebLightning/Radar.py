from sklearn.cluster import DBSCAN
from scipy.spatial import ConvexHull
import numpy as np
import matplotlib.pyplot as plt
import time
import shapefile
from matplotlib.patches import Polygon as poli
from shapely.geometry import Polygon
from shapely.geometry import Point
import LightingPlot as LP

kml = 'http://www.zeus.iag.usp.br/linet/linet_0-15.kml'
coordArray = LP.crawler(kml)

start = time.time()
buffer_ratio = LP.bufferArea(10000)


# Cluester em DBSCAN dos pontos. de 1400 foi pra 160
db = DBSCAN(eps=0.09, min_samples=10).fit(coordArray)
core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
core_samples_mask[db.core_sample_indices_] = True
labels = db.labels_
unique_labels = set(labels)

# Abre os arquivos shapefile do BR
#fname2 = 'gadm/gadm36_BRA_2.shp'
fnameSta = 'gadm/gadm36_BRA_1.shp'
fnameMun = 'gadm/BRMUE250GC_SIR.shp'

sf = shapefile.Reader(fnameMun)
sfBr = shapefile.Reader(fnameSta)
shapes = sf.shapes()

fig, ax = plt.subplots(figsize=(20, 10))
# Projecao do mapa
states = sfBr.shapes()
a, b, c, d = states[24].bbox
plt.xlim(a, c)
plt.ylim(b, d)
for state in states:
    LP.shapePatch(state, '#EEEEEE')
# Loop para todas as cidades do estado de sao paulo e passa cada ponto de dado

for city, shape in zip(sf.iterRecords(), sf.iterShapes()):
    if city[1][:2] == '35':
        cor = 'lightgray'

        shape_ex = shape.points
        polygon = Polygon(shape_ex)

        for k in unique_labels:
            class_member_mask = (labels == k)
            if k != -1:
                # ----Aki sao os clusters. Usa um centroid como base e faz o buffer que cobre uma area
                xy = coordArray[class_member_mask & core_samples_mask]
                hull = ConvexHull(xy)
                TS = Polygon(xy[hull.vertices])
                ''' 
                X = np.mean(xy[:,0])
                Y = np.mean(xy[:,1])
                TS = Point(X,Y).buffer(buffer_ratio)
                '''
                if polygon.intersects(TS):
                    X, Y = TS.exterior.coords.xy
                    plt.plot(X, Y, 'b')
                    print(city[0])
                    cor = 'r'
                    break
            else:
                # ----Aki sao os pontos isolados. E ha um array de pontos aki. Por isso o do loop interno.
                xy = coordArray[class_member_mask & ~core_samples_mask]
                for X, Y in xy:
                    point = Point(X, Y)
                    if polygon.contains(point):
                        plt.plot(X, Y, 'y*', markersize=10)
                        # print(city[0])
                        cor = 'b'
                        break
        # ---Plot das cidades.
        LP.shapePatch(shape, cor)

end = time.time()
print(end - start)
'''
# Number of clusters in labels, ignoring noise if present.
n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
n_noise_ = list(labels).count(-1)

print('Estimated number of clusters: %d' % n_clusters_)
print('Estimated number of noise points: %d' % n_noise_)

plt.title('Estimated number of clusters: %d' % n_clusters_) '''
ax.autoscale_view()
plt.show()