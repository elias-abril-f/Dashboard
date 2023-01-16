
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
        return df.hvplot.points('lon', 'lat', geo=True, tiles=True, responsive=True)
    
map = Map()
map_dmap = hv.DynamicMap(map.create_map)
app = pn.Column(map.param, map_dmap, sizing_mode="scale_both")
app.servable()
app.show()