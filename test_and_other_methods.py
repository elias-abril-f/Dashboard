
import holoviews as hv
import panel as pn
import numpy as np
import pandas as pd
import hvplot.pandas
import param
class Map(param.Parameterized):
    data = pd.read_csv("./data/stations_start.csv")
    value = param.Integer(default=97, bounds=(min(data["value"]), 300000))
    
    @param.depends('value')
    def create_map(self):
        df = self.data.loc[self.data["value"] >= self.value]
        return df.hvplot.points('lon', 'lat', geo=True, tiles=True)
    
map = Map()
map_dmap = hv.DynamicMap(map.create_map)
app = pn.Column(map.param, map_dmap)
app.servable()
app.show()


"""def _otherwaytodoit(data,title, x, widget, xlabel):
    def hooks(plot, element):
        p = plot.state
        p.toolbar.autohide = True
        p.toolbar.logo = None
        if "trips" in widget.value:
            p.yaxis.ticker=[0,2000000,4000000,6000000,8000000]
            p.yaxis.major_label_overrides={0:"0",2000000:"2M",4000000:"4M",6000000:"6M",8000000:"8M"} 
        else:
            p.yaxis.ticker = np.arange(0, 1400, 200)
            p.yaxis.major_label.overrides={0:"0", 200:"200", 400:"400", 600:"600", 800:"800", 1000:"1000",1200:"1200", 1400:"1400"}
    
    def plot(widget = widget):
        return data.hvplot(kind="bar",
                           x=x,
                           title=title,
                           xlabel=xlabel,
                           ylabel=re.sub(r"\([a-z,A-Z]*\)","", str(widget)).capitalize(),
                           y=widget,
                           color=MAIN,
                           line_color="white",
                           responsive=True,
                           min_width=350,
                           min_height=250,
                           label=re.sub(r"\([a-z,A-Z]*\)","", str(widget)).capitalize()).opts(legend_position='top',hooks=[hooks]) \
            * data.hvplot.line(x=x,
                             y=f"mean{widget}",
                             color=ACCENT,
                             responsive=True,
                             line_color="white",
                             min_width=350,
                             min_height=250,
                             label="Mean")
    plot = pn.bind(plot, widget=widget)
    return pn.Column(
        pn.pane.HoloViews(hv.DynamicMap(plot), sizing_mode="stretch_both"),
                sizing_mode="stretch_both",
    )"""
    
"""def _create_geocoord():
docks = pd.read_csv("./data/coordinates.csv")
docks["geometry"] = "POINT (" + docks["lon"].astype(str) + " " + docks["lat"].astype(str) + ")"
docks = docks[["station", "geometry"]]
docks.rename(columns={"station": "name"}, inplace = True)
docks.to_csv("./coordinatesGeo.csv", index=False)"""

"""def createGeodata():
    df4 = pd.read_csv("./data/popular_journeys.csv", sep=",")
    top = df4.sort_values("pop_journeys_value", ascending=False)
    coord = pd.read_csv("./coordinates.csv")
    top10 = top.head(10)
    top10 = pd.merge(top10, coord, on=["station"])
    top10.rename(columns={"station":"start_station", "lat": "start_lat", "lon": "start_lon", "end_station_name": "station"}, inplace = True)
    top10 = pd.merge(top10, coord, on=["station"])
    top10.rename(columns={"station":"end_station","lat":"end_lat", "lon":"end_lon"}, inplace=True)
    top10.drop(["stationid_x", "stationid_y"],axis=1, inplace = True)
    top10
    #   "LINESTRING (-3.7038 40.4168,38 56)","LineString"
    top10["geometry"] = "LINESTRING (" + top10["start_lon"].astype(str) + " " + top10["start_lat"].astype(str) + "," + top10["end_lon"].astype(str) + " " + top10["end_lat"].astype(str) + ")"
    top10["name"] = top10["start_station"] + " to " + top10["end_station"]
    top10Geo = top10[["name", "geometry"]]
    top10Geo.to_csv("./data/top10Geo.csv", index=False)"""