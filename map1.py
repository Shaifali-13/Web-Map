import folium
import pandas

data = pandas.read_csv("Volcanoes.txt")
lat = list(data["LAT"])
lon = list(data["LON"]) 
elev = list(data["ELEV"])
name = list(data["NAME"])


temples = pandas.read_csv("Temples.txt")
latitude = list(temples["LAT"])
longitude = list(temples["LONG"])
locate = list(temples["LOCATION"])
templeName = list(temples["TEMPLE_NAME"])


def color_producer(elevation):
    if elevation < 1000:
        return "green"
    elif 1000 <= elevation < 3000:
        return "orange"
    else:
        return "red"



map = folium.Map(location=[20.5937, 78.9629], zoom_start = 5, tiles="Stamen Terrain")

fgv = folium.FeatureGroup(name="Volcanoes")

html = """
Volcano name:<br>
<a href="https://www.google.com/search?q=%%20%s%%20" target="_blank">%s</a><br>
Height: %s m
"""

for lati, longi, el, name in zip(lat, lon, elev, name):          #zip(list1, list 2) so that the loop goes through these two lists at the same time i.e., in the same iterations.
    iframe = folium.IFrame(html=html % (name, name, el), width=200, height=100)
    fgv.add_child(folium.CircleMarker(location=[lati, longi], popup = folium.Popup(iframe), fill_color=color_producer(el), color = 'grey', opacity=0.8, fill=True))  #el stands for elevation


fgp = folium.FeatureGroup(name="Population")

fgp.add_child(folium.GeoJson(data = open('world.json', 'r', encoding ='utf-8-sig').read(),
style_function = lambda x: {'fillColor':'green' if x['properties']['POP2005'] < 1000000 
else 'yellow' if x['properties']['POP2005'] < 20000000 else 'red'}))


html = """
Temple Name:
<a href="https://www.google.com/search?q=%%22%s%%22" target="_blank">%s</a><br>
Location: %s 
"""
fgt = folium.FeatureGroup(name="Temples")

for temp_lat, temp_long, temp_loc, temp_name in zip(latitude, longitude, locate, templeName):
    iframe2 = folium.IFrame(html = html %(temp_name, temp_name, temp_loc), width = 200, height = 100)
    fgt.add_child(folium.Marker(location=[temp_lat, temp_long], popup = folium.Popup(iframe2), icon=folium.Icon(color="blue")))



map.add_child(fgv)
map.add_child(fgp)
map.add_child(fgt)

map.add_child(folium.LayerControl())

map.save("Map1.html")

