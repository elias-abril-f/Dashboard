
import holoviews as hv
import panel as pn
import numpy as np
import pandas as pd
import hvplot.pandas
import param
class Map(param.Parameterized):
    data = pd.read_csv("./data/stations_start.csv")
    value = param.Integer(default=10, bounds=(1, 10000))
    
    @param.depends('value')
    def create_map(self):
        df = self.data.loc[self.data["value"] >= self.value]
        return df.hvplot.points('lon', 'lat', geo=True, tiles=True)
    
map = Map()
map_dmap = hv.DynamicMap(map.create_map)
pn.Row(map.param, map_dmap)